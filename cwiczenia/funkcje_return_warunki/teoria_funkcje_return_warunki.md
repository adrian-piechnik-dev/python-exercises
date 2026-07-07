# Funkcje w Pythonie: return vs print, warunki, early return, kontrakt funkcji, None

---

## 1. Co to jest funkcja?

Wyobraź sobie automat z kawą. Wrzucasz monetę i wciskasz guzik z napisem "Cappuccino"
(to są **argumenty** — dane, które dajesz maszynie). Automat pracuje w środku — mieli ziarna,
grzeje wodę — a na końcu wysuwa kubek z kawą (to jest **wynik**, który dostajesz z powrotem).
Ciebie nie interesuje jak dokładnie działa środek maszyny. Interesuje cię tylko: *daję X, dostaję Y*.

Funkcja w Pythonie działa dokładnie tak:

```python
def zrob_kawe(rodzaj: str) -> str:
    wynik = "Twoja kawa: " + rodzaj
    return wynik
```

Możesz jej użyć tak:

```python
kawa = zrob_kawe("cappuccino")
print(kawa)   # wypisze: Twoja kawa: cappuccino
```

### Rozbicie nagłówka funkcji na kawałki:

```
def          — słowo kluczowe "definiuję nową funkcję"
zrob_kawe    — nazwa funkcji (sam ją wymyślasz)
(rodzaj: str)  — parametr: nazwa + dwukropek + typ (to jest type hint)
-> str       — strzałka + typ: co funkcja zwróci
:            — dwukropek kończący nagłówek (obowiązkowy!)
    wynik = ... — ciało funkcji — wcięte o 4 spacje (obowiązkowe!)
    return wynik — słowo kluczowe "zwróć tę wartość"
```

**Zasada PEP 8 — nazwy funkcji:** małe litery, słowa oddzielone podkreśleniem.
`zrob_kawe` — poprawnie. `ZrobKawe` — to styl dla klas, nie funkcji.

**Typowe błędy początkujących:**
- Brak dwukropka na końcu nagłówka → `SyntaxError`
- Brak wcięcia (4 spacje) w ciele funkcji → `IndentationError`
- Nazwa funkcji z wielkich liter (`ZrobKawe`) — działa, ale łamie PEP 8

---

## 2. `return` — oddanie wyniku przez funkcję

`return` to jak kelner, który przynosi zamówione danie do twojego stolika.
Funkcja wykonuje pracę, a na końcu **zwraca** wynik — oddaje go temu, kto ją wywołał.

```python
def dodaj(a: int, b: int) -> int:
    wynik = a + b
    return wynik
```

Używasz tej funkcji:

```python
suma = dodaj(3, 5)   # suma = 8
print(suma)          # wypisze: 8
print(suma * 2)      # wypisze: 16  — możesz używać wyniku dalej!
```

**Ważna zasada:** Po wykonaniu `return` funkcja **natychmiast kończy działanie**.
Żaden kod poniżej `return` (w tej samej gałęzi) się nie wykona.

```python
def przykład() -> int:
    return 42
    print("Ten kod nigdy się nie wykona")   # martwy kod
```

**Typowe błędy początkujących:**
- Myślenie że `return` wypisuje coś na ekran — NIE, to robi `print()`
- Pisanie kodu po `return` — nie wykona się, edytor zwykle to podkreśla

---

## 3. `print()` vs `return` — najważniejsza różnica

To jest NAJCZĘSTSZY błąd początkujących w całym Pythonie. Zapamiętaj na zawsze:

| `print()`                             | `return`                             |
|---------------------------------------|--------------------------------------|
| Wyświetla tekst na ekranie            | Zwraca wartość do miejsca wywołania  |
| Wynik "znika" — nie można go użyć    | Wynik można przypisać do zmiennej    |
| Nie kończy funkcji                    | Kończy funkcję natychmiast           |

**Przykład — różnica w praktyce:**

```python
# ŹLE — używa print zamiast return
def dodaj_zle(a: int, b: int) -> None:
    print(a + b)       # wyświetla "8" na ekranie, ale nic nie zwraca

# DOBRZE — używa return
def dodaj_dobrze(a: int, b: int) -> int:
    return a + b       # zwraca wartość 8
```

Teraz spróbuj użyć obu:

