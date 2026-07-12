# Teoria — mini_api_katalog (mini-projekt M2)

To drugi mini-projekt (jak M1): NIE uczysz się nowej biblioteki,
tylko składasz znane klocki z tematów 11 (requests), 7 (JSON)
i 16 (FastAPI + Pydantic) w jedną działającą całość — własny
katalog produktów zasilany danymi z zewnętrznego API.

Znane pojęcia tylko PRZYPOMINAM jednym zdaniem (wracaj do starych
teorii, gdy coś umknęło); od zera tłumaczę wyłącznie kilka NOWYCH
rzeczy. TODO w zadaniach mówią CO osiągnąć i odsyłają do wzorców —
nie dyktują kodu linijka po linijce. Piszesz logikę z głowy.

---

## 1. Co budujemy — mapa projektu

Wyobraź sobie mały sklep osiedlowy:

1. **Hurtownia** — wielki magazyn gdzieś daleko (zewnętrzne API).
   Jeździsz tam po towar (requests.get), czasem na kilka razy,
   bo do auta nie mieści się wszystko naraz (paginacja).
2. **Wybór towaru** — z hurtowni bierzesz tylko to, co się sprzeda:
   produkty dostępne, i tylko potrzebne informacje o nich
   (filtrowanie i przycinanie słowników).
3. **Półka w sklepie** — towar układasz u siebie (lokalny plik JSON).
   Klient nie czeka, aż pojedziesz do hurtowni — bierze z półki.
4. **Lada sklepowa** — klienci kupują u CIEBIE, nie w hurtowni
   (własne API FastAPI: lista produktów, szczegóły jednego,
   przyjmowanie nowych — z bramkarzem Pydantic przy wejściu).

Ten sam przepływ w numerach zadań:

```
zewnętrzne API (hurtownia)
   │  zadanie_01 (pobranie z kontrolą błędów)   ← temat 11
   │  zadanie_02 (pobranie strona po stronie)   ← temat 11 + NOWE 1
   ▼
surowa lista produktów (za dużo pól, część niedostępna)
   │  zadanie_03 (filtr dostępnych)             ← temat 2
   │  zadanie_04 (tylko potrzebne pola)         ← temat 3
   │  zadanie_05 (szukanie po id)               ← tematy 2-3
   ▼
czysty katalog
   │  zadanie_06 (zapis na półkę = plik JSON)   ← temat 7
   │  zadanie_07 (odczyt półki z kontrolą)      ← temat 7
   ▼
plik katalog.json
   │  zadanie_08 (bramkarz Pydantic)            ← temat 16 + NOWE 2
   │  zadanie_09 (GET lista)                    ← temat 16
   │  zadanie_10 (GET szczegóły + 404)          ← temat 16 + NOWE 3
   │  zadanie_11 (POST dodawanie)               ← temat 16
   ▼
zadanie_12 = dyrygent zaopatrzenia (hurtownia -> półka)
zadanie_13 = dyrygent całości (półka -> gotowy sklep z ladą)
```

---

## 2. Czego NIE tłumaczymy od nowa (przypomnienia jednozdaniowe)

- **requests.get(url, params=..., timeout=...)**, `status_code`,
  `raise_for_status()`, `response.json()` i łapanie
  `requests.RequestException` (rodzic wszystkich błędów sieci,
  także HTTPError z raise_for_status): temat 11.
- **Kontrakt None** przy spodziewanym braku (plik, sieć): tematy 1, 4-5.
- **list comprehension** z warunkiem `[x for x in lista if ...]`:
  temat 2; **budowanie słowników** i dostęp przez klucz: temat 3.
- **json.dump / json.load** na plikach (z `with open(...)`),
  `json.JSONDecodeError` przy zepsutej treści: temat 7.
- **FastAPI()**, endpoint jako `def w def` wewnątrz funkcji-fabryki,
  `@app.get` / `@app.post`, **parametr ścieżki z type hintem int**
  (automatyczne 422), **BaseModel** jako treść POST (złe dane = 422),
  `produkt.model_dump()`, **TestClient**: temat 16.
