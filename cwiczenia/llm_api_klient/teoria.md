# LLM API — klient do /v1/messages (requests + wyjątki + logging)

> Znasz już try/except i kolejność wyjątków szczegółowy→ogólny z tematu 4 —
> tutaj użyjesz tego do budowy odpornego klienta API. Biblioteka `requests`
> i moduł `logging` pojawiają się w tym temacie po raz pierwszy, więc dostają
> pełną teorię poniżej.

---

## Jak rozmawia się z modelem językowym przez API

Wyobraź sobie okienko pocztowe. Piszesz list (żądanie, po angielsku *request*),
wrzucasz do okienka pod konkretnym adresem, a po chwili dostajesz list zwrotny
(odpowiedź, *response*). Dokładnie tak działa API modelu językowego:

- **adres** to URL: `https://api.anthropic.com/v1/messages`
- **list** to żądanie HTTP typu **POST** — takie, które NIESIE dane
  (w przeciwieństwie do GET, które tylko o dane prosi)
- **treść listu** to payload — słownik z pytaniem do modelu
- **koperta** ma nagłówki (headers) — informacje "techniczne": kto pyta,
  jaką wersją API mówi, w jakim formacie jest treść

W Pythonie takie listy wysyła biblioteka `requests`.

---

## requests.post — wysyłanie żądania

`requests` to zewnętrzna biblioteka (third-party — w importach idzie po stdlib,
oddzielona pustą linią). Jej funkcja `post` wysyła żądanie POST:

```python
import requests

odpowiedz = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={"x-api-key": "sk-abc"},
    json={"model": "claude-sonnet-4-6"},
    timeout=30,
)
```

Linijka po linijce:
- pierwszy argument — URL, pod który leci żądanie,
- `headers=` — słownik nagłówków (koperta),
- `json=` — słownik z treścią; `requests` SAM zamienia go na tekst JSON
  i ustawia odpowiedni format przesyłki (nie musisz wołać `json.dumps`),
- `timeout=30` — maksymalnie 30 sekund czekania na odpowiedź; po tym czasie
  `requests` rzuca wyjątek zamiast wisieć w nieskończoność.

`requests.post` zwraca obiekt odpowiedzi (`requests.Response`), który ma:
- `odpowiedz.status_code` — kod HTTP (200 = sukces, 401 = zły klucz,
  500 = błąd serwera),
- `odpowiedz.json()` — treść odpowiedzi zamieniona z JSON na słownik Pythona,
- `odpowiedz.raise_for_status()` — nic nie robi przy sukcesie (2xx),
  a przy kodzie błędu (4xx/5xx) rzuca wyjątek `requests.exceptions.HTTPError`.
  To wygodny "bezpiecznik": zamiast ręcznie sprawdzać `status_code`,
  wołasz jedną metodę i błąd sam się zgłasza.

### Typowe błędy — requests.post
- Brak `timeout=` — gdy serwer nie odpowiada, program wisi bez końca.
  ZAWSZE podawaj timeout.
- `data=` zamiast `json=` — `data=` wysyła dane w innym formacie
  (formularz), a API modeli wymaga JSON. Używaj `json=`.
- `odpowiedz.json` bez nawiasów — to metoda, wołaj `odpowiedz.json()`.

---

## Nagłówki żądania do /v1/messages

API Anthropic wymaga trzech nagłówków:

```python
naglowki = {
    "x-api-key": "sk-abc123",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}
```

- `x-api-key` — Twój sekretny klucz, jak karta wstępu do budynku.
  Bez niego serwer odpowie kodem 401 (brak autoryzacji).
- `anthropic-version` — data wersji API, zawsze `"2023-06-01"`.
  Skąd się wzięło: API z czasem się zmienia; podając datę "przypinasz się"
  do konkretnej wersji i Twój kod nie zepsuje się przy zmianach.
- `content-type: application/json` — informacja "treść listu to JSON".

