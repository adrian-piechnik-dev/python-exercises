# pandas — wstęp

## Co to jest pandas?

Wyobraź sobie arkusz kalkulacyjny (jak Excel), ale w Pythonie.
Możesz go wczytać, przefiltrować wiersze, policzyć sumy i średnie — jednym poleceniem.
**pandas** to biblioteka, która dostarcza taką "tabelę danych" wprost do kodu.

Wymagana instalacja (w terminalu, jednorazowo):

```bash
pip install pandas openpyxl
```

`openpyxl` jest potrzebne do obsługi plików `.xlsx`.

Importujesz pandas z aliasem `pd` — to ogólna konwencja, którą stosuje cała społeczność:

```python
import pandas as pd
```

---

## DataFrame — tabela danych

**DataFrame** to tabela z wierszami i kolumnami, jak arkusz w Excelu.
Każda kolumna ma nazwę (nagłówek). Każdy wiersz to jeden rekord.

Możesz stworzyć DataFrame bezpośrednio ze słownika Pythona:

```python
df = pd.DataFrame({
    "imie":   ["Anna", "Piotr", "Zofia"],
    "wiek":   [20, 30, 40],
    "miasto": ["Warszawa", "Krakow", "Warszawa"],
})
```

Klucze słownika → nazwy kolumn. Listy pod kluczami → wartości w kolumnach.
Wynik wygląda tak:

```
    imie  wiek    miasto
0   Anna    20  Warszawa
1  Piotr    30    Krakow
2  Zofia    40  Warszawa
```

Liczby po lewej (0, 1, 2) to **indeks** — automatyczny numer wiersza.

### Typowe błędy — DataFrame ze słownika

- `KeyError` przy tworzeniu — sprawdź czy klucze są stringami w cudzysłowach.
- Listy różnych długości → `ValueError`. Każda kolumna musi mieć tę samą liczbę elementów.

---

## Wczytywanie danych z pliku

### pd.read_csv — plik CSV

Znasz już format CSV z tematu 6. pandas potrafi go wczytać jednym poleceniem:

```python
df = pd.read_csv("dane.csv")
```

Pierwsza linia pliku CSV jest automatycznie traktowana jako nagłówek (nazwy kolumn).
Funkcja zwraca `pd.DataFrame`.

```python
import pandas as pd


def wczytaj_plik(sciezka: str) -> pd.DataFrame:
    """Przykładowa funkcja wczytująca CSV.

    Args:
        sciezka: ścieżka do pliku CSV.

    Returns:
        pd.DataFrame: wczytana tabela danych.
    """
    return pd.read_csv(sciezka)
```

### pd.read_excel — plik Excel

Działa analogicznie, ale dla plików `.xlsx`:

```python
df = pd.read_excel("dane.xlsx")
```

Wczytuje domyślnie pierwszy arkusz. Wymaga zainstalowanego `openpyxl`.

### Typowe błędy — wczytywanie

- `FileNotFoundError` — sprawdź ścieżkę. Najlepiej przekaż absolutną ścieżkę albo upewnij się, że skrypt uruchamiasz z odpowiedniego katalogu.
- `ModuleNotFoundError: No module named 'openpyxl'` — zainstaluj: `pip install openpyxl`.
- Plik CSV bez nagłówka — domyślnie pandas traktuje pierwszą linię jako nazwy kolumn; podaj `header=None` jeśli pliku nie ma nagłówka.

---

## df["kolumna"] — dostęp do kolumny

Podajesz nazwę kolumny w nawiasach kwadratowych — dostajesz **Series**
(jednokolumnową serię wartości):

```python
# df ma kolumny: imie, wiek, miasto
wieki = df["wiek"]       # Series: 20, 30, 40
```

Żeby dostać zwykłą listę Pythona ze wszystkimi wartościami:

```python
lista_wiekow = df["wiek"].tolist()   # [20, 30, 40]
```

