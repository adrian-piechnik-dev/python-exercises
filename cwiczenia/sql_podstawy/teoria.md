# SQL — rozmowa z bazą danych

## Co to jest baza danych i SQL?

Baza danych to bardzo pilny bibliotekarz: trzyma dane w **tabelach**
(jak arkusze z wierszami i kolumnami) i błyskawicznie odpowiada na pytania
w rodzaju „którzy pracownicy zarabiają powyżej 7000?" albo „ile osób pracuje
w każdym mieście?".

SQL (Structured Query Language) to język, w którym zadaje się bibliotekarzowi
pytania. Nie jest częścią Pythona — to osobny język, używany przez prawie
wszystkie bazy świata (PostgreSQL, MySQL, SQLite, ...). Wygląda jak
uproszczony angielski:

```sql
SELECT imie FROM pracownicy WHERE miasto = 'Warszawa'
```

czyli: „WYBIERZ imię Z pracowników GDZIE miasto = Warszawa".

Konwencje SQL:
- słowa kluczowe piszemy WIELKIMI literami (`SELECT`, `FROM`, `WHERE`) —
  to nie wymóg, ale żelazny zwyczaj czytelności,
- teksty w **apostrofach** `'Warszawa'` (nie cudzysłowach!),
- wielkość liter w słowach kluczowych nie ma znaczenia dla bazy,
  ale w danych (`'Warszawa'` vs `'warszawa'`) — ma.

---

## sqlite3 — długopis do ćwiczenia SQL

Ten temat uczy **czystego SQL-a**. Żeby jednak testy mogły sprawdzić twoje
zapytania, potrzebujemy silnika, który je wykona. Używamy `sqlite3` —
malutkiej bazy wbudowanej w Pythona (stdlib, zero instalacji), która potrafi
istnieć **tylko w pamięci**, bez żadnego pliku.

> sqlite3 to tutaj wyłącznie długopis — treścią jest SQL. W temacie 15
> te same zapytania przeniesiesz na „dorosłego" PostgreSQL-a (psycopg2).

```python
import sqlite3

polaczenie = sqlite3.connect(":memory:")
polaczenie.execute("CREATE TABLE ksiazki (id INTEGER, tytul TEXT)")
wynik = polaczenie.execute("SELECT * FROM ksiazki").fetchall()
polaczenie.close()
```

Linijka po linijce:
- `sqlite3.connect(":memory:")` — otwiera połączenie z bazą; magiczna
  nazwa `":memory:"` znaczy „baza w pamięci RAM, zniknie po zamknięciu"
  (idealna do ćwiczeń i testów).
- `polaczenie.execute("...SQL...")` — wysyła jedno zapytanie SQL do bazy
  i zwraca kursor (wskaźnik na wyniki).
- `.fetchall()` — zabiera **wszystkie** wiersze wyniku jako **listę krotek**;
  jeden wiersz tabeli = jedna krotka, np. `[(1, 'Anna'), (2, 'Piotr')]`.
- `.fetchone()` — zabiera **jeden** (pierwszy) wiersz jako krotkę albo
  `None`, gdy wyników brak. Do zapytań zwracających jedną wartość:
  `polaczenie.execute("SELECT COUNT(*) FROM ksiazki").fetchone()[0]`
  (`[0]` — bo nawet pojedyncza wartość siedzi w krotce).
- `polaczenie.close()` — zamyka połączenie (baza w pamięci znika).

Zapytania wygodnie pisze się w potrójnych cudzysłowach — SQL bywa
wieloliniowy:

```python
polaczenie.execute(
    """
    SELECT tytul
    FROM ksiazki
    WHERE id = 1
    """
)
```

Uwaga o utrwalaniu: dopóki pracujemy na **jednym połączeniu** w pamięci,
wszystkie zmiany widać natychmiast. Zatwierdzanie zmian (`commit`)
i połączenia z prawdziwym serwerem poznasz w temacie 15.

### Typowe błędy początkujących

- `sqlite3.connect("memory")` bez dwukropków — utworzy PLIK o nazwie
  `memory`; baza ulotna to dokładnie `":memory:"`.
- `execute()` bez `fetchall()` i zdziwienie, że „nie ma wyników" —
  execute wysyła zapytanie, fetch dopiero odbiera wiersze.
