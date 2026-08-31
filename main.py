import json
import speech_recognition as sr
import webbrowser
from openai import OpenAI
from ddgs import DDGS
from datetime import datetime

dzisiaj = datetime.now().strftime("%d.%m.%Y")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def otworz_youtube():
    """otwiera strone główną youtube"""
    webbrowser.open("https://www.youtube.com/")
    return "Otworzyłem YouTube w przeglądarce."

def szukaj_w_internecie(zapytanie: str) -> str:
    try:
        with DDGS() as ddgs:
            wyniki = list(ddgs.text(zapytanie, region='pl-pl', max_results=6))
            if not wyniki:
                return "Brak wyników w wyszukiwarce"
            tekst_wynikow = "\n\n".join(
                f"Tytuł: {w.get('title', '')}\nFragment: {w.get('body', '')}" 
                for w in wyniki
            )
            return tekst_wynikow

    except Exception as e:
        print(f"[Błąd DuckDuckGo]: {e}")
        return f"Błąd podczas wyszukiwania: {e}"


mapa_funkcji = {
    "otworz_youtube": otworz_youtube,
    "szukaj_w_internecie": szukaj_w_internecie
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "otworz_youtube",
            "description": "Uruchom lub otwórz stronę YouTube w przeglądarce.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
            "type": "function",
            "function": {
                "name": "szukaj_w_internecie",
                "description": "Użyj ZA KAŻDYM RAZEM, gdy użytkownik pyta o pogodę, aktualne dane, fakty ze świata, wiedzę o grach, filmach lub cokolwiek wymagającego weryfikacji.",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "zapytanie": {
                            "type": "string",
                            "description": "Fraza do wyszukania w Google/DuckDuckGo"
                        }
                    },
                    "required": ["zapytanie"]
                    }
            }
        }
]

messages = [
    {
        "role": "system",
        "content": (
            f"Jesteś asystentem głosowym Jarvis. Dzisiejsza data: {dzisiaj}.\n"
            "Odpowiadaj naturalnie, zwięźle i bez znaczników Markdown.\n"
            "Podczas wyszukiwania formułuj ogólne, naturalne zapytania (np. 'kto jest prezydentem Polski', a nie na siłę dodając rok).\n"
            "Odpowiedzi na pytania o stan obecny formułuj na podstawie najnowszych faktów znalezionych w wynikach wyszukiwania."
        )
        
    }
]

def zapytaj_jarvisa(prompt: str) -> str:
    """Wysyła prompt do lokalnego LLM i zwraca odpowiedź."""
    messages.append({"role": "user", "content": prompt})
    

    response = client.chat.completions.create(
        model="local-model",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.7
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append({
            "role": "assistant",
            "content":msg.content or "",
            "tool_calls": msg.tool_calls
        })
        for tool_call in msg.tool_calls:
            nazwa = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"[Jarvis wywołuje funkcje: {nazwa}]")

            if nazwa in mapa_funkcji:
                wynik = mapa_funkcji[nazwa](**args)
            else:
                wynik = f"Nie znaleziono funkcji: {nazwa}"
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(wynik) if wynik else "Brak danych"
            })
        druga_odpowiedz = client.chat.completions.create(
            model="local-model",
            messages=messages,
            temperature=0.3
        )
        odpowiedz = druga_odpowiedz.choices[0].message.content
    else:
        odpowiedz = msg.content
    messages.append({"role": "assistant", "content": odpowiedz})
    return odpowiedz

def main():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Kalibracja szumu")
        r.adjust_for_ambient_noise(source, duration=1)

    print("Asystent czuwa w tle. Zawołaj 'Jarvis'...")

    while True:
        with sr.Microphone() as source:

            try:
                print("Say something!")
                audio = r.listen(source)
                raw_text = r.recognize_google(audio, language='pl-PL')
                print("Użytkownik:", raw_text)
                text=raw_text.lower()

                if "jarvis" in text:
                    odpowiedz = zapytaj_jarvisa(text)
                    print(f"Jarvis: {odpowiedz}")

            except sr.UnknownValueError:
                print("nie rozumiem")
            except Exception as e:
                print(f"Błąd: {e}")

if __name__ == "__main__":
    main()