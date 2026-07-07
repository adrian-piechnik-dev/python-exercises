# Pliki tekstowe w Pythonie: open, read, write, tryby

---

## 1. Otwieranie pliku — `open()` i kontekst menedżer `with`

Żeby pracować z plikiem, otwierasz go funkcją `open()`. Najlepiej zawsze
używaj bloku `with` — Python zamknie plik automatycznie nawet przy wyjątku:

```python
with open("dane.txt", "r", encoding="utf-8") as f:
    zawartosc = f.read()
# tutaj plik jest już zamknięty — f.close() wywołane automatycznie
```

Schemat: `with open(sciezka, tryb, encoding="utf-8") as f:`

**Dlaczego `with`?**
Bez `with` musisz pamiętać o `f.close()`. Gdy wyjątek przerwie kod między
`open()` a `close()`, plik zostaje niezamknięty — `with` eliminuje ten problem.

**Typowe błędy:**
- Zapomniane `encoding="utf-8"` → system używa domyślnego kodowania (może być różne na Windows/Linux)
- Brak `with` + brak `close()` → "wyciek" deskryptora pliku

---

## 2. Tryby otwarcia — `"r"`, `"w"`, `"a"`

Drugi argument `open()` to **tryb**:

| Tryb | Nazwa | Zachowanie |
|---|---|---|
| `"r"` | read | Czyta plik; `FileNotFoundError` gdy nie istnieje |
| `"w"` | write | Zapisuje plik; **nadpisuje** jeśli istnieje; tworzy gdy nie istnieje |
| `"a"` | append | Dopisuje na końcu; tworzy gdy nie istnieje |

```python
# odczyt
with open("dane.txt", "r", encoding="utf-8") as f:
    tekst = f.read()

# zapis (nadpisuje)
with open("dane.txt", "w", encoding="utf-8") as f:
    f.write("Nowa treść")

# dopisywanie
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("nowa linia\n")
```

**Typowe błędy:**
- Przypadkowe `"w"` zamiast `"a"` → cały plik jest kasowany
- Czytanie pliku otwartego w trybie `"w"` → `UnsupportedOperation`

---

## 3. Czytanie — `read()`, `readlines()`, `splitlines()`

Trzy sposoby wczytania zawartości:

```python
with open("dane.txt", "r", encoding="utf-8") as f:
    tekst = f.read()           # → jeden str z całą zawartością
```

```python
with open("dane.txt", "r", encoding="utf-8") as f:
    linie = f.readlines()      # → list[str] — każda linia z "\n" na końcu
    # ["ala ma kota\n", "pies i kot\n"]
```

```python
with open("dane.txt", "r", encoding="utf-8") as f:
    linie = f.read().splitlines()  # → list[str] — linie BEZ "\n"
    # ["ala ma kota", "pies i kot"]
```

**Rekomendacja:** `splitlines()` jest wygodniejszy — nie musisz ręcznie
usuwać `"\n"` z każdej linii.

Porównanie:
```python
# readlines() zostawia "\n" — trzeba usuwać:
linie = [l.rstrip("\n") for l in f.readlines()]

# splitlines() — bez dodatkowej pracy:
linie = f.read().splitlines()
```

---

## 4. Zapis — `write()` i `writelines()`

```python
with open("wyniki.txt", "w", encoding="utf-8") as f:
    f.write("Wyniki:\n")            # write() przyjmuje jeden str
    f.write("Ala: 5\n")
```

Zapis listy linii przez złączenie:
```python
linie = ["ala", "pies", "kot"]

with open("wyniki.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(linie))       # łączy stringi znakiem nowej linii
```

Alternatywa — `writelines()` (nie dodaje automatycznie `"\n"`!):
```python
with open("wyniki.txt", "w", encoding="utf-8") as f:
    f.writelines(l + "\n" for l in linie)   # musisz sam dodać "\n"
```

**Typowe błędy:**
- `f.write(liczba)` → `TypeError`, `write()` przyjmuje tylko `str`
- `"\n".join(linie)` bez `"\n"` na końcu — ostatnia linia bez newline
  (normalnie akceptowalne, zależy od wymagań)

---

## 5. Dopisywanie — tryb `"a"`

