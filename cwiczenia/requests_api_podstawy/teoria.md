# requests — rozmowa z API

## Co to jest API i HTTP?

Wyobraź sobie restaurację. Ty (program) nie wchodzisz do kuchni (serwera) —
składasz zamówienie kelnerowi, a kelner przynosi danie. API to właśnie taki
kelner: umówiony sposób składania zamówień do cudzego serwera i odbierania
odpowiedzi.

Zamówienia składa się w języku HTTP. Dwa najważniejsze rodzaje zamówień
(tzw. metody):

- **GET** — „poproszę dane" (nic nie zmieniasz, tylko czytasz),
- **POST** — „przynoszę dane" (wysyłasz coś do zapisania).

Odpowiedź serwera zawiera dwie rzeczy, które nas interesują:
**kod statusu** (czy się udało) i **treść** (najczęściej JSON — znasz go
z tematu 7).

## Biblioteka requests

`requests` to najpopularniejsza biblioteka Pythona do rozmów przez HTTP.
Jest zewnętrzna (jak pandas i openpyxl):

```
pip install requests
```

```python
import requests
```

---

## requests.get — poproszę dane

```python
import requests

response = requests.get("https://api.przyklad.pl/uzytkownicy", timeout=10)
```

Linijka po linijce:
- `requests.get(url, ...)` — wysyła zamówienie GET pod podany adres.
- `timeout=10` — czekaj najwyżej 10 sekund; potem przerwij z błędem.
- `response` — obiekt odpowiedzi; w środku siedzi kod statusu i treść.

> **Reguła kursu: timeout ZAWSZE.** Bez `timeout` program może wisieć
> w nieskończoność, gdy serwer nie odpowiada. Każde `requests.get`
> i `requests.post` w tym temacie ma mieć `timeout=10`.

### Typowe błędy początkujących

- Brak `timeout` — program zawisa na zawsze przy głuchym serwerze.
- `requests.get(url).json()` w jednej linii bez sprawdzenia, czy się
  udało — o obsłudze błędów za chwilę.

---

## response.status_code — czy się udało?

Serwer zawsze odpowiada trzycyfrowym kodem:

```python
response = requests.get("https://api.przyklad.pl/uzytkownicy", timeout=10)
print(response.status_code)   # 200
```

Najważniejsze kody:
- **200** — OK, wszystko się udało,
- **404** — nie znaleziono (literówka w adresie),
- **500** — serwer się wywalił (nie twoja wina).

Zasada ogólna: 2xx = sukces, 4xx = błąd po twojej stronie, 5xx = błąd serwera.

```python
if response.status_code == 200:
    print("sukces")
```

### Typowe błędy początkujących

- `response.status_code == "200"` — kod to **int**, nie string.

---

## response.json() — treść odpowiedzi jako słownik

Serwery API odpowiadają JSON-em. Metoda `.json()` robi to samo,
co `json.loads()` z tematu 7 — zamienia tekst odpowiedzi na słownik
lub listę:

```python
response = requests.get("https://api.przyklad.pl/uzytkownik/1", timeout=10)
dane = response.json()
print(dane["imie"])   # Anna
```

Gdy API zwraca listę użytkowników, `.json()` da listę słowników —
dokładnie taką strukturę, jaką znasz z tematów 6-7.

### Typowe błędy początkujących

- `response.json` bez nawiasów — to metoda; bez `()` dostajesz obiekt
  metody zamiast danych.
- Wołanie `.json()` na odpowiedzi, która nie jest JSON-em (np. strona
  błędu HTML) — wyjątek; dlatego najpierw sprawdzamy status.

---

## params — zapytanie z parametrami

Czasem zamówienie trzeba doprecyzować: „użytkownicy, ale tylko z Warszawy,
strona 2". Do adresu dokleja się parametry — requests zrobi to za ciebie:

```python
response = requests.get(
    "https://api.przyklad.pl/uzytkownicy",
    params={"miasto": "Warszawa", "strona": 2},
    timeout=10,
)
```

- `params={...}` — słownik parametrów; requests sam doklei go do adresu
  jako `?miasto=Warszawa&strona=2` i zadba o poprawne kodowanie.

### Typowe błędy początkujących

- Ręczne sklejanie adresu `url + "?miasto=" + miasto` — działa do pierwszej
  polskiej litery lub spacji; od tego jest `params`.

---

## raise_for_status — zamień zły kod na wyjątek

Sprawdzanie `if status_code == 200` przy każdym wywołaniu jest upierdliwe.
`raise_for_status()` robi to za ciebie: **nic nie robi** przy sukcesie (2xx),
a przy 4xx/5xx **rzuca wyjątek** `requests.HTTPError`:

