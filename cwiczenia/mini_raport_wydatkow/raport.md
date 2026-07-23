# Raport review — mini_raport_wydatkow

**Data:** 2026-07-23
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\mini_raport_wydatkow
plugins: anyio-4.14.2
collected 26 items

test_mini_raport_wydatkow.py ... (26 testów) ...                       [100%]

============================= 26 passed in 0.64s ==============================
```

Wszystkie 26 testów zielone.

## Status uwag z poprzedniej rundy

**1. 🔴 Zadanie 09 — `test_mini_raport_wydatkow.py:216` — brakujący assert**
→ **NAPRAWIONE**

```python
wynik = zadanie_09_eksportuj_raport(df_raport, str(sciezka))
assert wynik is True
assert Path(sciezka).exists()
```

Kontrakt `return True` zadania 09 jest teraz faktycznie sprawdzany, a test
dostarcza dokładnie to, co obiecuje jego nazwa i docstring.

**2. 🟡 Zadanie 12 — `mini_raport_wydatkow.py:208` — truthiness zamiast `is not None`**
→ **NAPRAWIONE**

```python
if komorka.value is not None and komorka.value > prog:
```

Pusta komórka jest teraz odróżniona od komórki z wartością `0`.

Poprawione zostały także drobiazgi 🟢 z poprzedniej rundy: `list(reader)`
zamiast comprehension (zadanie 01), podwójna spacja po `=` w zadaniu 13,
brak spacji w `{"kwota": []}` oraz zbyt długa linia z `PatternFill`
w zadaniu 10 (zawinięta).

## Uwagi bieżącej rundy

Brak nowych uwag 🔴/🟡.

### 🟢 Do zapamiętania na przyszłość (nie blokują)

- `test_mini_raport_wydatkow.py:226` — `Path(sciezka).exists()`, choć
  `sciezka` jest już obiektem `Path` (`tmp_path / "plik.xlsx"`) — owijanie
  jest zbędne, wystarczy `sciezka.exists()`.
- `test_mini_raport_wydatkow.py:354` — `assert not sciezka_xlsx.exists()`;
  w pozostałych tematach kursu stosujesz `.exists() is False` — kwestia
  spójności stylu, nie poprawności.
- `conftest.py` — usunięty nagłówek „UWAGA (reguły mini-projektu M1)".
- Zadanie 02 nadal podmienia kwotę wprost w słownikach wejściowych, więc
  modyfikuje dane dzwoniącego. **To nie jest uwaga do Ciebie** — TODO
  szkieletu kazało „podmienić kwotę na float". Wersja bez efektów
  ubocznych kopiowałaby wiersz: `{**wiersz, "kwota": kwota}`. Warto mieć
  to z tyłu głowy, bo zadania 04, 07 i 08 mają osobne testy pilnujące
  właśnie braku takich efektów.

## Werdykt

**ZALICZONE — gotowe do dalej.** pytest zielony, zero uwag 🔴/🟡.
Mini-projekt M1 domknięty: pełna ścieżka CSV → walidacja → pandas →
agregacja → Excel → formatowanie działa i jest pokryta testami.