Listę nazw wszystkich kolumn DataFrame sprawdzasz przez:

```python
df.columns    # Index(['imie', 'wiek', 'miasto'], dtype='object')
```

Sprawdzenie czy kolumna o danej nazwie istnieje:

```python
"wiek" in df.columns    # True
"wzrost" in df.columns  # False
```

### Typowe błędy — dostęp do kolumny

- `KeyError: 'Imie'` — nazwy kolumn są wrażliwe na wielkość liter. `"imie"` ≠ `"Imie"`.
- `df.wiek` zamiast `df["wiek"]` — działa dla prostych nazw, ale ukrywa błędy przy nazwach ze spacją lub myślnikiem. Zawsze używaj nawiasów kwadratowych.

---

## Agregacje — .sum() i .mean()

Wywołujesz na kolumnie numerycznej:

```python
df["wiek"].sum()     # 90.0  (suma: 20 + 30 + 40)
df["wiek"].mean()    # 30.0  (średnia: 90 / 3)
```

Obie metody zwracają wartość numeryczną (technicznie `numpy.float64`,
który zachowuje się dokładnie jak `float` w Pythonie).

Ile wierszy ma DataFrame — dwa równoważne sposoby:

```python
len(df)        # 3
df.shape[0]    # 3 — df.shape to krotka (liczba_wierszy, liczba_kolumn)
```

### Typowe błędy — agregacje

- `.sum()` na kolumnie tekstowej — zamiast błędu dostaniesz sklejony string (`"AnnaPiotrZofia"`). Używaj agregacji tylko na kolumnach numerycznych.
- `df.mean()` bez podania kolumny — liczy średnią dla WSZYSTKICH kolumn numerycznych naraz i zwraca Series. Zawsze podaj konkretną kolumnę: `df["wiek"].mean()`.

---

## Filtrowanie boolean

Filtrowanie w pandas składa się z dwóch kroków.

**Krok 1 — tworzysz maskę (serię True/False):**

```python
maska = df["wiek"] > 25
```

Wynik to Series z `True` lub `False` dla każdego wiersza:

```
0    False   ← Anna: 20 > 25? Nie
1     True   ← Piotr: 30 > 25? Tak
2     True   ← Zofia: 40 > 25? Tak
dtype: bool
```

**Krok 2 — przekazujesz maskę do DataFrame, żeby wybrać wiersze:**

```python
wynik = df[maska]
```

Albo krócej — bez zmiennej pośredniej:

```python
wynik = df[df["wiek"] > 25]
```

Wynik to nowy DataFrame zawierający tylko wiersze, gdzie maska była `True`.

### Dostępne operatory porównania

```python
df[df["wiek"] > 25]    # większy (ściśle)
df[df["wiek"] >= 25]   # większy lub równy
df[df["wiek"] < 25]    # mniejszy
df[df["wiek"] <= 30]   # mniejszy lub równy
df[df["wiek"] == 30]   # równy — DWA znaki równości!
```

Dla kolumny tekstowej:

```python
df[df["miasto"] == "Warszawa"]
```

### Typowe błędy — filtrowanie

- `df["wiek"] > 25` samo w sobie NIE filtruje — zwraca tylko maskę. Wynik musisz przekazać do `df[...]`.
- Jeden znak `=` zamiast `==` → `SyntaxError`. W porównaniach zawsze `==`.

---

## .copy() — kopia bez efektów ubocznych

W pandas przypisanie przez `=` NIE tworzy kopii:

```python
kopia = df           # kopia i df wskazują na TĘ SAMĄ tabelę
kopia["wiek"] = 0    # zmienia również df — efekt uboczny!
```

Żeby stworzyć niezależną kopię:

```python
kopia = df.copy()
kopia["wiek"] = 0    # df pozostaje bez zmian
```

