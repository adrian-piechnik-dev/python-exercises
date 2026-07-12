# Raport review — sql_podstawy

**Data:** 2026-07-11
**Tryb:** re-review nr 1

## Wynik pytest

```
........................                                                 [100%]
24 passed in 0.11s
```

Tym razem `24 passed` to prawdziwy zielony — oba testy, które wcześniej
przechodziły „na pusto", mają teraz realne asserty.

## Status uwag z poprzedniej rundy

### 🔴 → NAPRAWIONE — zad. 03, test_sql_podstawy.py:97
Było `wynik[0] = (...)` (przypisanie bez asserta). Jest:
```python
assert wynik[0] == (1, 'Anna', 'Warszawa', 8000, 1)
```
Test faktycznie porównuje pierwszy wiersz z pełną krotką — zgodnie z docstringiem.

### 🔴 → NAPRAWIONE — zad. 04, test_sql_podstawy.py:110
Był `assert [(...)]` (stała lista, zawsze truthy; `wynik` nieużyty). Jest:
```python
assert wynik == [('Anna',), ('Zofia',), ('Ewa',)]
```
Assert porównuje zwrócony `wynik` z oczekiwaną listą — zmienna już wykorzystana,
docstring pokryty.

### 🟢 → do zapamiętania (nie blokowało)
`conftest.py:85` — spacja na końcu wiersza SQL. Kosmetyka, pozostaje bez wpływu
na testy; do sprzątnięcia przy okazji.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony (24 passed), zero uwag 🔴,
zero uwag 🟡. Temat zamknięty.