```python
wynik_zle    = dodaj_zle(3, 5)    # na ekranie pojawi się "8", ale wynik_zle = None
wynik_dobrze = dodaj_dobrze(3, 5) # wynik_dobrze = 8

print(wynik_dobrze + 10)  # 18 — działa!
print(wynik_zle + 10)     # BŁĄD: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

**Analogia:** `print()` to głośnik — ogłasza wynik na sali, ale nikt go nie "trzyma w rękach".
`return` to ręka podająca ci wynik — możesz go wziąć i użyć.

**Kiedy używać `print`:** gdy chcesz coś wyświetlić użytkownikowi lub debugować.
**Kiedy używać `return`:** prawie zawsze, gdy funkcja coś oblicza — zwróć wynik!

**Typowe błędy początkujących:**
- Pisanie `print(wynik)` na końcu funkcji zamiast `return wynik`
- Pisanie `return print(wynik)` — `print()` zwraca `None`, więc funkcja też zwróci `None`
- Myślenie "przecież widzę wynik na ekranie, więc wszystko gra" — widzisz, ale nie możesz użyć

---

## 4. Type hinty — kontrakt funkcji

Type hint (dosł. "wskazówka typów") to **umowa**, którą składasz użytkownikom swojej funkcji.
Mówisz: "daj mi dwie liczby całkowite, a ja zwrócę ci tekst".

```python
def powitaj(imie: str, wiek: int) -> str:
    return f"Cześć {imie}, masz {wiek} lat!"
```

- `imie: str` — parametr `imie` powinien być tekstem (`str`)
- `wiek: int` — parametr `wiek` powinien być liczbą całkowitą (`int`)
- `-> str` — funkcja zwraca tekst (`str`)

**Podstawowe typy:**

| Typ     | Co oznacza                          | Przykłady                |
|---------|-------------------------------------|--------------------------|
| `int`   | liczba całkowita                    | `0`, `-5`, `100`, `42`   |
| `float` | liczba z częścią dziesiętną         | `3.14`, `-0.5`, `1.0`    |
| `str`   | tekst (string)                      | `"cześć"`, `"Python"`    |
| `bool`  | wartość logiczna (prawda/fałsz)     | `True`, `False`          |
| `None`  | brak wartości                       | `None`                   |

Python **nie blokuje** programu gdy wpiszesz zły typ, ale:
- Edytor (VS Code, PyCharm) podkreśli błąd z wyprzedzeniem
- Inni programiści od razu wiedzą jak używać funkcji
- Ty sam po miesiącu przerwy przypomnisz sobie co funkcja robi

**Typowe błędy początkujących:**
- Brak type hintów — kod działa, ale jest trudniejszy do czytania
- Pisanie `-> str:` z dwukropkiem zamiast `-> str:` — tu dwukropek jest OK, jest końcem nagłówka
- Mylenie `int` z `float`: `1` to `int`, `1.0` to `float`

---

## 5. f-stringi — wklejanie zmiennych do tekstu

f-string to wygodny sposób na tworzenie tekstu z wartościami zmiennych.
Przed cudzysłowem piszesz literę `f`, a wewnątrz tekstu używasz `{}` do wstawiania wartości:

```python
imie = "Anna"
wiek = 25
tekst = f"Cześć, {imie}! Masz {wiek} lat."
# wynik: "Cześć, Anna! Masz 25 lat."
```

W klamrach `{}` możesz wstawić zmienną lub proste wyrażenie:

```python
a = 3
b = 5
info = f"Suma {a} + {b} = {a + b}"
# wynik: "Suma 3 + 5 = 8"
```

**Typowe błędy początkujących:**
- Zapomnienie litery `f` przed cudzysłowem — klamry staną się zwykłym tekstem: `"{imie}"` zamiast wartości
- Literówka w nazwie zmiennej w klamrach → `NameError: name 'imię' is not defined`

---

## 6. Operatory arytmetyczne

Python wykonuje podstawowe działania matematyczne:

| Operator | Znaczenie              | Przykład       | Wynik   |
|----------|------------------------|----------------|---------|
| `+`      | dodawanie              | `3 + 2`        | `5`     |
| `-`      | odejmowanie            | `5 - 2`        | `3`     |
| `*`      | mnożenie               | `4 * 3`        | `12`    |
| `/`      | dzielenie              | `10 / 4`       | `2.5`   |
| `%`      | reszta z dzielenia     | `7 % 3`        | `1`     |
| `**`     | potęgowanie            | `2 ** 3`       | `8`     |

**Uwaga:** Dzielenie `/` zawsze zwraca `float` (`10 / 2` to `5.0`, nie `5`).

**Operator `%` — modulo (reszta z dzielenia):**
Przydaje się do sprawdzania parzystości:
```python
4 % 2   # → 0  (4 dzieli się przez 2 bez reszty → parzysta)
5 % 2   # → 1  (reszta 1 → nieparzysta)
7 % 3   # → 1  (7 = 2*3 + 1, reszta to 1)
```

**Operator `**` — potęgowanie:**
```python
2 ** 3       # → 8    (2 do potęgi 3)
1.75 ** 2    # → 3.0625  (1.75 do kwadratu)
9 ** 0.5     # → 3.0  (pierwiastek = potęga 0.5)
```

**Typowe błędy początkujących:**
- Pisanie `^` zamiast `**` do potęgowania — w Pythonie `^` to zupełnie inna operacja (XOR bitowy)!
- Zapominanie że `/` zwraca float: `5 / 2` to `2.5`, nie `2`

---

## 7. Wartości logiczne: `True` i `False`

Typ `bool` ma dokładnie dwie wartości: `True` (prawda) i `False` (fałsz).
Wielka litera na początku jest obowiązkowa.

```python
jest_dorosly = True
pada_deszcz  = False
```

Funkcje często zwracają `True` lub `False`:

```python
def jest_parzysta(liczba: int) -> bool:
    if liczba % 2 == 0:
        return True
    else:
        return False
