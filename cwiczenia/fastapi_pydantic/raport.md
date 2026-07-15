# Raport review — fastapi_pydantic

**Data:** 2026-07-15
**Tryb:** pełny (pierwszy review)

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Piechu\Desktop\CC_cwiczenia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\fastapi_pydantic
plugins: anyio-4.14.2
collecting ... collected 24 items

test_fastapi_pydantic.py::test_zadanie_01_zwraca_powitanie PASSED        [  4%]
test_fastapi_pydantic.py::test_zadanie_01_nieznana_sciezka_daje_404 PASSED [  8%]
test_fastapi_pydantic.py::test_zadanie_02_endpoint_glowny_dziala PASSED  [ 12%]
test_fastapi_pydantic.py::test_zadanie_02_endpoint_o_nas_dziala PASSED   [ 16%]
test_fastapi_pydantic.py::test_zadanie_03_liczba_z_adresu_jako_int PASSED [ 20%]
test_fastapi_pydantic.py::test_zadanie_03_tekst_w_adresie_daje_422 PASSED [ 25%]
test_fastapi_pydantic.py::test_zadanie_04_liczy_kwadrat PASSED           [ 29%]
test_fastapi_pydantic.py::test_zadanie_04_tekst_daje_422 PASSED          [ 33%]
test_fastapi_pydantic.py::test_zadanie_05_tworzy_produkt_z_konwersja PASSED [ 37%]
test_fastapi_pydantic.py::test_zadanie_05_zla_cena_rzuca_validation_error PASSED [ 41%]
test_fastapi_pydantic.py::test_zadanie_06_przyjmuje_poprawny_produkt PASSED [ 45%]
test_fastapi_pydantic.py::test_zadanie_06_brak_pola_daje_422 PASSED      [ 50%]
test_fastapi_pydantic.py::test_zadanie_07_liczy_wartosc_zamowienia PASSED [ 54%]
test_fastapi_pydantic.py::test_zadanie_07_zla_ilosc_daje_422 PASSED      [ 58%]
test_fastapi_pydantic.py::test_zadanie_08_tajne_pole_nie_wychodzi PASSED [ 62%]
test_fastapi_pydantic.py::test_zadanie_08_pola_modelu_zostaja PASSED     [ 66%]
test_fastapi_pydantic.py::test_zadanie_09_odsyla_przyjety_produkt PASSED [ 70%]
test_fastapi_pydantic.py::test_zadanie_09_puste_body_daje_422 PASSED     [ 75%]
test_fastapi_pydantic.py::test_zadanie_10_serwuje_zawartosc_pliku PASSED [ 79%]
test_fastapi_pydantic.py::test_zadanie_10_czyta_plik_przy_kazdym_zapytaniu PASSED [ 83%]
test_fastapi_pydantic.py::test_zadanie_11_dopisuje_do_pliku PASSED       [ 87%]
test_fastapi_pydantic.py::test_zadanie_11_zle_dane_nie_zmieniaja_pliku PASSED [ 91%]
test_fastapi_pydantic.py::test_zadanie_12_get_zwraca_liste_z_pliku PASSED [ 95%]
test_fastapi_pydantic.py::test_zadanie_12_post_potem_get_widzi_nowy_produkt PASSED [100%]

============================== warnings summary ===============================
..\..\.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\Piechu\Desktop\CC_cwiczenia\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

======================== 24 passed, 1 warning in 0.33s ========================
```

24 passed. Ostrzeżenie `StarletteDeprecationWarning` pochodzi z wnętrza
biblioteki FastAPI (nie z Twojego kodu) — nic do poprawy po Twojej stronie.

## Uwagi

Zero uwag 🔴 i 🟡 — audyt przeszedł czysto. Poniżej tylko drobiazgi 🟢.

### 🟢 Do zapamiętania na przyszłość (nie blokują)

- **`test_fastapi_pydantic.py:226` — literówka w nazwie zmiennej:**
  `respone = client.post(...)` (brak "s"). Działa, bo zmienna jest używana pod
  tą samą błędną nazwą w asercji linijkę niżej. Kosmetyka, ale nazwy zmiennych
  czyta się częściej niż pisze.

- **`test_fastapi_pydantic.py:44 i 270` — adres bez wiodącego ukośnika:**
  `client.get("nieistnieje")` i `client.get("konfiguracja")`. Testy przechodzą,
  bo TestClient dokleja adres do bazowego `http://testserver/` i wychodzi to
  samo co `/nieistnieje` i `/konfiguracja`. Ale docstringi tych testów mówią
  wprost „GET /nieistnieje" i endpoint jest zarejestrowany jako `/konfiguracja` —
  dla spójności z resztą pliku (wszędzie indziej masz `/...`) trzymaj wiodący
  ukośnik. Poleganie na relatywnym rozwijaniu URL-a to niepotrzebna niespójność.

- **PEP8 — brak spacji wokół operatorów/w literałach:**
  - `test_fastapi_pydantic.py:215` — `assert response.json() =={"nazwa": ...}`
    (brak spacji po `==`).
  - `test_fastapi_pydantic.py:178, 191` — spacja przed klamrą zamykającą:
    `"cena_jednostkowa": 10.0 }`.
  Drobiazg, ale `black`/`flake8` by to podświetliły.

## Co jest dobrze

- **Walidacja jako type hint** wykorzystana dokładnie tak, jak trzeba: `int`
  w parametrze ścieżki (zad. 03–04) i modele Pydantic w body (zad. 06–07) same
  generują 422 — zero ręcznego sprawdzania.
- **`response_model` zrozumiany** — zad. 08 zwraca słownik z `tajny_kod`,
  a filtr modelu wycina nadmiarowe pole; test sprawdza jego NIEobecność. To
  sedno tematu i jest trafione.
- **Kontrakt funkcji czysty** — `zadanie_05` sygnalizuje błąd wyjątkiem
  (`ValidationError`), nie stringiem; docstring to zapowiada, a test łapie przez
  `pytest.raises`. Zgodne ze standardem „wyjątek albo None, nigdy string-jako-błąd".
- **Praca z plikiem wzorowa** — wszędzie `with open(..., encoding="utf-8")`,
  osobny uchwyt do odczytu i zapisu (zad. 11–12), a test 11 sprawdza oba
  scenariusze: że poprawny POST dopisuje ORAZ że 422 nie rusza pliku
  (side effect zatrzymany na walidacji).
- **Testy plikowe na `tmp_path`** zamiast mockowania dysku — prawdziwy plik
  w katalogu tymczasowym, tak jak w poprzednich tematach.
- **Fixture `klient_api`** (conftest) to ładne domknięcie tematu: „specjalny
  fixture", który zamiast danych podaje gotowego klienta zbudowanego na
  `plik_produktow` — dokładnie idea z tematu 13.

## Werdykt

**ZALICZONE — gotowe do dalej.**
24/24 testy zielone, zero uwag 🔴, zero uwag 🟡.
