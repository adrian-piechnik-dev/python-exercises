# Słowniki w Pythonie: dict, dostęp, iteracja, budowanie

---

## 1. Co to jest słownik?

Wyobraź sobie prawdziwy słownik: szukasz słowo "pies" i znajdujesz "dog".
Słownik w Pythonie działa tak samo — łączy **klucz** z **wartością**.

```python
tlumaczenie = {"pies": "dog", "kot": "cat", "ryba": "fish"}
#               ↑ klucz        ↑ wartość
```

Każdy klucz musi być **unikalny** — nie możesz mieć dwóch wpisów "pies".
Wartości mogą się powtarzać.

Słownik to niezastąpione narzędzie gdy masz dane parowane: imię→wiek, produkt→cena, słowo→liczba wystąpień.

**Typowe błędy początkujących:**
- Mylenie z listą: lista to `[1, 2, 3]` (nawiasy kwadratowe, brak kluczy), słownik to `{"a": 1}` (nawiasy klamrowe, klucz: wartość)
- Brak dwukropka: `{"pies" "dog"}` → `SyntaxError`

---

## 2. Tworzenie słownika

```python
pusty = {}                               # pusty słownik
oceny = {"Anna": 5, "Piotr": 4}         # dwa wpisy od razu
ceny  = {"jabłko": 2.50, "banan": 1.20} # klucze: str, wartości: float
```

Kolejność wpisów jest zapamiętana (od Pythona 3.7+).

---

## 3. Dostęp przez klucz — `d["klucz"]`

```python
oceny = {"Anna": 5, "Piotr": 4}

oceny["Anna"]   # → 5
oceny["Piotr"]  # → 4
```

Schemat: `slownik["klucz"]`

**Uwaga:** jeśli klucz nie istnieje, Python rzuca `KeyError`:
```python
oceny["Zofia"]  # → KeyError: 'Zofia'
```

**Typowe błędy początkujących:**
- Używanie `slownik[0]` jak przy liście — słownik nie ma indeksów numerycznych (chyba że klucz to liczba)
- Brak cudzysłowów dla kluczy tekstowych: `oceny[Anna]` → `NameError`

---

## 4. Bezpieczny dostęp — `.get()`

`.get()` nie rzuca błędu gdy klucz nie istnieje — zwraca `None` lub wartość domyślną:

```python
oceny = {"Anna": 5, "Piotr": 4}

oceny.get("Anna")       # → 5    (klucz istnieje)
oceny.get("Zofia")      # → None (klucz nie istnieje, domyślnie None)
oceny.get("Zofia", 0)   # → 0    (klucz nie istnieje, zwróć 0)
```

Schemat: `slownik.get(klucz, wartosc_domyslna)`

Używaj `.get()` gdy nie masz pewności czy klucz istnieje.

**Typowe błędy początkujących:**
- Drugi argument `.get()` to wartość *zwracana*, a nie wstawiana do słownika

---

## 5. Sprawdzanie klucza — `in`

Operator `in` sprawdza czy klucz istnieje w słowniku:

```python
oceny = {"Anna": 5, "Piotr": 4}

"Anna" in oceny       # → True
"Zofia" in oceny      # → False
"Zofia" not in oceny  # → True
```

Schemat: `klucz in slownik` → `bool`

**Typowe błędy początkujących:**
- `"5" in oceny` sprawdza klucze, nie wartości — żeby sprawdzić wartości: `5 in oceny.values()`

---

## 6. Dodawanie i aktualizacja wpisów

Dodaj nowy klucz lub nadpisz istniejący przez przypisanie:

```python
oceny = {"Anna": 5}

oceny["Piotr"] = 4   # dodaje nowy klucz "Piotr"
oceny["Anna"]  = 3   # nadpisuje istniejący klucz "Anna"

# teraz: {"Anna": 3, "Piotr": 4}
```

Nie ma osobnej metody "add" — przypisanie tworzy lub nadpisuje.

---

## 7. Iteracja po kluczach

Domyślna iteracja po słowniku przechodzi po kluczach:

```python
oceny = {"Anna": 5, "Piotr": 4, "Zofia": 3}

for imie in oceny:
    print(imie)

# wypisze: Anna  Piotr  Zofia
```

