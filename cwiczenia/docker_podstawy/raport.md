# Raport review — docker_podstawy

**Data:** 2026-07-21
**Tryb:** re-review nr 1

## Wynik pytest

Uruchomione interpreterem z venv repo (`.venv\Scripts\python.exe`).

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Lenovo\Desktop\Python - Projekty\CC_Cwiczenia\cwiczenia\docker_podstawy
plugins: anyio-4.14.2
collected 27 items

test_docker_podstawy.py::test_zadanie_01_buduje_linie_from_dla_pythona PASSED [  3%]
test_docker_podstawy.py::test_zadanie_01_dziala_dla_innego_obrazu PASSED [  7%]
test_docker_podstawy.py::test_zadanie_02_buduje_linie_copy_do_kropki PASSED [ 11%]
test_docker_podstawy.py::test_zadanie_02_buduje_linie_copy_do_podfolderu PASSED [ 14%]
test_docker_podstawy.py::test_zadanie_03_laczy_dwa_polecenia_operatorem_and PASSED [ 18%]
test_docker_podstawy.py::test_zadanie_03_zwraca_none_dla_pustej_listy PASSED [ 22%]
test_docker_podstawy.py::test_zadanie_04_buduje_cmd_w_formie_exec PASSED [ 25%]
test_docker_podstawy.py::test_zadanie_04_zwraca_none_dla_pustej_listy PASSED [ 29%]
test_docker_podstawy.py::test_zadanie_05_sklada_pelny_dockerfile_w_kolejnosci PASSED [ 33%]
test_docker_podstawy.py::test_zadanie_05_pomija_run_gdy_brak_polecen PASSED [ 37%]
test_docker_podstawy.py::test_zadanie_06_buduje_polecenie_z_domyslnym_kontekstem PASSED [ 40%]
test_docker_podstawy.py::test_zadanie_06_uzywa_podanego_kontekstu PASSED [ 44%]
test_docker_podstawy.py::test_zadanie_07_parsuje_poprawne_mapowanie_na_krotke PASSED [ 48%]
test_docker_podstawy.py::test_zadanie_07_zwraca_none_gdy_brak_dwukropka PASSED [ 51%]
test_docker_podstawy.py::test_zadanie_07_zwraca_none_gdy_port_nie_jest_liczba PASSED [ 55%]
test_docker_podstawy.py::test_zadanie_08_buduje_pelne_polecenie_run PASSED [ 59%]
test_docker_podstawy.py::test_zadanie_08_zwraca_none_dla_zlego_mapowania PASSED [ 62%]
test_docker_podstawy.py::test_zadanie_09_buduje_usluge_z_portami_i_wolumenami PASSED [ 66%]
test_docker_podstawy.py::test_zadanie_09_pomija_puste_listy PASSED       [ 70%]
test_docker_podstawy.py::test_zadanie_10_opakowuje_uslugi_w_klucz_services PASSED [ 74%]
test_docker_podstawy.py::test_zadanie_10_zwraca_none_dla_pustych_uslug PASSED [ 77%]
test_docker_podstawy.py::test_zadanie_11_dockerfile_zawiera_wszystkie_linie PASSED [ 81%]
test_docker_podstawy.py::test_zadanie_11_uzywa_podanej_nazwy_pliku PASSED [ 85%]
test_docker_podstawy.py::test_zadanie_12_headless_daje_trzy_flagi PASSED [ 88%]
test_docker_podstawy.py::test_zadanie_12_bez_headless_sa_tylko_dwie_flagi PASSED [ 92%]
test_docker_podstawy.py::test_zadanie_13_buduje_compose_z_usluga_scraper PASSED [ 96%]
test_docker_podstawy.py::test_zadanie_13_wolumen_zawiera_podany_folder PASSED [100%]

