# Listy i pętle w Pythonie: for, akumulator, enumerate, zip, list comprehension

---

## 1. Co to jest lista?

Wyobraź sobie zakupy. Masz kartkę z listą produktów: mleko, chleb, masło.
Ta kartka to właśnie **lista** — jedno miejsce, w którym trzymasz wiele rzeczy po kolei.

W Pythonie lista wygląda tak:

```python
zakupy = ["mleko", "chleb", "masło"]
oceny  = [5, 4, 3, 5, 2]
pusta  = []                        # lista bez żadnych elementów
```

Lista jest **uporządkowana** — kolejność elementów ma znaczenie i jest zapamiętana.
Lista może być **pusta** — `[]` — i to jest poprawna, normalna lista.
Jeden typ danych na raz — listy liczb, listy tekstów, nie mieszamy bez powodu.

**Jak stworzyć listę:**
```python
imiona = ["Anna", "Piotr", "Zofia"]
liczby = [10, 20, 30, 40]
```

**Typowe błędy początkujących:**
- Pisanie `(1, 2, 3)` z nawiasami okrągłymi zamiast kwadratowych — to krotka (tuple), nie lista
- Brak przecinków między elementami: `["Anna" "Piotr"]` → `SyntaxError`

---

## 2. Dostęp do elementów — indeksy

Każdy element listy ma swój **numer pozycji** zwany **indeksem**.
Python liczy od **zera**:

```python
imiona = ["Anna", "Piotr", "Zofia"]
#           0       1        2

imiona[0]   # → "Anna"   (pierwszy element, indeks 0)
imiona[1]   # → "Piotr"  (drugi element, indeks 1)
imiona[2]   # → "Zofia"  (trzeci element, indeks 2)
imiona[-1]  # → "Zofia"  (ostatni element — ujemny indeks idzie od końca)
imiona[-2]  # → "Piotr"  (przedostatni)
```

**Typowe błędy początkujących:**
- `lista[1]` gdy lista jest pusta lub ma jeden element → `IndexError`
- Zakładanie że pierwszy element to `lista[1]` zamiast `lista[0]`

---

## 3. Długość listy — `len()`

`len()` zwraca liczbę elementów w liście:

```python
imiona = ["Anna", "Piotr", "Zofia"]
len(imiona)   # → 3

pusta = []
len(pusta)    # → 0
```

Przydatne do sprawdzania czy lista nie jest pusta:

```python
if len(imiona) == 0:
    print("Pusta lista!")
```

**Typowe błędy początkujących:**
- Pisanie `imiona.len()` zamiast `len(imiona)` — `len` to funkcja wbudowana, nie metoda listy

---

## 4. Dodawanie elementów — `append()`

`append()` to **metoda listy**, która dołącza jeden element na **końcu** listy:

```python
wynik = []                 # zaczynam od pustej listy
wynik.append("Anna")       # lista: ["Anna"]
wynik.append("Piotr")      # lista: ["Anna", "Piotr"]
wynik.append("Zofia")      # lista: ["Anna", "Piotr", "Zofia"]
```

Schemat: `lista.append(nowy_element)` — kropka, nazwa metody, nawias, co dodać.

**Typowe błędy początkujących:**
- `wynik = wynik.append("X")` → `wynik` staje się `None`! `append()` modyfikuje listę w miejscu i nic nie zwraca
- `append(wynik, "X")` → `NameError` — `append` to metoda wywoływana przez kropkę

---

## 5. Type hint dla listy — `list[int]`, `list[str]`

Tak jak `int` oznacza liczbę całkowitą, `list[int]` oznacza **listę liczb całkowitych**:

```python
def suma(liczby: list[int]) -> int:
    ...

def połącz(slowa: list[str]) -> str:
    ...
```

- `list[int]` — lista liczb całkowitych
- `list[str]` — lista tekstów
- `list[float]` — lista liczb z przecinkiem
- `list` (bez nawiasów) — lista dowolnych elementów

Działa w Pythonie 3.9 i nowszym (mamy 3.13, więc OK).

**Typowe błędy początkujących:**
- Pisanie `List[int]` z wielkiej litery — to stary styl (wymagał `from typing import List`); dziś używamy `list[int]`

---

## 6. Pętla `for` — przejdź po każdym elemencie

`for` (po angielsku "dla każdego") pozwala wykonać kod **dla każdego elementu listy po kolei**:

```python
imiona = ["Anna", "Piotr", "Zofia"]

for imie in imiona:
    print(imie)

# wypisze:
# Anna
# Piotr
# Zofia
```

Schemat:
```
for <zmienna> in <lista>:
    <kod wykonywany dla każdego elementu>
```