```python
response = requests.get("https://api.przyklad.pl/uzytkownik/1", timeout=10)
response.raise_for_status()   # tu wybuchnie przy 404 lub 500
dane = response.json()        # tu docieramy tylko przy sukcesie
```

Wzorzec: `raise_for_status()` zaraz po `get`/`post`, **przed** `.json()`.

### Typowe błędy początkujących

- `response.raise_for_status` bez nawiasów — metoda nie zostanie wywołana,
  błąd przejdzie niezauważony.
- `.json()` przed `raise_for_status()` — próbujesz parsować stronę błędu.

---

## RequestException — rodzina błędów sieciowych

Rozmowa przez sieć może się nie udać na wiele sposobów: brak internetu,
serwer nie odpowiada (timeout), zły kod statusu. Wszystkie błędy requests
dziedziczą po jednym przodku — `requests.RequestException`:

```
RequestException          ← przodek wszystkich
├── ConnectionError       ← brak połączenia z serwerem
├── Timeout               ← serwer nie zdążył przed timeout
└── HTTPError             ← zły kod statusu (z raise_for_status)
```

Znasz kolejność wyjątków z tematu 4 (szczegółowy → ogólny). Tu wystarczy
złapać przodka — złapie każde dziecko:

```python
import requests
from typing import Optional


def pobierz_dane(url: str) -> Optional[dict]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
```

Kontrakt funkcji jak zawsze: sukces → dane, każdy problem sieciowy → `None`.

### Typowe błędy początkujących

- `except Exception` — łapie za szeroko (także literówki w twoim kodzie);
  łap `requests.RequestException`.
- `except RequestException` bez przedrostka `requests.` — `NameError`,
  chyba że zaimportujesz osobno.

---

## requests.post — przynoszę dane

POST wysyła dane do serwera (rejestracja, dodanie wpisu):

```python
nowy = {"imie": "Anna", "wiek": 30}
response = requests.post(
    "https://api.przyklad.pl/uzytkownicy",
    json=nowy,
    timeout=10,
)
print(response.status_code)   # 201 (= utworzono)
```

- `json=nowy` — requests sam zamieni słownik na tekst JSON i ustawi
  odpowiedni typ treści. Nie robisz `json.dumps` ręcznie.
- Serwer zwykle odpowiada kodem **201** (utworzono) i odsyła zapisany
  obiekt w treści — `.json()` działa tak samo jak przy GET.

### headers — nagłówki zapytania

Nagłówki to metryczka doklejona do zamówienia — najczęściej klucz API
(dowód, że masz prawo pytać):

```python
naglowki = {"Authorization": "Bearer moj-tajny-klucz"}
response = requests.post(
    "https://api.przyklad.pl/uzytkownicy",
    json=nowy,
    headers=naglowki,
    timeout=10,
)
```

- `headers={...}` — słownik nagłówków; działa tak samo w `get` i `post`.

### Typowe błędy początkujących

- `requests.post(url, dane)` — dane jako drugi argument pozycyjny trafią
  w złe miejsce; zawsze nazwane `json=dane`.
- Mylenie `json=` (co wysyłasz) z `.json()` (co odbierasz).

---

## Zazębienie: odpowiedź API → plik (tematy 6-7)

Znasz `json.dump` (temat 7) i `csv.DictWriter` (temat 6) — tu tylko
przypomnienie jednym zdaniem: `json.dump(dane, f)` zapisuje strukturę
do otwartego pliku, a `csv.DictWriter(f, fieldnames=...)` +
`writeheader()` + `writerows(lista)` zapisuje listę słowników do CSV
(z `newline=""` i `encoding="utf-8"` przy `open`).

Wzorzec „pobierz i zapisz":

```python
response = requests.get(url, timeout=10)
response.raise_for_status()
dane = response.json()
with open("kopia.json", "w", encoding="utf-8") as f:
    json.dump(dane, f)
```

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Gdy pytest uruchamia `test_requests_api_podstawy.py`, Python musi znaleźć
moduł `requests_api_podstawy`. Folder tematu nie jest w `sys.path`, więc
`conftest.py` (ładowany automatycznie przed testami) dokleja go na początek:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie funkcji.
2. **Co udaje?** — w tym temacie wreszcie coś udajemy! Testy NIE chodzą
   po prawdziwym internecie — udają serwer (za chwilę zobaczysz jak).
3. **Co sprawdzam?** — co dokładnie weryfikuje `assert`.

### Dlaczego testy nie używają prawdziwego internetu?

Test musi być szybki, powtarzalny i działać w pociągu bez wifi. Prawdziwy
serwer bywa wolny, padnięty albo zwraca za każdym razem co innego. Dlatego
w testach **podmieniamy** `requests.get` na własną atrapę, która udaje
serwer i zwraca z góry ustaloną odpowiedź. Testujemy NASZĄ logikę
(co robimy z odpowiedzią), nie cudzy serwer.

