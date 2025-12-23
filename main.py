# Reasoning:
# 1. Migracja z PySimpleGUI na FreeSimpleGUI (open-source fork)
# 2. Zmiana importu: import FreeSimpleGUI as sg
# 3. Cała reszta kodu pozostaje bez zmian (100% kompatybilność)
# 4. FreeSimpleGUI jest darmowe i nie wymaga specjalnej instalacji

import FreeSimpleGUI as sg
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

# Nowoczesny motyw
sg.theme('DarkGrey13')

# Kolory
BG_COLOR = '#1e1e1e'
INPUT_BG = '#2d2d2d'
BUTTON_COLOR = ('#ffffff', '#0d7377')
TEXT_COLOR = '#e0e0e0'
ACCENT_COLOR = '#0d7377'

class GeminiChatApp:
    def __init__(self):
        self.config = Config()
        self.chat_manager = ChatManager()
        self.current_chat_id = None
        self.client = None
        self.chat_session = None
        
        if self.config.api_key:
            self.client = genai.Client(api_key=self.config.api_key)
    
    def get_safety_settings(self):
        if not self.config.enable_safety_filters:
            return [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
            ]
        else:
            return [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
            ]
        
    def create_chat_session(self):
        if not self.client:
            return None
        
        try:
            config = types.GenerateContentConfig(
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k,
                max_output_tokens=self.config.max_tokens,
                safety_settings=self.get_safety_settings(),
            )
            
            if self.config.system_instruction:
                config.system_instruction = self.config.system_instruction
            
            self.chat_session = self.client.chats.create(
                model=self.config.model_name,
                config=config
            )
            
            return self.chat_session
            
        except Exception as e:
            sg.popup_error(f"Błąd tworzenia sesji: {str(e)}", title="Błąd")
            return None
    
    def create_layout(self):
        """Utwórz pełen responsive layout"""
        
        # Główny tab czatu - PEŁEN RESPONSIVE
        chat_tab = [
            # Header
            [sg.Text('Gemini Chat', font=('Segoe UI', 18, 'bold'), text_color=ACCENT_COLOR, pad=(15, 15)),
             sg.Push(),
             sg.Text('', key='-CHAT_NAME-', font=('Segoe UI', 12), text_color=TEXT_COLOR, pad=(15, 15))],
            
            # Główna zawartość - horizontal layout
            [sg.Column([
                # Sidebar z czatami
                [sg.Text('Twoje czaty', font=('Segoe UI', 11, 'bold'), pad=(10, 10))],
                [sg.Listbox(
                    values=self.chat_manager.get_chat_list(),
                    size=(30, 20),
                    key='-CHAT_LIST-',
                    enable_events=True,
                    font=('Segoe UI', 10),
                    background_color=INPUT_BG,
                    text_color=TEXT_COLOR,
                    highlight_background_color=ACCENT_COLOR,
                    pad=(10, 5),
                    expand_y=True  # Rozciąga się w pionie
                )],
                [sg.Button('+ Nowy czat', key='-NEW_CHAT-', size=(12, 1), button_color=BUTTON_COLOR, font=('Segoe UI', 9, 'bold'), pad=(5, 5)),
                 sg.Button('✖ Usuń', key='-DELETE_CHAT-', size=(8, 1), button_color=('#ffffff', '#c74440'), font=('Segoe UI', 9), pad=(5, 5))]
            ], vertical_alignment='top', background_color=BG_COLOR, pad=(10, 10), expand_y=True),
            
            sg.VerticalSeparator(pad=(0, 10)),
            
            # Główne okno czatu - rozciąga się
            sg.Column([
                [sg.Multiline(
                    size=(80, 20),
                    key='-CHAT_HISTORY-',
                    disabled=True,
                    autoscroll=True,
                    font=('Consolas', 10),
                    background_color=INPUT_BG,
                    text_color=TEXT_COLOR,
                    border_width=0,
                    pad=(10, 10),
                    expand_x=True,  # Rozciąga się w poziomie
                    expand_y=True   # Rozciąga się w pionie
                )],
                
                # Input area - rozciąga się w poziomie
                [sg.Text('Załączone:', font=('Segoe UI', 9), pad=(10, 5)), 
                 sg.Text('', key='-ATTACHED_FILES-', font=('Segoe UI', 9), text_color='#6c757d', expand_x=True)],
                
                [sg.Multiline(
                    size=(80, 3),
                    key='-MESSAGE-',
                    font=('Segoe UI', 10),
                    background_color=INPUT_BG,
                    text_color=TEXT_COLOR,
                    border_width=1,
                    pad=(10, 5),
                    enter_submits=False,
                    expand_x=True  # Rozciąga się w poziomie
                )],
                
                [sg.Button('📎 Załącz', key='-ATTACH-', button_color=('#ffffff', '#6c757d'), font=('Segoe UI', 9), pad=(10, 10)),
                 sg.Push(),
                 sg.Button('➤ Wyślij', key='-SEND-', size=(15, 1), button_color=BUTTON_COLOR, font=('Segoe UI', 10, 'bold'), pad=(10, 10))]
                
            ], vertical_alignment='top', background_color=BG_COLOR, pad=(10, 10), expand_x=True, expand_y=True)]
        ]
        
        # Tab ustawień - scrollable
        settings_tab = [
            [sg.Column([
                [sg.Text('Konfiguracja API', font=('Segoe UI', 14, 'bold'), pad=(10, 20))],
                
                [sg.Frame('Klucz API', [
                    [sg.Input(
                        self.config.api_key,
                        key='-API_KEY-',
                        password_char='*',
                        font=('Segoe UI', 10),
                        background_color=INPUT_BG,
                        text_color=TEXT_COLOR,
                        pad=(10, 10),
                        expand_x=True
                    )]
                ], font=('Segoe UI', 10), pad=(10, 10), expand_x=True)],
                
                [sg.Frame('Wybór modelu', [
                    [sg.Combo(
                        ['gemini-3-flash-preview', 'gemini-3-pro-preview', 'gemini-3-pro-image-preview',
                         'gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash-exp',
                         'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b'],
                        default_value=self.config.model_name,
                        key='-MODEL-',
                        font=('Segoe UI', 10),
                        background_color=INPUT_BG,
                        readonly=True,
                        pad=(10, 10),
                        expand_x=True
                    )]
                ], font=('Segoe UI', 10), pad=(10, 10), expand_x=True)],
                
                [sg.Text('Parametry generowania', font=('Segoe UI', 12, 'bold'), pad=(10, 20))],
                
                [sg.Frame('Temperatura', [
                    [sg.Slider(
                        range=(0.0, 2.0),
                        default_value=self.config.temperature,
                        resolution=0.1,
                        orientation='h',
                        key='-TEMPERATURE-',
                        font=('Segoe UI', 9),
                        pad=(10, 10),
                        expand_x=True
                    )]
                ], font=('Segoe UI', 10), pad=(10, 5), expand_x=True)],
                
                [sg.Frame('Max Tokens', [
                    [sg.Input(
                        str(self.config.max_tokens),
                        key='-MAX_TOKENS-',
                        size=(20, 1),
                        font=('Segoe UI', 10),
                        background_color=INPUT_BG,
                        text_color=TEXT_COLOR,
                        pad=(10, 10)
                    )]
                ], font=('Segoe UI', 10), pad=(10, 5))],
                
                [sg.Frame('Top P', [
                    [sg.Slider(
                        range=(0.0, 1.0),
                        default_value=self.config.top_p,
                        resolution=0.05,
                        orientation='h',
                        key='-TOP_P-',
                        font=('Segoe UI', 9),
                        pad=(10, 10),
                        expand_x=True
                    )]
                ], font=('Segoe UI', 10), pad=(10, 5), expand_x=True)],
                
                [sg.Frame('Top K', [
                    [sg.Input(
                        str(self.config.top_k),
                        key='-TOP_K-',
                        size=(20, 1),
                        font=('Segoe UI', 10),
                        background_color=INPUT_BG,
                        text_color=TEXT_COLOR,
                        pad=(10, 10)
                    )]
                ], font=('Segoe UI', 10), pad=(10, 5))],
                
                [sg.Text('Zaawansowane', font=('Segoe UI', 12, 'bold'), pad=(10, 20))],
                
                [sg.Frame('Filtry bezpieczeństwa', [
                    [sg.Checkbox(
                        'Włącz filtry bezpieczeństwa (domyślnie wyłączone)',
                        default=self.config.enable_safety_filters,
                        key='-SAFETY_FILTERS-',
                        font=('Segoe UI', 9),
                        pad=(10, 10)
                    )]
                ], font=('Segoe UI', 10), pad=(10, 10), expand_x=True)],
                
                [sg.Frame('Instrukcje systemowe', [
                    [sg.Multiline(
                        self.config.system_instruction,
                        key='-SYSTEM_INSTRUCTION-',
                        size=(60, 6),
                        font=('Segoe UI', 9),
                        background_color=INPUT_BG,
                        text_color=TEXT_COLOR,
                        pad=(10, 10),
                        expand_x=True
                    )]
                ], font=('Segoe UI', 10), pad=(10, 10), expand_x=True)],
                
                [sg.Button('✔ Zapisz ustawienia', key='-SAVE_SETTINGS-', size=(20, 1), button_color=BUTTON_COLOR, font=('Segoe UI', 10, 'bold'), pad=(10, 20)),
                 sg.Button('↻ Reset', key='-RESET_SETTINGS-', size=(15, 1), button_color=('#ffffff', '#6c757d'), font=('Segoe UI', 10), pad=(5, 20))]
                
            ], scrollable=True, vertical_scroll_only=True, background_color=BG_COLOR, pad=(20, 20), expand_x=True, expand_y=True)]
        ]
        
        # Główny layout
        layout = [
            [sg.TabGroup([
                [sg.Tab('💬 Czat', chat_tab, font=('Segoe UI', 11), background_color=BG_COLOR),
                 sg.Tab('⚙️ Ustawienia', settings_tab, font=('Segoe UI', 11), background_color=BG_COLOR)]
            ], font=('Segoe UI', 10), tab_background_color=INPUT_BG, selected_background_color=ACCENT_COLOR, 
               background_color=BG_COLOR, pad=(0, 0), expand_x=True, expand_y=True)],
            
            # Status bar
            [sg.StatusBar(
                f'Model: {self.config.model_name} | Filtry: {"Włączone" if self.config.enable_safety_filters else "Wyłączone"}',
                key='-STATUS-',
                font=('Segoe UI', 9),
                pad=(0, 0),
                size=(150, 1)
            )]
        ]
        
        return layout
    
    def update_chat_display(self, window):
        if self.current_chat_id:
            chat = self.chat_manager.get_chat(self.current_chat_id)
            if chat:
                window['-CHAT_NAME-'].update(f"💬 {chat['name']}")
                
                history_text = ""
                for msg in chat['messages']:
                    role = "[TY]" if msg['role'] == 'user' else "[GEMINI]"
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
                    
                    attachments = ""
                    if 'attachments' in msg and msg['attachments']:
                        attachments = f" 📎({len(msg['attachments'])})"
                    
                    history_text += f"{timestamp} {role}{attachments}\n{msg['content']}\n\n{'='*80}\n\n"
                
                window['-CHAT_HISTORY-'].update(history_text)
    
    def update_status_bar(self, window, message=None):
        if message:
            window['-STATUS-'].update(message)
        else:
            window['-STATUS-'].update(
                f'Model: {self.config.model_name} | Filtry: {"Włączone" if self.config.enable_safety_filters else "Wyłączone"}'
            )
    
    def send_message(self, window, message, attachments=None):
        if not message.strip() and not attachments:
            return
        
        if not self.client:
            sg.popup_error("Skonfiguruj API Key w zakładce Ustawienia!", title="Błąd")
            return
        
        self.chat_manager.add_message(self.current_chat_id, 'user', message, attachments)
        self.update_chat_display(window)
        window['-MESSAGE-'].update('')
        window['-ATTACHED_FILES-'].update('')
        self.update_status_bar(window, 'Wysyłanie...')
        window.refresh()
        
        try:
            if not self.chat_session:
                self.chat_session = self.create_chat_session()
                if not self.chat_session:
                    return
            
            content_parts = []
            
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        ext = os.path.splitext(file_path)[1].lower()
                        mime_types = {
                            '.png': 'image/png',
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.gif': 'image/gif',
                            '.bmp': 'image/bmp'
                        }
                        
                        if ext in mime_types:
                            part = types.Part.from_bytes(data=file_data, mime_type=mime_types[ext])
                            content_parts.append(part)
                        else:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content_parts.append(f"[Plik: {os.path.basename(file_path)}]\n{f.read()}")
                    except Exception as e:
                        print(f"Błąd pliku {file_path}: {e}")
            
            if message.strip():
                content_parts.append(message)
            
            response = self.chat_session.send_message(content_parts)
            
            self.chat_manager.add_message(self.current_chat_id, 'model', response.text)
            self.update_chat_display(window)
            self.update_status_bar(window, 'Gotowe!')
            
        except Exception as e:
            sg.popup_error(f"Błąd: {str(e)}", title="Błąd komunikacji")
            if self.current_chat_id:
                chat = self.chat_manager.get_chat(self.current_chat_id)
                if chat and chat['messages']:
                    chat['messages'].pop()
                    self.chat_manager.save_chats()
            self.update_status_bar(window)
    
    def run(self):
        window = sg.Window(
            'Gemini Chat Pro',
            self.create_layout(),
            size=(1400, 800),
            resizable=True,
            finalize=True,
            icon=None,
            background_color=BG_COLOR,
            margins=(0, 0)
        )
        
        attached_files = []
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            elif event == '-NEW_CHAT-':
                chat_name = sg.popup_get_text('Nazwa nowego czatu:', default_text=f'Czat {len(self.chat_manager.chats) + 1}', font=('Segoe UI', 10))
                if chat_name:
                    self.current_chat_id = self.chat_manager.create_chat(chat_name)
                    self.chat_session = self.create_chat_session()
                    window['-CHAT_LIST-'].update(self.chat_manager.get_chat_list())
                    self.update_chat_display(window)
            
            elif event == '-CHAT_LIST-':
                if values['-CHAT_LIST-']:
                    chat_name = values['-CHAT_LIST-'][0]
                    for chat_id, chat in self.chat_manager.chats.items():
                        if chat['name'] == chat_name:
                            self.current_chat_id = chat_id
                            self.chat_session = self.create_chat_session()
                            self.update_chat_display(window)
                            attached_files = []
                            break
            
            elif event == '-DELETE_CHAT-':
                if self.current_chat_id:
                    confirm = sg.popup_yes_no('Czy na pewno usunąć ten czat?', font=('Segoe UI', 10), title='Potwierdzenie')
                    if confirm == 'Yes':
                        self.chat_manager.delete_chat(self.current_chat_id)
                        self.current_chat_id = None
                        self.chat_session = None
                        window['-CHAT_LIST-'].update(self.chat_manager.get_chat_list())
                        window['-CHAT_HISTORY-'].update('')
                        window['-CHAT_NAME-'].update('')
            
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
            
            elif event == '-SEND-':
                if self.current_chat_id:
                    msg = values['-MESSAGE-'].strip()
                    self.send_message(window, msg, attached_files if attached_files else None)
                    attached_files = []
                else:
                    sg.popup('Utwórz lub wybierz czat!', font=('Segoe UI', 10), title='Info')
            
            elif event == '-SAVE_SETTINGS-':
                self.config.api_key = values['-API_KEY-']
                self.config.model_name = values['-MODEL-']
                self.config.temperature = values['-TEMPERATURE-']
                self.config.max_tokens = int(values['-MAX_TOKENS-'])
                self.config.top_p = values['-TOP_P-']
                self.config.top_k = int(values['-TOP_K-'])
                self.config.system_instruction = values['-SYSTEM_INSTRUCTION-']
                self.config.enable_safety_filters = values['-SAFETY_FILTERS-']
                self.config.save()
                
                if self.config.api_key:
                    self.client = genai.Client(api_key=self.config.api_key)
                    if self.current_chat_id:
                        self.chat_session = self.create_chat_session()
                    self.update_status_bar(window)
                    sg.popup('Ustawienia zapisane!', font=('Segoe UI', 10), title='Sukces')
            
            elif event == '-RESET_SETTINGS-':
                self.config = Config()
                window['-API_KEY-'].update(self.config.api_key)
                window['-MODEL-'].update(self.config.model_name)
                window['-TEMPERATURE-'].update(self.config.temperature)
                window['-MAX_TOKENS-'].update(self.config.max_tokens)
                window['-TOP_P-'].update(self.config.top_p)
                window['-TOP_K-'].update(self.config.top_k)
                window['-SYSTEM_INSTRUCTION-'].update(self.config.system_instruction)
                window['-SAFETY_FILTERS-'].update(self.config.enable_safety_filters)
                self.update_status_bar(window)
                sg.popup('Ustawienia zresetowane!', font=('Segoe UI', 10), title='Info')
        
        window.close()

if __name__ == '__main__':
    app = GeminiChatApp()
    app.run()
