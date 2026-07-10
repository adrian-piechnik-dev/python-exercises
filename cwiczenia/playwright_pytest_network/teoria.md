# pytest-playwright i sieć pod kontrolą — teoria

## 1. O czym jest ten temat

W temacie 24 poznałeś robota (Playwright) i sam budowałeś dla niego
garaż: fixture z przeglądarką, yield, sprzątanie. Ten temat ma dwie
części:

1. **wtyczka pytest-playwright** — gotowy garaż: przeglądarkę i kartę
   dostajesz „za darmo", jako wbudowane fixture;
2. **sieć pod kontrolą** — nauczysz robota przechwytywać ruch
   sieciowy strony (`page.route`), testować API bez przeglądarki
   (`request_context`) oraz nagrywać swoje poczynania (codegen, trace).

To jest dokładnie ta sama idea PODMIANY, którą znasz z monkeypatch
i mocków (tematy 11/13) — zmienia się tylko narzędzie.

## 2. Wtyczka pytest-playwright — garaż w pakiecie

Instalacja (przeglądarki Chromium masz już z tematu 24):

```
pip install pytest-playwright
```

Wtyczka to rozszerzenie pytest: po instalacji pytest automatycznie
zyskuje nowe fixture. Pamiętasz, ile pracy kosztowała Cię w temacie 24
własna fixture `przegladarka` (start, launch, yield, close, stop)?
Wtyczka robi to wszystko za Ciebie. W teście po prostu piszesz:

```python
from playwright.sync_api import Page


def test_cos(page: Page) -> None:
    page.set_content("<h1>Czesc</h1>")
```

- `page` — wbudowana fixture wtyczki: ŚWIEŻA karta dla każdego testu,
  w współdzielonej przeglądarce (dokładnie wzorzec, który sam
  budowałeś: sesyjny silnik + karta per test). Sprzątanie w pakiecie.
- inne wbudowane fixture: `context` (kontekst przeglądarki — „profil",
  w którym żyją karty; przyda się do nagrywania trace) oraz
  `playwright` (sam silnik — przyda się do testów API).

### Przełączniki z linii poleceń

Wtyczka dodaje też opcje do komendy pytest:

```
pytest --headed          # pokaz okno przegladarki (do podgladania)
pytest --headless        # bez okna (domyslne)
pytest --browser firefox # odpal testy w innej przegladarce
```

- `--headed` / `--headless` — znasz te pojęcia z tematu 24
  (`headless=True` w launch) — tu sterujesz nimi bez zmiany kodu.

### Typowe błędy początkujących
- Pisanie własnej fixture o nazwie `page` — przykryjesz fixture
  wtyczki i wszystko się pomiesza. Nazwy `page`, `context`, `browser`,
  `playwright` są zajęte.
- Zdziwienie „skąd test bierze page?" — z wtyczki; jeśli
  `pip install pytest-playwright` nie zostal wykonany, pytest krzyknie
  `fixture 'page' not found`.

## 3. page.route — celnik na granicy przeglądarki

Strona internetowa bez przerwy wysyła zapytania: po HTML, po obrazki,
po dane z API. `page.route` stawia na granicy CELNIKA: każde zapytanie
pasujące do wzorca trafia najpierw do Twojej funkcji, a Ty decydujesz,
co z nim zrobić — podstawić własną odpowiedź albo je zablokować.

```python
def podstaw_dane(route):
    route.fulfill(status=200, json={"miasto": "Krakow"})


page.route("**/api/dane", podstaw_dane)
page.goto("https://sklep.testowy/api/dane")
```

Linijka po linijce:
- `def podstaw_dane(route):` — Twój celnik: zwykła funkcja, która
  dostaje obiekt `route` (zatrzymane zapytanie z pełną władzą nad nim).
- `route.fulfill(...)` — „odpowiedz za serwer": zapytanie NIGDY nie
  wychodzi w internet, przeglądarka dostaje Twoją odpowiedź.
  Parametry: `status` (np. 200), `json=` (słownik/lista jako treść)
  ALBO `body=` (surowy tekst) + `content_type=` (np. `"text/html"`).
