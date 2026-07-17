# Raport — selenium_podstawy

**Data:** 2026-07-17
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Piechu\Desktop\CC_cwiczenia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\selenium_podstawy
plugins: anyio-4.14.2
collecting ... collected 24 items

test_selenium_podstawy.py::test_zadanie_01_headless_dodaje_argumenty PASSED [  4%]
test_selenium_podstawy.py::test_zadanie_01_bez_headless_tylko_rozmiar PASSED [  8%]
test_selenium_podstawy.py::test_zadanie_02_przekazuje_sciezke_do_service PASSED [ 12%]
test_selenium_podstawy.py::test_zadanie_02_zwraca_drivera PASSED         [ 16%]
test_selenium_podstawy.py::test_zadanie_03_odwiedza_adres_i_zwraca_tytul PASSED [ 20%]
test_selenium_podstawy.py::test_zadanie_03_get_przed_odczytem_tytulu PASSED [ 25%]
test_selenium_podstawy.py::test_zadanie_04_zwraca_tekst_elementu PASSED  [ 29%]
test_selenium_podstawy.py::test_zadanie_04_brak_elementu_rzuca_wyjatek PASSED [ 33%]
test_selenium_podstawy.py::test_zadanie_05_zbiera_teksty_z_listy PASSED  [ 37%]
test_selenium_podstawy.py::test_zadanie_05_brak_elementow_pusta_lista PASSED [ 41%]
test_selenium_podstawy.py::test_zadanie_06_wpisuje_tekst_w_pole PASSED   [ 45%]
test_selenium_podstawy.py::test_zadanie_06_nie_klika_pola PASSED         [ 50%]
test_selenium_podstawy.py::test_zadanie_07_klika_element PASSED          [ 54%]
test_selenium_podstawy.py::test_zadanie_07_klika_dokladnie_raz PASSED    [ 58%]
test_selenium_podstawy.py::test_zadanie_08_wypelnia_oba_pola PASSED      [ 62%]
test_selenium_podstawy.py::test_zadanie_08_klika_przycisk_logowania PASSED [ 66%]
test_selenium_podstawy.py::test_zadanie_09_zwraca_obecny_element PASSED  [ 70%]
test_selenium_podstawy.py::test_zadanie_09_brak_elementu_konczy_sie_timeoutem PASSED [ 75%]
test_selenium_podstawy.py::test_zadanie_10_zwraca_tekst_gdy_element_jest PASSED [ 79%]
test_selenium_podstawy.py::test_zadanie_10_timeout_zwraca_none PASSED    [ 83%]
test_selenium_podstawy.py::test_zadanie_11_loguje_adres_strony PASSED    [ 87%]
test_selenium_podstawy.py::test_zadanie_11_zwraca_tytul_i_loguje_go PASSED [ 91%]
test_selenium_podstawy.py::test_zadanie_12_zamyka_przegladarke_po_sukcesie PASSED [ 95%]
test_selenium_podstawy.py::test_zadanie_12_zamyka_przegladarke_mimo_bledu PASSED [100%]

============================= 24 passed in 2.48s ==============================
```

---

## Status uwag z rundy 1

### 🔴 → ✅ NAPRAWIONE — Zadanie 03, `test_selenium_podstawy.py:96`

Dopisany brakujący assert:

```python
    assert driver.odwiedzone == ["https://sklep.pl"]
    assert wynik == "Sklep Python"
```

`wynik` nie jest już martwą zmienną, a test faktycznie broni tego, co ma
w nazwie — gdyby `zadanie_03_otworz_strone` przestało zwracać tytuł,
test teraz zaświeci na czerwono. Docstring i asserty zgadzają się co do joty.

### 🟡 → ✅ NAPRAWIONE — Zadanie 12, `test_selenium_podstawy.py:328` i `:349`

W obu testach atrapa ma teraz `def podmieniony_service(sciezka=None):`.
Nazwa parametru mówi prawdę o tym, co przez niego przechodzi (ścieżka do
chromedrivera), i nie przysłania już importowanej klasy `Service`.
Spójne z atrapą z zadania 02.

Nowych problemów w poprawionych fragmentach brak.

---

## Do zapamiętania na przyszłość (🟢 — nie blokowały zaliczenia)

- **`selenium_podstawy.py:191-194`** — `driver.title` czytany dwa razy
  (raz do loga, raz do `return`). Na prawdziwym driverze każdy odczyt `.title`
  to osobne zapytanie do przeglądarki. Czytelniej: `tytul = driver.title`,
  potem log i `return tytul`.
- **`conftest.py:84-85`** — `self.listy_elementow = (listy_elementow) if ... else {}`:
  nawiasy wokół samej nazwy nic nie robią i mylą przy czytaniu. Łamanie linii
  robi się po `=` albo wokół całego wyrażenia warunkowego.
- **`conftest.py`** — między metodami w klasie zostały dwie puste linie.
  Zasada „dwie puste linie" dotyczy funkcji na poziomie modułu; metody
  wewnątrz klasy oddziela jedna pusta linia (PEP 8).
- **Drobiazgi formatowania w testach:** `zadanie_03_otworz_strone(driver,"https://przyklad.pl" )`
  (linia 105 — brak spacji po przecinku, zbędna przed nawiasem), `elementy= {`
  (linia 116 — spacja po złej stronie `=`), `assert  wynik` (linia 313 — podwójna spacja).

---

## Werdykt

**ZALICZONE — gotowe do dalej**

24/24 testy zielone, zero uwag 🔴 i 🟡. Temat zamknięty.

Mocne strony tego tematu: kontrakty funkcji trzymają jeden typ zwracany albo
`None` (zad. 10 łapie `TimeoutException` i zwraca `None`, zamiast string-jako-błąd),
`try/finally` w zad. 12 realnie gwarantuje `quit()` — i masz na to test z awarią
`get`, a `FakeDriver.find_element` rzuca prawdziwym `NoSuchElementException`,
dzięki czemu `WebDriverWait` w zad. 09 działa na atrapie bez uruchamiania Chrome.
Cały zestaw 24 testów chodzi w 2,5 s bez ani jednej prawdziwej przeglądarki.
