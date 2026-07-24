# Raport review — playwright_pytest_network

**Data:** 2026-07-24
**Tryb:** re-review nr 1

---

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Piechu\Desktop\CC_cwiczenia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\playwright_pytest_network
plugins: anyio-4.14.2, base-url-2.1.0, playwright-0.8.0
collecting ... collected 24 items

test_playwright_pytest_network.py::test_zadanie_01_czyta_naglowek[chromium] PASSED [  4%]
test_playwright_pytest_network.py::test_zadanie_01_pusty_naglowek[chromium] PASSED [  8%]
test_playwright_pytest_network.py::test_zadanie_02_goto_dostaje_podstawiona_strone[chromium] PASSED [ 12%]
test_playwright_pytest_network.py::test_zadanie_02_naglowek_z_podstawionej_strony_widoczny[chromium] PASSED [ 16%]
test_playwright_pytest_network.py::test_zadanie_03_goto_pokazuje_podstawiony_json[chromium] PASSED [ 20%]
test_playwright_pytest_network.py::test_zadanie_03_zwraca_none[chromium] PASSED [ 25%]
test_playwright_pytest_network.py::test_zadanie_04_strona_dziala_mimo_zablokowanych_obrazkow[chromium] PASSED [ 29%]
test_playwright_pytest_network.py::test_zadanie_04_goto_na_png_rzuca_error[chromium] PASSED [ 33%]
test_playwright_pytest_network.py::test_zadanie_10_tworzy_plik_z_nagraniem[chromium] PASSED [ 37%]
test_playwright_pytest_network.py::test_zadanie_10_nagranie_nie_jest_puste[chromium] PASSED [ 41%]
test_playwright_pytest_network.py::test_zadanie_12_sklep_offline_rysuje_produkty[chromium] PASSED [ 45%]
test_playwright_pytest_network.py::test_zadanie_12_pusta_lista_produktow_daje_pusta_liste[chromium] PASSED [ 50%]
test_playwright_pytest_network.py::test_zadanie_05_status_200_dla_produktow PASSED [ 54%]
test_playwright_pytest_network.py::test_zadanie_05_status_404_dla_nieznanej_sciezki PASSED [ 58%]
test_playwright_pytest_network.py::test_zadanie_06_zwraca_slownik_produktu PASSED [ 62%]
test_playwright_pytest_network.py::test_zadanie_06_zwraca_none_dla_404 PASSED [ 66%]
test_playwright_pytest_network.py::test_zadanie_07_post_zwraca_201 PASSED [ 70%]
test_playwright_pytest_network.py::test_zadanie_07_post_w_zle_miejsce_zwraca_404 PASSED [ 75%]
test_playwright_pytest_network.py::test_zadanie_08_sklada_komende_codegen PASSED [ 79%]
test_playwright_pytest_network.py::test_zadanie_08_komenda_zaczyna_sie_od_playwright PASSED [ 83%]
test_playwright_pytest_network.py::test_zadanie_09_sklada_komende_show_trace PASSED [ 87%]
test_playwright_pytest_network.py::test_zadanie_09_sciezka_pliku_trafia_na_koniec PASSED [ 91%]
test_playwright_pytest_network.py::test_zadanie_11_tlumaczy_stare_podmiany PASSED [ 95%]
test_playwright_pytest_network.py::test_zadanie_11_none_dla_nieznanego_narzedzia PASSED [100%]