- `page.route("**/api/dane", podstaw_dane)` — rejestracja celnika:
  wzorzec + funkcja. `**` we wzorcu znaczy „cokolwiek" (dowolny
  protokół, domena, początek ścieżki) — `**/api/dane` złapie
  `https://cokolwiek.pl/api/dane`.
- KOLEJNOŚĆ ŚWIĘTA: celnik musi stanąć na granicy ZANIM ruch ruszy —
  `page.route(...)` zawsze PRZED `page.goto(...)`.

Dzięki temu `page.goto` na adres, którego NIE MA w internecie, działa
w teście doskonale — bo odpowiedź podstawia celnik. Zero sieci, pełna
kontrola. Poznajesz ten wzorzec? W temacie 23 to samo robił
`httpx.MockTransport` z funkcją-recepcjonistką — ta sama idea, inne
narzędzie.

### Podstawianie całej strony HTML

```python
def podstaw_strone(route):
    route.fulfill(
        status=200,
        body="<html><head><title>Atrapa</title></head></html>",
        content_type="text/html",
    )


page.route("https://sklep.testowy/sklep", podstaw_strone)
page.goto("https://sklep.testowy/sklep")
```

- `body=` + `content_type="text/html"` — przeglądarka dostaje tekst
  i informację „to jest HTML, wyrenderuj go jak stronę".

### Funkcja w funkcji — celnik, który pamięta

Celnik dostaje tylko `route` — a skąd ma wziąć TREŚĆ do podstawienia,
gdy piszesz funkcję ogólną? Definiujesz go WEWNĄTRZ swojej funkcji:

```python
def podmien_strone(page, url, html):
    def celnik(route):
        route.fulfill(status=200, body=html, content_type="text/html")

    page.route(url, celnik)
```

- `def celnik(route):` wewnątrz `podmien_strone` — funkcja
  zdefiniowana w środku innej funkcji. Wolno tak! Zaleta: celnik
  WIDZI zmienne funkcji, w której się urodził (tu: `html`) —
  i PAMIĘTA je nawet wtedy, gdy Playwright wywoła go dużo później.
  To się nazywa domknięcie (closure) — jak liścik w kieszeni celnika:
  wypisany przy rejestracji, odczytany przy kontroli.

### route.abort — celnik odmawia

```python
def zablokuj(route):
    route.abort()


page.route("**/*.png", zablokuj)
```

- `route.abort()` — zapytanie zostaje UBITE: przeglądarka zachowuje
  się, jakby sieć odmówiła. Wzorzec `**/*.png` łapie każdy adres
  kończący się na `.png` — tak blokuje się obrazki/reklamy, żeby
  testy były szybsze.
- Strona przeżyje brak obrazka (będzie po prostu pusty). Ale jeśli
  zrobisz `page.goto` PROSTO na zablokowany adres — nawigacja się
  nie uda i Playwright rzuci wyjątek `Error` (ogólny błąd Playwright,
  importowany z `playwright.sync_api`).

### Trik testowy: obejrzyj zmockowany JSON w przeglądarce

Gdy `route.fulfill(json=...)` odpowiada na adres, a Ty zrobisz
`page.goto` na ten adres, przeglądarka wyświetli surowy JSON jako
tekst na stronie — więc `page.get_by_text("Krakow")` znajdzie
wartość ze słownika. Wykorzystasz to w testach zadania o mockowaniu
JSON-a.

### Typowe błędy początkujących
- `page.route` PO `page.goto` — ruch już przeszedł, celnik spóźniony.
- `route.fulfill(json=...)` i `body=` naraz — wybierz jedno.
- Zapomnienie, że celnik to funkcja PRZEKAZYWANA (bez nawiasów!):
  `page.route(wzorzec, celnik)`, nie `page.route(wzorzec, celnik())`.
- Literówka we wzorcu (`*/api/dane` zamiast `**/api/dane`) — celnik
  nic nie łapie i zapytanie leci w prawdziwy internet.

## 4. Odczyt wielu elementów naraz — all_inner_texts

Z tematu 24 znasz `inner_text()` (tekst JEDNEGO elementu) i wiesz,
że locator może wskazywać wiele elementów naraz (`count()`).
Dla tekstów wszystkich naraz jest:

