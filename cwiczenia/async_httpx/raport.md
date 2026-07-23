# Raport review — async_httpx

**Data:** 2026-07-23
**Tryb:** re-review nr 1

## Wynik pytest

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Piechu\Desktop\CC_cwiczenia\cwiczenia\async_httpx
plugins: anyio-4.14.2
collected 26 items

test_async_httpx.py ... (26 testów) ...                                [100%]

============================= 26 passed in 0.66s ==============================
```

Wszystkie 26 testów zielone.

## Status uwag z poprzedniej rundy

**1. 🟡 `async_httpx.py:3-4` — martwe importy** → **NAPRAWIONE**
   `from http.client import responses` i `from types import coroutine`
   usunięte. Blok importów jest teraz czysty: `asyncio`, `time` (stdlib),
   pusta linia, `httpx`, `bs4` (third-party).

**2. 🟡 `test_async_httpx.py:129` — assert słabszy niż docstring** → **NAPRAWIONE**
   `assert wynik < 0.05` — zgodne z deklaracją w docstringu.

**3. 🟡 `test_async_httpx.py:53` — kod niezgodny z docstringiem** → **NAPRAWIONE**
   Spanie skrócone do `0.01`, zgodnie z docstringiem.

**4. 🟡 `conftest.py:21` — okrojona sekcja Returns** → **NAPRAWIONE**
   Wiersz tabeli znów opisuje pełną odpowiedź
   (`"<html><head><title>Testowa strona</title></head></html>"`).

**5. 🟡 `conftest.py:35` — niespójne wcięcie** → **NAPRAWIONE**
   Wszystkie gałęzie `if/elif` mają teraz równe wcięcie 8 spacji.

**6. 🟡 `async_httpx.py:171, 213` — comprehension tożsamościowa** → **NAPRAWIONE**
   Obie funkcje (zadania 11 i 13) zwracają teraz wprost `return odpowiedzi`.

Poprawione zostały także drobiazgi 🟢 z poprzedniej rundy: brak spacji
w `zadanie_10_pobierz_json(client, url)`, podwójna spacja w
`assert wynik == 404`, `request: httpx.Request` oraz nadmiarowe puste
linie na końcu `conftest.py`.

## Uwagi bieżącej rundy

Brak nowych uwag 🔴/🟡.

### 🟢 Do zapamiętania na przyszłość (nie blokują)

- `conftest.py:44` — przy okazji przeformatowania gałąź `/strona2` zamyka
  nawias w tej samej linii co argument
  (`...</html>")`), podczas gdy pozostałe sześć gałęzi zamyka go
  w osobnej linii. Czysta kosmetyka, ale warto trzymać jeden styl
  w obrębie jednej funkcji.
- `conftest.py:56` — fixture nadal oddaje `AsyncClient`, który nigdy nie
  zostaje zamknięty. Przy `MockTransport` nie generuje to ostrzeżeń, ale
  docelowy wzorzec dla zasobu to fixture z `yield` i `await client.aclose()`
  po nim.
- `async_httpx.py` — nagłówek ze spisem zadań nadal usunięty; pozostałe
  tematy w kursie go mają (kwestia spójności, nie poprawności).

## Werdykt

**ZALICZONE — gotowe do dalej.** pytest zielony, zero uwag 🔴/🟡.
