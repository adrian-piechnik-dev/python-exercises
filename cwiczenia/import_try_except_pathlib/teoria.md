# Import, try/except i pathlib

---

## 1. Podział kodu na pliki — import lokalny

Gdy projekt rośnie, kod rozkładasz na wiele plików. Każdy plik `.py` to **moduł**.
Żeby użyć funkcji z innego pliku, importujesz ją:

```python
# plik: utils.py
def podwoj(x: int) -> int:
    return x * 2
```

```python
# plik: main.py
from utils import podwoj   # importuje tylko tę jedną funkcję

wynik = podwoj(5)   # → 10
```

Schemat: `from <nazwa_pliku_bez_py> import <funkcja>`

Python szuka modułu w kolejności:
1. Katalogu skryptu który uruchamiasz
2. Zmiennej środowiskowej `PYTHONPATH`
3. Standardowej bibliotece i zainstalowanych pakietach

**Typowe błędy:**
- Literówka w nazwie modułu → `ModuleNotFoundError`
- Importowanie nieistniejącej funkcji → `ImportError`
- Circular import (A importuje B, B importuje A) → `ImportError`

---

## 2. `if __name__ == "__main__"`

Każdy moduł Python ma zmienną `__name__`. Gdy uruchamiasz plik **bezpośrednio**,
`__name__` wynosi `"__main__"`. Gdy plik jest **importowany**, `__name__` wynosi
nazwę modułu (np. `"utils"`).

```python
# plik: utils.py

def podwoj(x: int) -> int:
    return x * 2

if __name__ == "__main__":
    # wykona się TYLKO przy: python utils.py
    # NIE wykona się przy: from utils import podwoj
    print(podwoj(21))   # → 42
```

To standardowy sposób na oddzielenie "biblioteki" od "kodu uruchomieniowego".
Bez tej ochrony każdy import uruchamiałby twój skrypt.

---

## 3. try/except — obsługa wyjątków

Python rzuca **wyjątek** gdy coś pójdzie nie tak. Bez obsługi program się wysypuje.
Z `try/except` możesz zareagować i kontynuować działanie:

```python
try:
    wynik = 10 / 0
except ZeroDivisionError:
    print("Nie dziel przez zero!")
```

Schemat:
```python
try:
    <kod który może rzucić wyjątek>
except NazwaWyjatku:
    <co zrobić gdy wyjątek się pojawi>
```

Popularne wyjątki wbudowane:

| Wyjątek | Kiedy się pojawia |
|---|---|
| `ZeroDivisionError` | dzielenie przez zero |
| `ValueError` | zła wartość, np. `int("abc")` |
| `IndexError` | indeks poza zakresem listy, np. `[1, 2][5]` |
| `KeyError` | brak klucza w słowniku, np. `d["brak"]` |
| `FileNotFoundError` | plik nie istnieje |
| `TypeError` | zły typ, np. `"a" + 1` |

**Typowe błędy:**
- Łapanie wszystkiego przez `except Exception` — ukrywa prawdziwe błędy
- Pusty blok `except: pass` — połknięcie błędu bez żadnej reakcji

---

## 4. Kilka klauzul except — kolejność szczegółowy → ogólny

W jednym bloku `try` możesz obsłużyć kilka różnych wyjątków:

```python
def parsuj_i_podziel(tekst: str, dzielnik: int) -> Optional[float]:
    try:
        liczba = float(tekst)
        return liczba / dzielnik
    except ValueError:
        return None
    except ZeroDivisionError:
        return None
```

**WAŻNE — kolejność klauzul ma znaczenie:**
Python sprawdza je od góry do dołu i wykonuje **pierwsze** pasujące.
Bardziej ogólne wyjątki idą na końcu:

```python
# ŹLE — Exception łapie wszystko, ValueError nigdy nie zostanie trafiony:
try:
    int("abc")
except Exception:        # ← za ogólny, za wysoko
    print("cokolwiek")
except ValueError:       # ← martwy kod, niedostępny
    print("zła wartość")

# DOBRZE — najpierw szczegółowy:
try:
    int("abc")
except ValueError:       # ← szczegółowy wyżej
    print("zła wartość")
except Exception:        # ← ogólny niżej
    print("inny błąd")
```

---

## 5. Dostęp do komunikatu — `except ... as e`

