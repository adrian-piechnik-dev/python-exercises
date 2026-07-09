# BeautifulSoup — wyciąganie danych ze stron WWW

## Co to jest scraping?

Wyobraź sobie gazetę: ktoś czyta ją i wypisuje do zeszytu same ceny
z ogłoszeń, pomijając resztę. Scraping to dokładnie to, tylko robione
przez program: pobierasz stronę WWW i **wyciągasz z niej wybrane dane**
(ceny, tytuły, linki), ignorując ozdoby.

Strona WWW to tekst w języku HTML. Z tematu 11 umiesz już taki tekst
pobrać (`requests.get`). Ten temat uczy, jak z pobranego HTML-a wyłuskać
to, czego szukasz.

---

## HTML w 5 minut — tyle, ile trzeba

HTML składa się ze **znaczników** (tagów) w ostrych nawiasach. Znacznik
otwiera się `<p>` i zamyka `</p>`, a między nimi siedzi treść:

```html
<h1>Sklep Python</h1>
<p>Witamy w sklepie!</p>
<a href="/kontakt">Kontakt</a>
```

- `<h1>` — nagłówek strony (najważniejszy tytuł).
- `<p>` — akapit tekstu.
- `<a href="...">` — link; `href` to **atrybut** (dodatkowa informacja
  w znaczniku otwierającym) — mówi, dokąd link prowadzi.
- `<div>` — pudełko grupujące fragment strony.
- `<img src="...">` — obrazek; atrybut `src` wskazuje plik graficzny.
- `<table>`, `<tr>`, `<td>` — tabela, wiersz tabeli, komórka.

Znaczniki bywają zagnieżdżone jak pudełka w pudełkach:

```html
<div class="produkt">
  <h2>Klawiatura</h2>
  <p>99 zł</p>
</div>
```

Dwa atrybuty specjalne, których strony używają do oznaczania elementów:
- `class="produkt"` — etykieta **grupy** elementów (wiele elementów może
  mieć tę samą klasę),
- `id="stopka"` — etykieta **jednego, konkretnego** elementu (id nie
  powinno się powtarzać).

---

## BeautifulSoup — parser HTML

`BeautifulSoup` zamienia surowy tekst HTML na obiekt, po którym można
wygodnie szukać — jak spis treści zamiast sterty kartek.

Instalacja (biblioteka zewnętrzna):

```
pip install beautifulsoup4
```

```python
from bs4 import BeautifulSoup

html = "<html><body><h1>Sklep Python</h1></body></html>"
soup = BeautifulSoup(html, "html.parser")
```

- `from bs4 import ...` — uwaga: instalujesz `beautifulsoup4`,
  ale importujesz z `bs4`. Tak po prostu jest.
- Pierwszy argument — tekst HTML (string).
- `"html.parser"` — nazwa parsera wbudowanego w Pythona; podajesz ją
  zawsze, żeby BeautifulSoup nie zgadywał.

### Typowe błędy początkujących

- `import beautifulsoup4` — nie ma takiego modułu; import to `bs4`.
- Pominięcie `"html.parser"` — działa, ale wypisuje ostrzeżenie
  i może wybrać inny parser na innym komputerze.

---

## find — znajdź pierwszy znacznik

```python
naglowek = soup.find("h1")
print(naglowek)        # <h1>Sklep Python</h1>  ← cały znacznik
print(naglowek.text)   # Sklep Python           ← sama treść
```

- `soup.find("h1")` — zwraca **pierwszy** znacznik `<h1>` na stronie
  (obiekt, nie string).
- `.text` — wyciąga samą treść, bez ostrych nawiasów.

Gdy znacznika nie ma, `find` zwraca `None` — znajomy kontrakt:

```python
brak = soup.find("h5")
print(brak)   # None
```

### .text vs .get_text()

To niemal to samo: `.text` to skrót, `.get_text()` to metoda.
`.get_text()` przydaje się, gdy chcesz posprzątać białe znaki:

```python
naglowek.get_text(strip=True)   # treść z uciętymi spacjami po bokach
```

W tym kursie: `.text` do prostego wyciągania, `.get_text(strip=True)`
gdy treść może mieć zbędne spacje/entery wokół siebie.

### Typowe błędy początkujących

- `soup.find("h1").text` gdy `<h1>` nie istnieje —
  `AttributeError: 'NoneType' object has no attribute 'text'`.
  Najpierw sprawdź `is None`, potem sięgaj po `.text`.
- `find("<h1>")` — nazwa znacznika bez ostrych nawiasów: `find("h1")`.

---

## find_all — znajdź wszystkie znaczniki

```python
linki = soup.find_all("a")
print(len(linki))   # ile linków na stronie

for link in linki:
    print(link.text)
```