- Zapomniane `[0]` przy `fetchone()` — dostajesz krotkę `(5,)`,
  a nie liczbę `5`.

---

## CREATE TABLE — załóż tabelę

```sql
CREATE TABLE pracownicy (
    id INTEGER PRIMARY KEY,
    imie TEXT,
    miasto TEXT,
    pensja INTEGER,
    dzial_id INTEGER
)
```

- `CREATE TABLE pracownicy (...)` — „stwórz tabelę o nazwie pracownicy
  z takimi kolumnami".
- Każda kolumna: `nazwa TYP`. Typy, których używamy:
  - `INTEGER` — liczba całkowita,
  - `TEXT` — tekst,
- `PRIMARY KEY` — klucz główny: unikalny identyfikator wiersza
  (jak numer PESEL). Baza pilnuje, żeby się nie powtórzył.
- Kolumny rozdziela przecinek; po ostatniej przecinka NIE ma.

### Skąd wiadomo, że tabela powstała? sqlite_master

SQLite prowadzi „spis treści" bazy — ukrytą tabelę `sqlite_master`
z nazwami wszystkich utworzonych obiektów. Testy będą sprawdzać istnienie
tabeli właśnie tak:

```sql
SELECT name FROM sqlite_master WHERE name = 'pracownicy'
```

— zwróci wiersz, jeśli tabela istnieje, a `fetchone()` da `None`, jeśli nie.

### Typowe błędy początkujących

- Przecinek po ostatniej kolumnie przed `)` — błąd składni SQL.
- `CREATE TABLE` drugi raz na tej samej bazie — błąd „table already
  exists"; w ćwiczeniach każda baza startuje czysta, więc to nie zaboli.

---

## INSERT INTO — włóż wiersze

```sql
INSERT INTO pracownicy (id, imie, miasto, pensja, dzial_id) VALUES
    (1, 'Anna', 'Warszawa', 8000, 1),
    (2, 'Piotr', 'Krakow', 6000, 1),
    (3, 'Zofia', 'Warszawa', 9000, 2)
```

- `INSERT INTO tabela (kolumny) VALUES (wartości)` — kolejność wartości
  musi odpowiadać kolejności wymienionych kolumn.
- Kilka wierszy naraz: krotki wartości po przecinku.
- Teksty w apostrofach, liczby bez.
- `NULL` — specjalna wartość „brak danych" (odpowiednik None z Pythona);
  wpisuje się bez apostrofów: `(4, 'Marek', 'Krakow', 5500, NULL)`.

### Typowe błędy początkujących

- Cudzysłowy zamiast apostrofów wokół tekstu — część baz to przełknie,
  ale standard SQL mówi: apostrofy.
- Mniej wartości niż kolumn — błąd „table has 5 columns but 4 values
  were supplied".

---

## SELECT — zapytaj o dane

```sql
SELECT * FROM pracownicy          -- wszystkie kolumny, wszystkie wiersze
SELECT imie, pensja FROM pracownicy   -- tylko wybrane kolumny
```

- `*` — „wszystkie kolumny".
- Wynik to zawsze wiersze — w Pythonie lista krotek.

### WHERE — filtr wierszy

```sql
SELECT imie FROM pracownicy WHERE miasto = 'Warszawa'
SELECT imie FROM pracownicy WHERE pensja > 7000
```

- `WHERE warunek` — przechodzą tylko wiersze spełniające warunek.
- Porównania: `=`, `>`, `<`, `>=`, `<=`, `<>` (różne).
  Uwaga: **jedno** `=` (nie `==` jak w Pythonie!).

### Typowe błędy początkujących

- `WHERE miasto == 'Warszawa'` — podwójne `==` to Python; SQL używa
  pojedynczego `=`.
- `WHERE miasto = Warszawa` bez apostrofów — baza szuka KOLUMNY
  o nazwie Warszawa i zgłasza błąd.

---

## ORDER BY i LIMIT — posortuj i utnij

```sql
SELECT imie, pensja FROM pracownicy ORDER BY pensja DESC
SELECT imie, pensja FROM pracownicy ORDER BY pensja DESC LIMIT 2
```

