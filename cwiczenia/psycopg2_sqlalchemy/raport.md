# Raport review — psycopg2_sqlalchemy

**Data:** 2026-07-14
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Piechu\Desktop\CC_cwiczenia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\psycopg2_sqlalchemy
plugins: anyio-4.14.2
collecting ... collected 24 items

test_psycopg2_sqlalchemy.py::test_zadanie_01_przekazuje_dane_logowania PASSED [  4%]
test_psycopg2_sqlalchemy.py::test_zadanie_01_zwraca_polaczenie PASSED    [  8%]
test_psycopg2_sqlalchemy.py::test_zadanie_02_wysyla_create_table PASSED  [ 12%]
test_psycopg2_sqlalchemy.py::test_zadanie_02_zatwierdza_zmiany PASSED    [ 16%]
test_psycopg2_sqlalchemy.py::test_zadanie_03_uzywa_zaslepek_i_parametrow PASSED [ 20%]
test_psycopg2_sqlalchemy.py::test_zadanie_03_zatwierdza_zmiany PASSED    [ 25%]
test_psycopg2_sqlalchemy.py::test_zadanie_04_uzywa_executemany PASSED    [ 29%]
test_psycopg2_sqlalchemy.py::test_zadanie_04_zatwierdza_raz PASSED       [ 33%]
test_psycopg2_sqlalchemy.py::test_zadanie_05_zwraca_wiersze_z_kursora PASSED [ 37%]
test_psycopg2_sqlalchemy.py::test_zadanie_05_wysyla_select PASSED        [ 41%]
test_psycopg2_sqlalchemy.py::test_zadanie_06_zwraca_znaleziony_wiersz PASSED [ 45%]
test_psycopg2_sqlalchemy.py::test_zadanie_06_brak_produktu_zwraca_none PASSED [ 50%]
test_psycopg2_sqlalchemy.py::test_zadanie_07_sukces_zwraca_polaczenie PASSED [ 54%]
test_psycopg2_sqlalchemy.py::test_zadanie_07_blad_bazy_zwraca_none PASSED [ 58%]
test_psycopg2_sqlalchemy.py::test_zadanie_08_zwraca_liczbe PASSED        [ 62%]
test_psycopg2_sqlalchemy.py::test_zadanie_08_wysyla_count PASSED         [ 66%]
test_psycopg2_sqlalchemy.py::test_zadanie_09_zwraca_engine PASSED        [ 70%]
test_psycopg2_sqlalchemy.py::test_zadanie_09_silnik_dziala_z_pandas PASSED [ 75%]
test_psycopg2_sqlalchemy.py::test_zadanie_10_tabela_powstaje_w_bazie PASSED [ 79%]
test_psycopg2_sqlalchemy.py::test_zadanie_10_nadpisuje_istniejaca_tabele PASSED [ 83%]
test_psycopg2_sqlalchemy.py::test_zadanie_11_zwraca_dataframe PASSED     [ 87%]
test_psycopg2_sqlalchemy.py::test_zadanie_11_dziala_z_where PASSED       [ 91%]
test_psycopg2_sqlalchemy.py::test_zadanie_12_raport_w_bazie PASSED       [ 95%]
test_psycopg2_sqlalchemy.py::test_zadanie_12_zwraca_liczbe_wierszy_raportu PASSED [100%]

============================= 24 passed in 1.63s ==============================
```

24 passed — poprawki niczego nie zepsuły.

## Status uwag z rundy 1

### 🔴 → ✅ NAPRAWIONE — Zadanie 03 ignorowało własne argumenty (`psycopg2_sqlalchemy.py`)

```python
kursor.execute(
    "INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)",
    (nazwa, cena)
)
```

Krotka bierze się teraz z argumentów funkcji, nie z hardkodu. Linia złamana,
mieści się w limicie. To był jedyny realny błąd w temacie.

### 🟡 → ✅ NAPRAWIONE — martwy TODO w `conftest.py`

`# TODO: return self.kursor` usunięty. W całym folderze nie ma już ani jednego
TODO (sprawdzone grepem).

### 🟡 → ✅ NAPRAWIONE — `tmp_path` bez type hintu (`test_psycopg2_sqlalchemy.py`)

`def test_zadanie_09_zwraca_engine(tmp_path: Path) -> None:` — hint dodany
w obu testach zadania 09, `from pathlib import Path` wylądował w grupie stdlib
na samej górze, przed third-party. Kolejność importów zgodna ze standardem.

### 🟡 → ✅ NAPRAWIONE — rozpakowana i nieużyta zmienna `parametry`

W testach 02, 05 i 08 jest teraz `(sql, _) = polaczenie.kursor.wykonane[0]`.
W testach 03 i 06, gdzie `parametry` faktycznie służy do asercji, nazwa została —
dokładnie tak, jak powinno być.

### 🟢 → ✅ Naprawione przy okazji (choć nie blokowały)

- Literówki `polacznie` — poprawione we wszystkich czterech miejscach.
- `liczba_comitow` → `liczba_commitow` w `conftest.py`; kod i docstringi testów
  mówią teraz tą samą nazwą.
- Brak spacji po przecinku w wywołaniu `zadanie_04_wstaw_wiele` — poprawione.
- Wcięcia w `pd.DataFrame` w testach 10 i 11 — wyprostowane.

## Do zapamiętania na przyszłość (🟢 — nie blokuje zaliczenia)

- **Test 03 nadal używa tych samych danych, które wcześniej były zahardkodowane**
  (`"Klawiatura", 99.0`). Teraz test ma sens, bo funkcja faktycznie przekazuje
  argumenty — ale gdyby ktoś kiedyś wrócił do hardkodu akurat tymi wartościami,
  test dalej byłby zielony. Zasada na przyszłość: **dane w teście dobieraj tak,
  żeby wynik nie mógł wyjść przypadkiem** — inne niż jakakolwiek wartość
  domyślna czy przykładowa z kodu.
- Drobiazgi kosmetyczne, które zostały po szkielecie: puste nawiasy sygnatur
  łamane na dwie linie (`def test_zadanie_02_wysyla_create_table(\n) -> None:`)
  i pozostałe wcięcia w słownikach `pd.DataFrame` w testach 12. Nie ruszaj
  wstecz — po prostu nie powielaj w nowych plikach.

## Werdykt

**ZALICZONE — gotowe do dalej.**
24/24 testy zielone, zero uwag 🔴, zero uwag 🟡.