- **monkeypatch.setattr** i atrapa **FakeResponse** (podmieniaj tam,
  gdzie funkcja UŻYWA, czyli w module tego tematu): tematy 11 i 13.
- **tmp_path**: temat 10.

Jeśli coś z powyższych brzmi obco — najpierw tamta teoria, potem M2.

---

## 3. NOWE pojęcie 1: paginacja i sklejanie list (.extend)

### Co to jest?

Paginacja (stronicowanie) to sposób, w jaki API oddaje DUŻE zbiory
danych: nie wszystko naraz, tylko porcjami — strona 1, strona 2, 3...
Jak przeprowadzka: nie zniesiesz całego mieszkania w jednych rękach,
robisz kilka kursów.

O numer strony prosisz przez znany ci parametr zapytania:

```python
odpowiedz = requests.get(url, params={"strona": 2}, timeout=10)
```

### Skąd się wzięło?

Gdyby hurtownia z milionem produktów odpowiadała całością naraz,
odpowiedź ważyłaby gigabajty i padłoby i API, i twój program.
Dlatego serwery narzucają porcje, a klient (ty) dokleja porcję
do porcji.

### Dlaczego tak musi być?

Do doklejania służy metoda list `.extend()`:

```python
wszystkie = []
for numer in range(1, 4):
    porcja = pobierz_strone(numer)
    wszystkie.extend(porcja)
```

- `wszystkie = []` — akumulator, znasz go z tematu 2.
- `range(1, 4)` — liczby 1, 2, 3 (koniec zakresu jest WYŁĄCZONY —
  dlatego przy trzech stronach piszesz range(1, liczba_stron + 1)).
- `wszystkie.extend(porcja)` — dokleja KAŻDY element listy `porcja`
  na koniec `wszystkie`. Różnica względem znanego `.append()`:
  append wrzuciłby całą listę jako JEDEN element (lista w liście),
  extend wsypuje jej zawartość element po elemencie.

### Typowe błędy początkujących

- `.append(porcja)` zamiast `.extend(porcja)` — dostajesz listę list
  `[[...], [...]]` zamiast płaskiej listy produktów.
- `range(1, liczba_stron)` — gubisz ostatnią stronę (koniec wyłączony).
- Zapominanie, że `.extend()` zwraca None i modyfikuje listę
  w miejscu — `wszystkie = wszystkie.extend(porcja)` kasuje ci dane.

---

## 4. NOWE pojęcie 2: rozpakowanie słownika ** i łapanie ValidationError

### Co to jest?

Operator `**` przy wywołaniu funkcji rozpakowuje słownik na argumenty
nazwane. Te dwa wywołania znaczą DOKŁADNIE to samo:

```python
dane = {"tytul": "Diuna", "rok": 1965}
Ksiazka(tytul="Diuna", rok=1965)
Ksiazka(**dane)
```

(Przykład na książkach — twoje zadania mają inne pola.)

### Skąd się wzięło?

Dane z pliku czy z sieci przychodzą jako słownik — a model Pydantic
(znasz z tematu 16) przyjmuje argumenty nazwane. Bez `**` musiałbyś
przepisywać każde pole ręcznie: `Ksiazka(tytul=dane["tytul"], ...)`.
Przy 10 polach to męczarnia i proszenie się o literówkę.

### Dlaczego tak musi być?

- `**dane` mówi Pythonowi: „każdy klucz słownika potraktuj jak nazwę
  argumentu, a wartość jak jego wartość".
- Klucze muszą więc być stringami zgodnymi z nazwami pól modelu —
  jeśli w słowniku jest klucz, którego model nie zna, albo brakuje
  wymaganego, Pydantic rzuca `ValidationError`.
- `ValidationError` importujesz z pydantic i łapiesz jak każdy
  wyjątek (wzorzec z tematu 4). W temacie 16 tylko wiedziałeś, że
  ten wyjątek istnieje — teraz robisz z niego bramkę jakości
  z kontraktem None (dokładnie jak walidacja kwot w M1):