============================= 24 passed in 4.52s ==============================
```

---

## Status uwag z rundy 1

| # | Uwaga | Plik / linia | Status |
|---|-------|--------------|--------|
| 1 🔴 | `goto` na `/galeria` zamiast `/logo.png` — test nie sprawdzał `route.abort()` | `test_...py:124` | ✅ NAPRAWIONE |
| 2 🟡 | `Args: None.` zamiast `Args: Brak.` | `conftest.py:57, 80` | ✅ NAPRAWIONE |
| 3 🟡 | docstring `log_message` kłamał o argumentach | `conftest.py:103–105` | ✅ NAPRAWIONE |
| 4 🟡 | `serwer_api()` bez type hintu | `conftest.py:114` | ✅ NAPRAWIONE |
| 5 🟡 | jedna pusta linia przed `class Sprzedawca` | `conftest.py:40–41` | ✅ NAPRAWIONE |
| 6 🟢 | podwójna spacja przed `==` | `test_...py:68` | ✅ NAPRAWIONE |
| 7 🟢 | brak spacji po przecinku | `test_...py:80, 92` | ✅ NAPRAWIONE |
| 8 🟢 | brak pustej linii po docstringu klasy | `conftest.py:53` | ✅ NAPRAWIONE |
| 9 🟢 | opis docstringa w nowej linii po `"""` | `conftest.py` | ✅ NAPRAWIONE |
| 10 🟢 | `def celnik(route)` bez adnotacji | `...network.py:29, 51, 68` | 🟡→🟢 CZĘŚCIOWO |

### Szczegóły najważniejszych poprawek

**1 🔴 → naprawione.** Linia 124 to teraz
`page.goto("https://sklep.testowy/logo.png")`. Adres pasuje do wzorca `**/*.png`,
więc celnik z `route.abort()` faktycznie przechwytuje zapytanie i to **on** wywołuje
`Error` — test sprawdza wreszcie to, co deklaruje docstring, i nie zależy już od DNS.

**3 🟡 → naprawione.** `log_message` dokumentuje oba argumenty:
```python
Args:
    format: format stringa logu (ignorowany).
    *args: argumenty logu (ignorowane).
```

**4 🟡 → naprawione.** `def serwer_api() -> Iterator[str]:` plus
`from collections.abc import Iterator` w grupie stdlib (linia 5), poprawnie
posortowane alfabetycznie względem `http.server`.

---

## 🟢 Drobiazgi — do zapamiętania na przyszłość

**10.** `playwright_pytest_network.py` linie 29, 51, 68 — celnicy mają już
`-> None`, ale parametr wciąż bez adnotacji: `def celnik(route) -> None:`.
Komplet to `def celnik(route: Route) -> None:` (`Route` z `playwright.sync_api`).
Nie blokuje — teoria tematu modeluje ten sam skrócony styl.

**11.** `conftest.py` — sekcje `Returns:` w `do_GET`, `do_POST` i `log_message`
mają samo `None` zamiast formatu `None: <opis>` używanego w reszcie repo.

**12.** `conftest.py` linia 133 — `api()` ma adnotację `-> APIRequestContext`,
choć jest generatorem (`yield`). Skoro `Iterator` jest teraz zaimportowany dla
`serwer_api`, warto dla spójności dać `-> Iterator[APIRequestContext]`.
Adnotację narzucał TODO ze szkieletu, więc nie liczę jej jako błędu.

---

## Co jest dobre

- **Kontrakt `None`** w `zadanie_06` wzorcowy: `if response.ok is False: return None`
  — `is False` zamiast `== False`, błąd przez `None`, nigdy string-jako-błąd.
- **`zadanie_11`** — `dict.get()` bez wartości domyślnej: kontrakt „nieznane → `None`"
  w jednej linii, bez `if`-ów.
- **`zadanie_12`** składa dwóch celników i czeka przez
  `expect(...).to_be_visible(timeout=2000)` zamiast `sleep` — brak flake'a przy
  asynchronicznym `fetch` w skrypcie strony.
- **Zero martwego kodu** w trzech plikach: każdy import ma realne użycie,
  żadnych resztkowych `pass` ani TODO.
- Reakcja na review: wszystkie 5 uwag blokujących naprawione + 4 z 5 drobiazgów 🟢,
  bez zepsucia czegokolwiek innego (24/24 dalej zielone).

---

## Werdykt

**ZALICZONE — gotowe do dalej**

24/24 testów zielonych, zero uwag 🔴, zero uwag 🟡. Pozostałe punkty 10–12 są
kosmetyczne (🟢) i nie blokują zamknięcia tematu.