- `find_all("a")` — zwraca **listę** wszystkich znaczników `<a>`;
  pustą listę, gdy nic nie znaleziono (nie None!).
- Po liście chodzi się pętlą albo list comprehension (temat 2):

```python
teksty = [link.text for link in soup.find_all("a")]
```

### Szukanie po klasie — class_

```python
produkty = soup.find_all("div", class_="produkt")
```

- `class_="produkt"` — **z podkreśleniem na końcu!** Samo `class` to
  słowo zastrzeżone Pythona (do tworzenia klas), więc BeautifulSoup
  dodał podkreślenie.

### Szukanie po id

```python
stopka = soup.find(id="stopka")
```

- `find(id="stopka")` — zwraca element o tym id lub `None`.
  Id jest unikalne, więc używa się `find`, nie `find_all`.

### Typowe błędy początkujących

- `find_all("div", class="produkt")` — `SyntaxError`; musi być `class_`.
- Sprawdzanie `if wynik is None` po `find_all` — find_all zwraca pustą
  **listę**, nie None; sprawdzaj `len(wynik) == 0` albo `wynik == []`.

---

## Atrybuty — .get("href")

Treść to nie wszystko — często potrzebujesz atrybutu (adres z linku,
plik z obrazka):

```python
link = soup.find("a")
print(link.get("href"))   # /kontakt
```

- `.get("href")` — działa jak `.get()` na słowniku (temat 3): zwraca
  wartość atrybutu albo `None`, gdy atrybutu nie ma. Znacznik można
  zresztą traktować jak słownik atrybutów.

```python
adresy = [img.get("src") for img in soup.find_all("img")]
```

### Typowe błędy początkujących

- `link["href"]` gdy atrybutu brak — `KeyError`; `.get("href")` daje
  bezpiecznie None.
- `link.get(href)` — nazwa atrybutu to string: `link.get("href")`.

---

## Selektory CSS — select i select_one

Drugi sposób szukania, zwięźlejszy przy zagnieżdżeniach. Selektor CSS
to mini-język adresowania elementów (ten sam, którego strony używają
do stylowania):