```python
from pydantic import ValidationError

try:
    ksiazka = Ksiazka(**dane)
except ValidationError:
    return None
```

### Typowe błędy początkujących

- `Ksiazka(dane)` bez `**` — model dostaje JEDEN argument pozycyjny
  (cały słownik) i wybucha; rozpakowanie to `**`, nie sama nazwa.
- `except Exception:` zamiast `except ValidationError:` — łapiesz
  za dużo i ukrywasz prawdziwe bugi (np. NameError z literówki).
- Mylenie `**` w wywołaniu (rozpakowanie) z `**` w potędze `2 ** 3` —
  znaczenie zależy od miejsca: w środku nawiasów wywołania funkcji
  to zawsze rozpakowanie.

---

## 5. NOWE pojęcie 3: HTTPException — mówienie klientowi „nie ma"

### Co to jest?

`HTTPException` to wyjątek FastAPI, którym endpoint odpowiada
klientowi konkretnym kodem błędu HTTP:

```python
from fastapi import FastAPI, HTTPException

@app.get("/ksiazki/{numer}")
def szczegoly(numer: int) -> dict:
    ksiazka = znajdz(numer)
    if ksiazka is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    return ksiazka
```

### Skąd się wzięło?

Znasz kod 422 (FastAPI wysyła go SAM, gdy dane wejściowe nie przejdą
walidacji — temat 16) i kod 404 z tematu 11 (dostawałeś go od cudzych
API, gdy zasób nie istniał). Teraz strony się odwracają: to TWOJE API
musi umieć powiedzieć „nie mam produktu o tym id". Do tego służy
właśnie 404 — a HTTPException to mechanizm, którym go wysyłasz.

### Dlaczego tak musi być?