Żeby odczytać opis błędu, użyj składni `as e`:

```python
try:
    int("abc")
except ValueError as e:
    print(f"Błąd: {e}")
    # wypisze: Błąd: invalid literal for int() with base 10: 'abc'
```

`e` to obiekt wyjątku — `str(e)` daje czytelny komunikat, `type(e).__name__` to nazwa klasy.

---

## 6. pathlib — ścieżki jako obiekty

Moduł `pathlib` ze standardowej biblioteki zastępuje ręczne sklejanie stringów.
Zamiast `"/dane/" + katalog + "/" + plik` piszesz prosto i czytelnie:

```python
from pathlib import Path

p = Path("/dane/raporty/wyniki.csv")
```

---

## 7. Podstawowe atrybuty Path

```python
p = Path("/dane/raporty/wyniki.csv")

p.name            # → "wyniki.csv"         — sama nazwa pliku z rozszerzeniem
p.suffix          # → ".csv"               — rozszerzenie z kropką
p.stem            # → "wyniki"             — nazwa bez rozszerzenia
p.parent          # → Path("/dane/raporty") — katalog nadrzędny jako Path
str(p.parent)     # → "/dane/raporty"      — jako tekst
```

Zmiana rozszerzenia — metoda `.with_suffix()`:
```python
p.with_suffix(".txt")   # → Path("/dane/raporty/wyniki.txt")
str(p.with_suffix(".txt"))   # → "/dane/raporty/wyniki.txt"
```

---

## 8. Łączenie ścieżek — operator `/`

Zamiast `os.path.join(...)` używasz operatora `/` — czytelnie i bezpiecznie:

```python
katalog = Path("/dane/raporty")
plik    = "wyniki.csv"

pelna = katalog / plik          # → Path("/dane/raporty/wyniki.csv")
str(pelna)                      # → "/dane/raporty/wyniki.csv"
```

Można łączyć wiele segmentów naraz:
```python
Path("/dane") / "raporty" / "wyniki.csv"   # → Path("/dane/raporty/wyniki.csv")
```

---

## 9. Czytanie pliku i sprawdzanie istnienia

```python
p = Path("/dane/wyniki.csv")

p.exists()                             # → True / False — czy istnieje
p.read_text(encoding="utf-8")          # → str z zawartością — FileNotFoundError gdy brak
p.write_text("treść", encoding="utf-8")  # → zapisuje plik (nadpisuje)
```

Klasyczny wzorzec — czytaj plik z obsługą braku:

```python
from pathlib import Path
from typing import Optional

def czytaj_bezpiecznie(sciezka: str) -> Optional[str]:
    try:
        return Path(sciezka).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
```

---

## 10. Spirala — pojęcia ze `slowniki`

Znasz już z poprzedniego tematu (`slowniki`):
- budowanie słownika w pętli: `wynik = {}`, potem `wynik[klucz] = wartosc`
- iteracja po parach: `for k, v in slownik.items()`

W ostatnich zadaniach tego tematu połączysz `try/except` + `pathlib`
z budowaniem słownika: wczytasz plik konfiguracyjny i sparstujesz go
do `dict[str, str]`. Nie tłumaczę tych pojęć od nowa — opierasz się
na tym, co już wiesz.

---

## Podsumowanie — mapa pojęć

```python
from modul import funkcja              # import lokalny (plik: modul.py)
from pathlib import Path               # import z stdlib

if __name__ == "__main__":             # blok uruchomieniowy — chroni kod
    main()

try:
    wynik = float(tekst) / dzielnik
except ValueError:                     # szczegółowy — wyżej
    return None
except ZeroDivisionError:              # inny szczegółowy — wyżej
    return None
except Exception as e:                 # ogólny — zawsze na końcu
    print(f"Nieoczekiwany błąd: {e}")

p = Path("/dane/wyniki.csv")
p.name                                 # "wyniki.csv"
p.suffix                               # ".csv"
p.stem                                 # "wyniki"
str(p.parent)                          # "/dane"
str(p.with_suffix(".txt"))             # "/dane/wyniki.txt"
str(Path(katalog) / plik)             # łączenie ścieżek operatorem /
p.exists()                             # bool
p.read_text(encoding="utf-8")          # str — FileNotFoundError gdy brak pliku
```