```

**Zasada PEP 8:** Sprawdzaj wartości logiczne przez `is True` / `is False`,
a najlepiej bezpośrednio bez porównania:

```python
wynik = jest_parzysta(4)

if wynik is True:      # OK, PEP 8
    print("parzysta")

if wynik:              # jeszcze lepiej — bezpośrednie użycie
    print("parzysta")

if wynik == True:      # działa, ale PEP 8 mówi: nie rób tak
    print("parzysta")
```

**Typowe błędy początkujących:**
- Pisanie `true` lub `TRUE` z małej litery → `NameError` (Python jest case-sensitive)
- Porównywanie przez `== True` zamiast `is True` lub bezpośrednio

---

## 8. Operatory porównania

Porównują dwie wartości i zwracają `True` lub `False`:

| Operator | Znaczenie              | Przykład     | Wynik   |
|----------|------------------------|--------------|---------|
| `==`     | równe                  | `5 == 5`     | `True`  |
| `!=`     | różne                  | `5 != 3`     | `True`  |
| `<`      | mniejsze               | `3 < 5`      | `True`  |
| `>`      | większe                | `5 > 3`      | `True`  |
| `<=`     | mniejsze lub równe     | `3 <= 3`     | `True`  |
| `>=`     | większe lub równe      | `5 >= 6`     | `False` |

```python
wynik = 10 > 5     # wynik = True
wynik = 10 == 10   # wynik = True
wynik = 10 != 10   # wynik = False
```

**Typowe błędy początkujących:**
- Mylenie `=` (przypisanie wartości do zmiennej) z `==` (porównanie):
  `if x = 5:` → `SyntaxError` — zamiast tego musisz napisać `if x == 5:`
- Porównywanie tekstu z liczbą: `"5" == 5` → zawsze `False` (to różne typy!)

---

## 9. Instrukcja warunkowa `if`

`if` (po angielsku "jeśli") pozwala wykonać kod tylko wtedy, gdy warunek jest spełniony.

```python
def sprawdz_haslo(haslo: str) -> str:
    if haslo == "tajne":
        return "Witaj!"
    return "Brak dostępu"
```

Schemat:
```
if <warunek>:
    <kod do wykonania gdy warunek jest True>
```

Wcięcie (4 spacje) mówi Pythonowi: "ten kod należy do bloku if".

```python
wiek = 20
if wiek >= 18:
    print("Dorosły")   # wykona się, bo 20 >= 18 → True
print("Zawsze to widzę")  # wykona się zawsze (brak wcięcia = poza if)
```

**Typowe błędy początkujących:**
- Brak dwukropka po warunku → `SyntaxError`
- Brak wcięcia w ciele `if` → `IndentationError`
- `if wiek = 18:` (jedno `=`) zamiast `if wiek == 18:` → `SyntaxError`

---

## 10. `if` / `else` — dwa wyjścia

`else` (po angielsku "w przeciwnym razie") obsługuje przypadek gdy `if` jest fałszywy:

```python
def parzysta_czy_nie(liczba: int) -> str:
    if liczba % 2 == 0:
        return "parzysta"
    else:
        return "nieparzysta"
