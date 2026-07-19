# Raport review — llm_api_klient

**Data:** 2026-07-19
**Tryb:** re-review nr 1

## Wynik pytest

Uruchomione interpreterem z venv repo (`.venv\Scripts\python.exe`).

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Lenovo\Desktop\Python - Projekty\CC_Cwiczenia\cwiczenia\llm_api_klient
plugins: anyio-4.14.2
collected 25 items

test_llm_api_klient.py::test_zadanie_01_naglowki_zawieraja_klucz_i_wersje PASSED [  4%]
test_llm_api_klient.py::test_zadanie_01_naglowki_maja_content_type_i_nic_wiecej PASSED [  8%]
test_llm_api_klient.py::test_zadanie_02_payload_ma_model_i_max_tokens PASSED [ 12%]
test_llm_api_klient.py::test_zadanie_02_messages_to_lista_z_rola_user PASSED [ 16%]
test_llm_api_klient.py::test_zadanie_03_zwraca_odpowiedz_z_post PASSED   [ 20%]
test_llm_api_klient.py::test_zadanie_03_przekazuje_payload_i_timeout PASSED [ 24%]
test_llm_api_klient.py::test_zadanie_04_zwraca_slownik_dla_poprawnej_odpowiedzi PASSED [ 28%]
test_llm_api_klient.py::test_zadanie_04_rzuca_httperror_dla_bledu PASSED [ 32%]
test_llm_api_klient.py::test_zadanie_05_wyciaga_tekst_z_odpowiedzi PASSED [ 36%]
test_llm_api_klient.py::test_zadanie_05_rzuca_keyerror_gdy_brak_content PASSED [ 40%]
test_llm_api_klient.py::test_zadanie_06_zwraca_tekst_dla_poprawnych_danych PASSED [ 44%]
test_llm_api_klient.py::test_zadanie_06_zwraca_none_dla_zepsutej_struktury PASSED [ 48%]
test_llm_api_klient.py::test_zadanie_07_loguje_nazwe_modelu PASSED       [ 52%]
test_llm_api_klient.py::test_zadanie_07_zwraca_none PASSED               [ 56%]
test_llm_api_klient.py::test_zadanie_08_loguje_komunikat_bledu PASSED    [ 60%]
test_llm_api_klient.py::test_zadanie_08_loguje_na_poziomie_error PASSED  [ 64%]
test_llm_api_klient.py::test_zadanie_09_zwraca_odpowiedz_gdy_brak_bledu PASSED [ 68%]
test_llm_api_klient.py::test_zadanie_09_rzuca_blad_klienta_przy_timeout PASSED [ 72%]
test_llm_api_klient.py::test_zadanie_10_zwraca_slownik_dla_sukcesu PASSED [ 76%]
test_llm_api_klient.py::test_zadanie_10_rzuca_blad_klienta_przy_connectionerror PASSED [ 80%]
test_llm_api_klient.py::test_zadanie_10_rzuca_blad_klienta_przy_bledzie_http PASSED [ 84%]
test_llm_api_klient.py::test_zadanie_11_zwraca_slownik_odpowiedzi PASSED [ 88%]
test_llm_api_klient.py::test_zadanie_11_wysyla_naglowki_z_kluczem_api PASSED [ 92%]
test_llm_api_klient.py::test_zadanie_12_zwraca_tekst_odpowiedzi PASSED   [ 96%]
test_llm_api_klient.py::test_zadanie_12_zwraca_none_i_loguje_blad_przy_timeout PASSED [100%]

