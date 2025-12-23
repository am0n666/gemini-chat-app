# Gemini Chat Application

Pełnofunkcjonalna aplikacja do czatu z Google Gemini API, zbudowana w Pythonie z interfejsem graficznym PySimpleGUI.

## Funkcje

- 💬 **Wieloczatowość** - Twórz i zarządzaj wieloma czatami jednocześnie
- 📎 **Załączniki** - Wysyłaj obrazy i pliki tekstowe do modelu
- ⚙️ **Pełna konfiguracja** - Dostosuj model, temperaturę, instrukcje systemowe i więcej
- 💾 **Automatyczny zapis** - Historia czatów zapisywana lokalnie w JSON
- 🎨 **Przyjazny interfejs** - Intuicyjny GUI z listą czatów, historią i ustawieniami
- 🔄 **Kontekst konwersacji** - Używa chat.send_message() dla zachowania kontekstu
- ⭐ **Najnowsze modele** - Obsługa Gemini 3 Pro, Flash i Pro Image

## Instalacja

### Wymagania

- Python 3.9 lub nowszy
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

**LUB zainstaluj wszystko z requirements.txt:**
```bash
pip install -r requirements.txt
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

## Najnowsza API

Aplikacja używa **najnowszej** biblioteki `google-genai` zgodnie z oficjalną dokumentacją:
- Import: `from google import genai`
- Użycie `client.chats.create()` dla sesji czatu
- Metoda `chat.send_message()` dla zachowania kontekstu konwersacji
- `types.Part.from_bytes()` dla obrazów

Dokumentacja: https://googleapis.github.io/python-genai/

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

### ⭐ Gemini 3 (Najnowsze - Grudzień 2025)
- **gemini-3-flash-preview** (domyślny) - Pro-level inteligencja przy prędkości Flash
- **gemini-3-pro-preview** - Najinteligentniejszy model Google z state-of-the-art rozumowaniem
- **gemini-3-pro-image-preview** - Generowanie obrazów 4K

### Gemini 2.5
- **gemini-2.5-flash** - Szybki model ogólnego przeznaczenia
- **gemini-2.5-pro** - Zaawansowany model z rozszerzonym rozumowaniem

### Gemini 2.0 & 1.5
- **gemini-2.0-flash-exp** - Eksperymentalny model drugiej generacji
- **gemini-1.5-pro** - Zaawansowany model o dużej pojemności
- **gemini-1.5-flash** - Szybki model ogólnego przeznaczenia
- **gemini-1.5-flash-8b** - Lekki i wydajny model

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

### Błąd importu
```
ImportError: cannot import name 'genai' from 'google'
```
**Rozwiązanie:** Upewnij się że zainstalowałeś `google-genai` (nie `google-generativeai`):
```bash
pip uninstall google-generativeai
pip install google-genai
```

### Błąd API Key
- Sprawdź czy klucz API jest prawidłowy
- Upewnij się że masz aktywne konto Google AI Studio
- Sprawdź limity API na swoim koncie

### Błąd wysyłania obrazów
- Upewnij się że używasz modelu obsługującego wizję (np. gemini-3-pro-preview, gemini-3-flash-preview)
- Sprawdź czy obrazy nie są zbyt duże (maks. 20MB)

### Aplikacja nie zapisuje historii
- Sprawdź uprawnienia do zapisu w folderze aplikacji
- Upewnij się że plik `chats.json` nie jest otwarty w innym programie

## Changelog

### v3.0 (2025-12-23)
- ⭐ Dodanie najnowszych modeli Gemini 3: Pro, Flash, Pro Image
- 🔄 Zmiana domyślnego modelu na gemini-3-flash-preview
- 📚 Zaktualizowana lista modeli w dokumentacji

### v2.1 (2025-12-23)
- ✅ PEŁNA migracja do najnowszej API `google-genai`
- 🔄 Użycie `chat.send_message()` dla lepszego kontekstu konwersacji
- 📚 Aktualizacja zgodnie z oficjalną dokumentacją

### v2.0 (2025-12-23)
- ✨ Migracja do nowej API `google-genai`
- 🔧 Poprawki kompatybilności z PySimpleGUI

### v1.0 (2025-12-23)
- 🎉 Pierwsze wydanie

## Cechy modeli Gemini 3

### Gemini 3 Pro Preview
- **Context Window**: 1M tokenów wejściowych / 64k wyjściowych
- **Knowledge Cutoff**: Styczeń 2025
- **Pricing**: $2/$12 za milion tokenów (<200k) lub $4/$18 (>200k)
- **Najlepszy do**: Złożonych zadań wymagających głębokiego rozumowania

### Gemini 3 Flash Preview  
- **Context Window**: 1M tokenów wejściowych / 64k wyjściowych
- **Knowledge Cutoff**: Styczeń 2025
- **Pricing**: $0.50/$3 za milion tokenów
- **Najlepszy do**: Szybkich odpowiedzi z inteligencją na poziomie Pro

### Gemini 3 Pro Image Preview
- **Context Window**: 65k tokenów wejściowych / 32k wyjściowych
- **Knowledge Cutoff**: Styczeń 2025
- **Pricing**: $2 za tekst wejściowy / $0.134 za obraz wyjściowy
- **Najlepszy do**: Generowania obrazów 4K z rozumowaniem i grounding

## Licencja

MIT License - możesz swobodnie używać, modyfikować i dystrybuować tę aplikację.

## Autor

Stworzone przez am0n666

## Linki

- [Google Gemini API](https://ai.google.dev/)
- [Oficjalna dokumentacja google-genai](https://googleapis.github.io/python-genai/)
- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Quickstart Guide](https://ai.google.dev/gemini-api/docs/quickstart)
- [Dokumentacja PySimpleGUI](https://www.pysimplegui.org/)
- [Repozytorium GitHub](https://github.com/am0n666/gemini-chat-app)
