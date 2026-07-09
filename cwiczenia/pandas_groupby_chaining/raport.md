# Raport review — pandas_groupby_chaining

**Data:** 2026-07-09
**Tryb:** Re-review nr 2

---

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 24 items

cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_01_zlicza_grupy_po_miescie PASSED [  4%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_01_wynik_jest_series PASSED [  8%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_02_sumuje_wiek_po_miescie PASSED [ 12%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_02_wynik_jest_series PASSED [ 16%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_03_srednia_wiek_krakow PASSED [ 20%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_03_wynik_jest_series PASSED [ 25%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_04_agg_suma_zwraca_dataframe PASSED [ 29%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_04_suma_wiek_warszawa PASSED [ 33%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_05_agg_srednia_zwraca_dataframe PASSED [ 37%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_05_srednia_wynagrodzenie_krakow PASSED [ 41%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_06_agg_wiele_kolumn_zwraca_dataframe PASSED [ 45%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_06_suma_wiek_i_srednia_wynagrodzenie PASSED [ 50%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_07_assign_dodaje_kolumne_region PASSED [ 54%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_07_oryginal_bez_kolumny_region PASSED [ 58%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_08_assign_dodaje_kolumne_premia PASSED [ 62%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_08_premia_to_10_procent_wynagrodzenia PASSED [ 66%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_09_chain_zwraca_series PASSED [ 70%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_09_suma_premii_warszawa PASSED [ 75%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_10_copy_assign_dodaje_kolumne PASSED [ 79%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_10_oryginal_niezmieniony PASSED [ 83%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_11_filtruje_i_liczy_grupy PASSED [ 87%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_11_bardzo_wysoki_prog_daje_jedna_grupe PASSED [ 91%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_12_suma_wynagrodzen_po_miescie PASSED [ 95%]
cwiczenia/pandas_groupby_chaining/test_pandas_groupby_chaining.py::test_zadanie_12_prog_powyzej_max_zwraca_pusty_dataframe PASSED [100%]

============================= 24 passed in 0.17s ==============================
```

---

## Status uwag z poprzednich rund

| Runda | Plik | Uwaga | Status |
|-------|------|-------|--------|
| R1 🟡 | linia 238 — brak spacji `df_osoby,"wiek"` | ✅ NAPRAWIONE |
| R1 🟡 | linia 250 — brak spacji `df_osoby,"wiek"` | ✅ NAPRAWIONE |
| R1→R2 🔴 | linia 165 — test nie wywołuje `zadanie_07_assign_stala()` | ✅ NAPRAWIONE |
| R1→R2 🔴 | linia 227 — test nie wywołuje `zadanie_10_copy_assign()` | ✅ NAPRAWIONE |

---

## Werdykt

**ZALICZONE — gotowe do dalej**

24/24 testów zielonych, zero uwag 🔴, zero uwag 🟡.
