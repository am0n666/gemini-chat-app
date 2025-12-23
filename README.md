# Gemini Chat Application

Pełnofunkcjonalna aplikacja do czatu z Google Gemini API, zbudowana w Pythonie z interfejsem graficznym PySimpleGUI.

## Funkcje

- 💬 **Wieloczatowość** - Twórz i zarządzaj wieloma czatami jednocześnie
- 📎 **Załączniki** - Wysyłaj obrazy i pliki tekstowe do modelu
- ⚙️ **Pełna konfiguracja** - Dostosuj model, temperaturę, instrukcje systemowe i więcej
- 💾 **Automatyczny zapis** - Historia czatów zapisywana lokalnie w JSON
- 🎨 **Przyjazny interfejs** - Intuicyjny GUI z listą czatów, historią i ustawieniami

## Instalacja

### Wymagania

- Python 3.8 lub nowszy
- Klucz API Google Gemini ([uzyskaj tutaj](https://aistudio.google.com/apikey))

### Kroki instalacji

1. Sklonuj repozytorium:
```bash
git clone https://github.com/am0n666/gemini-chat-app.git
cd gemini-chat-app
```

2. Zainstaluj wymagane biblioteki:

**WAŻNE - PySimpleGUI wymaga specjalnej instalacji:**
```bash
# Najpierw odinstaluj starą wersję (jeśli jest)
python -m pip uninstall PySimpleGUI
python -m pip cache purge

# Zainstaluj z prywatnego serwera PyPI
python -m pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI

# Zainstaluj pozostałe zależności
pip install google-genai Pillow
```

3. (Opcjonalnie) Ustaw zmienną środowiskową z kluczem API:
```bash
# Windows CMD
set GEMINI_API_KEY=twoj_klucz_api

# Windows PowerShell
$env:GEMINI_API_KEY="twoj_klucz_api"

# Linux/Mac
export GEMINI_API_KEY=twoj_klucz_api
```

Alternatywnie możesz wprowadzić klucz API bezpośrednio w ustawieniach aplikacji.

## Użycie

1. Uruchom aplikację:
```bash
python main.py
```

2. **Pierwsza konfiguracja:**
   - Wprowadź swój klucz API Gemini w panelu "Ustawienia" (po prawej stronie)
   - Kliknij "Zapisz ustawienia"

3. **Tworzenie czatu:**
   - Kliknij "Nowy czat" w lewym panelu
   - Wprowadź nazwę czatu

4. **Wysyłanie wiadomości:**
   - Wpisz wiadomość w polu na dole
   - (Opcjonalnie) Kliknij 📎 aby załączyć pliki
   - Kliknij "Wyślij" lub naciśnij Enter

5. **Dostosowanie modelu:**
   - W ustawieniach możesz wybrać model Gemini
   - Dostosuj parametry: temperatura, max tokens, top_p, top_k
   - Dodaj instrukcje systemowe dla modelu

## Migracja do nowej API

Aplikacja używa nowej biblioteki `google-genai` (zamiast przestarzałej `google.generativeai`). Jeśli migrowano z wcześniejszej wersji:

1. Odinstaluj starą bibliotekę:
```bash
pip uninstall google-generativeai
```

2. Zainstaluj nową:
```bash
pip install google-genai
```

## Struktura plików

```
gemini-chat-app/
│
├── main.py              # Główna aplikacja GUI
├── chat_manager.py      # Zarządzanie czatami i historią
├── config.py            # Konfiguracja i ustawienia
├── requirements.txt     # Zależności Python
├── README.md           # Ten plik
│
├── chats.json          # Historia czatów (tworzona automatycznie)
└── config.json         # Zapisane ustawienia (tworzone automatycznie)
```

## Dostępne modele

- `gemini-2.0-flash-exp` (domyślny) - Najnowszy eksperymentalny model
- `gemini-1.5-pro` - Zaawansowany model o dużej pojemności
- `gemini-1.5-flash` - Szybki model ogólnego przeznaczenia
- `gemini-1.5-flash-8b` - Lekki i wydajny model

## Obsługiwane typy plików

### Obrazy
- PNG, JPG, JPEG, GIF, BMP
- Automatycznie wysyłane do modelu wizyjnego Gemini

### Teksty
- TXT, MD
- Zawartość dołączana do wiadomości tekstowej

## Rozwiązywanie problemów

### Problem z PySimpleGUI
```
AttributeError: module 'PySimpleGUI' has no attribute 'theme'
```
**Rozwiązanie:** Zainstaluj PySimpleGUI z prywatnego serwera:
```bash
python -m pip uninstall PySimpleGUI
python -m pip cache purge
python -m pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

### Problem z przestarzałą API
```
FutureWarning: All support for the `google.generativeai` package has ended
```
**Rozwiązanie:** Zaktualizowano do `google-genai`. Zainstaluj najnowszą wersję:
```bash
pip uninstall google-generativeai
pip install google-genai
```

### Błąd API Key
- Sprawdź czy klucz API jest prawidłowy
- Upewnij się że masz aktywne konto Google AI Studio
- Sprawdź limity API na swoim koncie

### Błąd wysyłania obrazów
- Upewnij się że używasz modelu obsługującego wizję (np. gemini-1.5-pro, gemini-2.0-flash-exp)
- Sprawdź czy obrazy nie są zbyt duże (maks. 20MB)

### Aplikacja nie zapisuje historii
- Sprawdź uprawnienia do zapisu w folderze aplikacji
- Upewnij się że plik `chats.json` nie jest otwarty w innym programie

## Changelog

### v2.0 (2025-12-23)
- ✨ Migracja do nowej API `google-genai`
- 🔧 Poprawki kompatybilności z PySimpleGUI
- 📚 Zaktualizowana dokumentacja instalacji

### v1.0 (2025-12-23)
- 🎉 Pierwsze wydanie
- 💬 Podstawowa funkcjonalność czatu
- 📎 Obsługa załączników
- ⚙️ Panel konfiguracji

## Licencja

MIT License - możesz swobodnie używać, modyfikować i dystrybuować tę aplikację.

## Autor

Stworzone przez am0n666

## Linki

- [Google Gemini API](https://ai.google.dev/)
- [Nowa dokumentacja google-genai](https://github.com/googleapis/python-genai)
- [Dokumentacja PySimpleGUI](https://www.pysimplegui.org/)
- [Repozytorium GitHub](https://github.com/am0n666/gemini-chat-app)
