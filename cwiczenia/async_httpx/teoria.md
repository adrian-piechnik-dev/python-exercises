# async/await i httpx — teoria

## 1. Problem: czekanie marnuje czas

Wyobraź sobie kelnera w restauracji. Kelner-amator podchodzi do
stolika 1, przyjmuje zamówienie, zanosi do kuchni i... STOI przy
kuchni 10 minut, aż danie będzie gotowe. Dopiero potem idzie do
stolika 2. Trzy stoliki = 30 minut stania.

Kelner-zawodowiec robi inaczej: przyjmuje zamówienie ze stolika 1,
oddaje do kuchni i — zamiast stać — idzie do stolika 2, potem 3.
Gdy kuchnia zadzwoni dzwonkiem „gotowe!", wraca po danie. Trzy
stoliki = ~10 minut, bo CZEKANIE się nakłada.

Twój dotychczasowy kod (np. `requests.get` z tematu 11) to
kelner-amator: wysyła zapytanie do internetu i BLOKUJE cały program,
aż odpowiedź wróci. Przy jednym URL-u to bez znaczenia. Przy
pięćdziesięciu — czekasz 50 razy z rzędu.

**Programowanie asynchroniczne (async)** to styl kelnera-zawodowca:
gdy jedno zadanie CZEKA (na internet, na dysk, na timer), program
w tym czasie robi inne zadania. Ważne: to nadal JEDEN kelner (jeden
wątek) — po prostu nie stoi bezczynnie.

### Typowe błędy początkujących
- Myślenie, że async przyspiesza OBLICZENIA (mnożenie macierzy itp.).
  Nie — async przyspiesza tylko CZEKANIE (sieć, dysk, sen). Kelner
  nie gotuje szybciej, on tylko nie stoi bezczynnie.

## 2. Coroutine — przepis, który umie czekać

Zwykłą funkcję znasz. Funkcję asynchroniczną definiuje się słowem
`async` przed `def`:

```python
async def zwroc_powitanie(imie: str) -> str:
    return f"Czesc, {imie}!"
```