Tryb `"a"` nie niszczy istniejącej zawartości — otwiera plik
i ustawia kursor na końcu:

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("2026-07-07: uruchomiono program\n")
```

Jeśli plik nie istnieje, zostaje utworzony — identycznie jak `"w"`.
Różnica: `"w"` kasuje istniejącą treść, `"a"` zachowuje ją i dopisuje.

```python
# sekwencja dwóch dopisań:
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("linia 1\n")
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("linia 2\n")
# plik: "linia 1\nlinia 2\n"
```

---

## 6. Encoding — dlaczego `"utf-8"` zawsze

Python 3 na różnych systemach używa różnych domyślnych kodowań:
- Linux/macOS: UTF-8
- Windows: często `cp1250` (polskie znaki działają inaczej)

Żeby program działał tak samo wszędzie, **zawsze podawaj encoding="utf-8"**:

```python
# dobrze — jawne kodowanie
with open("dane.txt", "r", encoding="utf-8") as f:
    ...

# źle — zależne od systemu
with open("dane.txt", "r") as f:   # ← może się wysypać na Windows
    ...
```

---

## 7. Newline — `\n` i `\r\n`

Na Windowsie standardowy plik tekstowy używa `\r\n` (CRLF).
Domyślny tryb tekstowy `"r"` automatycznie zamienia `\r\n` → `\n`
przy czytaniu (i `\n` → `\r\n` przy zapisie), więc w kodzie zawsze masz `\n`.

Jeśli potrzebujesz surowego zachowania (np. przy CSV), używasz `newline=""` — 
ale to temat następnego mini-kursu (`csv_dict_reader_writer`).

---

## 8. Spirala — pojęcia z `import_try_except_pathlib`

Znasz już z poprzedniego tematu (`import_try_except_pathlib`):
- `try/except FileNotFoundError` przy próbie otwarcia nieistniejącego pliku
- Wzorzec: `try: ... except FileNotFoundError: return None`

W ostatnich 3 zadaniach tego tematu będziesz otwierać pliki
z obsługą `FileNotFoundError`. Nie tłumaczę tego od nowa — opierasz się
na tym, co już wiesz.

---

## 9. Testowanie kodu z plikami — `tmp_path` w pytest

### Problem: testy potrzebują prawdziwych plików

Funkcja czytająca plik potrzebuje pliku na dysku — nie możesz jej przetestować
podając string z treścią. Musisz plik najpierw **stworzyć**, przekazać ścieżkę,
a potem **posprzątać** (żeby testy nie zaśmiecały dysku i nie wpływały na siebie).

pytest robi to za ciebie przez wbudowany fixture `tmp_path`.

### `tmp_path` — tymczasowy katalog per test

`tmp_path` to fixture pytest dostępny w każdym teście bez dodatkowych importów.
Zwraca `Path` do unikalnego, tymczasowego katalogu — każdy test dostaje swój własny,
a po zakończeniu wszystkich testów pytest sprząta automatycznie:

```python
from pathlib import Path

def test_przyklad(tmp_path: Path) -> None:
    # tmp_path to Path do unikalnego katalogu, np. C:/Temp/pytest-123/test_0/
    plik = tmp_path / "dane.txt"
    plik.write_text("zawartość", encoding="utf-8")

    assert plik.exists()
    assert plik.read_text(encoding="utf-8") == "zawartość"
```

Żeby użyć `tmp_path`, wystarczy dodać go jako parametr funkcji testowej.
pytest wstrzykuje go automatycznie — to jest właśnie **fixture**.

### Fixture — funkcja przygotowująca środowisko testu

Fixture to funkcja oznaczona `@pytest.fixture`, której wynik pytest
wstrzykuje do testu jako argument:

```python
import pytest
from pathlib import Path

@pytest.fixture
def dane_plik(tmp_path: Path) -> Path:
    p = tmp_path / "dane.txt"
    p.write_text("ala\nma\nkota", encoding="utf-8")
    return p

def test_cos(dane_plik: Path) -> None:
    # dane_plik to gotowy Path do pliku z treścią
    wynik = dane_plik.read_text(encoding="utf-8")
    assert "ala" in wynik
