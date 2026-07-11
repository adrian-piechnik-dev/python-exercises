# Raport review — scraping_beautifulsoup

**Data:** 2026-07-11
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 24 items

... (24 testów)
test_scraping_beautifulsoup.py::test_zadanie_12_zapisuje_linki_do_csv PASSED [ 95%]
test_scraping_beautifulsoup.py::test_zadanie_12_strona_bez_linkow_zwraca_zero PASSED [100%]

============================= 24 passed in 0.46s ==============================
```

## Status uwag z poprzedniej rundy

### 🟡 → NAPRAWIONE — test_scraping_beautifulsoup.py:5, martwy import
`from numpy.ma.core import append` usunięty. Linia 5 to teraz `import pytest`,
kolejność importów czysta: `csv`, `pathlib` (stdlib) → `pytest` (third-party)
→ `conftest`, `scraping_beautifulsoup` (local).

### 🟢 → NAPRAWIONE — scraping_beautifulsoup.py zad. 03 i 09, precyzja adnotacji
`zadanie_03_adresy_linkow` i `zadanie_09_adresy_obrazkow` mają teraz zwrot
`list[Optional[str]]` — adnotacja odpowiada faktycznemu kontraktowi
(`.get()` może zwrócić `None`). Uwaga była niewymagana (🟢), ale poprawiona.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony (24 passed), zero uwag 🔴,
zero uwag 🟡. Temat zamknięty.