```

Schemat:
```
if <warunek>:
    <kod gdy True>
else:
    <kod gdy False>
```

**Ważne:** `else` nigdy nie przyjmuje warunku — to po prostu "w każdym innym przypadku".

**Typowe błędy początkujących:**
- Złe wcięcie `else` — musi być na tym samym poziomie co `if`
- Pisanie `else(warunek):` — `else` nie przyjmuje warunku, od tego jest `elif`

---

## 11. `if` / `elif` / `else` — wiele wyjść

Gdy masz więcej niż dwa przypadki, używasz `elif` (skrót od "else if" — "a może"):

```python
def opis_wyniku(procent: int) -> str:
    if procent >= 90:
        return "Świetnie!"
    elif procent >= 60:
        return "Dobrze"
    elif procent >= 40:
        return "Przeciętnie"
    else:
        return "Słabo"
```

Python sprawdza warunki **od góry w dół** i zatrzymuje się przy **pierwszym spełnionym**.
Gdy `procent = 95`:
1. `95 >= 90` → `True` → zwraca `"Świetnie!"` → **koniec, reszta się nie sprawdza**

Gdyby warunki były odwrotnie (od najmniejszego):

```python
# ŹLE — kolejność warunków jest zepsuta
def opis_zle(procent: int) -> str:
    if procent >= 40:     # 95 >= 40 → True → od razu zwróci "Przeciętnie"!
        return "Przeciętnie"
    elif procent >= 60:   # to się nigdy nie sprawdzi dla >= 40
        return "Dobrze"
```

Schemat:
```
if <warunek1>:
    <kod1>
elif <warunek2>:
    <kod2>
elif <warunek3>:
    <kod3>
else:
    <kod domyślny gdy żaden warunek nie pasuje>
```

**Typowe błędy początkujących:**
- Pisanie `else if` zamiast `elif` → `SyntaxError`
- Zła kolejność warunków — bardziej szczegółowe warunki idą WYŻEJ (najpierw `>= 90`, potem `>= 60`)
- Brak `else` gdy istnieje przypadek niepokryty żadnym `elif` → funkcja zwróci `None` bez wiedzy o tym

---

## 12. Operatory logiczne: `and`, `or`, `not`

Pozwalają łączyć kilka warunków w jeden:

| Operator | Znaczenie                            | Przykład                   | Wynik   |
|----------|--------------------------------------|----------------------------|---------|
| `and`    | oba warunki muszą być `True`         | `5 > 3 and 2 < 4`          | `True`  |
| `or`     | przynajmniej jeden musi być `True`   | `5 < 3 or 2 < 4`           | `True`  |
| `not`    | odwraca wartość logiczną             | `not True`                 | `False` |

```python
def kwalifikuje_do_przetargu(wiek: int, wzrost: int) -> bool:
    if wiek >= 18 and wzrost >= 160:
        return True
    return False
```

```python
def wymaga_uwagi(temperatura: float, cisnienie: float) -> bool:
    if temperatura > 38.0 or cisnienie > 140:
        return True
    return False
```

**Ważne:** Każdy warunek po `and` / `or` musi być **kompletny**:

```python
# ŹLE
if wiek >= 18 and <= 65:         # błąd — Python nie wie czego <= 65 dotyczy

# DOBRZE
if wiek >= 18 and wiek <= 65:    # oba warunki są kompletne
```

**Typowe błędy początkujących:**
- Pisanie `&&` zamiast `and` (składnia z C/Java/JavaScript) → `SyntaxError`
- Pisanie `||` zamiast `or` → `SyntaxError`
- Niekompletny warunek: `if wiek >= 18 and <= 65:` → `SyntaxError`

---

## 13. `None` — brak wartości

`None` to specjalna wartość Pythona oznaczająca "nic", "brak odpowiedzi", "nie wiem".

**Analogia:** Zamówiłeś w restauracji "zupę dnia". Kelner wraca i mówi: "przykro mi,
zupa się skończyła." Nie dostałeś zupy — dostałeś odpowiedź "brak". To właśnie `None`.

```python
wynik = None
print(wynik)          # None
print(type(wynik))    # <class 'NoneType'>
```

**Kiedy funkcja zwraca `None`:**

1. Gdy dane wejściowe są nieprawidłowe i funkcja nie może wykonać pracy
2. Gdy szukany element nie istnieje

```python
def znajdz_dzien(numer: int) -> ...:
    if numer == 1:
        return "poniedziałek"
    elif numer == 2:
        return "wtorek"
    # ... itd.
    else:
        return None   # numer spoza zakresu 1–7 — brak odpowiedzi
