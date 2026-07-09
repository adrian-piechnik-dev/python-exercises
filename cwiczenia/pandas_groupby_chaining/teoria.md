# pandas — groupby, agg, assign, method chaining

> Z tematu 8 znasz już filtrowanie boolean (`df[df["col"] > x]`). W tym temacie
> nauczysz się grupować dane po kategoriach, agregować wyniki i łączyć wiele
> operacji w jeden płynny łańcuch bez zmiennych pośrednich.

---

## .groupby() — dzielenie danych na grupy

Wyobraź sobie, że masz listę uczniów z różnych klas. Chcesz dowiedzieć się,
ile osób jest w każdej klasie albo jaka jest średnia ocena w każdej klasie.
`.groupby()` robi dokładnie to: dzieli tabelę na grupy według wartości w wybranej kolumnie.

```python
import pandas as pd

df = pd.DataFrame({
    "imie":          ["Anna", "Piotr", "Zofia", "Marek", "Ewa"],
    "miasto":        ["Warszawa", "Krakow", "Warszawa", "Krakow", "Warszawa"],
    "wiek":          [20, 30, 40, 25, 35],
    "wynagrodzenie": [3000, 4000, 5000, 3500, 4500],
})
```

Grupowanie samo w sobie nic nie liczy — dopiero wywołana po nim metoda daje wynik.

---

## .size() — COUNT: ile rekordów w każdej grupie

```python
wynik = df.groupby("miasto").size()
```

Wynik to **Series** z nazwami grup jako indeksem i liczbą wierszy jako wartościami:

```
miasto
Krakow      2
Warszawa    3
dtype: int64
```

Dostęp do wartości konkretnej grupy:
```python
wynik["Warszawa"]   # 3
wynik["Krakow"]     # 2
```

### Typowe błędy — .size()
- Mylenie `.size()` z `.count()` — `.size()` liczy wszystkie wiersze (też z NaN),
  `.count()` liczy tylko niepuste wartości w kolumnie. Dla kompletnych danych wyniki są takie same.

---

## [kolumna].sum() i .mean() — SUM i AVG po grupach

Dodajesz wybór kolumny **między** `groupby` a metodą agregacji:

```python
# SUM po grupach
wynik_suma = df.groupby("miasto")["wiek"].sum()
# Warszawa: 20+40+35=95, Krakow: 30+25=55

# AVG po grupach
wynik_srednia = df.groupby("miasto")["wiek"].mean()
# Warszawa: 95/3 ≈ 31.67, Krakow: 55/2 = 27.5
```

Oba wywołania zwracają **Series** (tak samo jak `.size()`).

```python
wynik_suma["Warszawa"]    # 95
wynik_srednia["Krakow"]   # 27.5
```

### Typowe błędy — .sum()/.mean()
- Brak `["kolumna"]` przed `.sum()` — `df.groupby("miasto").sum()` działa, ale sumuje
  WSZYSTKIE kolumny numeryczne naraz i zwraca DataFrame, nie Series.

---

## .agg() — elastyczna agregacja

`.agg()` to uogólniona wersja agregatów. Zamiast jednej metody dostajesz słownik
z instrukcją: „dla tej kolumny użyj tej funkcji".

### Jedna kolumna, jedna funkcja → DataFrame

```python
wynik = df.groupby("miasto").agg({"wiek": "sum"})
```

Wynik to **DataFrame** (nie Series!) z „miasto" jako indeksem i „wiek" jako kolumną:

```
          wiek
miasto
Krakow      55
Warszawa    95
```

Dostęp do wartości:
```python
wynik["wiek"]["Warszawa"]   # 95
wynik["wiek"]["Krakow"]     # 55
```

Dostępne funkcje agregujące jako string: `"sum"`, `"mean"`, `"count"`.

### Wiele kolumn, różne funkcje → DataFrame

```python
wynik = df.groupby("miasto").agg({
    "wiek":          "sum",
    "wynagrodzenie": "mean",
})
```

Wynik ma dwie kolumny — jedną per klucz słownika:

```python
wynik["wiek"]["Warszawa"]           # 95
wynik["wynagrodzenie"]["Krakow"]    # 3750.0
```

### Typowe błędy — .agg()
- `.agg("sum")` zamiast `.agg({"kolumna": "sum"})` — forma bez słownika sumuje
  wszystkie kolumny numeryczne; do precyzyjnej kontroli zawsze podawaj słownik.
- `wynik.loc["Warszawa"]["wiek"]` i `wynik["wiek"]["Warszawa"]` — obie formy działają;
  druga jest bardziej naturalna przy dostępie przez nazwę kolumny.

---

## .assign() — dodawanie kolumny przez łańcuch

`.assign()` przyjmuje nazwaną wartość lub lambda i **zwraca nowy DataFrame**
z dołączoną kolumną. Oryginał pozostaje niezmieniony.

### Stała wartość

```python
wynik = df.assign(region="Europa")
# nowa kolumna "region" z wartością "Europa" w każdym wierszu
```

```python
wynik["region"].tolist()   # ["Europa", "Europa", "Europa", "Europa", "Europa"]
```

### Lambda — wartość obliczona z istniejącej kolumny

```python
wynik = df.assign(premia=lambda d: d["wynagrodzenie"] * 0.1)
```

Wewnątrz lambdy `d` to **bieżący DataFrame** (to ważne w łańcuchu — lambda zawsze
dostaje aktualny stan, nie oryginalny `df`).

```python
wynik["premia"].tolist()   # [300.0, 400.0, 500.0, 350.0, 450.0]
```