- `"a"` — wszystkie znaczniki `<a>`,
- `".produkt"` — wszystko z `class="produkt"` (kropka = klasa),
- `"#stopka"` — element z `id="stopka"` (płotek = id),
- `"div.produkt"` — znaczniki `<div>` z klasą `produkt`,
- `"table td"` — wszystkie `<td>` **wewnątrz** `<table>` (spacja =
  „gdzieś w środku").

```python
produkty = soup.select("div.produkt")     # lista (jak find_all)
stopka = soup.select_one("#stopka")       # pierwszy lub None (jak find)
```

- `select(selektor)` — lista wszystkich pasujących (pusta gdy brak).
- `select_one(selektor)` — pierwszy pasujący lub `None`.

### Typowe błędy początkujących

- `select(".produkt")` vs `select("produkt")` — bez kropki szukasz
  znacznika `<produkt>`, który nie istnieje; klasa wymaga kropki.
- Mylenie zwrotów: `select` zawsze lista, `select_one` element/None.

---

## Tabele — wiersze i komórki

Tabela HTML to `<table>` z wierszami `<tr>`, a w każdym wierszu komórki `<td>`:

```html
<table>
  <tr><td>Anna</td><td>30</td></tr>
  <tr><td>Piotr</td><td>25</td></tr>
</table>
```

Wzorzec „tabela → lista list": znajdź wiersze, w każdym wierszu znajdź
komórki, z komórek weź tekst:

```python
wiersze = []
for tr in soup.find_all("tr"):
    komorki = [td.text for td in tr.find_all("td")]
    wiersze.append(komorki)
# [["Anna", "30"], ["Piotr", "25"]]
```

---

## Etyka scrapingu: robots.txt i User-Agent

Scraping to odwiedzanie cudzego serwera — obowiązują zasady dobrego gościa.

**robots.txt** — plik pod adresem `https://strona.pl/robots.txt`, w którym
właściciel strony pisze, czego robotom nie wolno odwiedzać:

```
User-agent: *
Disallow: /admin/
```

Znaczy: „wszystkie roboty (`*`): nie wchodźcie do `/admin/`".
Zanim scrapujesz stronę, zajrzyj do jej robots.txt i uszanuj zakazy.
To nie jest mechanizm techniczny (nic cię nie zatrzyma) — to umowa,
której łamanie może naruszać regulamin strony.

**User-Agent** — nagłówek HTTP (znasz `headers` z tematu 11), w którym
przedstawiasz się serwerowi. Uczciwy scraper mówi kim jest:

```python
naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
response = requests.get(url, headers=naglowki, timeout=10)
```

Bez User-Agenta część serwerów odrzuca zapytania, a podszywanie się
pod przeglądarkę bywa wprost zakazane w regulaminach.

**Rate limiting — time.sleep** — nie zasypuj serwera setką zapytań
na sekundę. Między kolejnymi zapytaniami rób pauzę:

```python
import time

for url in adresy:
    response = requests.get(url, headers=naglowki, timeout=10)
    # ...przetwórz odpowiedź...
    time.sleep(1.0)   # odczekaj sekundę przed następnym zapytaniem
```

- `time` — moduł wbudowany (stdlib, import bez pip).
- `time.sleep(1.0)` — zatrzymuje program na podaną liczbę sekund (float).

### Typowe błędy początkujących

- Pętla po 100 adresach bez `sleep` — serwer może zablokować twoje IP.
- `time.sleep(1000)` w przekonaniu, że to milisekundy — to sekundy;
  1000 = kwadrans z hakiem.

---

## Zazębienie: requests i CSV

Źródłem HTML-a jest `requests.get` z tematu 11 (z `timeout=10`
i `raise_for_status()` — pamiętasz wzorzec). Wyniki scrapingu zapisuje się
do CSV przez `csv.DictWriter` z tematu 6 (z `newline=""`
i `encoding="utf-8"`). Nowość: z odpowiedzi bierzesz **`response.text`**
(surowy HTML jako string), a nie `response.json()` — strony WWW to HTML,
nie JSON.

```python
response = requests.get(url, headers=naglowki, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
```

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak w poprzednich tematach: pytest musi znaleźć moduł
`scraping_beautifulsoup`, a folder tematu nie jest w `sys.path`.
`conftest.py` (ładowany automatycznie) dokleja go na początek listy:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie funkcji.
2. **Co udaje?** — zadania 1-9 parsują HTML podany jako string, więc
   nic nie udajemy; zadania 10-12 chodzą „do internetu", więc udajemy
   `requests.get` (i `time.sleep`).
3. **Co sprawdzam?** — co dokładnie weryfikuje `assert`.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

`monkeypatch` znasz z tematu 11 — fixture pytest, który podmienia
atrybut na czas jednego testu i sam cofa podmianę. Przykład na temacie
INNYM niż scraping — funkcja rzucająca monetą:

```python
# moneta.py
import random


def rzut_moneta() -> str:
    return random.choice(["orzel", "reszka"])
```

```python
def test_rzut_moneta_zwraca_wylosowana_strone(monkeypatch) -> None:
    """Co testuje: czy rzut_moneta zwraca to, co wskazał random.choice.
    Co udaje: random.choice — zawsze zwraca "orzel".
    Co sprawdzam: wynik == "orzel".
    """
    # przygotuj
    def podmieniony_choice(opcje):
        return "orzel"

    # podmień (tam, gdzie używane: moduł moneta)
    monkeypatch.setattr("moneta.random.choice", podmieniony_choice)

    # wywołaj
    wynik = rzut_moneta()

    # sprawdź
    assert wynik == "orzel"
```

W tym temacie podmieniasz analogicznie:
`"scraping_beautifulsoup.requests.get"` oraz
`"scraping_beautifulsoup.time.sleep"`.

### FakeResponse dla HTML

W temacie 11 atrapa miała metodę `json()`. Strony WWW zwracają HTML,
więc tutejsza atrapa (w `conftest.py`) ma zamiast tego **atrybut
`text`** — string z HTML-em:

```python
class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"kod {self.status_code}")
```

Test podmienia `requests.get` na funkcję zwracającą
`FakeResponse(200, "<html>...</html>")` — funkcja z zadania parsuje ten
HTML, jakby przyszedł z sieci.

### Podmiana time.sleep — test nie może czekać naprawdę

Test zadania z pauzami nie będzie spał po sekundzie na wywołanie —
podmieniamy `time.sleep` na funkcję, która tylko **zapisuje, że została
wywołana**:

```python
uspienia = []

def podmieniony_sleep(sekundy):
    uspienia.append(sekundy)

monkeypatch.setattr("scraping_beautifulsoup.time.sleep", podmieniony_sleep)
```

Po wywołaniu testowanej funkcji lista `uspienia` mówi, ile razy
(i z jaką pauzą) funkcja chciała spać — to właśnie sprawdza assert.
Ten sam chwyt „zamiennik zapisuje wywołania do listy" znasz z tematu 11
(test przekazywania params).

### Fixtures tego tematu

W `conftest.py` przygotujesz dwa fixtures ze stałym HTML-em
(`html_strona`, `html_tabela`) i klasę `FakeResponse`. Fixtures
HTML-owe zwracają zwykłe stringi — testy zadań 1-9 podają je funkcjom
bezpośrednio, bez żadnej sieci i bez plików.
