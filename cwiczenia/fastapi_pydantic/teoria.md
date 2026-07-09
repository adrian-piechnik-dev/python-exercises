# FastAPI i Pydantic — twoje własne API

## Druga strona lustra

W temacie 11 byłeś **klientem** restauracji: `requests.get` składało
zamówienia do cudzych API. Teraz przechodzisz na drugą stronę — budujesz
własną kuchnię. FastAPI to biblioteka, w której piszesz **serwer**:
program odbierający zapytania HTTP i odsyłający odpowiedzi JSON.

Pydantic to jego bramkarz: sprawdza, czy dane wchodzące do kuchni mają
właściwy kształt (czy „cena" to na pewno liczba?), i odsyła precyzyjny
błąd, gdy nie mają.

Instalacja (dwie biblioteki — druga potrzebna do testowania):

```
pip install fastapi httpx
```

---

## FastAPI() i pierwszy endpoint

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def powitanie() -> dict:
    return {"wiadomosc": "Witaj w API"}
```

Linijka po linijce:
- `app = FastAPI()` — tworzy aplikację: pustą „centralę telefoniczną",
  która będzie kierować zapytania do funkcji.
- `@app.get("/")` — dekorator-rejestracja: „gdy przyjdzie zapytanie GET
  na ścieżkę `/`, wywołaj funkcję poniżej". Taka para (metoda + ścieżka
  + funkcja) to **endpoint**.
- Funkcja zwraca zwykły słownik — FastAPI **sam** zamienia go na JSON
  (pamiętasz `json.dumps` z tematu 7? tu dzieje się automatycznie).

Ścieżka to część adresu po nazwie serwera: w `https://sklep.pl/produkty`
ścieżką jest `/produkty`. Jedna aplikacja może mieć wiele endpointów —
po prostu dopisujesz kolejne funkcje z dekoratorami.

### Endpoint wewnątrz funkcji zadania

W tym temacie każde zadanie **buduje i zwraca** własną mini-aplikację.
Endpointy definiuje się wtedy wewnątrz funkcji zadania (tak, `def`
w `def` — Python na to pozwala, a dekorator rejestruje funkcję w `app`
niezależnie od tego, gdzie ją zapisano):

```python
def zbuduj_aplikacje() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def powitanie() -> dict:
        return {"wiadomosc": "Witaj w API"}

    return app
```

- Wcięcie: wszystko, łącznie z dekoratorem, jedno piętro w głąb.
- Na końcu `return app` — funkcja oddaje gotową, skonfigurowaną aplikację.

### Typowe błędy początkujących

- `@app.get()` bez ścieżki — ścieżka jest obowiązkowa: `@app.get("/")`.
- `return powitanie` zamiast `return app` — zwracasz aplikację,
  nie funkcję endpointu.
- Zapomniane `return app` — funkcja zadania zwróci None i testy wywalą
  się przy tworzeniu klienta.

---

## Parametry ścieżki — {nazwa} + type hint = walidacja

Adres bywa „dziurawy": `/uzytkownicy/7`, `/uzytkownicy/42` — końcówka
to parametr. W FastAPI dziurę oznaczasz klamrami, a wartość wpada
do funkcji jako argument:

```python
@app.get("/uzytkownicy/{id_uzytkownika}")
def pobierz_uzytkownika(id_uzytkownika: int) -> dict:
    return {"id": id_uzytkownika}
```

- `{id_uzytkownika}` w ścieżce i parametr `id_uzytkownika` w funkcji —
  **te same nazwy**, tak FastAPI je paruje.
- Type hint `int` to nie dekoracja — to **rozkaz walidacji**: FastAPI
  skonwertuje `"7"` z adresu na `7` (int), a dla `/uzytkownicy/abc`
  sam odeśle błąd **422** — twoja funkcja nawet się nie uruchomi.

### Kod 422 — „rozumiem cię, ale dane są złe"

W temacie 11 poznałeś 200/404/500. Kod **422 Unprocessable Entity**
znaczy: zapytanie dotarło, ale dane w nim nie przechodzą walidacji
(tekst zamiast liczby, brakujące pole). To wizytówka FastAPI — dostajesz
go za darmo dzięki type hintom.

### Typowe błędy początkujących

- Inna nazwa w klamrach niż w parametrze funkcji — FastAPI zgłosi błąd
  przy starcie aplikacji.
- Brak type hinta — parametr przyjdzie jako string i `"7" * 2` da
  `"77"` zamiast `14`.

---

## BaseModel — formularz z bramkarzem

### Co to jest?

Gdy klient POST-em przysyła JSON (np. nowy produkt), trzeba sprawdzić:
są wszystkie pola? typy się zgadzają? Ręcznie to sito ifów. Pydantic
robi to deklaratywnie — opisujesz **kształt** danych klasą:

```python
from pydantic import BaseModel


class Produkt(BaseModel):
    nazwa: str
    cena: float
```

- Dziedziczysz po `BaseModel` (klasa w nawiasie) — stąd cała magia.
- Każde pole to linia `nazwa_pola: typ` — sam type hint, bez wartości.

Tworzenie obiektu i dostęp do pól:

```python
produkt = Produkt(nazwa="Mysz", cena=49.0)
print(produkt.nazwa)   # Mysz
print(produkt.cena)    # 49.0
```

Pydantic **konwertuje, co się da**: `Produkt(nazwa="Mysz", cena="49")`
przejdzie (string „49" to legalna liczba), ale `cena="darmo"` — już nie:

```python
from pydantic import ValidationError

try:
    Produkt(nazwa="Mysz", cena="darmo")
except ValidationError:
    print("złe dane!")
```

`ValidationError` — wyjątek Pydantica; w testach złapiesz go przez
`pytest.raises` (temat 13).

Model umie też zamienić się z powrotem w słownik — przyda się przy
zapisie do pliku JSON:

```python
produkt.model_dump()   # {"nazwa": "Mysz", "cena": 49.0}
```

### Typowe błędy początkujących

- `class Produkt:` bez `(BaseModel)` — zwykła klasa, zero walidacji.
- `nazwa = str` z `=` zamiast `:` — to przypisanie typu jako wartości,
  nie deklaracja pola.
- Łapanie `ValueError` zamiast `ValidationError` — akurat by zadziałało
  (ValidationError dziedziczy po ValueError), ale konwencja kursu:
  łap dokładnie `pydantic.ValidationError`.

---

## POST z modelem — FastAPI + Pydantic razem

```python
@app.post("/produkty")
def dodaj_produkt(produkt: Produkt) -> dict:
    return {"przyjeto": produkt.nazwa}
```

- `@app.post(...)` — rejestracja na metodę POST (klient **przynosi** dane).
- Parametr z type hintem **modelu** (`produkt: Produkt`) — FastAPI wie:
  weź JSON z treści zapytania, przepuść przez bramkarza Pydantic,
  podaj funkcji gotowy obiekt.
- Klient wyśle `{"nazwa": "Mysz", "cena": 49.0}` — funkcja dostanie
  `produkt` z atrybutami.
- Brak pola albo zły typ → automatyczne **422**, funkcja się nie uruchomi.

### Typowe błędy początkujących

- `produkt: dict` zamiast `produkt: Produkt` — dostaniesz surowy słownik
  bez walidacji; cała robota Pydantica przepada.
- Mylenie parametru ścieżki z treścią: parametry proste (int, str) FastAPI
  bierze ze ścieżki, parametry-modele — z treści (body) zapytania.

---

## response_model — cenzor odpowiedzi

Endpoint czasem „wie za dużo" — np. słownik z danymi ma pola, których
klient nie powinien zobaczyć. `response_model` to filtr na wyjściu:

```python
@app.get("/produkty/polecany", response_model=Produkt)
def polecany() -> dict:
    return {"nazwa": "Klawiatura", "cena": 99.0, "tajny_kod": "X99"}
```

- `response_model=Produkt` — w dekoratorze, obok ścieżki.
- FastAPI przytnie odpowiedź do pól modelu: klient dostanie tylko
  `nazwa` i `cena`; `tajny_kod` **nie wyjdzie** z serwera.
- Bonus: response_model to też dokumentacja („ten endpoint zwraca
  Produkt") i walidacja odpowiedzi.

To zazębienie z tematem 7: struktura JSON, którą projektowałeś ręcznie,
tu dostaje formalny opis — model odpowiedzi.

### Typowe błędy początkujących

- `response_model` jako parametr funkcji zamiast dekoratora — to
  ustawienie endpointu, nie argument.
- Odpowiedź bez któregoś pola modelu — FastAPI zgłosi błąd 500
  (odpowiedź nie przechodzi własnej walidacji).

---

## TestClient — odpytywanie API bez serwera

Jak przetestować serwer, nie uruchamiając serwera? `TestClient` —
zaślepka sieci wbudowana w FastAPI: podajesz mu aplikację, a on udaje
przeglądarkę i „dzwoni" do niej **wewnątrz procesu testu**:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

response = client.get("/")
print(response.status_code)   # 200
print(response.json())        # {"wiadomosc": "Witaj w API"}

response = client.post("/produkty", json={"nazwa": "Mysz", "cena": 49.0})
```

Interfejs znasz z tematu 11 — TestClient celowo naśladuje requests:
`.get(sciezka)`, `.post(sciezka, json=slownik)`, `.status_code`,
`.json()`. Różnica: zamiast pełnego adresu podajesz samą ścieżkę,
a „siecią" jest pamięć procesu.

### Typowe błędy początkujących

- `TestClient(zbuduj_aplikacje)` bez nawiasów wywołania — podajesz
  funkcję zamiast aplikacji; ma być `TestClient(zbuduj_aplikacje())`.
- `client.post(..., data=slownik)` — treść JSON przekazuje się przez
  `json=` (jak w requests).

---

## Zazębienie: pliki JSON i fixtures

W zadaniach 10-12 API czyta i zapisuje dane w pliku JSON — wzorce
`json.load`/`json.dump` (z `encoding="utf-8"` i `with`) znasz z tematu 7,
a dopisywanie do listy z pliku to dokładnie `dopisz_wpis` stamtąd.
W conftest.py zbudujesz fixture (temat 13) dostarczającą TestClient
gotowego API — „specjalny fixture", który zamiast danych podaje
całego klienta.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak zawsze: pytest musi znaleźć moduł `fastapi_pydantic`, a folder tematu
nie jest w `sys.path`. `conftest.py` dokleja go na początek:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretny endpoint/zachowanie.
2. **Co udaje?** — sieć: TestClient podmienia całą warstwę HTTP
  (zapytanie nigdy nie wychodzi z procesu); w zadaniach plikowych
  dodatkowo tmp_path udaje dysk produkcyjny.
3. **Co sprawdzam?** — status_code, treść `.json()`, zawartość pliku.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania — API biblioteki z książkami:

```python
def test_wypozyczenie_ksiazki_zwraca_potwierdzenie() -> None:
    """Co testuje: czy POST /wypozyczenia przyjmuje tytuł i potwierdza.
    Co udaje: sieć — TestClient woła aplikację w pamięci, bez serwera.
    Co sprawdzam: status 200 i pole "potwierdzono" w odpowiedzi.
    """
    # przygotuj + podmień (TestClient to gotowa podmiana sieci)
    client = TestClient(zbuduj_api_biblioteki())

    # wywołaj
    response = client.post("/wypozyczenia", json={"tytul": "Lalka"})

    # sprawdź
    assert response.status_code == 200
    assert response.json()["potwierdzono"] == "Lalka"
```

### Sprawdzanie odpowiedzi 422

Walidację testuje się, wysyłając celowo złe dane:

```python
response = client.post("/wypozyczenia", json={})   # brak pola tytul
assert response.status_code == 422
```

Nie sprawdzasz treści błędu 422 — wystarczy kod; szczegóły komunikatu
to sprawa FastAPI, nie twoja.
