# JSON — zapis i odczyt danych

## Co to jest JSON?

JSON (JavaScript Object Notation) to format tekstowy do przechowywania danych.
Wyobraź sobie, że chcesz wysłać komuś listę zakupów SMS-em — musisz zamienić
obiekt z pamięci komputera w ciąg tekstu. JSON robi dokładnie to: zamienia
słownik Pythona na tekst, który można zapisać do pliku, wysłać przez sieć
albo wczytać w innym programie (napisanym nawet w innym języku).

Przykład: słownik `{"imie": "Anna", "wiek": 30}` po zamianie na JSON wygląda
prawie tak samo, ale jest to teraz *zwykły tekst*, a nie obiekt w pamięci.

### Dlaczego nie str()?

`str({"imie": "Anna"})` daje `"{'imie': 'Anna'}"` — Python używa apostrofów,
JSON wymaga cudzysłowów podwójnych. Inne programy (JavaScript, Java, Go) nie
rozumieją apostrofów. JSON to powszechna umowa między programami, dlatego
używamy biblioteki `json`, nie `str()`.

---

## Importowanie biblioteki json

```python
import json
```

`json` jest częścią biblioteki standardowej Pythona — nie trzeba instalować niczego przez `pip`.

---

## json.dumps() — słownik → string

`dumps` = „dump to string" (zrzuć do stringa).

```python
import json

slownik = {"imie": "Anna", "wiek": 30}
tekst = json.dumps(slownik)
print(tekst)          # '{"imie": "Anna", "wiek": 30}'
print(type(tekst))    # <class 'str'>
```

`json.dumps()` przyjmuje jeden argument (obiekt) i zwraca `str`.
Oryginał (`slownik`) pozostaje niezmieniony.

> **Ważne:** W JSON klucze to zawsze stringi (cudzysłowy).
> Wartości mogą być: stringiem, liczbą całkowitą (int), zmiennoprzecinkową (float),
> listą, słownikiem, `true`/`false` albo `null`
> (odpowiedniki Pythona: `True`/`False`, `None`).

### Parametr `indent` — czytelne formatowanie

```python
slownik = {"imie": "Anna", "wiek": 30}
tekst = json.dumps(slownik, indent=2)
print(tekst)
# {
#   "imie": "Anna",
#   "wiek": 30
# }
```

`indent=2` dodaje wcięcia o 2 spacje. Bez `indent` całość trafia w jedną linię.
Parametr przydatny do debugowania i plików, które chce czytać człowiek.

### Typowe błędy — dumps

- `json.dump(slownik)` zamiast `json.dumps(slownik)` — `dump` (bez `s`) pisze
  do pliku i wymaga drugiego argumentu; dostaniesz `TypeError`.
- Wartość nieserializowalna (np. obiekt własnej klasy, `datetime`) —
  `TypeError: Object of type … is not JSON serializable`.

---

## json.loads() — string → słownik

`loads` = „load from string" (wczytaj ze stringa).

```python
import json

tekst = '{"imie": "Anna", "wiek": 30}'
slownik = json.loads(tekst)
print(slownik["imie"])            # Anna
print(type(slownik))              # <class 'dict'>
print(type(slownik["wiek"]))      # <class 'int'>  ← liczba zostaje liczbą!
```

> **Ważne:** `json.loads()` przywraca typy — int zostaje int, float zostaje float.
> To różni JSON od CSV, gdzie wszystko jest stringiem.

### Typowe błędy — loads

- `json.loads("{'imie': 'Anna'}")` — apostrofy to nie JSON;
  dostaniesz `json.JSONDecodeError`.
- `json.loads(slownik)` — `loads` oczekuje stringa, nie słownika.

---

## json.JSONDecodeError — błąd parsowania

Gdy tekst nie jest poprawnym JSON-em, Python rzuca `json.JSONDecodeError`.
Jest podklasą `ValueError`.

```python
import json

try:
    wynik = json.loads("to nie jest json")
except json.JSONDecodeError:
    print("Błąd: niepoprawny JSON")
```

Kontrakt dobrej funkcji: złap wyjątek i zwróć `None` zamiast pozwalać
mu się propagować do kodu wywołującego.

---

## json.dump() — słownik → plik

`dump` (bez `s`) = „dump to file" (zrzuć do pliku).

```python
import json

slownik = {"imie": "Anna", "wiek": 30}
with open("dane.json", "w", encoding="utf-8") as f:
    json.dump(slownik, f, indent=2)
```

- Pierwszy argument: obiekt do zapisania.
- Drugi argument: uchwyt pliku (`f` — nie string ze ścieżką!).
- `encoding="utf-8"` — zawsze, żeby polskie znaki zapisały się poprawnie.
- `with` — zawsze zamykaj plik przez `with`.