### Typowe błędy — nagłówki
- Literówki w nazwach (`x-api_key`, `Anthropic-Version` z wielkiej litery
  bywa tolerowane, ale trzymaj się dokładnie dokumentacji: małe litery,
  myślniki).
- Wstawianie klucza API do payloadu zamiast do nagłówków — klucz zawsze
  jedzie w kopercie (headers), nie w treści listu.

---

## Payload — treść zapytania do modelu

```python
payload = {
    "model": "claude-sonnet-4-6",
    "max_tokens": 100,
    "messages": [
        {"role": "user", "content": "Jaka jest stolica Polski?"},
    ],
}
```

- `model` — nazwa modelu, do którego piszesz.
- `max_tokens` — górny limit długości odpowiedzi (token ≈ kawałek słowa).
  To pole jest WYMAGANE — bez niego serwer odrzuci żądanie.
- `messages` — **lista** słowników. Dlaczego lista? Bo rozmowa może mieć
  wiele tur (user pyta, model odpowiada, user dopytuje...). Każda tura to
  słownik z `"role"` (`"user"` = Ty) i `"content"` (treść).

### Typowe błędy — payload
- `messages` jako pojedynczy słownik zamiast listy słowników —
  serwer wymaga listy, nawet gdy wiadomość jest jedna.
- Pominięcie `max_tokens` — pole obowiązkowe.
- `"rola"` / `"tresc"` po polsku — klucze to dokładnie `"role"` i `"content"`.

---

## Struktura odpowiedzi i parsowanie content[0]["text"]

Po `odpowiedz.json()` dostajesz słownik. Najważniejszy fragment:

```python
dane = {
    "content": [
        {"type": "text", "text": "Stolica Polski to Warszawa."},
    ],
}
```

`"content"` to **lista bloków** — model może zwrócić kilka kawałków treści
różnych typów, dlatego lista. Tekst pierwszego bloku wyciągasz tak:

```python
tekst = dane["content"][0]["text"]
```

Czytaj od lewej: weź wartość klucza `"content"` (lista) → weź element `[0]`
(pierwszy blok, słownik) → weź wartość klucza `"text"` (string).

Uwaga: gdy serwer zwraca błąd, w odpowiedzi NIE ma klucza `"content"` —
jest za to klucz `"error"`. Wtedy `dane["content"]` rzuci `KeyError`,
a `dane["content"][0]` na pustej liście rzuci `IndexError`. Odporny kod
łapie oba wyjątki i zwraca `None` (kontrakt: `str | None` — funkcja zwraca
string albo None, nigdy "komunikat błędu jako string").

### Typowe błędy — parsowanie
- `dane["content"]["text"]` — pominięcie `[0]`; `"content"` to lista,
  najpierw wybierz element.
- Zakładanie, że struktura zawsze jest poprawna — błędna odpowiedź nie ma
  `"content"`; bez try/except program się wywraca.

---

## Wyjątki requests — 4 warstwy obsługi

Z tematu 4 pamiętasz: w try/except wyjątki łapie się od SZCZEGÓŁOWEGO
do OGÓLNEGO. Biblioteka `requests` ma rodzinę wyjątków
w `requests.exceptions`:

| Warstwa | Wyjątek | Kiedy |
|---|---|---|
| 1 | `requests.exceptions.Timeout` | serwer nie odpowiedział w `timeout` sekund |
| 2 | `requests.exceptions.ConnectionError` | brak internetu / zły adres |
| 3 | `requests.exceptions.HTTPError` | `raise_for_status()` przy kodzie 4xx/5xx |
| 4 | `requests.exceptions.RequestException` | RODZIC wszystkich powyższych — łapie każdy inny błąd requests |

`RequestException` musi być OSTATNI: to klasa-rodzic, więc gdyby stała
pierwsza, przechwyciłaby wszystko i warstwy 1–3 nigdy by nie zadziałały.

