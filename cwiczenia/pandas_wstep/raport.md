# Raport review — pandas_wstep

**Data:** 2026-07-09
**Tryb:** RE-REVIEW nr 1

---

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\python_execise
collected 24 items

cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_01_zwraca_dataframe PASSED [  4%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_01_ma_kolumne_wiek PASSED [  8%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_02_zwraca_liste PASSED [ 12%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_02_poprawna_liczba_elementow PASSED [ 16%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_03_suma_wiekow PASSED [ 20%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_03_suma_jednej_wartosci PASSED [ 25%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_04_srednia_wiekow PASSED [ 29%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_04_srednia_jednej_wartosci PASSED [ 33%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_05_zwraca_wiersze_powyzej_progu PASSED [ 37%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_05_brak_wierszy_powyzej_progu PASSED [ 41%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_06_filtruje_po_miescie PASSED [ 45%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_06_brak_dopasowania_zwraca_pusty_df PASSED [ 50%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_07_kopia_ma_te_same_dane PASSED [ 54%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_07_modyfikacja_kopii_nie_zmienia_oryginalu PASSED [ 58%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_08_zwraca_dataframe PASSED [ 62%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_08_ma_kolumne_imie PASSED [ 66%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_09_zwraca_wiersze_mniejsze_rowne_progowi PASSED [ 70%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_09_wszystkie_wiersze_spelniaja_warunek PASSED [ 75%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_10_suma_wyfiltrowanych_wierszy PASSED [ 79%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_10_brak_wierszy_suma_wynosi_zero PASSED [ 83%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_11_kopia_ma_nowa_kolumne PASSED [ 87%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_11_oryginal_nie_ma_nowej_kolumny PASSED [ 91%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_12_zwraca_wiersze_powyzej_sredniej PASSED [ 95%]
cwiczenia/pandas_wstep/test_pandas_wstep.py::test_zadanie_12_wynik_jest_dataframe PASSED [100%]

============================= 24 passed in 0.85s ==============================
```

---

## Status uwag z poprzedniej rundy

### 🟡 Uwaga 1 — `test_pandas_wstep.py`, linia 4 — `import pytest` (nieużywany)
**Status: NAPRAWIONE** — linia `import pytest` usunięta.

---

## Werdykt

**ZALICZONE — gotowe do dalej**
