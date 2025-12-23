# config.py
# Konfiguracja aplikacji i ustawienia API

import json
import os
from pathlib import Path

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        
        # Domyślne wartości - najnowszy model Gemini 3 Flash
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        self.model_name = 'gemini-3-flash-preview'
        self.temperature = 1.0
        self.max_tokens = 8192
        self.top_p = 0.95
        self.top_k = 40
        self.system_instruction = ''
        
        self.load()
    
    def load(self):
        """Wczytaj konfigurację z pliku"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.api_key = data.get('api_key', self.api_key)
                    self.model_name = data.get('model_name', self.model_name)
                    self.temperature = data.get('temperature', self.temperature)
                    self.max_tokens = data.get('max_tokens', self.max_tokens)
                    self.top_p = data.get('top_p', self.top_p)
                    self.top_k = data.get('top_k', self.top_k)
                    self.system_instruction = data.get('system_instruction', self.system_instruction)
            except Exception as e:
                print(f"Błąd wczytywania konfiguracji: {e}")
    
    def save(self):
        """Zapisz konfigurację do pliku"""
        try:
            data = {
                'api_key': self.api_key,
                'model_name': self.model_name,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'top_p': self.top_p,
                'top_k': self.top_k,
                'system_instruction': self.system_instruction
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd zapisywania konfiguracji: {e}")