```python
try:
    odpowiedz = requests.post(url, headers=naglowki, json=payload, timeout=30)
    odpowiedz.raise_for_status()
except requests.exceptions.Timeout as error:
    ...
except requests.exceptions.ConnectionError as error:
    ...
except requests.exceptions.HTTPError as error:
    ...
except requests.exceptions.RequestException as error:
    ...
```

Zauważ: `raise_for_status()` stoi WEWNĄTRZ try — to on rzuca `HTTPError`.

### Typowe błędy — warstwy wyjątków
- `RequestException` jako pierwszy except — połyka wszystkie pozostałe.
- `raise_for_status()` poza blokiem try — `HTTPError` wyleci nieobsłużony.

---

## Klasa w pigułce

Za chwilę spotkasz `class` w dwóch miejscach: własny wyjątek w module zadań
i atrapa odpowiedzi w testach. Klasa to PRZEPIS na obiekt — jak foremka
do ciastek: z jednej foremki (klasy) robisz wiele ciastek (obiektów).

```python
class Termometr:
    """Prosty termometr pamiętający jedną temperaturę."""

    def __init__(self, temperatura: float) -> None:
        self.temperatura = temperatura

    def odczyt(self) -> float:
        return self.temperatura
```

Linijka po linijce:
- `class Termometr:` — definicja przepisu; nazwy klas piszemy WielkąLiterą
  (PEP 8), bez podkreśleń.
- `def __init__(self, temperatura)` — specjalna metoda uruchamiana przy
  TWORZENIU obiektu; tu zapisujesz dane do środka.
- `self` — "ten konkretny obiekt". Każda metoda klasy dostaje `self` jako
  pierwszy parametr automatycznie — Ty go nie przekazujesz przy wywołaniu.
- `self.temperatura = temperatura` — zapis wartości do ATRYBUTU obiektu;
  atrybut żyje w obiekcie tak długo jak sam obiekt.
- `def odczyt(self)` — zwykła metoda; czyta atrybut przez `self.`.

Użycie:

```python
t = Termometr(36.6)     # __init__ dostaje 36.6, self powstaje automatycznie
t.odczyt()              # 36.6 — metodę wołasz z nawiasami
```

### Typowe błędy — klasy
- Zapomnienie `self` w definicji metody — `TypeError` przy wywołaniu.
- `t.odczyt` bez nawiasów — dostajesz metodę zamiast wyniku.
- `temperatura = temperatura` zamiast `self.temperatura = temperatura` —
  wartość znika po zakończeniu `__init__`.

---

## Własny wyjątek i raise ... from

Twój klient będzie miał JEDEN własny typ błędu:

```python
class BladKlientaLLM(Exception):
    """Wyjątek sygnalizujący błąd komunikacji z API modelu."""
```

Dwie linijki i koniec: `class BladKlientaLLM(Exception)` znaczy
"nowy typ wyjątku, dziedziczy po wbudowanym `Exception`" — dzięki temu
można go rzucać (`raise`) i łapać (`except`) jak każdy inny wyjątek.
Ciała nie potrzebuje — sam docstring wystarczy.

Po co własny wyjątek? Ktoś, kto używa Twojego klienta, nie chce znać
czterech typów błędów requests — chce złapać JEDEN: `BladKlientaLLM`.
Ale oryginalna przyczyna nie może zginąć. Do tego służy `raise ... from`:

```python
except requests.exceptions.Timeout as error:
    raise BladKlientaLLM("Przekroczono limit czasu") from error
```

- `as error` — łapiesz oryginalny wyjątek do zmiennej,
- `raise BladKlientaLLM(...)` — rzucasz SWÓJ wyjątek z czytelnym komunikatem,
- `from error` — doklejasz oryginał jako PRZYCZYNĘ; w traceback zobaczysz
  "The above exception was the direct cause of the following exception"
  i pełną historię błędu.

### Typowe błędy — raise ... from
- `raise BladKlientaLLM(...)` bez `from error` — przyczyna ginie,
  debugowanie staje się zgadywanką.
