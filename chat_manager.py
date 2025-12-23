# chat_manager.py
# Zarządzanie czatami i historią rozmów

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

class ChatManager:
    def __init__(self, storage_file='chats.json'):
        self.storage_file = storage_file
        self.chats = {}
        self.load_chats()
    
    def load_chats(self):
        """Wczytaj czaty z pliku JSON"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.chats = json.load(f)
            except Exception as e:
                print(f"Błąd wczytywania czatów: {e}")
                self.chats = {}
        else:
            self.chats = {}
    
    def save_chats(self):
        """Zapisz czaty do pliku JSON"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.chats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd zapisywania czatów: {e}")
    
    def create_chat(self, name):
        """Utwórz nowy czat"""
        chat_id = str(uuid.uuid4())
        self.chats[chat_id] = {
            'id': chat_id,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'messages': []
        }
        self.save_chats()
        return chat_id
    
    def delete_chat(self, chat_id):
        """Usuń czat"""
        if chat_id in self.chats:
            del self.chats[chat_id]
            self.save_chats()
    
    def get_chat(self, chat_id):
        """Pobierz czat po ID"""
        return self.chats.get(chat_id)
    
    def get_chat_list(self):
        """Pobierz listę nazw czatów"""
        return [chat['name'] for chat in self.chats.values()]
    
    def add_message(self, chat_id, role, content, attachments=None):
        """Dodaj wiadomość do czatu"""
        if chat_id in self.chats:
            message = {
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
            if attachments:
                message['attachments'] = attachments
            
            self.chats[chat_id]['messages'].append(message)
            self.save_chats()
    
    def get_messages(self, chat_id):
        """Pobierz wiadomości z czatu"""
        if chat_id in self.chats:
            return self.chats[chat_id]['messages']
        return []
