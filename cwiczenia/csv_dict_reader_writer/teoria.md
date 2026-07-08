# CSV w Pythonie: csv.DictReader, csv.DictWriter, fieldnames

---

## 1. Co to jest CSV?

Wyobraź sobie tabelę z Excela: pierwsza linia to nagłówki kolumn, każda kolejna
to jeden wiersz danych. CSV (Comma-Separated Values) to dokładnie to samo,
zapisane jako zwykły plik tekstowy:

```
imie,wiek,miasto
Anna,30,Warszawa
Piotr,25,Kraków
Zofia,35,Gdańsk
```

Pierwsza linia — `imie,wiek,miasto` — to **nagłówek**: nazwy kolumn.
Każda następna linia to jeden **wiersz danych**, wartości oddzielone przecinkami.

CSV jest wszędzie: eksport z Excela, dane z baz, raporty z systemów.
Dlatego Python ma wbudowany moduł `csv` — nie trzeba go instalować.

---

## 2. Dlaczego moduł `csv`, a nie zwykłe `open()`?

Mógłbyś próbować czytać CSV jak zwykły plik i dzielić po przecinku:

```python
# ŹLE — nie rób tego
with open("dane.csv", "r", encoding="utf-8") as f:
    for linia in f:
        czesci = linia.split(",")   # niebezpieczne!
```

Problem: wartości mogą zawierać przecinki wewnątrz cudzysłowów:
```
imie,opis
Anna,"Mieszka w Warszawie, stolicy Polski"
```

`split(",")` rozbiłoby to źle. Moduł `csv` obsługuje cudzysłowy, nowe linie
wewnątrz pól i inne edge-case'y poprawnie.

```python
import csv   # zawsze na początku pliku
```

---

## 3. `newline=""` przy `open()` — OBOWIĄZKOWO dla CSV

Przy pracy z modułem `csv` musisz otworzyć plik z `newline=""`:

```python
with open("dane.csv", "r", newline="", encoding="utf-8") as f:
    ...
```

**Dlaczego?** Python domyślnie przetłumaczyłby `\r\n` (Windows) na `\n`
zanim `csv` je zobaczy. `newline=""` wyłącza to tłumaczenie — moduł `csv`
sam obrabia znaki nowej linii. Bez tego na Windowsie możesz dostać puste
wiersze między danymi.

**Zasada:** `newline=""` zawsze przy `open()` razem z modułem `csv`.

---

## 4. `csv.DictReader` — czytanie wierszy jako słowniki

`csv.DictReader` czyta plik CSV i zamienia każdy wiersz danych na **słownik**,
gdzie klucze to nazwy kolumn z nagłówka:

```python
import csv

with open("dane.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for wiersz in reader:
        print(wiersz)

# wypisze (kolejno):
# {'imie': 'Anna', 'wiek': '30', 'miasto': 'Warszawa'}
# {'imie': 'Piotr', 'wiek': '25', 'miasto': 'Kraków'}
# {'imie': 'Zofia', 'wiek': '35', 'miasto': 'Gdańsk'}
```

Schemat: `reader = csv.DictReader(f)` — pierwszy argument to otwarty plik.

Nagłówek jest **wczytany automatycznie** — nie pojawia się wśród wierszy.

Żeby dostać listę wszystkich wierszy od razu (zamiast iterować):
```python
with open("dane.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    wiersze = list(reader)   # ← list() zbiera wszystkie słowniki naraz
```

**Typowe błędy początkujących:**
- Brak `newline=""` → puste wiersze na Windowsie
- Próba użycia `reader` po wyjściu z bloku `with` → plik już zamknięty
- Zapomnienie `list(reader)` i próba dwukrotnej iteracji → drugi raz pusta

---

## 5. `reader.fieldnames` — nazwy kolumn

Po utworzeniu `DictReader`, atrybut `reader.fieldnames` zawiera listę
nazw kolumn (pobrana z nagłówka):

```python
with open("dane.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)   # → ['imie', 'wiek', 'miasto']
```

Uwaga: `reader.fieldnames` jest dostępny dopiero po pierwszym dostępie
do `reader` (np. po `list(reader)` lub po pierwszej iteracji), a nie
natychmiast po `DictReader(f)`.