- `print("błąd")` + `return "błąd"` zamiast raise — łamie kontrakt funkcji
  (string-jako-błąd); błąd sygnalizujemy wyjątkiem albo None.

---

## logging — dziennik pokładowy programu

`print` znika po zamknięciu konsoli i nie mówi, KIEDY i JAK WAŻNE było
zdarzenie. Moduł `logging` (stdlib) prowadzi dziennik z POZIOMAMI:
INFO (zwykłe zdarzenie), ERROR (coś poszło źle) i innymi.

```python
import logging

logging.info("Wysylam zapytanie do modelu %s, max_tokens=%s", model, max_tokens)
logging.error("Blad klienta LLM: %s", komunikat)
```

Zwróć uwagę na `%s`: to NIE jest f-string. Podajesz szablon z `%s`
i wartości jako OSOBNE argumenty, a `logging` sam je wstawi — ale tylko
wtedy, gdy dany poziom jest w ogóle zapisywany. Dlaczego tak:
- wydajność — przy wyłączonym poziomie sklejanie tekstu w ogóle się nie
  odbywa (f-string skleiłby się zawsze, nawet do kosza),
- konwencja — narzędzia analizujące logi grupują wpisy po szablonie.

Domyślnie logging pokazuje tylko WARNING i wyżej. Żeby zobaczyć INFO,
program (nie moduł!) konfiguruje próg:

```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
```

Dlaczego w `__main__` (znasz z tematu 4)? Moduł-biblioteka nie powinien
narzucać konfiguracji temu, kto go importuje. Konfiguruje ten, kto
URUCHAMIA program — czyli blok `__main__`.

### Typowe błędy — logging
- `logging.info(f"model {model}")` — f-string zamiast `%s`; działa,
  ale formatuje zawsze i psuje analizę logów. Używaj `%s` + argumenty.
- `basicConfig` na poziomie modułu (poza `__main__`) — konfiguracja
  "wycieka" do każdego, kto zaimportuje moduł.
- `logging.error()` w miejscu, gdzie powinien polecieć wyjątek — log
  informuje, ale NIE przerywa; to nie zamiennik raise.

---

## Teoria testowa

conftest.py i `sys.path.insert` znasz z poprzednich tematów — dzięki nim
plik testów widzi moduł `llm_api_klient.py` z tego samego folderu.

### Schemat 3 pytań

Każdy test odpowiada w docstringu na:

1. **Co testuje?** — jaką konkretną wartość lub efekt sprawdzam
2. **Co udaje?** — co podmieniam zamiast prawdziwego środowiska
3. **Co sprawdzam?** — jakie twierdzenie zawiera assert

### Schemat przygotuj → podmień → wywołaj → sprawdź

W tym temacie po raz pierwszy będziesz UDAWAĆ prawdziwy świat: testy nie
mogą wysyłać żądań do prawdziwego API (koszt, internet, losowość odpowiedzi).
Przykład z INNEJ dziedziny — funkcja rzucająca kością:

```python
import random


def rzut_koscia() -> int:
    """Zwraca wynik rzutu kością.

    Args:
        Brak.

    Returns:
        int: liczba oczek od 1 do 6.
    """
    return random.randint(1, 6)
```

Test nie może polegać na losowości — podmienia `random.randint`:

```python
def test_rzut_koscia_zwraca_podmieniony_wynik(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy rzut_koscia zwraca to, co wylosuje randint.
    Co udaje: random.randint — podmieniam na funkcję zwracającą zawsze 6.
    Co sprawdzam: wynik == 6.
    """
    # przygotuj: fałszywa funkcja o TEJ SAMEJ sygnaturze co oryginał
    def falszywy_randint(a: int, b: int) -> int:
        return 6

    # podmień
    monkeypatch.setattr(random, "randint", falszywy_randint)

    # wywołaj
    wynik = rzut_koscia()

    # sprawdź
    assert wynik == 6
```

