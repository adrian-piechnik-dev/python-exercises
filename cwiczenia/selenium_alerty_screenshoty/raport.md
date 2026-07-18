# Raport review — selenium_alerty_screenshoty

**Data:** 2026-07-18
**Tryb:** re-review nr 1

## Wynik pytest

Uruchomione interpreterem z venv repo (`.venv\Scripts\python.exe`) — globalne
`python` (Python313) nie ma zainstalowanego selenium.

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Lenovo\Desktop\Python - Projekty\CC_Cwiczenia\cwiczenia\selenium_alerty_screenshoty
plugins: anyio-4.14.2
collected 20 items

test_selenium_alerty_screenshoty.py::test_zadanie_01_tworzy_plik_zrzutu PASSED [  5%]
test_selenium_alerty_screenshoty.py::test_zadanie_01_przekazuje_sciezke_jako_string PASSED [ 10%]
test_selenium_alerty_screenshoty.py::test_zadanie_02_sklada_sciezke_i_robi_zrzut PASSED [ 15%]
test_selenium_alerty_screenshoty.py::test_zadanie_02_zwraca_path_nie_string PASSED [ 20%]
test_selenium_alerty_screenshoty.py::test_zadanie_03_zwraca_uchwyt_alertu PASSED [ 25%]
test_selenium_alerty_screenshoty.py::test_zadanie_03_nie_klika_niczego PASSED [ 30%]
test_selenium_alerty_screenshoty.py::test_zadanie_04_zwraca_tresc_alertu PASSED [ 35%]
test_selenium_alerty_screenshoty.py::test_zadanie_04_nie_zamyka_alertu PASSED [ 40%]
test_selenium_alerty_screenshoty.py::test_zadanie_05_akceptuje_alert PASSED [ 45%]
test_selenium_alerty_screenshoty.py::test_zadanie_05_nie_odrzuca PASSED  [ 50%]
test_selenium_alerty_screenshoty.py::test_zadanie_06_odrzuca_alert PASSED [ 55%]
test_selenium_alerty_screenshoty.py::test_zadanie_06_nie_akceptuje PASSED [ 60%]
test_selenium_alerty_screenshoty.py::test_zadanie_07_zwraca_tresc_gdy_alert_jest PASSED [ 65%]
test_selenium_alerty_screenshoty.py::test_zadanie_07_brak_alertu_zwraca_none PASSED [ 70%]
test_selenium_alerty_screenshoty.py::test_zadanie_08_zwraca_obecny_alert PASSED [ 75%]
test_selenium_alerty_screenshoty.py::test_zadanie_08_brak_alertu_konczy_sie_timeoutem PASSED [ 80%]
test_selenium_alerty_screenshoty.py::test_zadanie_09_czyta_i_akceptuje PASSED [ 85%]
test_selenium_alerty_screenshoty.py::test_zadanie_09_timeout_zwraca_none PASSED [ 90%]
test_selenium_alerty_screenshoty.py::test_zadanie_10_akceptuje_i_robi_zrzut PASSED [ 95%]
test_selenium_alerty_screenshoty.py::test_zadanie_10_bez_alertu_none_i_brak_zrzutu PASSED [100%]

============================= 20 passed in 3.49s ==============================
```

## Status uwag z rundy 1

| # | Uwaga | Plik | Status |
|---|-------|------|--------|
| 1 | 🟡 Trzy puste linie między zad. 01 a zad. 02 | `selenium_alerty_screenshoty.py` | **NAPRAWIONE** — dwie puste linie (22-24) |
| 2 | 🟢 Podwójna spacja w `wynik  =` (zad. 09) | `test_selenium_alerty_screenshoty.py` | **NAPRAWIONE** |
| 3 | 🟢 `self.zrzuty = []` bez adnotacji typu | `conftest.py:105` | nadal aktualne — 🟢, nie blokuje |

Żadna poprawka nie zepsuła niczego innego: 20/20 nadal zielone.

## Uwagi w tej rundzie

🔴 — brak.
🟡 — brak.

🟢 **Do zapamiętania na przyszłość** — `conftest.py:105`: `self.zrzuty = []`
bez adnotacji typu, podczas gdy reszta pliku jest w pełni otypowana.
Docelowo `self.zrzuty: list[str] = []`. Lista budowana w `__init__` i
uzupełniana w `save_screenshot` to dokładnie ten przypadek, gdzie adnotacja
mówi czytelnikowi, co w środku siedzi — sam `[]` tego nie mówi.

## Co jest dobrze

- Type hinty na każdej funkcji, także testowej (`-> None`).
- Docstringi w formacie Args/Returns; `Args: Brak.` przy metodach
  bezargumentowych w `conftest.py` (`accept`, `dismiss`, property `alert`).
- `is None` / `is True` / `is False` wszędzie tam, gdzie sprawdzasz tożsamość —
  zero `== None` / `== True`.
- Brak martwego kodu: żadnych nieużywanych importów, żadnych zostawionych TODO
  ani `pass` po implementacji.
- Kolejność importów stdlib → third-party → local zachowana we wszystkich
  trzech plikach, grupy oddzielone pustą linią.
- Kontrakt funkcji trzymany: zad. 07/09/10 zwracają `Optional[...]`, błąd
  sygnalizowany przez `None`, nigdy przez string-jako-błąd. Zad. 08 świadomie
  przepuszcza `TimeoutException` w górę — i test to sprawdza `pytest.raises`.
- Testy trzymają schemat przygotuj → podmień → wywołaj → sprawdź, a asserty
  pokrywają dokładnie to, co deklaruje docstring testu (w szczególności
  zad. 10: sprawdzasz i `None`, i BRAK pliku zrzutu — to dobry test negatywny).
- Zad. 01 z osobnym testem na konwersję `Path` → `str` — dokładnie ta pułapka,
  o którą chodziło w temacie.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony, zero 🔴, zero 🟡.
Temat zamknięty i zacommitowany.