============================= 25 passed in 0.08s ==============================
```

## Status uwag z rundy 1

| # | Uwaga | Plik | Status |
|---|-------|------|--------|
| 1 | 🟡 Martwa zmienna `wynik` w `test_zadanie_11_wysyla_naglowki_z_kluczem_api` | `test_llm_api_klient.py:387` | **NAPRAWIONE** — wywołanie bez przypisania |
| 2 | 🟡 Brak type hintów w 8× zagnieżdżonej atrapie `falszywy_post` | `test_llm_api_klient.py` | **NAPRAWIONE** — wszystkie 11 atrap otypowane |
| 3 | 🟢 `except(KeyError, IndexError)` bez spacji | `llm_api_klient.py:103` | **NAPRAWIONE** |
| 4 | 🟢 Brak spacji po przecinku w wywołaniach zad. 11/12 | `test_llm_api_klient.py:362, 388, ...` | nadal aktualne — 🟢, nie blokuje |
| 5 | 🟢 Dwie za długie linie | `test_llm_api_klient.py`, `conftest.py:66` | nadal aktualne — 🟢, nie blokuje |

Żadna poprawka nie zepsuła niczego innego: 25/25 nadal zielone.

Uwaga 2 poprawiona **lepiej niż zalecenie**: w atrapach, które rzucają wyjątek
(`test_zadanie_09_..._timeout:268`, `..._connectionerror:310`,
`test_zadanie_12_..._timeout:428`), dałeś `-> None` zamiast
`-> FalszywaOdpowiedz`. Dokładnie o to chodziło — funkcja, która nigdy nie
wraca normalnie, nie powinna deklarować typu zwracanego, którego nigdy nie
zwróci. Sygnatura sama mówi czytelnikowi "to jest atrapa awarii".

## Uwagi w tej rundzie

🔴 — brak.
🟡 — brak.

🟢 **Do zapamiętania na przyszłość:**

**1. Brak spacji po przecinku** — `test_llm_api_klient.py:362, 388` i dalej:
`"https://api.anthropic.com/v1/messages","sk-test-123"`. W długich listach
argumentów to realnie utrudnia policzenie, który argument jest który.

**2. Długie linie** — `test_llm_api_klient.py:388` (~95 znaków),
`conftest.py:66` (~100 znaków). Reszta pliku trzyma się ~88.

Oba to kandydaci na jedno uruchomienie formattera (`black` / `ruff format`) —
przy następnym temacie warto go wpiąć, żeby takie rzeczy nie zajmowały miejsca
w review.

## Co jest dobrze

- **Kolejność warstw `except` w zad. 10 jest poprawna** i to nie jest
  przypadek: `Timeout` → `ConnectionError` → `HTTPError` → `RequestException`.
  Gdybyś dał `RequestException` wyżej, złapałby wszystko i pozostałe warstwy
  byłyby martwe. Tu każda warstwa realnie działa — i każda ma swój test.
- `raise ... from error` w każdej z 5 konwersji wyjątków — oryginalna przyczyna
  nie ginie, traceback pokazuje pełny łańcuch.
- Kontrakt funkcji trzymany bez wyjątku: zad. 05 rzuca `KeyError` (twardy),
  zad. 06 zwraca `str | None` (miękki), zad. 12 zwraca `str | None` i loguje —
  zero string-jako-błąd, każdy wariant przetestowany z obu stron.
- Zad. 11 i 12 zbudowane z wcześniejszych funkcji zamiast kopiowania kodu —
  dokładnie o to chodziło w tym temacie.
- `monkeypatch.setattr("llm_api_klient.requests.post", ...)` — podmiana
  w przestrzeni nazw modułu testowanego, nie globalnie w `requests`. To jest
  poprawny cel patcha i najczęstszy błąd początkujących; tu go nie ma.
- Testy trzymają schemat przygotuj → podmień → wywołaj → sprawdź, docstringi
  "Co testuję / Co udaję / Co sprawdzam" zgadzają się z assertami.
- `conftest.py`: atrapa `FalszywaOdpowiedz` udaje tylko `json()`
  i `raise_for_status()` — czyli dokładnie to, czego używa testowany kod,
  bez udawania całego `Response`. Dwie fixtury pokrywają sukces i błąd HTTP.
- `is True` / `is None` w assertach, `self.blad_http is True` w conftest.
- Kolejność importów stdlib → third-party → local zachowana we wszystkich
  trzech plikach.

## Werdykt

**ZALICZONE — gotowe do dalej.** Pytest zielony, zero 🔴, zero 🟡.
Temat zamknięty i zacommitowany.