```python
teksty = page.get_by_role("listitem").all_inner_texts()
```

- `.all_inner_texts()` — lista tekstów wszystkich pasujących
  elementów, w kolejności ze strony; pusta lista, gdy nic nie pasuje.
  (`listitem` to rola elementu listy `<li>`.)

Przypomnienie jednym zdaniem: `expect(...).to_be_visible(timeout=...)`
znasz z tematu 24 — to asercja, która czeka; przyda się, zanim
odczytasz elementy dorysowane przez skrypt strony.

## 5. Testy API bez przeglądarki — request_context

Czasem nie chcesz renderować żadnej strony — chcesz tylko zapytać
API i sprawdzić odpowiedź, jak w testach API z tematu 16 (ta sama
idea: status + JSON, tylko narzędzie inne). Playwright ma do tego
osobny mechanizm — **APIRequestContext** (kontekst zapytań API):

```python
api = playwright.request.new_context()
response = api.get("http://127.0.0.1:8000/produkty")
print(response.status)   # 200
print(response.ok)       # True (ok = status 200-299)
print(response.json())   # [{"id": 1, "nazwa": "kubek"}]
api.dispose()
```

Linijka po linijce:
- `playwright.request.new_context()` — zbuduj „telefon do API"
  (obiekt `playwright` bierzesz z fixture wtyczki o tej nazwie).
- `api.get(url)` / `api.post(url, data=slownik)` — wyślij zapytanie;
  `data=` ze słownikiem samo zamieni się w JSON w treści zapytania.
  Wzorzec znasz z requests (temat 11) — tu nawet bez await.
- `response.status` — kod odpowiedzi (int), `response.ok` — wygodny
  skrót „czy status jest z rodziny 2xx" (bool), `response.json()` —
  treść jako słownik/lista.
- `api.dispose()` — odłóż słuchawkę (sprzątanie; we fixture zrobisz
  to po yield).

UWAGA, ważna różnica: celnicy z `page.route` pilnują GRANICY
PRZEGLĄDARKI — zapytania z `APIRequestContext` idą inną bramą
i route ich NIE przechwyci. Dlatego do testów API postawimy prawdziwy,
malutki serwer na Twoim komputerze (następna sekcja).

### Typowe błędy początkujących
- Próba mockowania `api.get` przez `page.route` — nie zadziała,
  to osobna brama.
- `response.json` bez nawiasów — to metoda.
- Zapominanie `dispose()` — telefon wisi do końca sesji.

## 6. Udawany serwer — budka z lemoniadą na podwórku

Prawdziwe API w internecie bywa wolne, płatne i zmienne. Do testów
stawia się własną BUDKĘ Z LEMONIADĄ: malutki serwer HTTP na Twoim
komputerze, serwujący z góry ustalone odpowiedzi. Postawimy go
narzędziami z samej biblioteki standardowej — `http.server`
i `threading`.

```python
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class Sprzedawca(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/lemoniada":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"cena": 5}).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"blad": "nie ma"}).encode("utf-8"))

    def log_message(self, format, *args):
        pass


serwer = HTTPServer(("127.0.0.1", 0), Sprzedawca)
port = serwer.server_address[1]
threading.Thread(target=serwer.serve_forever, daemon=True).start()
# ...serwer dziala pod http://127.0.0.1:{port} ...
serwer.shutdown()
```