Linijka po linijce:
- `async def` — „to jest funkcja asynchroniczna". Taka funkcja
  nazywa się **coroutine** (czyt. „korutina", po polsku czasem
  „współprogram").
- reszta — jak w zwykłej funkcji.

Najważniejsza pułapka całego tematu: **wywołanie coroutine NIE
uruchamia jej kodu**. Porównaj:

```python
wynik = zwroc_powitanie("Ala")
print(wynik)   # <coroutine object zwroc_powitanie at 0x...>
```

Dostałeś nie tekst, tylko dziwny „obiekt coroutine". Dlaczego?
Bo `async def` tworzy PRZEPIS na pracę, a nie samą pracę. To jak
zamówienie w restauracji: `zwroc_powitanie("Ala")` to wypisanie
karteczki z zamówieniem — kucharz jeszcze nie zaczął gotować.
Karteczkę trzeba dopiero oddać „dyrygentowi" (o nim za chwilę).

### Typowe błędy początkujących
- `wynik = moja_coroutine()` i zdziwienie, że wynik to
  `<coroutine object ...>` zamiast wartości. Coroutine trzeba
  uruchomić przez `asyncio.run` albo `await` — nigdy „samą siebie".
- Python wypisuje wtedy też ostrzeżenie
  `RuntimeWarning: coroutine ... was never awaited` — to znak, że
  wypisałeś zamówienie i nikt go nie zrealizował.

## 3. Event loop i asyncio.run — dyrygent orkiestry

Ktoś musi pilnować, które zadanie teraz gra, a które czeka.
Ten ktoś to **event loop** (pętla zdarzeń) — dyrygent orkiestry:
wskazuje batutą „teraz ty", a gdy muzyk ma pauzę, wskazuje innego.

Dyrygenta uruchamia się funkcją `asyncio.run` z wbudowanego
(stdlib) modułu `asyncio`:

```python
import asyncio


wynik = asyncio.run(zwroc_powitanie("Ala"))
print(wynik)   # Czesc, Ala!
```

Linijka po linijce:
- `import asyncio` — moduł stdlib, nic nie instalujesz.
- `asyncio.run(...)` — „weź tę coroutine, powołaj dyrygenta,
  wykonaj wszystko do końca i zwróć wynik". To BRAMA między światem
  zwykłym (synchronicznym) a asynchronicznym. Wywołujesz ją w zwykłym
  kodzie — nigdy wewnątrz `async def`.
- `asyncio.run` zwraca to, co coroutine zwróciła przez `return`.

Skąd się to wzięło? Ktoś musi „kręcić korbą" świata async — zwykły
Python sam z siebie tego nie robi. `asyncio.run` tworzy pętlę
zdarzeń, wykonuje zadanie i sprząta po sobie.

### Typowe błędy początkujących
- `asyncio.run(zwroc_powitanie)` — przekazanie FUNKCJI zamiast
  wywołania. Musi być `asyncio.run(zwroc_powitanie("Ala"))` —
  najpierw wypisujesz zamówienie (nawiasy!), potem oddajesz
  dyrygentowi.
- Wywołanie `asyncio.run` WEWNĄTRZ `async def` →
  `RuntimeError: asyncio.run() cannot be called from a running
  event loop`. Wewnątrz coroutine używa się `await`, nie `run`.

## 4. await — „czekaj, ale nie blokuj"

Wewnątrz `async def` (i TYLKO tam) możesz użyć słowa `await`:

```python
import asyncio


async def poczekaj_i_zwroc(sekundy: float, wartosc: str) -> str:
    await asyncio.sleep(sekundy)
    return wartosc
```

Linijka po linijce:
- `await asyncio.sleep(sekundy)` — „zaśnij na tyle sekund, ALE
  oddaj w tym czasie dyrygenta innym". `await` = „tu będę czekać —
  dyrygencie, zajmij się w międzyczasie resztą orkiestry".
- `asyncio.sleep` to asynchroniczny brat zwykłego `time.sleep`.
  Różnica fundamentalna: `time.sleep(2)` to kelner-amator (STOI
  i blokuje wszystko), `await asyncio.sleep(2)` to zawodowiec
  (czeka, ale inni pracują).

`await` stawiasz przed KAŻDĄ coroutine, którą wywołujesz z innej
coroutine:

```python
async def podwojne_powitanie() -> str:
    pierwsze = await zwroc_powitanie("Ala")
    drugie = await zwroc_powitanie("Ola")
    return pierwsze + " " + drugie
```

### Typowe błędy początkujących
- `await` poza `async def` → `SyntaxError: 'await' outside async
  function`. `await` działa tylko w środku coroutine.
- Zapomnienie `await` przed wywołaniem coroutine — dostajesz obiekt
  coroutine zamiast wyniku (i `RuntimeWarning`).
- Użycie `time.sleep` w kodzie async — działa, ale blokuje CAŁĄ
  orkiestrę. W async zawsze `await asyncio.sleep`.

## 5. asyncio.gather — odpal wszystko naraz

Sekwencyjne `await` po `await` (jak w `podwojne_powitanie` wyżej)
czeka na zadania PO KOLEI — kelner-amator wrócił! Żeby zadania
czekały RÓWNOLEGLE, jest `asyncio.gather` („zbierz"):

```python
import asyncio


async def dwa_naraz() -> list:
    wyniki = await asyncio.gather(
        poczekaj_i_zwroc(2.0, "pierwszy"),
        poczekaj_i_zwroc(2.0, "drugi"),
    )
    return wyniki   # ["pierwszy", "drugi"] — po ~2 s, nie ~4 s!
```

Linijka po linijce:
- `asyncio.gather(coroutine_a, coroutine_b, ...)` — przyjmuje DOWOLNIE
  wiele coroutine (oddzielonych przecinkami), uruchamia wszystkie
  naraz i czeka, aż skończy się OSTATNIA.
- `await` przed gather — bo samo gather też jest „czekaniem".
- Wynik to LISTA wyników w kolejności PODANIA (nie kończenia!) —
  nawet jeśli „drugi" skończył pierwszy, w liście będzie na pozycji 1.

Dwa spania po 2 sekundy trwają razem ~2 sekundy — bo czekanie się
nakłada. To jest CAŁY sens tego tematu w jednej linijce.

### Gwiazdka: lista coroutine → gather

`gather` przyjmuje coroutine wymienione po przecinku. A jeśli masz
je w LIŚCIE (np. zbudowanej pętlą)? Wtedy używasz operatora `*`
(gwiazdka), który „wysypuje" listę na osobne argumenty:

```python
zadania = [poczekaj_i_zwroc(1.0, "a"), poczekaj_i_zwroc(1.0, "b")]
wyniki = await asyncio.gather(*zadania)
```

- `*zadania` — „rozpakuj listę": `gather(*[a, b])` to dokładnie to
  samo co `gather(a, b)`. Bez gwiazdki gather dostałby JEDEN argument
  (całą listę) i się wywalił.

To standardowy wzorzec na „pobierz N rzeczy naraz":

```python
zadania = [pobierz(url) for url in lista_urli]
wyniki = await asyncio.gather(*zadania)
```

### Typowe błędy początkujących
- `await asyncio.gather(zadania)` bez gwiazdki, gdy `zadania` to
  lista → `TypeError`. Lista wymaga `*zadania`.
- Oczekiwanie, że kolejność wyników = kolejność KOŃCZENIA.
  Nie — kolejność wyników = kolejność PODANIA.
- `gather` na pustej liście (`gather(*[])`) jest legalny — zwraca
  pustą listę. Warto wiedzieć, to nasz przypadek brzegowy.

## 6. Mierzenie czasu — time.perf_counter

Żeby UDOWODNIĆ, że async jest szybszy, trzeba zmierzyć czas.
W stdlib jest do tego `time.perf_counter` (performance counter —
licznik wydajności):

```python
import time


start = time.perf_counter()
# ...cos, co trwa...
czas = time.perf_counter() - start   # ile sekund minelo (float)
```

- `time.perf_counter()` — zwraca odczyt bardzo dokładnego stopera
  (float, w sekundach). Sama liczba nic nie znaczy — znaczenie ma
  RÓŻNICA dwóch odczytów: stoper „klik" na starcie, „klik" na mecie,
  odejmujesz i masz czas trwania.
- Dlaczego nie `time.time()`? `perf_counter` jest dokładniejszy
  i nie przeskakuje, gdy system zmienia zegar — do pomiarów zawsze on.

W zadaniach porównasz: N spań wykonanych sekwencyjnie (await po
await w pętli) kontra te same spania przez `gather`. Sekwencyjnie
czas ≈ SUMA spań, równolegle ≈ NAJDŁUŻSZE spanie.

### Typowe błędy początkujących
- `time.perf_counter` bez nawiasów w odejmowaniu — odejmujesz
  funkcje zamiast liczb.
- Porównywanie czasów co do sekundy („ma być równo 0.1") — pomiary
  zawsze mają drobny narzut; sprawdzaj nierówności (`<`, `>=`),
  nie równość.

## 7. httpx — requests, który umie async

Bibliotekę `requests` znasz z tematu 11 — tu tylko jedno zdanie
przypomnienia: `requests.get(url)` zwraca odpowiedź z polami
`.status_code`, `.text` i metodą `.json()`. Problem: `requests`
NIE UMIE async — to kelner-amator z urodzenia.

**httpx** to nowoczesna biblioteka HTTP, która wygląda niemal
identycznie jak requests, ale ma tryb asynchroniczny. Instalacja:

```
pip install httpx
```

### AsyncClient — asynchroniczny klient HTTP

```python
import httpx


async def pokaz_status(url: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.status_code
```

Linijka po linijce:
- `httpx.AsyncClient()` — tworzy KLIENTA: obiekt, który umie
  wysyłać zapytania (jak słuchawka telefonu — jedną słuchawką
  wykonujesz wiele połączeń).
- `async with ... as client:` — asynchroniczny brat znanego Ci
  `with` (ten sam, którym zamykasz pliki): otwiera klienta i GWARANTUJE
  jego zamknięcie po wyjściu z bloku.
- `await client.get(url)` — wyślij zapytanie GET i CZEKAJ na
  odpowiedź nie blokując innych. Ten sam wzorzec co
  `requests.get(url)` — tylko z `await`.
- `response.status_code` — kod odpowiedzi (200 = OK, 404 = nie ma),
  `response.text` — treść jako tekst, `response.json()` — treść
  jako słownik. Identycznie jak w requests.

WAŻNE dla zadań: w tym temacie funkcje NIE tworzą klienta same —
dostają go jako ARGUMENT (`client: httpx.AsyncClient`). Dlaczego?
Po pierwsze: jeden klient obsłuży wiele zapytań (tańsze niż nowa
słuchawka do każdego telefonu). Po drugie: w testach można wtedy
podać klienta-atrapę, który nie dzwoni do prawdziwego internetu
(o tym w sekcji testowej).

### Typowe błędy początkujących
- `import httpx` bez `pip install httpx` → `ModuleNotFoundError`.
- Zgubienie `await` przed `client.get(...)` — dostajesz obiekt
  coroutine zamiast odpowiedzi i potem `AttributeError` przy
  `.status_code`.
- Zwykłe `with` zamiast `async with` przy AsyncClient → błąd —
  asynchroniczne obiekty wymagają asynchronicznego with.

## 8. Wzorzec „pobierz wiele naraz" — sedno tematu

Składamy klocki 5 i 7. Pobranie listy URL-i równolegle:

```python
import asyncio

import httpx


async def pobierz_statusy(client: httpx.AsyncClient, urle: list[str]) -> list[int]:
    zadania = [client.get(url) for url in urle]
    odpowiedzi = await asyncio.gather(*zadania)
    return [odpowiedz.status_code for odpowiedz in odpowiedzi]
```

- list comprehension buduje listę „zamówień" (coroutine) — jeszcze
  nic nie leci przez sieć,
- `gather(*zadania)` odpala wszystkie zapytania naraz,
- druga list comprehension wyciąga z odpowiedzi to, co potrzebne.

Przy 50 URL-ach po pół sekundy każdy: sekwencyjnie ~25 s,
przez gather ~0.5 s. To jest ta „skala", o którą chodzi
w scrapingu wielu stron.

## 9. Zazębienia — co już znasz

- **requests (temat 11):** wzorzec „sprawdź `status_code`, gdy 200 —
  zwróć `.json()`, w przeciwnym razie `None`" przenosisz żywcem,
  tylko biblioteka inna (httpx) i doszło `await`.
- **BeautifulSoup (temat 12):** parsowanie HTML znasz —
  `BeautifulSoup(html, "html.parser")` i `soup.find("tag")`;
  w ostatnich zadaniach użyjesz tego na stronach pobranych
  RÓWNOLEGLE (scraping w skali). Przypomnienie: `find` zwraca
  znacznik albo `None`, tekst znacznika daje `.get_text()`.

## 10. Teoria testowa

### Po co jest conftest.py i co robi sys.path.insert

Gdy pytest uruchamia `test_async_httpx.py`, ten plik robi
`from async_httpx import ...`. Python szuka modułów tylko w miejscach
z listy `sys.path` — a folderu tematu tam nie ma (pytest bywa
uruchamiany z głównego folderu repo). Dlatego w `conftest.py`
(plik wczytywany przez pytest AUTOMATYCZNIE, przed testami)
dopisujemy folder tematu na początek listy:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` — pełna ścieżka do conftest.py,
- `os.path.dirname(...)` — utnij nazwę pliku, zostaw folder,
- `sys.path.insert(0, ...)` — wstaw folder na pozycję 0 (początek),
  żeby wygrał z innymi miejscami poszukiwań.

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

W docstringu każdego testu odpowiadasz na trzy pytania:

1. **Co testuję?** — którą funkcję i które jej zachowanie.
2. **Co udaję?** — czego nie robię naprawdę (u nas: prawdziwego
   internetu!) i czym to zastępuję.
3. **Co sprawdzam?** — jaki konkretnie assert kończy test.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Cztery fazy ciała testu (faza „podmień" bywa pusta). Przykład
z INNEJ dziedziny niż ten temat — funkcja licząca rabat w sklepie:

```python
def test_rabat_dla_stalego_klienta() -> None:
    """Co testuje: czy staly klient dostaje 10% rabatu od 200 zl.
    Co udaje: nic — czysta funkcja na liczbach.
    Co sprawdzam: wynik == 180.0.
    """
    cena = 200.0                                # przygotuj
    wynik = policz_rabat(cena, staly_klient=True)   # wywołaj
    assert wynik == 180.0                       # sprawdź
```

### Jak testować coroutine — asyncio.run w teście

Funkcja testowa pytest jest ZWYKŁA (synchroniczna), a testowana
funkcja to coroutine. Rozwiązanie znasz z sekcji 3 — brama
`asyncio.run`:

```python
def test_poczekaj_i_zwroc_oddaje_wartosc() -> None:
    wynik = asyncio.run(poczekaj_i_zwroc(0.01, "gotowe"))
    assert wynik == "gotowe"
```

Test przygotowuje argumenty, oddaje coroutine dyrygentowi przez
`asyncio.run`, dostaje zwykłą wartość i robi zwykły assert.
W spaniach testowych używaj MAŁYCH czasów (0.01–0.05 s) — testy
mają być szybkie.

### httpx.MockTransport — udawany internet (faza „podmień")

Testy NIGDY nie dzwonią do prawdziwego internetu (wolne, zawodne,
wyniki się zmieniają). httpx ma wbudowaną atrapę: **MockTransport**.
Działa tak: piszesz zwykłą funkcję-recepcjonistkę, która dostaje
KAŻDE zapytanie i sama decyduje, co odpowiedzieć:

```python
import httpx


def odpowiadacz(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/dane":
        return httpx.Response(200, json={"miasto": "Krakow"})
    return httpx.Response(404, text="nie ma")


klient = httpx.AsyncClient(transport=httpx.MockTransport(odpowiadacz))
```

Linijka po linijce:
- `odpowiadacz(request)` — recepcjonistka: dostaje obiekt zapytania
  (`httpx.Request`) i MUSI zwrócić odpowiedź (`httpx.Response`).
- `request.url.path` — sama końcówka adresu, np. dla
  `https://testowy.pl/dane` to `"/dane"`. Po niej rozpoznajesz,
  o co pytano.
- `httpx.Response(200, json={...})` — budujesz odpowiedź ręcznie:
  pierwszy argument to status, `json=` ustawia treść-słownik
  (który potem `.json()` odda), `text=` ustawia treść tekstową.
- `httpx.MockTransport(odpowiadacz)` — „transport" to warstwa,
  która normalnie wysyła bajty w świat; podmieniamy ją na atrapę,
  która zamiast dzwonić — pyta recepcjonistkę.
- `httpx.AsyncClient(transport=...)` — klient z podmienionym
  transportem wygląda i działa jak prawdziwy (ma `.get`, `await`,
  `.status_code`), ale ŻADEN bajt nie opuszcza komputera.

To jest nasza faza „podmień" w najczystszej postaci: testowana
funkcja dostaje klienta-atrapę jako argument i nawet nie wie,
że internet jest udawany. Dokładnie po to funkcje w zadaniach
przyjmują `client` jako parametr.

W conftest.py zbudujesz z tego fixture (funkcja z dekoratorem
`@pytest.fixture`, której wynik pytest wstrzykuje do testu przez
parametr o tej samej nazwie — znasz to z poprzednich tematów).

### Typowe błędy początkujących
- Test dzwoniący do prawdziwego internetu — działa dziś, jutro
  serwer padnie i test zrobi się czerwony bez winy kodu.
- Zapomnienie `asyncio.run` w teście — assert porównuje obiekt
  coroutine z wartością i test wybucha.
- Recepcjonistka bez `return` dla któregoś adresu → zwraca `None`
  → httpx się wywala. Zawsze miej gałąź domyślną (końcowy `return`).
- Asserty na dokładny czas („trwało równo 0.1 s") — sprawdzaj
  nierówności, pomiar zawsze ma narzut.

## 11. Co dalej

W zadaniach przejdziesz drogę: pierwsza coroutine → await i sen →
brama asyncio.run → gather → pomiar czasu sekwencyjnie vs równolegle
(dowód na sens async!) → httpx.AsyncClient → status/tekst/JSON tym
samym wzorcem co w requests → równoległe pobieranie wielu URL-i →
na finał scraping tytułów wielu stron naraz.