### monkeypatch — podmiana na czas testu

`monkeypatch` to wbudowany fixture pytest (dostajesz go jak `tmp_path` —
przez parametr funkcji testowej). Podmienia dowolny atrybut na czas
jednego testu i **automatycznie przywraca oryginał** po teście:

```python
monkeypatch.setattr("modul.atrybut", nowa_wartosc)
```

- `setattr` — „ustaw atrybut": pierwszy argument to ścieżka (string)
  do podmienianego obiektu, drugi to zamiennik.
- Po zakończeniu testu pytest sam cofa podmianę — kolejny test widzi
  oryginał. Dlatego to bezpieczne.

Przykład na temacie INNYM niż HTTP — funkcja losująca rzut kostką:

```python
# kostka.py
import random


def rzut_kostka() -> int:
    return random.randint(1, 6)
```

Test nie może zależeć od losowości — podmieniamy `randint`:

```python
def test_rzut_kostka_zwraca_wylosowana_liczbe(monkeypatch) -> None:
    """Co testuje: czy rzut_kostka zwraca to, co wylosował randint.
    Co udaje: random.randint — zawsze zwraca 4 (bez prawdziwej losowości).
    Co sprawdzam: wynik == 4.
    """
    # przygotuj — zamiennik o tej samej "sygnaturze" co oryginał
    def podmieniony_randint(a, b):
        return 4

    # podmień — na czas tego jednego testu
    monkeypatch.setattr("kostka.random.randint", podmieniony_randint)

    # wywołaj
    wynik = rzut_kostka()

    # sprawdź
    assert wynik == 4
```

Zwróć uwagę na ścieżkę `"kostka.random.randint"` — podmieniamy `randint`
**widziany przez moduł kostka** (tam, gdzie jest używany). W tym temacie
analogicznie: `"requests_api_podstawy.requests.get"`.

To jest pełny schemat **przygotuj → podmień → wywołaj → sprawdź** —
w poprzednich tematach krok „podmień" był pusty, tu pracuje.

### FakeResponse — atrapa odpowiedzi serwera

Prawdziwe `requests.get` zwraca obiekt odpowiedzi (status_code, json(),
raise_for_status()). Nasza atrapa musi wyglądać tak samo — na tyle,
na ile funkcje z zadań jej używają. Budujemy ją klasą w `conftest.py`:

```python
class FakeResponse:
    def __init__(self, status_code, dane):
        self.status_code = status_code
        self._dane = dane

    def json(self):
        return self._dane

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"kod {self.status_code}")
```

- `__init__` zapamiętuje, jaki kod i jakie dane ma udawać.
- `json()` oddaje zapamiętane dane — jak prawdziwa odpowiedź.
- `raise_for_status()` rzuca `HTTPError` przy kodach 4xx/5xx — jak prawdziwa.
- `_dane` z podkreśleniem — konwencja: „atrybut wewnętrzny, nie ruszaj
  z zewnątrz".

W teście podmieniasz `requests.get` na funkcję zwracającą taką atrapę:

```python
def test_przyklad(monkeypatch) -> None:
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"imie": "Anna"})

    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    # ... wywołaj funkcję z zadania i sprawdź wynik ...
```

Zamiennik ma parametry `url, params=None, timeout=None`, żeby przyjąć
wszystko, co funkcje z zadań przekazują do `get`. Dla `post` analogicznie:
`url, json=None, headers=None, timeout=None`.

Do udawania awarii sieci podmieniasz get na funkcję, która **rzuca**:

```python
def podmieniony_get(url, params=None, timeout=None):
    raise requests.ConnectionError("brak internetu")
```

`ConnectionError` jest dzieckiem `RequestException`, więc `except
requests.RequestException` w testowanej funkcji go złapie.

### Typowe błędy początkujących — monkeypatch

- Podmiana `"requests.get"` zamiast `"requests_api_podstawy.requests.get"` —
  podmieniaj tam, gdzie funkcja jest UŻYWANA.
- Zamiennik bez parametrów `def podmieniony_get():` — `TypeError`, bo
  testowana funkcja woła go z argumentami (url, timeout...).
- Wywołanie zamiast podania: `monkeypatch.setattr(..., podmieniony_get())`
  z nawiasami — podajesz WYNIK funkcji zamiast samej funkcji; bez nawiasów.

### Fixture tmp_path (przypomnienie)

`tmp_path` znasz z poprzednich tematów: czysty folder tymczasowy (obiekt
`Path`), osobny dla każdego testu. W zadaniach 11-12 łączysz go
z monkeypatchem: atrapa udaje serwer, a funkcja zapisuje „pobrane" dane
do pliku w `tmp_path`.