```

Fixture jest wykonywany **raz przed każdym testem** który go używa.

---

## 10. conftest.py — sys.path i fixtures

### Dlaczego testy nie widzą modułu?

Gdy pytest uruchamia `test_pliki_tekstowe.py`, szuka modułu `pliki_tekstowe`
w `sys.path` — liście katalogów gdzie Python szuka modułów.
Twój folder `cwiczenia/pliki_tekstowe/` domyślnie tam nie ma.

### sys.path.insert — rozwiązanie

W `conftest.py` (specjalny plik konfiguracyjny pytest) wstawiasz folder tematu
na początek `sys.path`:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# os.path.abspath(__file__)  → absolutna ścieżka do conftest.py
# os.path.dirname(...)       → katalog tego pliku (= folder tematu)
# sys.path.insert(0, ...)    → wstaw na pierwszą pozycję listy
```

`conftest.py` jest ładowany przez pytest **automatycznie** przed testami
w tym folderze. Fixtures zdefiniowane w `conftest.py` są dostępne
w każdym pliku testowym w tym folderze — wystarczy podać ich nazwę jako parametr.

**Kolejność implementacji:**
1. Uzupełnij `conftest.py` (sys.path + fixtures)
2. Uzupełnij `pliki_tekstowe.py` (logika funkcji)
3. Uzupełnij `test_pliki_tekstowe.py` (ciała testów)
4. Uruchom pytest — powinno być zielono

---

## 11. Schemat 3 pytań — jak pisać docstring testu

Zanim zaczniesz pisać ciało testu, odpowiedz na 3 pytania i wstaw je jako docstring.
Dokładne odpowiedzi to dokumentacja — pomogą ci gdy test nie przejdzie:

```
Co testuje:  <jedno zachowanie / jeden kontrakt funkcji>
Co udaje:    <co symulujemy / co zastępujemy — albo "nic" gdy używamy prawdziwych danych>
Co sprawdzam: <co konkretnie weryfikuje assert>
```

Przykład dla testu funkcji `obetnij(tekst: str, n: int) -> str`:
```python
def test_obetnij_za_krotki_tekst() -> None:
    """Co testuje: tekst krótszy niż n jest zwracany bez zmian.
    Co udaje: nic — czysta funkcja na stringach, brak zależności zewnętrznych.
    Co sprawdzam: wynik == tekst (niezmieniony) i len(wynik) < n.
    """
```

---

## 12. Schemat przygotuj → wywołaj → sprawdź

Ciało każdego testu ma ten sam rytm trzech faz:

```python
def test_przyklad() -> None:
    # przygotuj — dane wejściowe
    tekst = "Python jest super"
    n = 6

    # wywołaj — jedno wywołanie testowanej funkcji
    wynik = obetnij(tekst, n)

    # sprawdź — assert
    assert wynik == "Python"
    assert len(wynik) == n
```

Gdy test wymaga pliku, faza "przygotuj" obejmuje stworzenie pliku:

```python
def test_czytaj_pierwsza_ze_zdania(tmp_path: Path) -> None:
    """Co testuje: zwraca pierwsze słowo z pierwszej linii.
    Co udaje: nic — tworzę plik przez tmp_path.
    Co sprawdzam: wynik == "Python".
    """
    # przygotuj
    p = tmp_path / "tekst.txt"
    p.write_text("Python jest super\njęzyk skryptowy\n", encoding="utf-8")

    # wywołaj
    wynik = pierwsze_slowo_z_pierwszej_linii(str(p))

    # sprawdź
    assert wynik == "Python"
```

Uwaga: funkcja `pierwsze_slowo_z_pierwszej_linii` i plik z "Python jest super"
są tu fikcyjne — służą pokazaniu wzorca, nie gotowcowi do zadań w tym temacie.

---

## Podsumowanie — mapa pojęć

```python
# odczyt całości
with open(sciezka, "r", encoding="utf-8") as f:
    tekst = f.read()               # → str

# odczyt linii (bez "\n")
with open(sciezka, "r", encoding="utf-8") as f:
    linie = f.read().splitlines()  # → list[str]

# zapis (nadpisuje)
with open(sciezka, "w", encoding="utf-8") as f:
    f.write(tekst)

# zapis listy linii
with open(sciezka, "w", encoding="utf-8") as f:
    f.write("\n".join(linie))

# dopisywanie
with open(sciezka, "a", encoding="utf-8") as f:
    f.write(linia + "\n")

# odczyt z obsługą braku (spirala z import_try_except_pathlib)
try:
    with open(sciezka, "r", encoding="utf-8") as f:
        return f.read()
except FileNotFoundError:
    return None
```