```

**Sprawdzanie czy wartość to `None`:**

```python
wynik = znajdz_dzien(99)

if wynik is None:       # DOBRZE — PEP 8
    print("Nieznany dzień")

if wynik == None:       # ŹLE — działa, ale PEP 8 mówi: używaj is
    print("Nieznany dzień")
```

Zasada: **zawsze `is None`, nigdy `== None`**.

**Typowe błędy początkujących:**
- Używanie `== None` zamiast `is None`
- Zwracanie stringa jako błędu: `return "błąd"` lub `return "nie znaleziono"` — to zły wzorzec!
  Przy `None` sprawdzasz jednym `is None`, a przy stringach musiałbyś porównywać treść.
- Ignorowanie `None`: używanie wyniku funkcji bez sprawdzenia → program może crashować

---

## 14. `Optional` — type hint dla "X lub `None`"

Gdy funkcja może zwrócić wartość **albo** `None`, używamy `Optional`:

```python
from typing import Optional

def znajdz_dzien(numer: int) -> Optional[str]:
    if numer == 1:
        return "poniedziałek"
    return None
```

`Optional[str]` czyta się jako: "ta funkcja zwraca `str` **albo** `None`".

Importujesz `Optional` z wbudowanego modułu `typing`:

```python
from typing import Optional   # ten import idzie na górze pliku
```

Inne przykłady:
- `Optional[int]` — zwraca `int` albo `None`
- `Optional[float]` — zwraca `float` albo `None`
- `Optional[bool]` — zwraca `bool` albo `None`

**Typowe błędy początkujących:**
- Zapomnienie o `from typing import Optional` → `NameError: name 'Optional' is not defined`
- Pisanie `Optional(str)` z nawiasami okrągłymi zamiast `Optional[str]` z kwadratowymi → `TypeError`

---

## 15. Early return — wychodzenie z funkcji jak najwcześniej

**Early return** (dosł. "wczesny powrót") to technika polegająca na tym, że wychodzimy z funkcji
natychmiast gdy wiemy, że nie możemy lub nie powinniśmy dalej pracować (np. dane są nieprawidłowe).

**Bez early return — kod się zagnieżdża:**

```python
def oblicz_rabat(cena: float, czy_vip: bool) -> Optional[float]:
    if cena > 0:
        if czy_vip:
            return cena * 0.8
        else:
            return cena
    else:
        return None
```

**Z early return — czytelniej i płasko:**

```python
def oblicz_rabat(cena: float, czy_vip: bool) -> Optional[float]:
    if cena <= 0:
        return None          # ← early return: od razu wychodzimy

    if czy_vip:
        return cena * 0.8   # ← early return: mamy wynik dla VIP
    return cena              # ← normalna ścieżka
```

**Wzorzec early return:**
1. Na początku funkcji sprawdź czy dane są prawidłowe
2. Jeśli nie — zwróć `None` (lub rzuć wyjątek) i wyjdź
3. Resztę funkcji pisz bez zagnieżdżania `if`-ów

**Typowe błędy początkujących:**
- Zagnieżdżanie wielu `if` w sobie — zamiast tego: early return na początku
- Pisanie kodu po early return (nie wykona się — to martwy kod)
- Zapomnienie early return → funkcja może crashować na złych danych

---

## Podsumowanie — mapa pojęć

```python
from typing import Optional   # import na górze pliku

def nazwa(param: Typ) -> TypZwracany:    # nagłówek: def, name, hints
    if warunek_niepoprawnydanych:        # early return: sprawdź błąd
        return None                      # sygnał braku wartości

    if warunek1:                         # if/elif/else: wiele ścieżek
        return wynik1
    elif warunek2:
        return wynik2
    else:
        return wynik_domyslny

# return → zwraca wartość (użyj zawsze gdy coś obliczasz)
# print() → wyświetla na ekranie (nie zwraca wartości)
# None → brak wartości (sprawdzaj przez: if wynik is None)
# Optional[Typ] → Typ albo None (type hint)
```