To samo co `for imie in oceny.keys()`.

---

## 8. `.keys()`, `.values()`, `.items()`

Trzy metody do wyboru co chcesz przeglądać:

```python
oceny = {"Anna": 5, "Piotr": 4}

oceny.keys()    # → dict_keys(["Anna", "Piotr"])             — same klucze
oceny.values()  # → dict_values([5, 4])                      — same wartości
oceny.items()   # → dict_items([("Anna", 5), ("Piotr", 4)])  — pary
```

Żeby dostać listę, owiń w `list()`:
```python
list(oceny.keys())    # → ["Anna", "Piotr"]
list(oceny.values())  # → [5, 4]
```

Najczęściej przydatne `.items()` — daje dostęp do klucza i wartości jednocześnie:

```python
for imie, ocena in oceny.items():
    print(f"{imie}: {ocena}")

# wypisze:
# Anna: 5
# Piotr: 4
```

**Typowe błędy początkujących:**
- `for wpis in oceny.items():` — dostaniesz krotkę `("Anna", 5)`, nie rozpakowane wartości
- Modyfikowanie słownika podczas iteracji po nim → `RuntimeError`

---

## 9. Budowanie słownika w pętli

Wzorzec: zaczynam od pustego słownika, w pętli dodaję wpisy:

```python
def policz_dlugosci(slowa: list[str]) -> dict[str, int]:
    wynik = {}
    for slowo in slowa:
        wynik[slowo] = len(slowo)
    return wynik

policz_dlugosci(["ala", "pies"])   # → {"ala": 3, "pies": 4}
```

**Wzorzec akumulatora dla zliczania** (ile razy słowo wystąpiło):

```python
def zlicz(slowa: list[str]) -> dict[str, int]:
    licznik = {}
    for slowo in slowa:
        if slowo in licznik:
            licznik[slowo] += 1   # zwiększ istniejący
        else:
            licznik[slowo] = 1    # utwórz nowy wpis
    return licznik

zlicz(["pies", "kot", "pies"])   # → {"pies": 2, "kot": 1}
```

---

## 10. Type hint dla słownika — `dict[str, int]`

```python
def zadanie(oceny: dict[str, int]) -> dict[str, int]:
    ...
```

- `dict[str, int]` — klucze tekstowe, wartości całkowite
- `dict[str, str]` — klucze i wartości tekstowe
- `dict[str, list[int]]` — wartości to listy liczb

---

## 11. Spirala — pojęcia z `listy_petle`

Znasz już z poprzedniego tematu (`listy_petle`):
- `zip(klucze, wartosci)` — idealne do budowania słownika z dwóch list jednocześnie
- list comprehension `[... for ... in ...]` — działa też na `.items()`, np. do filtrowania kluczy

Nie tłumaczę tych pojęć od nowa — opierasz się na tym, co już wiesz.

Przykład z `zip`:
```python
imiona      = ["Anna", "Piotr", "Zofia"]
oceny_lista = [5, 4, 3]

slownik = {}
for imie, ocena in zip(imiona, oceny_lista):   # ← zip z listy_petle
    slownik[imie] = ocena

# → {"Anna": 5, "Piotr": 4, "Zofia": 3}
```

Przykład z list comprehension na `.items()`:
```python
oceny = {"Anna": 5, "Piotr": 4, "Zofia": 3}

prymusi = [imie for imie, ocena in oceny.items() if ocena == 5]
# → ["Anna"]
```

---

## Podsumowanie — mapa pojęć

```python
d = {"klucz": wartosc}           # literał słownika
d = {}                            # pusty słownik

d["klucz"]                        # dostęp — KeyError gdy brak
d.get("klucz", domyslna)          # bezpieczny dostęp
"klucz" in d                      # True / False — czy istnieje
d["klucz"] = nowa_wartosc         # dodaj lub nadpisz

for k in d:                       # iteracja po kluczach
for v in d.values():              # iteracja po wartościach
for k, v in d.items():            # iteracja po parach (klucz, wartość)

list(d.keys())                    # → lista kluczy
list(d.values())                  # → lista wartości

wynik = {}
for ... in ...:
    wynik[k] = v                  # budowanie słownika w pętli

[k for k, v in d.items() if v > 3]   # list comprehension na .items()
```