### Typowe błędy — .assign()
- `df["nowa"] = wartosc` zamiast `df.assign(nowa=wartosc)` — forma z `=` modyfikuje
  oryginał (efekt uboczny). `.assign()` jest bezpieczne w łańcuchu bo zawsze
  zwraca nowy DataFrame.
- Użycie `df["kolumna"]` w lambdzie zamiast `d["kolumna"]` — `df` to zewnętrzna
  zmienna; `d` w lambdzie to bieżący DataFrame w łańcuchu. W prostych przypadkach
  efekt ten sam, ale `d` jest poprawnym i bezpiecznym wzorcem.

---

## Method chaining — łańcuch metod

Zamiast zapisywać wyniki do wielu zmiennych pośrednich, możesz łączyć wywołania
w jeden płynny łańcuch. Każda metoda zwraca nowy obiekt, na którym od razu
wywołujesz następną.

**Bez łańcucha:**
```python
krok1 = df.assign(premia=lambda d: d["wynagrodzenie"] * 0.1)
krok2 = krok1.groupby("miasto")["premia"]
wynik = krok2.sum()
```

**Z łańcuchem:**
```python
wynik = (
    df
    .assign(premia=lambda d: d["wynagrodzenie"] * 0.1)
    .groupby("miasto")["premia"]
    .sum()
)
```

Nawiasy zewnętrzne `(...)` pozwalają rozłożyć łańcuch na wiele linii bez
konieczności używania backslasha `\`. To konwencja PEP 8 dla długich wyrażeń.

Każda linia wewnątrz to kolejny krok transformacji. Czytasz od góry do dołu
jak przepis: „weź df → dodaj kolumnę premia → zgrupuj po mieście → zsumuj".

### Typowe błędy — method chaining
- Nie zwijanie nawiasów przy wieloliniowym łańcuchu — `SyntaxError`. Zawsze owijaj
  w `(...)` gdy rozpisujesz na kilka linii.
- Modyfikowanie `df` wewnątrz lambdy zamiast `d` — może dawać nieoczekiwane wyniki
  gdy df zmienia się między krokami łańcucha.

---

## .copy() w łańcuchu

Jeśli zaczynasz łańcuch od `.copy()`, masz pewność, że żadna operacja w dalszej
części nie dotknie oryginalnego DataFrame:

```python
wynik = (
    df
    .copy()
    .assign(region="Europa")
    .groupby("miasto")
    .size()
)
# df jest niezmieniony; wynik to Series
```

Kiedy używać `.copy()` w łańcuchu: gdy masz wątpliwości, czy któraś z kolejnych
operacji może zmutować oryginał. `.assign()` samo w sobie jest bezpieczne, ale
`copy()` na początku to dobra praktyka obronna.

---

## Zazębienie — filtrowanie boolean jako krok w łańcuchu

Znasz już `df[df["col"] > x]` z tematu 8. To wyrażenie możesz wstawić wprost
jako pierwszy krok łańcucha:

```python
wynik = (
    df[df["wiek"] > 28]
    .groupby("miasto")
    .size()
)
# liczy osoby w wieku > 28 per miasto
```

Możesz też połączyć filtr z kopią, assign i agg:

```python
wynik = (
    df[df["wiek"] >= 30]
    .assign(premia=lambda d: d["wynagrodzenie"] * 0.1)
    .groupby("miasto")
    .agg({"premia": "sum"})
)
```

### Typowe błędy — filtr w łańcuchu
- `df[df.copy()["wiek"] > 28]` — nie potrzeba `.copy()` wewnątrz filtra boolowskiego,
  ponieważ wynik filtrowania to nowy obiekt (widok lub kopia — pandas decyduje).
- Zapominanie nawiasów po `.copy()` kiedy dalej jest nawias kwadratowy:
  `df.copy()[df["wiek"] > 28]` — poprawne; pandas najpierw kopiuje, potem filtruje.

---

## Teoria testowa

Znasz już conftest.py, sys.path.insert i tmp_path z tematu 8. W tym temacie
nie będziesz czytać żadnych plików — fixture dostarcza DataFrame bezpośrednio.

### Schemat 3 pytań

1. **Co testuje?** — jaką konkretną wartość lub efekt sprawdzam
2. **Co udaje?** — co przygotowuję zamiast prawdziwego środowiska
3. **Co sprawdzam?** — jakie twierdzenie zawiera assert

### Co sprawdzać w testach groupby/assign

```python
# typ zwracanego obiektu
assert isinstance(wynik, pd.Series)
assert isinstance(wynik, pd.DataFrame)

# wartość konkretnej grupy (Series z groupby)
assert wynik["Warszawa"] == 3

# wartość w komórce (DataFrame z agg)
assert wynik["wiek"]["Warszawa"] == 95

# czy kolumna istnieje po assign
assert "premia" in wynik.columns

# lista wartości nowej kolumny
assert wynik["premia"].tolist() == [300.0, 400.0, 500.0, 350.0, 450.0]

# liczba grup (czy filtr zadziałał)
assert len(wynik) == 2
```

### Przykład testu z innej dziedziny

```python
def test_max_z_trzech_liczb() -> None:
    """Co testuje: czy max() zwraca największą z trzech liczb.
    Co udaje: nic — używam literałów.
    Co sprawdzam: wynik == 9.
    """
    # przygotuj
    liczby = [3, 9, 1]

    # wywołaj
    wynik = max(liczby)

    # sprawdź
    assert wynik == 9
```
