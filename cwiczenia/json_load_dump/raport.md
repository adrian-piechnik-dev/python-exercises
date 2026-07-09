# Raport review — json_load_dump

**Data:** 2026-07-09
**Tryb:** RE-REVIEW nr 1

---

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\python_execise
collected 24 items

cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_01_zwraca_string PASSED [  4%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_01_liczba_zachowana_jako_int PASSED [  8%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_02_zwraca_slownik PASSED [ 12%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_02_liczba_jako_int PASSED [ 16%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_03_plik_zawiera_poprawny_json PASSED [ 20%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_03_nadpisuje_istniejacy_plik PASSED [ 25%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_04_zwraca_slownik PASSED [ 29%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_04_liczba_wczytana_jako_int PASSED [ 33%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_05_zwraca_string_z_wcieciami PASSED [ 37%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_05_wynik_parsuje_sie_do_oryginalu PASSED [ 41%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_06_zwraca_string PASSED [ 45%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_06_pierwszy_element_zachowany PASSED [ 50%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_07_zwraca_liste_trzech_elementow PASSED [ 54%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_07_pierwszy_element_to_anna PASSED [ 58%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_08_poprawny_json_zwraca_slownik PASSED [ 62%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_08_niepoprawny_json_zwraca_none PASSED [ 66%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_09_istniejacy_plik_zwraca_liste PASSED [ 70%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_09_brak_pliku_zwraca_none PASSED [ 75%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_10_plik_zawiera_liste PASSED [ 79%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_10_pusta_lista_tworzy_plik PASSED [ 83%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_11_lista_rosnie_o_jeden PASSED [ 87%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_11_nowy_wpis_na_koncu PASSED [ 91%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_12_zlicza_po_miescie PASSED [ 95%]
cwiczenia/json_load_dump/test_json_load_dump.py::test_zadanie_12_pusta_lista_zwraca_pusty_slownik PASSED [100%]

============================= 24 passed in 0.19s ==============================
```

---

## Status uwag z poprzedniej rundy

### 🟡 Uwaga 1 — zadanie 01–07, 09 | `test_json_load_dump.py` — `isinstance(...) is True`
**Status: NAPRAWIONE** — `is True` usunięte we wszystkich 7 miejscach.

### 🟡 Uwaga 2 — zadanie 11 | `json_load_dump.py` — zagnieżdżone `with`
**Status: NAPRAWIONE** — dwa oddzielne bloki `with` (odczyt, potem zapis).

### 🟡 Uwaga 3 — `conftest.py` — kolejność importów
**Status: NAPRAWIONE** — `import pytest` oddzielony pustą linią od stdlib.

---

## Drobne (do zapamiętania na przyszłość)

- **`test_json_load_dump.py` linie 59, 107:** docstringi testów zadanie_02 i zadanie_04 wciąż opisują `isinstance(...) is True` w sekcji "Co sprawdzam:" mimo że kod już tego nie ma. Semantycznie zgodne, ale warto synchronizować opis z kodem.

---

## Werdykt

**ZALICZONE — gotowe do dalej**
