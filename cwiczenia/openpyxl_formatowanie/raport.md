# Raport review — openpyxl_formatowanie

**Data:** 2026-07-10
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\python_execise\cwiczenia\openpyxl_formatowanie
collecting ... collected 24 items

test_openpyxl_formatowanie.py::test_zadanie_01_tworzy_plik_na_dysku PASSED [  4%]
test_openpyxl_formatowanie.py::test_zadanie_01_zapisuje_wartosc_i_zwraca_true PASSED [  8%]
test_openpyxl_formatowanie.py::test_zadanie_02_odczytuje_naglowek PASSED   [ 12%]
test_openpyxl_formatowanie.py::test_zadanie_02_odczytuje_liczbe PASSED     [ 16%]
test_openpyxl_formatowanie.py::test_zadanie_03_naglowki_pogrubione PASSED  [ 20%]
test_openpyxl_formatowanie.py::test_zadanie_03_zwraca_true PASSED          [ 25%]
test_openpyxl_formatowanie.py::test_zadanie_04_kolor_czcionki_ustawiony PASSED [ 29%]
test_openpyxl_formatowanie.py::test_zadanie_04_zwraca_true PASSED          [ 33%]
test_openpyxl_formatowanie.py::test_zadanie_05_tlo_wypelnione_kolorem PASSED [ 37%]
test_openpyxl_formatowanie.py::test_zadanie_05_zwraca_true PASSED          [ 41%]
test_openpyxl_formatowanie.py::test_zadanie_06_naglowki_wysrodkowane PASSED [ 45%]
test_openpyxl_formatowanie.py::test_zadanie_06_zwraca_true PASSED          [ 50%]
test_openpyxl_formatowanie.py::test_zadanie_07_obramowanie_ze_wszystkich_stron PASSED [ 54%]
test_openpyxl_formatowanie.py::test_zadanie_07_zwraca_true PASSED          [ 58%]
test_openpyxl_formatowanie.py::test_zadanie_08_freeze_ustawiony_na_a2 PASSED [ 62%]
test_openpyxl_formatowanie.py::test_zadanie_08_zwraca_true PASSED          [ 66%]
test_openpyxl_formatowanie.py::test_zadanie_09_szerokosc_kolumny_ustawiona PASSED [ 70%]
test_openpyxl_formatowanie.py::test_zadanie_09_zwraca_true PASSED          [ 75%]
test_openpyxl_formatowanie.py::test_zadanie_10_sumuje_kolumne_b PASSED     [ 79%]
test_openpyxl_formatowanie.py::test_zadanie_10_same_naglowki_daja_zero PASSED [ 83%]
test_openpyxl_formatowanie.py::test_zadanie_11_plik_ma_naglowki_bez_indeksu PASSED [ 87%]
test_openpyxl_formatowanie.py::test_zadanie_11_dwie_kolumny_i_true PASSED  [ 91%]
test_openpyxl_formatowanie.py::test_zadanie_12_raport_ma_zsumowane_wartosci PASSED [ 95%]
test_openpyxl_formatowanie.py::test_zadanie_12_naglowek_pogrubiony_i_zamrozony PASSED [100%]

============================= 24 passed in 0.93s ==============================
```

Wszystkie 24 testy zielone — poprawki niczego nie zepsuły.

---

## Status uwag z poprzedniej rundy

**🟡 nr 1 — Zadanie 01, `test_openpyxl_formatowanie.py:34-44`** — **NAPRAWIONE**
Test asertuje teraz `wynik is True`, a następnie otwiera plik i sprawdza
`ws["A1"].value == "Raport"`. Asserty pokrywają dokładnie to, co deklaruje
docstring i obiecuje nazwa testu.

**🟡 nr 2 — Zadanie 06, `test_openpyxl_formatowanie.py:138-150`** — **NAPRAWIONE**
Dołożone dwa asserty na `ws["B1"]` (horizontal i vertical). Test sprawdza teraz
obie komórki nagłówka, zgodnie z docstringiem — usunięcie linijki dla B1
z funkcji produkcyjnej zapali ten test na czerwono.

Nowych problemów w poprawionych fragmentach nie ma.

---

## Uwagi w tej rundzie

### 🔴 Krytyczne
Brak.

### 🟡 Do poprawy
Brak.

### 🟢 Drobne (do zapamiętania na przyszłość — nie blokują zaliczenia)

Poniższe uwagi przenoszone z rundy 1. Nie blokują zaliczenia tematu, ale warto
mieć je z tyłu głowy przy kolejnych ćwiczeniach.

**3. `openpyxl_formatowanie.py:177-192` — kontrakt `zadanie_10_zsumuj_kolumne_b`**
Sygnatura obiecuje `-> int`, a `suma += wiersz[1]` przyjmie cokolwiek jest
w kolumnie B. Dla liczb zmiennoprzecinkowych zwrócisz `float`, a dla pustej
komórki (`None`) dostaniesz `TypeError`. Docstring mówi „Sumuje wartości
**liczbowe**", więc kod powinien to filtrowanie realizować, np. przez
`if isinstance(wiersz[1], (int, float))`. Testy tego nie łapią, bo fixture ma
tylko czyste `int`.

**4. `openpyxl_formatowanie.py:209-211` — docstring wieloliniowy w pierwszej linii**
Linia podsumowania docstringa powinna być jednym zdaniem w jednej linii,
a szczegóły po pustej linii. Teraz zdanie łamie się zaraz po `"""`.

**5. `test_openpyxl_formatowanie.py:60` i `:264` — brak spacji po przecinku**
`zadanie_02_wczytaj_komorke(str(plik_xlsx),"B2")` oraz
`zadanie_11_zapisz_dataframe(str(p),df_sprzedaz)`. PEP 8 wymaga spacji
po przecinku w liście argumentów.

**6. `conftest.py:1-2` — kolejność importów stdlib**
`import sys` przed `import os`. Grupa jest poprawna (stdlib pierwsza), ale
wewnątrz grupy przyjęta konwencja to porządek alfabetyczny: `os`, potem `sys`.

---

## Werdykt

**ZALICZONE — gotowe do dalej**

pytest zielony (24 passed), zero uwag 🔴, zero uwag 🟡. Obie uwagi blokujące
z rundy 1 naprawione dokładnie zgodnie z zaleceniem — testy sprawdzają teraz to,
co deklarują ich docstringi.

Temat zamknięty: 12 zadań pokrywających `Workbook`/`load_workbook`, `Font`,
`PatternFill`, `Alignment`, `Border`/`Side`, `freeze_panes`, `iter_rows`,
`column_dimensions` oraz integrację pandas → Excel z `index=False`.