**Efekt uboczny (ang. side effect)** — sytuacja, gdy funkcja niechcący zmienia dane
wejściowe. Dobra praktyka: funkcja przyjmuje DataFrame i zwraca NOWY DataFrame
zamiast modyfikować ten, który dostała.

Dodawanie nowej kolumny do kopii (istniejące kolumny zostają, nowa dołącza):

```python
kopia = df.copy()
kopia["nowa_kolumna"] = [1, 2, 3]
```

### Typowe błędy — copy

- `df2 = df` zamiast `df2 = df.copy()` — oba wskazują na to samo, modyfikacja jednego zmienia drugie.
- Brak `index=False` przy `to_csv`/`to_excel` — plik dostaje dodatkową kolumnę z indeksami (0, 1, 2...), której zazwyczaj nie chcemy.

---

## Zapisywanie do pliku (tylko w conftest.py — do tworzenia danych testowych)

Żeby stworzyć testowe pliki CSV i Excel w fixture, będziesz potrzebował:

```python
df.to_csv("plik.csv", index=False)      # index=False: nie zapisuje numeru wiersza
df.to_excel("plik.xlsx", index=False)   # wymaga openpyxl
```

`index=False` jest ważne — bez niego plik dostaje dodatkową kolumnę `0, 1, 2, ...`
z indeksami, której w danych nie chcemy.

---

## Teoria testowa

### conftest.py i sys.path

pytest szuka pliku `conftest.py` w folderze testu. Zawiera on **fixtures** —
gotowe dane lub zasoby, które pytest wstrzykuje do testów automatycznie
(dekorator `@pytest.fixture`).

Linia:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

mówi Pythonowi: "szukaj modułów również w tym samym folderze co conftest.py".
Bez niej `import pandas_wstep` w pliku testowym skończyłby się `ModuleNotFoundError`.

### tmp_path — tymczasowy katalog

`tmp_path` to wbudowany fixture pytest — dostajesz go za darmo, nie musisz go
definiować. Daje unikalny, czysty katalog tymczasowy dla każdego testu.
pytest automatycznie usuwa go po zakończeniu testów.

Używasz go jako ścieżki bazowej dla pliku:

```python
@pytest.fixture
def csv_przyklad(tmp_path: Path) -> Path:
    """Tymczasowy plik CSV z przykładowymi danymi.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Path: ścieżka do gotowego pliku CSV.
    """
    p = tmp_path / "dane.csv"
    pd.DataFrame({"x": [1, 2, 3]}).to_csv(str(p), index=False)
    return p
```

### Schemat 3 pytań

Przed napisaniem każdego testu odpowiedz sobie:

1. **Co testuje?** — jaki konkretny efekt sprawdzam
2. **Co udaję?** — jakie dane symuluje (a co jest prawdziwe)
3. **Co sprawdzam?** — jakie konkretne twierdzenie zawiera assert

### Schemat przygotuj → wywołaj → sprawdź

Przykład testu niezwiązanego z zadaniami (żebyś nie miał gotowca):

```python
def test_dlugosc_listy_po_dodaniu() -> None:
    """Co testuje: czy append zwiększa długość listy o 1.
    Co udaje: nic — używam listy stworzonej bezpośrednio.
    Co sprawdzam: len(lista) == 4 po dodaniu elementu.
    """
    # przygotuj
    lista = [1, 2, 3]

    # wywołaj
    lista.append(99)

    # sprawdź
    assert len(lista) == 4
```

### Co sprawdzać w testach pandas

Najczęstsze asercje:

```python
# czy wynik jest DataFrame
assert isinstance(wynik, pd.DataFrame)

# ile wierszy przeszło przez filtr
assert len(wynik) == 2

# czy kolumna istnieje
assert "miasto" in wynik.columns

# czy wartości w kolumnie są zgodne z oczekiwaniem
assert wynik["wiek"].tolist() == [30, 40]

# czy suma/średnia jest poprawna
assert wynik["wiek"].sum() == 70
assert wynik["wiek"].mean() == 30.0
```