============================= 27 passed in 0.11s ==============================
```

## Status uwag z rundy 1

| # | Uwaga | Plik | Status |
|---|-------|------|--------|
| 1 | 🔴 Obcy, nieużywany import `pandas.core.dtypes.cast` | `docker_podstawy.py:3` | **NAPRAWIONE** — linia usunięta, zostało samo `import json` |
| 2 | 🟡 CMD dopisywany bez guardu None (zad. 05) | `docker_podstawy.py:97` | **NAPRAWIONE** — dodane `if linia_cmd is not None` |
| 3 | 🟢 Podwójna spacja po `=` | `test_docker_podstawy.py:28` | nadal aktualne — 🟢, nie blokuje |
| 4 | 🟢 Zad. 13 deklaruje `-> dict`, propaguje `dict \| None` | `docker_podstawy.py:230` | nadal aktualne — 🟢, nie blokuje |
| 5 | 🟢 Długie linie | `test_docker_podstawy.py:253, 360` | nadal aktualne — 🟢, nie blokuje |

Poprawki niczego nie zepsuły: 27/27 nadal zielone.

Uwaga 2 zweryfikowana realnie — ten sam przypadek, który wcześniej wywalał
`TypeError`, teraz zwraca poprawny string:

```
>>> zadanie_05_zbuduj_dockerfile("python", "3.12-slim", [["a","."]], [], [])
'FROM python:3.12-slim\nCOPY a .'
```

Dockerfile bez CMD to legalna konstrukcja (obraz dziedziczy CMD z bazy), więc
takie zachowanie jest poprawne — pusty `cmd` po prostu pomija linię, zamiast
przerywać budowę.

## Uwagi w tej rundzie

🔴 — brak.
🟡 — brak.

🟢 **Do zapamiętania na przyszłość:**

**1. `test_docker_podstawy.py:28`** — podwójna spacja po `=`
(`wynik =  zadanie_01_linia_from(...)`).

**2. Zadanie 13 — `docker_podstawy.py:230`** — sygnatura `-> dict`, a zwracany
jest wynik `zadanie_10_zbuduj_compose` o typie `dict | None`. W praktyce zawsze
niepusty słownik, więc `None` nie wystąpi — ale typ deklarowany rozjeżdża się
z propagowanym. Docelowo `-> dict | None` albo krótki komentarz.

**3. Długie linie** — `test_docker_podstawy.py:253 (101), 360 (112)`, oba to
asserty na pełnych słownikach.

Punkty 1 i 3 to robota dla formattera — `ruff format` przy okazji kolejnego
tematu je zdejmie.

## Co jest dobrze

- **Kontrakt `None` konsekwentny w warstwie parsującej** — zad. 03, 04, 07, 10
  zwracają `None` dla pustego/niepoprawnego wejścia, każde z osobnym testem
  brzegowym. Zad. 08 poprawnie deleguje walidację do zad. 07 zamiast
  duplikować `split(":")` — i test to sprawdza (`"abc:80"` → None).
- **Po poprawce zad. 05 jest w pełni spójne** — RUN i CMD mają teraz ten sam
  guard `is not None`, obie linie opcjonalne traktowane tak samo.
- **Zazębienie z wcześniejszymi tematami zrobione przez kompozycję**, nie
  kopiowanie: zad. 11 składa Dockerfile z zad. 01-05, zad. 13 buduje compose
  z zad. 09-10.
- Zad. 04 na `json.dumps(czesci)` zamiast ręcznego sklejania cudzysłowów —
  poprawny sposób na formę exec CMD, odporny na znaki specjalne.
- Zad. 09 warunkowo dokłada klucze `ports`/`volumes` tylko dla niepustych
  list — i test „pomija puste listy" sprawdza dokładnie brak tych kluczy.
- `headless is True` w zad. 12, `is None` w assertach.
- Type hinty i docstringi Args/Returns kompletne; testy mają `-> None`
  i konwencję „Co testuję / Co udaję / Co sprawdzam" spójną z resztą repo.
- `conftest.py` minimalny (tylko `sys.path`) — tu fixtury nie są potrzebne.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony, zero 🔴, zero 🟡.
Temat zamknięty i zacommitowany.