### monkeypatch — podmiana na czas testu

`monkeypatch` to wbudowany fixture pytest (nic nie importujesz — pytest
wstrzykuje go, gdy wpiszesz `monkeypatch` jako parametr testu; type hint:
`pytest.MonkeyPatch`).

```python
monkeypatch.setattr(random, "randint", falszywy_randint)
```

Czytaj: "w obiekcie `random` podmień atrybut o nazwie `"randint"` na
`falszywy_randint`". Po zakończeniu testu pytest AUTOMATYCZNIE przywraca
oryginał — inne testy dostają czysty świat.

W tym temacie będziesz podmieniać `requests.post`:

```python
monkeypatch.setattr(requests, "post", falszywy_post)
```

Fałszywa funkcja musi przyjmować te same argumenty, które przekazuje
testowany kod (`url`, `headers`, `json`, `timeout`). Gdy test chce
sprawdzić, CO zostało przekazane, fałszywka zapisuje argumenty do słownika:

```python
zapisane: dict = {}


def falszywy_post(
    url: str, headers: dict, json: dict, timeout: int
) -> FalszywaOdpowiedz:
    zapisane["url"] = url
    zapisane["json"] = json
    zapisane["timeout"] = timeout
    return odpowiedz_ok
```

Po wywołaniu testowanej funkcji zaglądasz do `zapisane` i robisz asserty.

#### Typowe błędy — monkeypatch
- Podmiana PO wywołaniu testowanej funkcji — kolejność: najpierw
  `setattr`, potem wywołanie.
- Fałszywka z inną sygnaturą niż oryginał — `TypeError` w środku testu.

### Atrapa odpowiedzi — po co klasa w conftest

Testowany kod woła na odpowiedzi METODY: `odpowiedz.json()`,
`odpowiedz.raise_for_status()`. Zwykły słownik ich nie ma — dlatego
w conftest.py budujesz małą klasę `FalszywaOdpowiedz` z tymi metodami
(teorię klas masz wyżej). Testowany kod nie zauważa różnicy: obchodzi go
tylko to, że obiekt MA te metody, nie skąd pochodzi.

### pytest.raises — test, który OCZEKUJE wyjątku

Jak sprawdzić, że funkcja rzuca wyjątek? Zwykły assert nie zadziała —
wyjątek przerwałby test. Do tego jest `pytest.raises` (tu potrzebny
import pytest):

```python
with pytest.raises(KeyError):
    slownik_bez_klucza["brakuje"]
```

Test PRZECHODZI, gdy w bloku `with` poleci wyjątek podanego typu.
Test PADA, gdy wyjątek NIE poleci (albo poleci inny typ).

#### Typowe błędy — pytest.raises
- Wywołanie funkcji POZA blokiem with — wyjątek leci przed wejściem
  w `pytest.raises` i test się wywraca.
- Zbyt ogólny typ (`Exception`) — test przejdzie przy każdym błędzie,
  także nieoczekiwanym; podawaj konkretny typ.

### caplog — przechwytywanie logów w teście

`caplog` to wbudowany fixture pytest (type hint: `pytest.LogCaptureFixture`)
łapiący wszystko, co program wysłał do logging:

```python
def test_funkcja_loguje_start(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    funkcja_ktora_loguje()
    assert "start" in caplog.text
```

- `caplog.set_level(logging.INFO)` — bez tego caplog łapie dopiero od
  WARNING, więc wpisy INFO by przepadły,
- `caplog.text` — jeden długi string ze wszystkimi wpisami: poziomami
  (np. `INFO`, `ERROR`) i komunikatami; sprawdzasz przez `in`.

#### Typowe błędy — caplog
- Brak `set_level` przy testowaniu `logging.info` — pusty `caplog.text`.
- Szukanie w `caplog.text` dokładnego pełnego wpisu — sprawdzaj fragment
  przez `in`, nie równość.