Bezpieczna metoda — wczytaj wiersz i wtedy pobierz nagłówki:

```python
with open("dane.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    wiersze = list(reader)         # wczytuje dane I ładuje fieldnames
    kolumny = reader.fieldnames    # teraz bezpieczne
```

**Typowe błędy początkujących:**
- `reader.fieldnames` przed iteracją zwraca `None` (plik nieodczytany)

---

## 6. CSV zawsze zwraca stringi — konwersja typów

Każda wartość z `DictReader` jest **stringiem**, nawet liczby:

```python
wiersz = {'imie': 'Anna', 'wiek': '30', 'miasto': 'Warszawa'}
wiersz['wiek']         # → '30'   (str, nie int!)
int(wiersz['wiek'])    # → 30     (int po konwersji)
```

Dlatego żeby dodawać wartości liczbowe, musisz je najpierw przekonwertować:

```python
suma = 0
for wiersz in wiersze:
    suma += int(wiersz['wiek'])   # str → int przed dodawaniem
```

**Typowe błędy początkujących:**
- `suma = suma + wiersz['wiek']` — TypeError lub konkatenacja stringów
- Zapomnienie `int()` i dziwienie się, że `'30' + '25'` = `'3025'`

---

## 7. `csv.DictWriter` — zapisywanie słowników do CSV

`csv.DictWriter` zamienia słowniki z powrotem na wiersze CSV:

```python
import csv

wiersze = [
    {'imie': 'Anna', 'wiek': '30', 'miasto': 'Warszawa'},
    {'imie': 'Piotr', 'wiek': '25', 'miasto': 'Kraków'},
]
kolumny = ['imie', 'wiek', 'miasto']

with open("wynik.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=kolumny)
    writer.writeheader()    # zapisz nagłówek (imie,wiek,miasto)
    writer.writerows(wiersze)  # zapisz wszystkie wiersze naraz
```

Schemat krok po kroku:
1. `open(...)` z `"w"`, `newline=""`, `encoding="utf-8"`
2. `csv.DictWriter(f, fieldnames=lista_kolumn)` — powiedz jakie kolumny
3. `writer.writeheader()` — zapisz nagłówek (ZAWSZE jako pierwszy)
4. `writer.writerow(jeden_slownik)` LUB `writer.writerows(lista_slownikow)`

**Różnica między `writerow` a `writerows`:**
```python
writer.writerow({'imie': 'Anna', 'wiek': '30', 'miasto': 'Warszawa'})
# zapisuje jeden wiersz

writer.writerows([wiersz1, wiersz2, wiersz3])
# zapisuje wiele wierszy naraz — wygodniejsze przy liście
```

**Typowe błędy początkujących:**
- Brak `writeheader()` → plik bez nagłówka, DictReader nie będzie wiedział co to za kolumny
- Brak `newline=""` → podwójne puste linie między wierszami na Windowsie
- Zła kolejność: `writerows` przed `writeheader` → dane przed nagłówkiem

---

## 8. Tryb `"a"` — dopisywanie wierszy do CSV

Tak jak przy zwykłych plikach (tematy poprzednie), tryb `"a"` dopisuje
bez kasowania istniejącej zawartości:

```python
nowy_wiersz = {'imie': 'Marek', 'wiek': '28', 'miasto': 'Poznań'}
kolumny = ['imie', 'wiek', 'miasto']

with open("dane.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=kolumny)
    writer.writerow(nowy_wiersz)   # BEZ writeheader — nagłówek już jest!
```

Przy dopisywaniu **nie wywołuj `writeheader()`** — nagłówek zostałby
wstawiony w środku danych.

**Typowe błędy początkujących:**
- `writeheader()` w trybie `"a"` → duplikat nagłówka w środku pliku

---

## 9. Spirala — pojęcia z poprzednich tematów

Znasz już z poprzednich tematów (`slowniki`, `pliki_tekstowe`) —
nie tłumaczę od nowa:

**Ze `slowniki` (temat 3):**
- Dostęp przez klucz: `wiersz['imie']`
- Iteracja `.items()`: `for k, v in wiersz.items()`
- Budowanie słownika w pętli: `licznik[wartosc] += 1`