`imie` to zmienna tymczasowa — przy każdym obrocie pętli dostaje wartość kolejnego elementu.
Możesz ją nazwać jak chcesz, ale używaj sensownych nazw.

**Pętla dla pustej listy — nic się nie dzieje:**
```python
for x in []:
    print(x)    # nie wykona się ani razu
```

**Typowe błędy początkujących:**
- Brak dwukropka na końcu `for` → `SyntaxError`
- Brak wcięcia (4 spacje) w ciele pętli → `IndentationError`
- Mylenie `in` z `==`: `for x == lista:` → `SyntaxError`

---

## 7. Wzorzec akumulatora

**Akumulator** to zmienna, którą na początku ustawiasz na wartość neutralną,
a w pętli stopniowo "nakładasz" na nią wartości z listy.

**Licznik — ile elementów?**
```python
def policz(lista: list) -> int:
    licznik = 0          # wartość neutralna dla zliczania
    for _ in lista:      # _ zamiast zmiennej gdy nie używamy elementu
        licznik += 1     # += to skrót od: licznik = licznik + 1
    return licznik
```

**Suma — ile razem?**
```python
def suma(liczby: list[int]) -> int:
    suma = 0             # wartość neutralna dla sumowania
    for liczba in liczby:
        suma += liczba
    return suma
```

**Typowe błędy początkujących:**
- Inicjalizowanie akumulatora wewnątrz pętli (resetuje się przy każdym obrocie!) zamiast przed pętlą
- Zapomnienie `return` po pętli — funkcja zwróci `None`

---

## 8. Budowanie nowej listy w pętli

Często zamiast zliczać lub sumować, chcesz **zbudować nową listę** na podstawie starej:

```python
def podwoj(liczby: list[int]) -> list[int]:
    wynik = []                          # zaczynam od pustej listy
    for liczba in liczby:
        wynik.append(liczba * 2)        # dodaję przetworzoną wartość
    return wynik

podwoj([1, 2, 3])   # → [2, 4, 6]
```

**Typowe błędy początkujących:**
- Zwracanie `None` bo napisano `wynik.append(...)` i zapomnienie o `return wynik`
- Tworzenie listy `wynik` wewnątrz pętli — każdy obieg tworzyłby nową pustą listę

---

## 9. Filtrowanie — `for` + `if`

Łącząc pętlę z warunkiem `if`, możesz **wybierać** tylko te elementy, które spełniają kryterium:

```python
def tylko_parzyste(liczby: list[int]) -> list[int]:
    wynik = []
    for liczba in liczby:
        if liczba % 2 == 0:         # sprawdź warunek
            wynik.append(liczba)    # dodaj tylko gdy warunek True
    return wynik

tylko_parzyste([1, 2, 3, 4, 5])   # → [2, 4]
```

**Typowe błędy początkujących:**
- Wcięcie `return wynik` wewnątrz pętli (zwróci po pierwszym elemencie!) zamiast po zakończeniu pętli
- Brak wcięcia kodu pod `if` wewnątrz pętli

---

## 10. `enumerate` — numer + element razem

Gdy chcesz mieć jednocześnie **numer pozycji** i **wartość** elementu, użyj `enumerate`:

```python
imiona = ["Anna", "Piotr", "Zofia"]

for indeks, imie in enumerate(imiona):
    print(f"{indeks}: {imie}")

# wypisze:
# 0: Anna
# 1: Piotr
# 2: Zofia
```

Domyślnie liczy od 0. Żeby zacząć od 1, użyj `start=1`:

```python
for numer, imie in enumerate(imiona, start=1):
    print(f"{numer}. {imie}")

# wypisze:
# 1. Anna
# 2. Piotr
# 3. Zofia
```

**Schemat:** `for <zmienna_indeksu>, <zmienna_elementu> in enumerate(<lista>, start=<skąd_liczyć>):`

**Typowe błędy początkujących:**
- Pisanie `for indeks in enumerate(lista):` — dostaniesz parę `(0, "Anna")`, a nie sam element
- Zapomnienie o `start=1` gdy potrzebujesz numeracji od 1

---

## 11. `zip` — równoległa iteracja po dwóch listach

`zip` łączy dwie (lub więcej) listy w pary i pozwala iterować po nich równocześnie:

```python
imiona   = ["Anna", "Piotr", "Zofia"]
oceny    = [5, 4, 3]

for imie, ocena in zip(imiona, oceny):
    print(f"{imie}: {ocena}")

# wypisze:
# Anna: 5
# Piotr: 4
# Zofia: 3
```

**Schemat:** `for <zm1>, <zm2> in zip(<lista1>, <lista2>):`

Gdy listy mają różne długości, `zip` **zatrzymuje się przy krótszej**:
```python
zip([1, 2, 3], ["a", "b"])   # da tylko dwie pary: (1,"a"), (2,"b")
```

