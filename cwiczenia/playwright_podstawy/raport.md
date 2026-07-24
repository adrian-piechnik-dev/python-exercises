# Raport — `playwright_podstawy`

**Data:** 2026-07-24
**Tryb:** re-review nr 2 (z pełnym audytem plików odblokowanym po zielonym pytest)

---

## Wynik pytest

```
$ python -m pytest -q

........................                                                 [100%]
24 passed in 13.91s
```

Wszystkie 24 testy zielone — blokada importu zniknęła, więc dopiero teraz
mogłem przejść przez `playwright_podstawy.py` i `test_playwright_podstawy.py`
(oba pliki nietknięte od pierwszego review).

---

## Status uwag z poprzednich rund

### 🔴 1. `conftest.py:5` — brak importów `Browser` i `Page` — **NAPRAWIONE**

```python
from playwright.sync_api import Browser, Page, sync_playwright
```

Jeden import third-party, trzy nazwy, żadnego echa Selenium. Kolejność grup
(stdlib → third-party) zachowana.

### 🟡 2. `conftest.py:114` — type hinty w `strona_logowania` — **NAPRAWIONE**
(potwierdzone w rundzie 1)

---

## Audyt pozostałych plików

### `playwright_podstawy.py` — czysto

- Type hinty na wszystkich 12 funkcjach, docstringi w formacie Args/Returns
  (zad. 01 i 11 z argumentami nie-`page`, zad. 06 z jawnym `Returns: None`).
- Kontrakt jeden-typ-albo-None trzymany: zad. 08 i 11 zwracają `str | None`,
  sygnalizacja braku przez `None`, nigdzie string-jako-błąd.
- Zad. 08 słusznie sprawdza `count() == 0` **przed** `get_attribute` — dzięki
  temu brak linku daje `None` od razu, bez czekania na timeout.
- Zad. 09 zwraca `True` albo pozwala `expect` rzucić `AssertionError` —
  dokładnie to, co deklaruje docstring.
- Brak martwego kodu: wszystkie trzy importy (`Page`, `expect`,
  `sync_playwright`) są w użyciu.

### `test_playwright_podstawy.py` — czysto

- Wszystkie testy z `-> None`, fixture z adnotacją `Page` / `tmp_path: Path`.
- Asserty pokrywają się z tym, co deklaruje docstring testu — sprawdziłem
  parami wszystkie 24.
- Para „ścieżka szczęśliwa + przypadek brzegowy" na każde zadanie: pusty
  `<title>`, rola nieobecna na stronie (0), brak linku (`None`), tekst,
  który nigdy się nie pojawia (`pytest.raises(AssertionError)`).
- Test 03 na ukrytej promocji i test 09 na tej samej promocji po kliknięciu
  ładnie pokazują różnicę migawka vs. auto-waiting — sedno tematu złapane.

---

## 🟢 Drobiazgi — do zapamiętania na przyszłość (nie blokują)

1. **`test_playwright_podstawy.py:4-5`** — dwa osobne importy z tego samego
   modułu:
   ```python
   from playwright.sync_api import expect
   from playwright.sync_api import Page
   ```
   Jedna linia z dwiema nazwami czyta się lepiej (jak w `conftest.py:5`).

2. **`playwright_podstawy.py:151`** — spacje wokół `=` przy argumencie
   nazwanym: `name = "Akceptuje regulamin"`. PEP8 chce tu `name="..."`
   (spacje tylko przy przypisaniu do zmiennej). Pozostałe 5 wywołań w pliku
   masz już bez spacji — to pojedyncza literówka stylistyczna.

3. **`test_playwright_podstawy.py:151-152`** — łamanie linii z zamykającym
   nawiasem w środku:
   ```python
   expect(
       strona.get_by_text("Dziekujemy za zgloszenie")).to_be_visible(timeout=2000)
   ```
   Czytelniej: wyciągnąć locator do zmiennej albo złamać przed `.to_be_visible`.
   Druga linia ma 81 znaków, więc i tak wychodzi poza 79.

---

## Werdykt

**ZALICZONE — gotowe do dalej**

Zero uwag 🔴, zero 🟡, pytest zielony. Temat zamknięty, commit wykonany.
