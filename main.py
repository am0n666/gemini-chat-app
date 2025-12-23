# Reasoning:
# 1. Migracja z google.generativeai na google.genai (nowa API)
# 2. Poprawki dla PySimpleGUI - użycie PySimpleGUI.PySimpleGUI zamiast sg.theme
# 3. Zachowanie wszystkich funkcji aplikacji

import PySimpleGUI as sg
import os
import json
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from PIL import Image
import io

from chat_manager import ChatManager
from config import Config

# Konfiguracja PySimpleGUI
try:
    sg.theme('DarkBlue3')
except:
    pass  # Starsza wersja PySimpleGUI może nie mieć theme

class GeminiChatApp:
    def __init__(self):
        self.config = Config()
        self.chat_manager = ChatManager()
        self.current_chat_id = None
        self.client = None
        self.model = None
        
        # Inicjalizacja Gemini API
        if self.config.api_key:
            self.client = genai.Client(api_key=self.config.api_key)
            self.update_model()
        
    def update_model(self):
        """Aktualizuj model Gemini na podstawie konfiguracji"""
        try:
            if not self.client:
                if self.config.api_key:
                    self.client = genai.Client(api_key=self.config.api_key)
            
            # Konfiguracja generowania
            self.generation_config = types.GenerateContentConfig(
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k,
                max_output_tokens=self.config.max_tokens,
            )
            
            # System instruction
            if self.config.system_instruction:
                self.generation_config.system_instruction = self.config.system_instruction
            
            self.model = self.config.model_name
            
        except Exception as e:
            sg.popup_error(f"Błąd inicjalizacji modelu: {str(e)}")
    
    def create_layout(self):
        """Utwórz layout aplikacji"""
        # Lista czatów (sidebar)
        chat_list_column = [
            [sg.Text('Czaty', font=('Helvetica', 14, 'bold'))],
            [sg.Listbox(
                values=self.chat_manager.get_chat_list(),
                size=(30, 25),
                key='-CHAT_LIST-',
                enable_events=True,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE
            )],
            [sg.Button('Nowy czat', size=(12, 1)), sg.Button('Usuń czat', size=(12, 1))],
        ]
        
        # Główne okno czatu
        chat_column = [
            [sg.Text('Gemini Chat', font=('Helvetica', 16, 'bold'), key='-CHAT_TITLE-')],
            [sg.Multiline(
                size=(80, 25),
                key='-CHAT_HISTORY-',
                disabled=True,
                autoscroll=True,
                font=('Courier New', 10)
            )],
            [sg.Text('Załączone pliki:'), sg.Text('', size=(60, 1), key='-ATTACHED_FILES-')],
            [sg.Input(key='-MESSAGE-', size=(65, 1), enable_events=True),
             sg.Button('📎', key='-ATTACH-', size=(3, 1)),
             sg.Button('Wyślij', bind_return_key=True, size=(8, 1))],
        ]
        
        # Panel ustawień
        settings_column = [
            [sg.Text('Ustawienia', font=('Helvetica', 14, 'bold'))],
            [sg.Text('API Key:')],
            [sg.Input(self.config.api_key, key='-API_KEY-', password_char='*', size=(35, 1))],
            [sg.Text('Model:')],
            [sg.Combo(
                ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b'],
                default_value=self.config.model_name,
                key='-MODEL-',
                size=(33, 1),
                readonly=True
            )],
            [sg.Text('Temperatura:')],
            [sg.Slider(
                range=(0.0, 2.0),
                default_value=self.config.temperature,
                resolution=0.1,
                orientation='h',
                size=(30, 15),
                key='-TEMPERATURE-'
            )],
            [sg.Text('Max Tokens:')],
            [sg.Input(str(self.config.max_tokens), key='-MAX_TOKENS-', size=(35, 1))],
            [sg.Text('Top P:')],
            [sg.Slider(
                range=(0.0, 1.0),
                default_value=self.config.top_p,
                resolution=0.05,
                orientation='h',
                size=(30, 15),
                key='-TOP_P-'
            )],
            [sg.Text('Top K:')],
            [sg.Input(str(self.config.top_k), key='-TOP_K-', size=(35, 1))],
            [sg.Text('Instrukcje systemowe:')],
            [sg.Multiline(
                self.config.system_instruction,
                key='-SYSTEM_INSTRUCTION-',
                size=(35, 8)
            )],
            [sg.Button('Zapisz ustawienia', size=(15, 1)), sg.Button('Reset', size=(15, 1))],
        ]
        
        # Layout główny z zakładkami
        layout = [
            [sg.Column(chat_list_column, vertical_alignment='top'),
             sg.VSeperator(),
             sg.Column(chat_column, vertical_alignment='top'),
             sg.VSeperator(),
             sg.Column(settings_column, vertical_alignment='top', scrollable=True, size=(400, 600))]
        ]
        
        return layout
    
    def update_chat_display(self, window):
        """Aktualizuj wyświetlanie historii czatu"""
        if self.current_chat_id:
            chat = self.chat_manager.get_chat(self.current_chat_id)
            if chat:
                window['-CHAT_TITLE-'].update(f"Czat: {chat['name']}")
                
                # Formatowanie historii
                history_text = ""
                for msg in chat['messages']:
                    role = "Ty" if msg['role'] == 'user' else "Gemini"
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
                    
                    # Sprawdź czy są załączniki
                    attachments = ""
                    if 'attachments' in msg and msg['attachments']:
                        attachments = f" [📎 {len(msg['attachments'])} plik(ów)]"
                    
                    history_text += f"[{timestamp}] {role}{attachments}:\n{msg['content']}\n\n"
                
                window['-CHAT_HISTORY-'].update(history_text)
    
    def send_message(self, window, message, attachments=None):
        """Wyślij wiadomość do Gemini API"""
        if not message.strip() and not attachments:
            return
        
        if not self.client:
            sg.popup_error("Skonfiguruj API Key w ustawieniach!")
            return
        
        # Dodaj wiadomość użytkownika
        self.chat_manager.add_message(
            self.current_chat_id,
            'user',
            message,
            attachments
        )
        self.update_chat_display(window)
        window['-MESSAGE-'].update('')
        window['-ATTACHED_FILES-'].update('')
        window.refresh()
        
        try:
            # Przygotuj zawartość wiadomości
            content_parts = []
            
            # Dodaj załączniki (obrazy)
            if attachments:
                for file_path in attachments:
                    try:
                        # Sprawdź czy to obraz
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        # Określ MIME type
                        ext = os.path.splitext(file_path)[1].lower()
                        mime_types = {
                            '.png': 'image/png',
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.gif': 'image/gif',
                            '.bmp': 'image/bmp'
                        }
                        
                        if ext in mime_types:
                            # To jest obraz
                            part = types.Part.from_bytes(
                                data=file_data,
                                mime_type=mime_types[ext]
                            )
                            content_parts.append(part)
                        else:
                            # Plik tekstowy
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content_parts.append(types.Part.from_text(f"[Zawartość pliku {os.path.basename(file_path)}]:\n{f.read()}"))
                    except Exception as e:
                        print(f"Błąd przetwarzania pliku {file_path}: {e}")
            
            # Dodaj tekst wiadomości
            if message.strip():
                content_parts.append(types.Part.from_text(message))
            
            # Wyślij do Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=content_parts,
                config=self.generation_config
            )
            
            # Dodaj odpowiedź modelu
            self.chat_manager.add_message(
                self.current_chat_id,
                'model',
                response.text
            )
            self.update_chat_display(window)
            
        except Exception as e:
            sg.popup_error(f"Błąd wysyłania wiadomości: {str(e)}")
            # Usuń ostatnią wiadomość użytkownika jeśli wystąpił błąd
            if self.current_chat_id:
                chat = self.chat_manager.get_chat(self.current_chat_id)
                if chat and chat['messages']:
                    chat['messages'].pop()
                    self.chat_manager.save_chats()
    
    def run(self):
        """Uruchom aplikację"""
        window = sg.Window(
            'Gemini Chat Application',
            self.create_layout(),
            size=(1400, 700),
            resizable=True,
            finalize=True
        )
        
        attached_files = []
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            # Nowy czat
            elif event == 'Nowy czat':
                chat_name = sg.popup_get_text('Nazwa nowego czatu:', default_text=f'Czat {len(self.chat_manager.chats) + 1}')
                if chat_name:
                    self.current_chat_id = self.chat_manager.create_chat(chat_name)
                    window['-CHAT_LIST-'].update(self.chat_manager.get_chat_list())
                    self.update_chat_display(window)
            
            # Wybór czatu
            elif event == '-CHAT_LIST-':
                if values['-CHAT_LIST-']:
                    chat_name = values['-CHAT_LIST-'][0]
                    for chat_id, chat in self.chat_manager.chats.items():
                        if chat['name'] == chat_name:
                            self.current_chat_id = chat_id
                            self.update_chat_display(window)
                            attached_files = []
                            break
            
            # Usuń czat
            elif event == 'Usuń czat':
                if self.current_chat_id:
                    confirm = sg.popup_yes_no('Czy na pewno usunąć ten czat?')
                    if confirm == 'Yes':
                        self.chat_manager.delete_chat(self.current_chat_id)
                        self.current_chat_id = None
                        window['-CHAT_LIST-'].update(self.chat_manager.get_chat_list())
                        window['-CHAT_HISTORY-'].update('')
                        window['-CHAT_TITLE-'].update('Gemini Chat')
            
            # Załącz plik
            elif event == '-ATTACH-':
                files = sg.popup_get_file(
                    'Wybierz pliki',
                    multiple_files=True,
                    file_types=(('Obrazy', '*.png *.jpg *.jpeg *.gif *.bmp'), ('Teksty', '*.txt *.md'), ('Wszystkie', '*.*'))
                )
                if files:
                    if isinstance(files, str):
                        files = [files]
                    attached_files.extend(files)
                    window['-ATTACHED_FILES-'].update(', '.join([os.path.basename(f) for f in attached_files]))
            
            # Wyślij wiadomość
            elif event == 'Wyślij' or (event == '-MESSAGE-' and values['-MESSAGE-'].endswith('\n')):
                if self.current_chat_id:
                    msg = values['-MESSAGE-'].strip()
                    self.send_message(window, msg, attached_files if attached_files else None)
                    attached_files = []
                else:
                    sg.popup('Utwórz lub wybierz czat!')
            
            # Zapisz ustawienia
            elif event == 'Zapisz ustawienia':
                self.config.api_key = values['-API_KEY-']
                self.config.model_name = values['-MODEL-']
                self.config.temperature = values['-TEMPERATURE-']
                self.config.max_tokens = int(values['-MAX_TOKENS-'])
                self.config.top_p = values['-TOP_P-']
                self.config.top_k = int(values['-TOP_K-'])
                self.config.system_instruction = values['-SYSTEM_INSTRUCTION-']
                self.config.save()
                
                # Rekonfiguruj API
                if self.config.api_key:
                    self.client = genai.Client(api_key=self.config.api_key)
                    self.update_model()
                    sg.popup('Ustawienia zapisane!')
            
            # Reset ustawień
            elif event == 'Reset':
                self.config = Config()
                window['-API_KEY-'].update(self.config.api_key)
                window['-MODEL-'].update(self.config.model_name)
                window['-TEMPERATURE-'].update(self.config.temperature)
                window['-MAX_TOKENS-'].update(self.config.max_tokens)
                window['-TOP_P-'].update(self.config.top_p)
                window['-TOP_K-'].update(self.config.top_k)
                window['-SYSTEM_INSTRUCTION-'].update(self.config.system_instruction)
                sg.popup('Ustawienia zresetowane!')
        
        window.close()

if __name__ == '__main__':
    app = GeminiChatApp()
    app.run()
