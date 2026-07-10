# Raport review — requests_api_podstawy

**Data:** 2026-07-10
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 24 items

... (24 testów) ...
test_requests_api_podstawy.py::test_zadanie_10_zwraca_wartosc_pola PASSED [ 79%]
test_requests_api_podstawy.py::test_zadanie_10_brak_pola_zwraca_none PASSED [ 83%]
test_requests_api_podstawy.py::test_zadanie_11_zapisuje_dane_do_pliku PASSED [ 87%]
test_requests_api_podstawy.py::test_zadanie_11_blad_serwera_nie_tworzy_pliku PASSED [ 91%]
test_requests_api_podstawy.py::test_zadanie_12_zapisuje_csv_i_zwraca_liczbe PASSED [ 95%]
test_requests_api_podstawy.py::test_zadanie_12_naglowki_z_kluczy_slownika PASSED [100%]

============================= 24 passed in 0.22s ==============================
```

## Status uwag z poprzedniej rundy

### 🟡 → ✅ NAPRAWIONE

**1. zadanie_05 — `timeout=None`**
Plik: `requests_api_podstawy.py`, linia 73
Teraz `requests.get(url, timeout=10)` — zgodne z regułą kursu „timeout ZAWSZE".
Reguła spełniona we wszystkich 12 funkcjach.

### 🟢 (drobiazgi z poprzedniej rundy)

**2. Nazwy atrap dla `requests.post` → ✅ NAPRAWIONE**
Testy zadań 07 i 08 używają teraz `podmieniony_post` (linie 197, 211, 226, 244).

**3. Docstring „Co udaje" w zadaniu_10 → 🟡 CZĘŚCIOWO (nie blokuje)**
- `test_zadanie_10_zwraca_wartosc_pola` (linia 290): docstring wyrównany
  do kodu (`{"imie": "Anna", "wiek": 30}`). NAPRAWIONE.
- `test_zadanie_10_brak_pola_zwraca_none` (linia 304): docstring nadal mówi
  `FakeResponse(200, {"imie": "Anna"})`, a kod (linia 308) zwraca
  `{"imie": "Anna", "wiek": 30}`. Drobny rozjazd opis↔kod; assert poprawny.
  Do wyrównania przy okazji — nie blokuje.

**4. Drobne PEP 8 → NIENAPRAWIONE (nie blokuje)**
- Linia 368: `open(str(p),"r", ...)` — wciąż brak spacji po przecinku.
- Linia 383: `FakeResponse(200,[...])` — wciąż brak spacji po przecinku.
  Kosmetyka; warto wyrobić nawyk spacji po przecinku.

## Werdykt

**ZALICZONE — gotowe do dalej.** pytest zielony (24 passed), zero uwag 🔴,
zero 🟡. Pozostałe drobiazgi 🟢 (punkty 3–4) są kosmetyczne i nie blokują
zamknięcia tematu — do zapamiętania na przyszłość.
