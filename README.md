# Jarvis LLM

Modułowy, lokalnie hostowany asystent głosowy w Pythonie, oparty o lokalne modele LLM, z obsługą wyszukiwania w internecie i wywoływania narzędzi (tool-calling).

> **Status projektu: porzucony / eksperymentalny.** Ten kod nie jest rozwijany dalej. Repozytorium pozostaje jako punkt odniesienia i materiał edukacyjny.

## O projekcie

Jarvis to prywatny projekt asystenta głosowego aktywowanego słowem kluczowym „Jarvis”. Nasłuchuje mikrofonu, rozpoznaje mowę po polsku, a następnie wysyła zapytanie do lokalnego modelu LLM (przez serwer zgodny z OpenAI API, np. LM Studio), który w razie potrzeby korzysta z zewnętrznych narzędzi (wyszukiwarka DuckDuckGo, otwieranie stron w przeglądarce).

### Historia rozwoju

Projekt przeszedł kilka iteracji, zanim przyjął obecną formę:

1. **Wersja 1 — dopasowywanie słów kluczowych.** Prosty algorytm sprawdzający obecność słów „pogoda” i „Jarvis” w rozpoznanym tekście i zwracający dane pogodowe.
2. **Wersja 2 — Gemini API.** Zastąpienie sztywnej logiki wywołaniami do chmurowego API Gemini.
3. **Wersja 3 (obecna) — lokalny LLM.** Przejście na model hostowany lokalnie (LM Studio) z pełnym tool-callingiem (function calling), co dało większą kontrolę i niezależność od zewnętrznych usług AI.

## Funkcje

- Rozpoznawanie mowy w języku polskim (`speech_recognition` + Google Speech API)
- Komunikacja z lokalnym LLM przez interfejs zgodny z OpenAI (`localhost:1234/v1`, np. LM Studio)
- Tool-calling: model sam decyduje, kiedy wywołać funkcję
- Wbudowane narzędzia:
  - `otworz_youtube` — otwiera YouTube w przeglądarce
  - `szukaj_w_internecie` — wyszukuje informacje przez DuckDuckGo (`ddgs`), używane automatycznie przy pytaniach o aktualne fakty, pogodę, wydarzenia itp.
- Aktywacja głosowa słowem „Jarvis”

## Wymagania

- Python 3.10+
- Lokalny serwer LLM zgodny z OpenAI API (np. [LM Studio](https://lmstudio.ai/)) uruchomiony na `localhost:1234`
- Mikrofon podłączony do systemu
- Połączenie z internetem (wymagane dla rozpoznawania mowy Google oraz wyszukiwania DuckDuckGo)

### Zależności Python

```bash
pip install openai speechrecognition ddgs pyaudio
```

> Uwaga: `pyaudio` bywa problematyczny w instalacji na niektórych systemach — na Windows warto skorzystać z gotowego wheela, na Linuksie zainstalować wcześniej `portaudio19-dev`.

## Uruchomienie

1. Uruchom lokalny model w LM Studio (lub innym serwerze kompatybilnym z OpenAI API) na porcie `1234`.
2. Uruchom skrypt:

```bash
python main.py
```

3. Poczekaj na kalibrację szumu tła, a następnie powiedz polecenie zawierające słowo „Jarvis”.

## Znane ograniczenia

- Cały kod znajduje się w jednym pliku (`main.py`) — mimo nazwy w opisie, nie jest to w pełni modularna architektura.
- Rozpoznawanie mowy opiera się na Google Speech API, więc mimo lokalnego LLM projekt nadal wymaga dostępu do internetu.
- Brak pliku `requirements.txt`, testów i obsługi konfiguracji zewnętrznej (adres serwera LLM jest zahardkodowany w kodzie).
- Aktywacja słowem kluczowym odbywa się po pełnym rozpoznaniu wypowiedzi, a nie przez dedykowany mechanizm wake-word.

## Licencja

Brak określonej licencji — projekt prywatny/eksperymentalny.