- `ORDER BY kolumna` — sortuj rosnąco (domyślnie, można dopisać `ASC`).
- `DESC` — malejąco (descending).
- `LIMIT 2` — zwróć najwyżej 2 pierwsze wiersze wyniku.
- Kolejność pisania: najpierw `ORDER BY`, potem `LIMIT` — „najlepiej
  opłacana dwójka" to sortowanie malejąco + LIMIT 2.

### Typowe błędy początkujących

- `LIMIT 2 ORDER BY pensja` — zła kolejność; LIMIT zawsze na końcu.
- LIMIT bez ORDER BY — dostaniesz „jakieś" 2 wiersze; bez sortowania
  wynik nie ma gwarantowanej kolejności.

---

## Agregacje — COUNT, AVG, SUM

Agregacja zamienia wiele wierszy w jedną liczbę:

```sql
SELECT COUNT(*) FROM pracownicy               -- ile wierszy
SELECT AVG(pensja) FROM pracownicy            -- średnia
SELECT SUM(pensja) FROM pracownicy            -- suma
```

- `COUNT(*)` — liczba wierszy.
- `AVG(kolumna)` — średnia z kolumny (wychodzi liczba z ułamkiem).
- `SUM(kolumna)` — suma kolumny.
- Wynik agregacji to **jeden wiersz z jedną wartością** — w Pythonie
  odbierasz go przez `fetchone()[0]`.

To dokładnie te operacje, które w pandas robiłeś przez `.count()`,
`.mean()`, `.sum()` — SQL miał je pierwszy.

### Typowe błędy początkujących

- `COUNT(pensja)` vs `COUNT(*)` — COUNT(kolumna) pomija wiersze z NULL
  w tej kolumnie; do liczenia wierszy używaj `COUNT(*)`.

---

## GROUP BY — agregacja w grupach

„Suma pensji **per miasto**" — jak `.groupby()` z pandas (temat 9),
tylko po SQL-owemu:

```sql
SELECT miasto, SUM(pensja)
FROM pracownicy
GROUP BY miasto
ORDER BY miasto
```

Wynik: jeden wiersz na miasto — `[('Krakow', 11500), ('Warszawa', 24000)]`.

- `GROUP BY miasto` — sklej wiersze o tym samym mieście w grupy;
  agregacja (SUM/COUNT/AVG) liczy się osobno w każdej grupie.
- W `SELECT` mogą być tylko: kolumna grupująca i agregacje.
- `ORDER BY` na końcu — grupy same z siebie nie mają gwarantowanej
  kolejności.

### HAVING — filtr GRUP

`WHERE` filtruje pojedyncze wiersze **przed** grupowaniem. Do filtrowania
całych **grup po** agregacji służy `HAVING`:

```sql
SELECT miasto, COUNT(*)
FROM pracownicy
GROUP BY miasto
HAVING COUNT(*) >= 3
```

— „pokaż tylko te miasta, w których pracują co najmniej 3 osoby".

Ściąga: `WHERE` = filtr wierszy (przed GROUP BY), `HAVING` = filtr grup
(po GROUP BY, może używać agregacji).

### Typowe błędy początkujących

- `WHERE COUNT(*) >= 3` — WHERE nie zna agregacji (działa przed
  grupowaniem); warunki na agregacje tylko w HAVING.
- HAVING bez GROUP BY — bez sensu; HAVING filtruje grupy.

---

## JOIN — sklejanie dwóch tabel

Dane rozbija się na tabele, żeby się nie powtarzały: pracownik ma tylko
**numer** działu (`dzial_id`), a nazwy działów żyją w osobnej tabeli:

```sql
CREATE TABLE dzialy (
    id INTEGER PRIMARY KEY,
    nazwa TEXT
)
```

`JOIN` skleja tabele z powrotem — dopasowuje wiersze po wspólnej wartości:

### INNER JOIN — tylko pary

```sql
SELECT pracownicy.imie, dzialy.nazwa
FROM pracownicy
INNER JOIN dzialy ON pracownicy.dzial_id = dzialy.id
```

- `INNER JOIN dzialy ON warunek` — do każdego pracownika doklej wiersz
  z dzialy, w którym `dzialy.id` równa się jego `dzial_id`.
- `tabela.kolumna` — przy dwóch tabelach mówisz wprost, czyją kolumnę
  masz na myśli.