**Z `pliki_tekstowe` (temat 5):**
- `try/except FileNotFoundError` do obsługi brakującego pliku
- `with open(...)` do bezpiecznego zamykania

Przykład łączący oba:
```python
import csv

def wczytaj_bezpiecznie(sciezka: str) -> list[dict[str, str]] | None:
    try:
        with open(sciezka, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return None
```

---

## 10. Teoria testowa

### Dlaczego `conftest.py` i `sys.path.insert`?

Znasz to z poprzedniego tematu — przypomnij: pytest zbiera testy z różnych
folderów i bez `sys.path.insert` nie znajdzie lokalnego modułu
`csv_dict_reader_writer.py`. `conftest.py` jest wczytywany automatycznie
przed testami i ustawia ścieżkę.

### Schemat 3 pytań do każdego testu

Każda funkcja testowa odpowiada na 3 pytania:
- **Co testuje?** — konkretne zachowanie funkcji (nie "testuje zadanie 01")
- **Co udaje?** — czy mockuję coś, czy używam prawdziwych danych
- **Co sprawdzam?** — dokładna wartość lub właściwość w `assert`

### Schemat: przygotuj → wywołaj → sprawdź

```python
def test_suma_dlugosci_slow() -> None:
    """Co testuje: czy funkcja sumuje długości słów z listy.
    Co udaje: nic — używam prawdziwej listy.
    Co sprawdzam: wynik == 9 dla ["ala", "pies", "kot"].
    """
    # przygotuj
    slowa = ["ala", "pies", "kot"]     # 3 + 4 + 3 = 10... sprawdź sam :)
    # wywołaj
    wynik = suma_dlugosci(slowa)
    # sprawdź
    assert wynik == 10
```

Powyższy przykład jest z tematu list — nie przepisuj go, to tylko wzorzec.

### `tmp_path` — tymczasowy katalog pytest

Znasz z `pliki_tekstowe` — `tmp_path` to fixture wstrzykiwany przez pytest,
dający katalog tymczasowy (inny dla każdego testu, automatycznie usuwany).
Dla CSV tworzysz tam pliki testowe:

```python
def test_cos(tmp_path: Path) -> None:
    p = tmp_path / "test.csv"
    p.write_text("imie,wiek\nAnna,30\n", encoding="utf-8")
    # teraz p to gotowy plik CSV do przekazania testowanej funkcji
```

### Fixture w `conftest.py` — wspólne dane testowe

Kiedy wiele testów potrzebuje tego samego pliku CSV, wydzielasz go
do fixture w `conftest.py`, żeby nie duplikować kodu:

```python
@pytest.fixture
def plik_csv(tmp_path: Path) -> Path:
    p = tmp_path / "dane.csv"
    p.write_text("imie,wiek,miasto\nAnna,30,Warszawa\n", encoding="utf-8")
    return p
```

Fixture wstrzykujesz przez parametr — pytest sam go wywoła:
```python
def test_wczytaj(plik_csv: Path) -> None:
    wynik = moja_funkcja(str(plik_csv))
    assert ...
```

---

## Podsumowanie — mapa pojęć

```python
import csv

# Czytanie
with open(sciezka, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    wiersze = list(reader)          # lista słowników
    kolumny = reader.fieldnames     # lista nazw kolumn

# Każdy wiersz to słownik
wiersz["imie"]                      # → "Anna"  (zawsze str)
int(wiersz["wiek"])                 # → 30      (konwersja na int)

# Pisanie (nowy plik)
with open(sciezka, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["imie", "wiek"])
    writer.writeheader()            # nagłówek jako pierwszy
    writer.writerow(jeden_slownik)  # jeden wiersz
    writer.writerows(lista)         # wiele wierszy naraz

# Dopisywanie (bez kasowania)
with open(sciezka, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["imie", "wiek"])
    writer.writerow(nowy_wiersz)    # BEZ writeheader!

# Obsługa brakującego pliku (spirala z pliki_tekstowe)
try:
    with open(sciezka, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
except FileNotFoundError:
    return None
```