Linijka po linijce:
- `class Sprzedawca(BaseHTTPRequestHandler):` — Twój sprzedawca
  w budce; dziedziczy (dwukropek w nawiasie = „jest rodzajem")
  po gotowym pomocniku ze stdlib, który umie rozmawiać protokołem
  HTTP — Ty dopisujesz tylko, CO odpowiadać.
- `def do_GET(self):` — metoda wywoływana automatycznie przy każdym
  zapytaniu GET. Analogicznie `do_POST` obsłuży POST.
- `self.path` — sama końcówka adresu (np. `"/lemoniada"`) — po niej
  rozpoznajesz, o co klient pyta (jak `request.url.path`
  u recepcjonistki z tematu 23 — ta sama idea).
- Odpowiedź składa się ZAWSZE z trzech kroków w tej kolejności:
  `send_response(200)` (kod), `send_header(...)` + `end_headers()`
  (nagłówki i ich zamknięcie), `wfile.write(...)` (treść).
- `json.dumps(slownik)` — słownik na tekst JSON (znasz z tematu 7);
  `.encode("utf-8")` — tekst na bajty, bo `wfile.write` przyjmuje
  tylko bajty (rura do klienta przenosi bajty, nie napisy).
- `log_message` z `pass` — ucisza sprzedawcę (domyślnie wypisuje
  każde zapytanie na konsolę i zaśmieca wynik testów).
- `HTTPServer(("127.0.0.1", 0), Sprzedawca)` — budka na adresie
  lokalnym; port `0` = „wybierz sam pierwszy wolny" (żeby testy
  nie pobiły się o zajęty port). Wylosowany port odczytujesz
  z `serwer.server_address[1]`.
- `threading.Thread(target=serwer.serve_forever, daemon=True).start()`
  — serwer musi obsługiwać klientów CIĄGLE (`serve_forever` to pętla
  bez końca), więc odpalamy go w OSOBNYM WĄTKU — jak pomocnik
  w budce, który pracuje, podczas gdy Ty (test) robisz swoje.
  `daemon=True` = „pomocnik znika razem z końcem programu"
  (nie przytrzyma pytest przy życiu). `target=` dostaje funkcję
  BEZ nawiasów.
- `serwer.shutdown()` — zamknij budkę (we fixture: po yield).

W `do_POST` dochodzi jeden krok: odbierz treść zapytania, żeby nie
zatkać rury — `self.rfile.read(int(self.headers.get("Content-Length", 0)))`
(przeczytaj dokładnie tyle bajtów, ile klient zapowiedział
w nagłówku Content-Length).

### Typowe błędy początkujących
- `wfile.write(json.dumps(...))` bez `.encode("utf-8")` →
  `TypeError: a bytes-like object is required`.
- Zamiana kolejności: treść przed `end_headers()` — odpowiedź
  wychodzi połamana.
- Sztywny port (`8000`) zamiast `0` — drugi bieg testów zastaje
  port zajęty.
- Brak `daemon=True` — pytest kończy testy i… wisi w nieskończoność.

## 7. codegen — magnetofon, który pisze kod

`playwright codegen` to narzędzie uruchamiane W TERMINALU (nie
w kodzie): otwiera przeglądarkę, a obok okno, w którym NA ŻYWO
powstaje kod Pythona odpowiadający Twoim kliknięciom:

```
playwright codegen https://example.com
```

- klikasz, wpisujesz, zaznaczasz — a codegen zapisuje każdy ruch
  jako gotowe `page.get_by_role(...).click()` z poprawnymi locatorami.
  Magnetofon do nagrywania szkiców testów: nagrywasz scenariusz,
  kopiujesz kod, doprawiasz asercje.

### Typowe błędy początkujących
- Wklejanie nagrania 1:1 jako testu — codegen nagrywa RUCHY, ale nie
  wie, CO chcesz sprawdzić; asercje (expect) dopisujesz sam.

## 8. Trace — czarna skrzynka lotu

Test padł w CI o 3 w nocy — co się stało? **Trace** to czarna
skrzynka samolotu: nagranie CAŁEGO przebiegu (zrzuty ekranu, migawki
DOM, każda akcja), które można odtworzyć po katastrofie.

Nagrywanie steruje się z poziomu KONTEKSTU (fixture `context`):

```python
context.tracing.start(screenshots=True, snapshots=True)
# ...akcje na stronach tego kontekstu...
context.tracing.stop(path="nagranie.zip")
```