- `raise`, nie `return`! Wyjątek przerywa funkcję endpointu
  natychmiast, a FastAPI łapie go i zamienia na odpowiedź HTTP
  z podanym kodem. Zwrócenie `HTTPException(...)` returnem
  wysłałoby klientowi dziwny obiekt z kodem 200 („wszystko OK").
- `status_code=404` — kod odpowiedzi; `detail="..."` — komunikat,
  który klient zobaczy w treści JSON jako {"detail": "..."}.
- Wewnątrz endpointu NIE obowiązuje kontrakt None: endpoint
  rozmawia protokołem HTTP, a w nim „braku" sygnalizuje się kodem,
  nie None-em. Kontrakt None zostaje dla zwykłych funkcji Pythona
  (np. tych, które endpoint woła pod spodem).

### Typowe błędy początkujących

- `return HTTPException(...)` zamiast `raise` — klient dostaje 200
  z treścią wyglądającą jak błąd; klasyczny bug w API.
- Zwracanie None z endpointu, gdy zasobu brak — klient dostaje 200
  z pustą treścią i nie wie, że coś poszło nie tak.
- `HTTPException(404)` bez nazwy argumentu zadziała, ale pisz
  `status_code=404` — czytelniej i zgodnie z dokumentacją FastAPI.

---

## 6. Sekcja przekrojowa: architektura sklepu (cache w pliku)

Najważniejsza decyzja projektowa M2: **własne API NIE dzwoni do
hurtowni przy każdym zapytaniu klienta**. Zaopatrzenie (pobranie +
filtrowanie + zapis do pliku) to osobny krok, uruchamiany raz;
lada sklepowa (endpointy) czyta wyłącznie z lokalnej półki (pliku).

Dlaczego tak?

- **Szybkość** — odczyt pliku to ułamki milisekund; strzał do
  cudzego API przez internet to setki. Klient nie może czekać.
- **Odporność** — hurtownia może paść, a twój sklep dalej sprzedaje
  to, co ma na półce.
- **Grzeczność** — nie zalewasz cudzego API tysiącem zapytań;
  tę zasadę szacunku znasz już ze scrapingu (temat 12).

Taki wzorzec (lokalna kopia cudzych danych) nazywa się **cache**.
Cena: dane na półce mogą się zestarzeć — dlatego dyrygent
zaopatrzenia (zadanie 12) jest osobną funkcją, którą można
uruchomić ponownie, gdy chcesz odświeżyć towar.

Druga zasada, znana z M1: **kontrakt None płynie przez pipeline** —
gdy hurtownia nie odpowiada (zadanie 01 zwraca None), dyrygenci
(zadania 12-13) przerywają się early returnem i też zwracają None,
a na dysku NIE zostaje ani pusty, ani na wpół zapisany plik.

---

## 7. Teoria testowa

### Po co conftest.py i sys.path.insert — przypomnienie

pytest odpalany z głównego folderu repo nie widzi modułu
`mini_api_katalog.py`; `sys.path.insert(0, ...)` w conftest.py
dopisuje folder tematu do miejsc, gdzie Python szuka modułów.
conftest.py to też dom fixture i klas pomocniczych — pytest
wczytuje go sam.

**Jak w M1: conftest dostajesz GOTOWY, bez TODO** (reguła
mini-projektów — dane i infrastruktura gotowe, ty piszesz logikę
i asserty). Jest tam też gotowa klasa `FakeResponse` — dokładnie
ta, którą sam budowałeś w temacie 11. Przeczytaj conftest uważnie,
zanim zaczniesz testować.

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

1. **Co testuję?** — który klocek i który jego obowiązek.
2. **Co udaję?** — co podmieniam atrapą (tu: requests.get, żeby
   testy nie chodziły po prawdziwej sieci) albo nic, gdy wystarczy
   tmp_path.
3. **Co sprawdzam?** — konkretny assert kończący test.

Docstringi testów mają te odpowiedzi wypełnione — przekładasz je
na kod.

### Schemat przygotuj → podmień → wywołaj → sprawdź

Przykład na INNYM temacie niż ten projekt — funkcja `losuj_nagrode`,
która pod spodem używa `random.choice`:

```python
def test_losuj_nagrode_zwraca_wylosowana(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def podmieniony_choice(lista):                        # przygotuj
        return "hulajnoga"
    monkeypatch.setattr(                                  # podmień
        "loteria.random.choice", podmieniony_choice
    )
    wynik = losuj_nagrode(["rower", "hulajnoga"])         # wywołaj
    assert wynik == "hulajnoga"                           # sprawdź
```

Zwróć uwagę: podmieniamy `random.choice` W MODULE `loteria`, bo tam
funkcja go używa. W tym projekcie działa identyczna zasada —
podmianę `requests.get` w module tematu znasz z tematu 11 i tu
stosujesz ją bez zmian (atrapą jest gotowa FakeResponse z conftest;
podmieniona funkcja może też RZUCIĆ wyjątek, żeby udać padniętą sieć).

W testach endpointów nic nie podmieniasz — TestClient z tematu 16
rozmawia z aplikacją bez sieci, a pliki dostajesz od tmp_path.

### Gotowe fixture i klasy w conftest.py tego projektu

| Nazwa             | Co daje                                                     |
|-------------------|-------------------------------------------------------------|
| `FakeResponse`    | klasa-atrapa odpowiedzi HTTP: status_code, json(), raise_for_status() |
| `surowe_produkty` | lista 4 słowników z hurtowni (pola: id, nazwa, cena, dostepny, magazyn); dostępne są 3: id 1, 3, 4 |
| `czyste_produkty` | lista 3 dostępnych produktów przyciętych do pól id/nazwa/cena |
| `katalog_json`    | Path do gotowego pliku JSON z zawartością czyste_produkty   |
| `zepsuty_json`    | Path do pliku, który JSON-em tylko udaje (do testu odczytu) |

Dane kontrolne (sprawdź sam w conftest.py): produkty to Klawiatura
99.0 (id 1), Mysz 49.0 (id 2, NIEdostępna), Monitor 899.0 (id 3),
Kabel HDMI 25.0 (id 4).
