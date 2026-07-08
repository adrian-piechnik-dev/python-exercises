# Raport review — csv_dict_reader_writer

**Data:** 2026-07-08
**Tryb:** Re-review nr 1

---

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 24 items

cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_01_zwraca_liste_slownikow PASSED [  4%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_01_pusty_csv_zwraca_pusta_liste PASSED [  8%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_02_zwraca_nazwy_kolumn PASSED [ 12%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_02_zwraca_liste PASSED [ 16%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_03_trzy_wiersze PASSED [ 20%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_03_pusty_csv_zero PASSED [ 25%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_04_kolumna_imie PASSED [ 29%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_04_pusta_lista_dla_pustego_csv PASSED [ 33%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_05_zapisuje_wiersze PASSED [ 37%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_05_pusty_plik_z_naglowkiem PASSED [ 41%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_06_dopisuje_wiersz PASSED [ 45%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_06_nie_duplikuje_naglowka PASSED [ 50%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_07_filtruje_po_miescie PASSED [ 54%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_07_brak_dopasowania_pusta_lista PASSED [ 58%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_08_zwraca_pierwszy_pasujacy PASSED [ 62%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_08_brak_wiersza_zwraca_none PASSED [ 66%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_09_suma_wieku PASSED [ 70%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_09_pusty_csv_zwraca_zero PASSED [ 75%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_10_istniejacy_plik PASSED [ 79%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_10_brak_pliku_zwraca_none PASSED [ 83%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_11_filtruje_i_zapisuje PASSED [ 87%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_11_zero_gdy_brak_dopasowania PASSED [ 91%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_12_zlicza_po_miescie PASSED [ 95%]
cwiczenia/csv_dict_reader_writer/test_csv_dict_reader_writer.py::test_zadanie_12_pusty_csv_zwraca_pusty_slownik PASSED [100%]

============================= 24 passed in 0.27s ==============================
```

---

## Status uwag z poprzedniej rundy

| # | Plik | Uwaga | Status |
|---|------|-------|--------|
| 🔴 | `csv_dict_reader_writer.py` linia 4 | Martwy import `from pygments.lexers.csound import newline` | ✅ NAPRAWIONE |
| 🟡 | `csv_dict_reader_writer.py` linie 101-103 | 3 puste linie miedzy z06 a z07 | ✅ NAPRAWIONE |
| 🟡 | `csv_dict_reader_writer.py` linie 143-145 | 3 puste linie miedzy z08 a z09 | ✅ NAPRAWIONE |
| 🟡 | `conftest.py` linie 24-27 | 4 puste linie miedzy fixtures | ✅ NAPRAWIONE |

---

## Werdykt

**ZALICZONE — gotowe do dalej**

24/24 testow zielonych, zero uwag 🔴, zero uwag 🟡.