- **INNER = tylko dopasowani**: pracownik z `dzial_id = NULL` (bez działu)
  w wyniku się NIE pojawi.

### LEFT JOIN — wszystko z lewej, pary jeśli są

```sql
SELECT pracownicy.imie, dzialy.nazwa
FROM pracownicy
LEFT JOIN dzialy ON pracownicy.dzial_id = dzialy.id
```

- **LEFT = cała lewa tabela zostaje**: każdy pracownik pojawi się
  w wyniku; jeśli nie ma dopasowanego działu, w kolumnie nazwa będzie
  `NULL` (w Pythonie: `None` w krotce).

Analogia: INNER JOIN = lista par na potańcówce (kto bez pary, odpada);
LEFT JOIN = lista wszystkich gości, z pustym miejscem przy samotnych.

### Typowe błędy początkujących

- Zapomniane `ON` — baza nie wie, po czym łączyć; JOIN zawsze z ON.
- `ON pracownicy.dzial_id = pracownicy.id` — porównanie kolumn tej samej
  tabeli zamiast łączenia dwóch; sprawdź, czy po obu stronach `=` są
  różne tabele.
- INNER JOIN, gdy potrzebujesz też wierszy bez pary — „znikające wiersze"
  to sygnał, że miało być LEFT.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak w każdym temacie: pytest musi znaleźć moduł `sql_podstawy`, a folder
tematu nie jest w `sys.path`. `conftest.py` (ładowany automatycznie)
dokleja go na początek listy poszukiwań:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zapytanie/zachowanie.
2. **Co udaje?** — bazę: prawdziwej bazy na serwerze nie ma, jest
   ulotna baza w pamięci zbudowana przez fixture.
3. **Co sprawdzam?** — zawartość zwróconych krotek / liczbę wierszy /
   wartość agregacji.

### Fixture z yield — rekwizyt, który po sobie sprząta

Dotąd fixtures **zwracały** rekwizyt (`return`). Połączenie z bazą trzeba
po teście **zamknąć** — do tego służy fixture z `yield`:

```python
@pytest.fixture
def pusta_baza():
    polaczenie = sqlite3.connect(":memory:")   # przygotowanie
    yield polaczenie                           # oddaj rekwizyt testowi
    polaczenie.close()                         # sprzątanie PO teście
```

- Kod **przed** `yield` wykonuje się przed testem (przygotowanie).
- `yield polaczenie` — w tym miejscu fixture „oddaje" wartość i czeka,
  aż test się skończy.
- Kod **po** `yield` wykonuje się po teście (sprzątanie) — zawsze,
  nawet gdy test padł.

To jak wypożyczalnia nart: przygotuj sprzęt → wydaj → po zwrocie
zakonserwuj. Zwykłe `return` kończyłoby funkcję i na sprzątanie nie
byłoby już szansy.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania (biblioteka i książki):

```python
def test_wyszukanie_ksiazki_po_tytule(pusta_baza) -> None:
    """Co testuje: czy SELECT z WHERE znajduje książkę po tytule.
    Co udaje: bazę — ulotna baza w pamięci zamiast serwera.
    Co sprawdzam: fetchone zwraca krotkę z id == 2.
    """
    # przygotuj
    pusta_baza.execute("CREATE TABLE ksiazki (id INTEGER, tytul TEXT)")
    pusta_baza.execute(
        "INSERT INTO ksiazki (id, tytul) VALUES (1, 'Lalka'), (2, 'Potop')"
    )

    # wywołaj
    wynik = pusta_baza.execute(
        "SELECT id FROM ksiazki WHERE tytul = 'Potop'"
    ).fetchone()

    # sprawdź
    assert wynik == (2,)
```

Krok „podmień" załatwia sama fixture — udajemy serwer bazą w pamięci.

### Porównywanie wyników w assertach

Wyniki SQL to listy krotek — porównuj je wprost z oczekiwaną listą:

```python
assert wynik == [('Krakow', 11500), ('Warszawa', 24000)]
```

Krotka jednoelementowa ma przecinek: `(5,)`. Wartość `NULL` z bazy
przychodzi do Pythona jako `None` — sprawdzasz ją przez `is None`
(elementy krotki) albo porównując całą krotkę z `('Marek', None)`.