### Typowe błędy — dump

- `json.dump(slownik, "dane.json")` — string zamiast uchwytu pliku;
  `AttributeError: 'str' object has no attribute 'write'`.
- Pominięcie `encoding="utf-8"` — na Windowsie inne kodowanie, psuje
  polskie znaki.

---

## json.load() — plik → słownik

`load` (bez `s`) = „load from file" (wczytaj z pliku).

```python
import json

with open("dane.json", "r", encoding="utf-8") as f:
    slownik = json.load(f)

print(slownik["imie"])   # Anna
```

- Plik musi istnieć — inaczej `FileNotFoundError`.
- Zawartość musi być poprawnym JSON-em — inaczej `json.JSONDecodeError`.

### Typowe błędy — load

- `json.load("dane.json")` — string zamiast uchwytu; `AttributeError`.
- Próba odczytu pliku `.csv` przez `json.load()` — CSV to nie JSON;
  dostaniesz `JSONDecodeError`.

---

## Zagnieżdżone struktury — lista słowników

Znasz słowniki z tematu 3. W JSON możesz je zagnieżdżać w listach —
format obsługuje to naturalnie:

```python
import json

lista = [
    {"imie": "Anna", "wiek": 30},
    {"imie": "Piotr", "wiek": 25},
]

tekst = json.dumps(lista, indent=2)
odczytana = json.loads(tekst)
print(type(odczytana))          # <class 'list'>
print(odczytana[0]["imie"])     # Anna
print(odczytana[0]["wiek"])     # 30  (int, nie string!)
```

`json.dumps()` i `json.loads()` działają tak samo dla list jak dla słowników.
`json.dump()` i `json.load()` też — po prostu zamiast słownika przekazujesz listę.

---

## Wzorzec bezpiecznego wczytania pliku JSON

```python
import json
from typing import Optional

def wczytaj_ustawienia(sciezka: str) -> Optional[dict]:
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
```

Kolejność `except`: najpierw szczegółowy wyjątek, potem bardziej ogólny.
Oba bloki zwracają `None` — kontrakt funkcji.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Kiedy pytest uruchamia `test_json_load_dump.py`, Python szuka modułu
`json_load_dump`. Folder `cwiczenia/json_load_dump/` nie jest automatycznie
w `sys.path` (liście miejsc, gdzie Python szuka plików `.py`).

`conftest.py` ładuje się automatycznie przed testami. Wstawiamy w nim:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` → pełna ścieżka do `conftest.py`
- `os.path.dirname(...)` → folder zawierający ten plik
- `sys.path.insert(0, ...)` → wstaw na początek listy — Python znajdzie
  `json_load_dump.py` przed czymkolwiek innym

### Trzy pytania przed każdym testem

Zanim napiszesz test, odpowiedz na 3 pytania:

1. **Co testuje?** — konkretny scenariusz lub zachowanie
2. **Co udaje?** — czy potrzebuję pliku tymczasowego lub innego zasobu?
   Opisz, czy i jakiego fixture używasz.
3. **Co sprawdzam?** — jaki wynik lub efekt weryfikuje `assert`?

### Schemat: przygotuj → wywołaj → sprawdź

```python
def test_wczytanie_ocen_ucznia(tmp_path: Path) -> None:
    """Co testuje: czy json.load poprawnie odczytuje oceny z pliku.
    Co udaje: nic — tworzę plik tymczasowy przez tmp_path.
    Co sprawdzam: wynik["matematyka"] == 5 po wczytaniu.
    """
    # przygotuj
    p = tmp_path / "oceny.json"
    p.write_text('{"matematyka": 5, "polski": 4}', encoding="utf-8")

    # wywołaj
    with open(str(p), "r", encoding="utf-8") as f:
        wynik = json.load(f)

    # sprawdź
    assert wynik["matematyka"] == 5
```

Przykład testuje coś *innego* niż zadania — chodzi o wzorzec, nie gotowca.

### Fixture tmp_path

`tmp_path` to wbudowany fixture pytest. Dostarcza obiekt `Path` wskazujący
na czysty folder tymczasowy — odrębny dla każdego testu, usuwany po sesji.

```python
def test_przyklad(tmp_path: Path) -> None:
    p = tmp_path / "dane.json"
    p.write_text('{"klucz": "wartość"}', encoding="utf-8")
    # p teraz istnieje — można ją przekazać do testowanej funkcji
```

Własne fixtures (jak `plik_json_slownik`, `plik_json_lista`) zdefiniowane
w `conftest.py` działają identycznie — pytest wstrzykuje je w parametrze
funkcji testowej po nazwie.