- `tracing.start(screenshots=True, snapshots=True)` — włącz nagrywanie:
  zrzuty ekranu (film poklatkowy) + migawki DOM (możliwość „cofnięcia
  czasu" i obejrzenia strony z każdej chwili).
- `tracing.stop(path="nagranie.zip")` — zatrzymaj i zapisz nagranie
  do pliku `.zip` pod podaną ścieżką.

Nagranie ogląda się narzędziem terminalowym:

```
playwright show-trace nagranie.zip
```

### Typowe błędy początkujących
- `stop()` bez `path=` — nagranie przepada zamiast trafić do pliku.
- Szukanie trace'a w formacie wideo — to `.zip` do otwarcia przez
  `playwright show-trace`, nie plik mp4.

## 9. Ściąga zazębienia: podmiany, które już znasz

Ideę podmiany prawdziwego zasobu atrapą znasz z monkeypatch i mocków
(tematy 11/13) oraz MockTransport (temat 23) — jedno zdanie
przypomnienia i mapa na nowe narzędzie:

| stare narzędzie (tematy 11/13/23) | odpowiednik w tym temacie |
|---|---|
| `monkeypatch.setattr` (podmień funkcję) | `page.route` (podmień odpowiedź sieci) |
| `return_value` mocka (ustaw wynik) | `route.fulfill` (ustaw odpowiedź) |
| `side_effect` z wyjątkiem (symuluj awarię) | `route.abort` (symuluj awarię sieci) |
| `httpx.MockTransport` (udawany internet) | `page.route` + `route.fulfill` |

## 10. Teoria testowa

### Po co jest conftest.py i co robi sys.path.insert

Gdy pytest uruchamia `test_playwright_pytest_network.py`, ten plik
robi `from playwright_pytest_network import ...`. Python szuka
modułów tylko w miejscach z listy `sys.path` — a folderu tematu tam
nie ma (pytest bywa uruchamiany z głównego folderu repo). Dlatego
w `conftest.py` (wczytywanym przez pytest automatycznie, przed
testami) dopisujemy folder tematu na początek listy:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` — pełna ścieżka do conftest.py,
- `os.path.dirname(...)` — utnij nazwę pliku, zostaw folder,
- `sys.path.insert(0, ...)` — wstaw folder na pozycję 0, żeby wygrał
  z innymi miejscami poszukiwań.

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

W docstringu każdego testu odpowiadasz na trzy pytania:

1. **Co testuję?** — którą funkcję i które jej zachowanie.
2. **Co udaję?** — czego nie robię naprawdę (u nas: internetu — 
   zastępują go celnicy z route albo lokalna budka-serwer).
3. **Co sprawdzam?** — jaki konkretnie assert kończy test.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Cztery fazy ciała testu. Przykład z INNEJ dziedziny niż ten temat —
funkcja sprawdzająca, czy termostat ma włączyć grzanie:

```python
def test_termostat_wlacza_grzanie_ponizej_progu() -> None:
    """Co testuje: czy przy 17 stopniach i progu 20 grzanie sie wlacza.
    Co udaje: czujnik temperatury — podaje sztywna wartosc 17.
    Co sprawdzam: wynik is True.
    """
    temperatura_z_czujnika = 17.0                       # przygotuj (podmien)
    wynik = czy_grzac(temperatura_z_czujnika, prog=20.0)   # wywołaj
    assert wynik is True                                # sprawdź
```

### Narzędzia, które już znasz — przypomnienia jednym zdaniem

- fixture z `yield` i `scope="session"` — temat 24 (przygotuj przed
  yield, sprzątaj po; session = jedna sztuka na całą sesję),
- `tmp_path` — świeży folder tymczasowy od pytest (tu: na plik trace),
- `pytest.raises` — blok, który MUSI rzucić wskazany wyjątek
  (tu: `Error` z `playwright.sync_api` przy goto na zablokowany adres).

### Typowe błędy początkujących
- Rejestrowanie celników PO nawigacji (spóźniony celnik = prawdziwa
  sieć w teście).
- Budowanie własnej fixture `page` obok wtyczki.
- Testy API na cudzym, prawdziwym API — dziś 200, jutro limit zapytań
  i czerwono; budka-serwer jest Twoja i niezmienna.

## 11. Co dalej

W zadaniach: rozgrzewka na fixture wtyczki → celnicy (podmiana strony,
podmiana JSON-a API, blokada obrazków) → testy REST przez
request_context na lokalnej budce-serwerze (status, JSON z kontraktem
None, POST) → komendy codegen i show-trace → nagranie prawdziwego
trace'a do pliku → tłumacz starych podmian na nowe → finał: sklep
działający w 100% offline, gdzie celnicy podstawiają i stronę, i jej API.