**Typowe błędy początkujących:**
- `for para in zip(a, b):` — dostaniesz krotkę `(1, "a")`, nie rozpakowane wartości
- Zakładanie że zip zachowuje "nadmiarowe" elementy dłuższej listy

---

## 12. List comprehension — skrócona budowa listy

**List comprehension** to elegancki skrót do budowania nowej listy w jednej linii.

Porównanie — zwykła pętla vs. comprehension:

```python
# Zwykła pętla
kwadraty = []
for x in [1, 2, 3, 4]:
    kwadraty.append(x ** 2)
# kwadraty = [1, 4, 9, 16]

# List comprehension — to samo w jednej linii
kwadraty = [x ** 2 for x in [1, 2, 3, 4]]
# kwadraty = [1, 4, 9, 16]
```

**Schemat:**
```
[<co_zrobić_z_elementem>  for  <element>  in  <lista>]
```

Czytaj od lewej: "zbuduj listę, w której każdy element to `x ** 2`, dla każdego `x` z listy".

**Typowe błędy początkujących:**
- Nawiasy okrągłe zamiast kwadratowych: `(x for x in lista)` — to generator, nie lista
- Zapomnienie słowa `for` w środku

---

## 13. List comprehension z warunkiem

Do list comprehension możesz dodać `if` na końcu, żeby **filtrować**:

```python
liczby = [1, 2, 3, 4, 5, 6]

# Tylko parzyste
parzyste = [x for x in liczby if x % 2 == 0]
# parzyste = [2, 4, 6]

# Tylko słowa krótsze niż 4 litery
slowa = ["ala", "pies", "kot", "słoń"]
krotkie = [s for s in slowa if len(s) < 4]
# krotkie = ["ala", "kot"]
```

**Schemat:**
```
[<wyrażenie>  for  <element>  in  <lista>  if  <warunek>]
```

**Typowe błędy początkujących:**
- Mylenie kolejności: `[x if warunek for x in lista]` → `SyntaxError`. Warunek zawsze **na końcu**.
- Używanie `elif` w comprehension — nie istnieje. Jeśli potrzebny `elif`, użyj zwykłej pętli.

---

## 14. Metoda `str.upper()` — wielkie litery

Każdy tekst (`str`) ma metodę `upper()`, która zwraca wersję z **wszystkimi wielkimi literami**:

```python
"python".upper()     # → "PYTHON"
"Anna".upper()       # → "ANNA"
"hello world".upper()# → "HELLO WORLD"
```

Wywołujesz przez kropkę: `tekst.upper()`.

Przydatne w list comprehension:
```python
slowa = ["ala", "bela", "cela"]
wielkie = [s.upper() for s in slowa]
# wielkie = ["ALA", "BELA", "CELA"]
```

**Typowe błędy początkujących:**
- `upper(slowo)` zamiast `slowo.upper()` — `upper` to metoda, nie funkcja wbudowana

---

## 15. Spirala — pojęcia z `funkcje_return_warunki`

Znasz już z poprzedniego tematu (`funkcje_return_warunki`):
- `if/elif/else` — działają tak samo **wewnątrz pętli**, łącząc filtrowanie z klasyfikacją
- `Optional[int]` i `return None` — gdy szukasz w liście elementu, który może nie istnieć,
  zwracasz `None` jako sygnał "nie znaleziono" (tak samo jak w funkcjach bez wyniku)
- `is None` — porównuj przez `is None`, nigdy `== None`

Przykład łączący oba tematy:

```python
from typing import Optional

def pierwsza_dorosla(wieki: list[int]) -> Optional[int]:
    for wiek in wieki:
        if wiek >= 18:       # ← if z poprzedniego tematu, użyty w pętli
            return wiek      # ← early return: znaleźliśmy, wyjdź od razu
    return None              # ← None jako sygnał: nic nie znaleziono
```

Nie tłumaczę tych pojęć od nowa — opierasz się na tym, co już wiesz.

---

## Podsumowanie — mapa pojęć

```python
lista = [1, 2, 3]                          # literał listy
len(lista)                                 # → 3, długość
lista[0]                                   # → 1, dostęp przez indeks

wynik = []                                 # pusta lista do budowania
wynik.append(element)                      # dodaj element na koniec

for element in lista:                      # iteruj po każdym elemencie
    ...

akumulator = 0
for x in lista:
    akumulator += x                        # wzorzec sumy/licznika

for indeks, element in enumerate(lista, start=1):  # z numerem od 1
    ...

for a, b in zip(lista1, lista2):           # dwie listy równocześnie
    ...

[x * 2 for x in lista]                    # list comprehension
[x for x in lista if x > 0]              # list comprehension z filtrem

"tekst".upper()                            # → "TEKST"
```
