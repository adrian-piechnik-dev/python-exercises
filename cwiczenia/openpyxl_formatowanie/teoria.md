# openpyxl — Excel z formatowaniem

## Co to jest openpyxl?

Excel to program do tabel — wiersze, kolumny, komórki. Plik Excela (`.xlsx`)
to taki cyfrowy zeszyt w kratkę: każda kratka (komórka) ma swój adres,
np. `A1` = kolumna A, wiersz 1 — jak w grze w statki.

`openpyxl` to biblioteka Pythona, która umie takie zeszyty tworzyć, czytać
i ozdabiać (pogrubienia, kolory, ramki) — bez otwierania Excela.
CSV (temat 6) przechowywał tylko goły tekst; `.xlsx` przechowuje też
**wygląd**: czcionki, kolory tła, obramowania, szerokości kolumn.

Instalacja (biblioteka zewnętrzna, jak pandas):

```
pip install openpyxl
```

---

## Workbook — nowy skoroszyt

Skoroszyt (workbook) = cały plik Excela. Arkusz (worksheet) = jedna zakładka
w tym pliku. Nowy skoroszyt zawsze ma jeden pusty arkusz.

```python
from openpyxl import Workbook

wb = Workbook()        # nowy, pusty skoroszyt w pamięci
ws = wb.active         # aktywny (pierwszy) arkusz
ws["A1"] = "Produkt"   # wpisz tekst do komórki A1
wb.save("raport.xlsx") # dopiero TERAZ plik powstaje na dysku
```

Linijka po linijce:
- `wb = Workbook()` — tworzy skoroszyt **w pamięci**; na dysku jeszcze nic nie ma.
- `ws = wb.active` — bierze pierwszy arkusz (skrót od "active worksheet").
- `ws["A1"] = "Produkt"` — zapis do komórki przez adres jak w statkach.
- `wb.save("raport.xlsx")` — zrzuca wszystko na dysk. **Bez save nie ma pliku.**

> **Najważniejsza reguła tematu:** wszystkie zmiany żyją w pamięci, dopóki
> nie wywołasz `wb.save(...)`. Wzorzec z tego kursu: funkcja modyfikująca
> plik Excela kończy się `wb.save(sciezka)`, a dopiero **po** nim `return True`.
> Kolejność odwrotna (return przed save) = plik bez zmian, bo return
> natychmiast kończy funkcję.

### Typowe błędy początkujących

- Zapomniany `wb.save()` — kod działa, błędu nie ma, ale plik na dysku
  się nie zmienia. Najczęstszy błąd w openpyxl.
- `return True` przed `wb.save()` — save nigdy się nie wykona (kod po
  return jest martwy).
- `wb.save()` bez argumentu — `TypeError`; save wymaga ścieżki.

---

## ws.append — dodawanie całych wierszy

Zamiast wpisywać komórka po komórce, można dokleić cały wiersz na koniec:

```python
ws.append(["miasto", "sprzedaz"])   # wiersz 1: nagłówki
ws.append(["Warszawa", 100])        # wiersz 2: dane
ws.append(["Krakow", 200])          # wiersz 3: dane
```

`append` przyjmuje listę — pierwszy element trafia do kolumny A,
drugi do B itd. Każde kolejne `append` pisze wiersz niżej.

### Typowe błędy początkujących

- `ws.append("Warszawa")` — string zamiast listy; openpyxl potraktuje
  go jak listę liter i rozsypie po jednej literze na kolumnę.

---

## load_workbook — otwieranie istniejącego pliku

```python
from openpyxl import load_workbook

wb = load_workbook("raport.xlsx")
ws = wb.active
print(ws["A1"].value)   # Produkt
```

- `load_workbook(sciezka)` — wczytuje plik z dysku do pamięci.
- `ws["A1"]` — to obiekt komórki; **sama wartość** siedzi w `.value`.
- Plik musi istnieć — inaczej `FileNotFoundError`.

Różnica zapisu i odczytu, którą łatwo pomylić:
- **zapis**: `ws["A1"] = "tekst"` (bez `.value` — openpyxl pozwala na skrót)
- **odczyt**: `ws["A1"].value` (z `.value` — bez tego dostajesz obiekt
  `<Cell 'Sheet'.A1>`, nie wartość)

### Typowe błędy początkujących

- `print(ws["A1"])` — wypisze `<Cell 'Sheet'.A1>` zamiast wartości;
  brakuje `.value`.
- Modyfikacja wczytanego pliku bez `wb.save()` na końcu — zmiany przepadają.

---

## openpyxl.styles — skrzynka z ozdobami

Wszystkie narzędzia do formatowania importuje się z jednego miejsca:

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
```

Wzorzec jest zawsze ten sam: tworzysz obiekt stylu i **przypisujesz go
do komórki** — jak naklejkę na kratkę zeszytu.

---

## Font — czcionka (pogrubienie, rozmiar, kolor)

```python
from openpyxl.styles import Font

ws["A1"].font = Font(bold=True)                 # pogrubienie
ws["B1"].font = Font(size=14)                   # rozmiar 14
ws["C1"].font = Font(bold=True, color="FF0000") # pogrubiony czerwony
```

- `bold=True` — pogrubienie; wartość logiczna, nie string `"true"`.
- `color="FF0000"` — kolor w zapisie szesnastkowym RRGGBB, jak w internecie:
  `FF0000` czerwony, `00FF00` zielony, `0000FF` niebieski, `FFFF00` żółty.

**Odczyt koloru — pułapka z alfą.** openpyxl przechowuje kolory z dodatkowym
kanałem przezroczystości z przodu (tzw. alpha). Ustawisz `"FF0000"`,
a odczytasz `"00FF0000"`. Dlatego w testach sprawdzaj końcówkę:

```python
komorka = ws["C1"]
komorka.font.color.rgb.endswith("FF0000")   # True — tak porównuj kolory
komorka.font.bold                            # True — odczyt pogrubienia
```

### Typowe błędy początkujących

- `Font(bold="True")` — string zamiast `True`; formatowanie nie zadziała
  poprawnie.
- Porównanie koloru przez `==` z `"FF0000"` — zawiedzie przez doklejoną alfę;
  używaj `.endswith("FF0000")`.
- `ws["A1"].font.bold = True` — obiektu stylu nie zmienia się „w miejscu";
  zawsze przypisuj **nowy** `Font(...)` do `.font`.

---

## PatternFill — kolor tła komórki

```python
from openpyxl.styles import PatternFill

ws["A1"].fill = PatternFill(
    start_color="FFFF00",
    end_color="FFFF00",
    fill_type="solid",
)
```

- `start_color` i `end_color` — ten sam kolor (gradientów nie używamy);
  zapis RRGGBB jak w Font.
- `fill_type="solid"` — pełne wypełnienie. **Bez tego parametru komórka
  zostanie biała**, mimo podanych kolorów — to najczęstsza wpadka.

Odczyt w testach (znowu końcówką, przez alfę):

```python
ws["A1"].fill.start_color.rgb.endswith("FFFF00")   # True
ws["A1"].fill.fill_type == "solid"                  # True
```

### Typowe błędy początkujących

- Pominięcie `fill_type="solid"` — brak efektu, zero błędów. Bardzo mylące.
- Kolor z kratką `"#FFFF00"` jak w CSS — openpyxl nie chce `#`; sam hex.

---

## Alignment — wyrównanie w komórce

```python
from openpyxl.styles import Alignment

ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
```

- `horizontal` — `"left"`, `"center"`, `"right"`.
- `vertical` — `"top"`, `"center"`, `"bottom"`.

Odczyt: `ws["A1"].alignment.horizontal` zwraca `"center"`.

### Typowe błędy początkujących

- `Alignment(horizontal="middle")` — nie ma wartości `"middle"`;
  środek to zawsze `"center"`.

---

## Border i Side — obramowanie

Ramka komórki składa się z 4 boków. Najpierw definiujesz wygląd jednego
boku (`Side`), potem składasz z boków ramkę (`Border`):

```python
from openpyxl.styles import Border, Side

cienka = Side(style="thin")
ws["A1"].border = Border(left=cienka, right=cienka, top=cienka, bottom=cienka)
```

- `Side(style="thin")` — cienka linia; inne style: `"medium"`, `"thick"`.
- `Border(left=..., right=..., top=..., bottom=...)` — który bok ma jaką linię;
  pominięty bok zostaje bez ramki.

Odczyt: `ws["A1"].border.left.style` zwraca `"thin"`.

### Typowe błędy początkujących

- `Border(style="thin")` — Border nie przyjmuje `style` bezpośrednio;
  styl należy do `Side`, a Side wkłada się do Border.
- Zdefiniowanie tylko `left` i zdziwienie, że reszta boków pusta —
  każdy bok podaje się osobno.

---

## freeze_panes — zamrożenie nagłówka

Przy przewijaniu długiej tabeli nagłówek ucieka do góry. `freeze_panes`
przybija go na stałe:

```python
ws.freeze_panes = "A2"
```

Zasada: podajesz **pierwszą komórkę, która ma się przewijać**. `"A2"` oznacza:
wszystko powyżej wiersza 2 (czyli wiersz 1 z nagłówkami) stoi w miejscu.

To właściwość arkusza (`ws`), nie komórki — nie ma tu żadnego obiektu stylu.
Odczyt: `ws.freeze_panes` zwraca `"A2"`.

### Typowe błędy początkujących

- `ws.freeze_panes = "A1"` — zamraża „wszystko powyżej A1", czyli nic;
  chcesz zamrozić wiersz 1 → podaj `"A2"`.
- Próba `ws["A2"].freeze_panes` — to cecha arkusza, nie komórki.

---

## column_dimensions — szerokość kolumny

Domyślne kolumny są wąskie i długie teksty się ucinają:

```python
ws.column_dimensions["A"].width = 25
```

- `column_dimensions["A"]` — ustawienia całej kolumny A (litera, nie adres).
- `.width = 25` — szerokość w znakach (mniej więcej).

Odczyt: `ws.column_dimensions["A"].width` zwraca `25`.

### Typowe błędy początkujących

- `ws.column_dimensions["A1"]` — adres komórki zamiast litery kolumny;
  ma być samo `"A"`.

---

## iter_rows — przechodzenie po wierszach

Do policzenia czegoś z danych trzeba przejść po wierszach:

```python
for wiersz in ws.iter_rows(min_row=2, values_only=True):
    print(wiersz)        # ("Warszawa", 100) — krotka wartości
    print(wiersz[1])     # 100 — druga kolumna (indeks od 0!)
```

- `min_row=2` — zacznij od wiersza 2, czyli **pomiń nagłówek** z wiersza 1.
- `values_only=True` — dawaj same wartości (krotki), nie obiekty komórek.
- `wiersz[0]` to kolumna A, `wiersz[1]` to kolumna B — indeksy krotki
  liczą się od zera, jak w listach.

Suma kolumny B po wszystkich wierszach danych — wzorzec akumulatora,
który znasz z pętli:

```python
suma = 0
for wiersz in ws.iter_rows(min_row=2, values_only=True):
    suma += wiersz[1]
```

### Typowe błędy początkujących

- Brak `values_only=True` — dostajesz obiekty `Cell` i `suma += wiersz[1]`
  wybucha `TypeError`; trzeba by pisać `wiersz[1].value`.
- Brak `min_row=2` — nagłówek `"sprzedaz"` (string) wpada do sumy
  i `TypeError: unsupported operand`.

---

## Zazębienie: DataFrame → Excel

Z tematów 8-9 znasz `pd.DataFrame`, `.groupby()` i `.agg()` — tu tylko
przypomnienie, że wynik groupby ma grupy w **indeksie**, nie w kolumnie.

### df.to_excel — zapis DataFrame do pliku Excela

```python
import pandas as pd

df = pd.DataFrame({"miasto": ["Warszawa", "Krakow"], "sprzedaz": [100, 200]})
df.to_excel("raport.xlsx", index=False)
```

- `to_excel(sciezka, index=False)` — pandas sam tworzy plik `.xlsx`
  (pod spodem używa openpyxl); nie trzeba żadnego `wb.save()`.
- `index=False` — **nie zapisuj indeksu** (0, 1, 2...) jako dodatkowej
  pierwszej kolumny. Bez tego raport ma śmieciową kolumnę numerków
  i nagłówki przesuwają się o jedną kolumnę w prawo.

### reset_index — indeks grup z powrotem do kolumny

Wynik `groupby().agg()` trzyma nazwy grup w indeksie. Przy `index=False`
indeks przepada — czyli stracisz nazwy miast! Ratunek: `.reset_index()`
przenosi indeks z powrotem do zwykłej kolumny:

```python
wynik = df.groupby("miasto").agg({"sprzedaz": "sum"}).reset_index()
wynik.to_excel("raport.xlsx", index=False)
```

Po `reset_index()` tabela ma zwykłe kolumny `miasto` i `sprzedaz` —
i obie trafiają do Excela.

### Łączenie światów: pandas zapisuje, openpyxl ozdabia

pandas nie umie formatować. Wzorzec końcowy kursu:

```python
df.to_excel("raport.xlsx", index=False)   # 1. pandas: dane do pliku
wb = load_workbook("raport.xlsx")          # 2. openpyxl: otwórz ten plik
ws = wb.active
ws["A1"].font = Font(bold=True)            # 3. ozdób
wb.save("raport.xlsx")                     # 4. zapisz PRZED return
```

### Typowe błędy początkujących

- Zapomniane `index=False` — dodatkowa kolumna z numerami 0, 1, 2.
- `index=False` na wyniku groupby **bez** `reset_index()` — znikają
  nazwy grup.
- Formatowanie przez openpyxl przed `to_excel` — pandas nadpisze cały plik;
  kolejność musi być: najpierw dane, potem ozdoby, na końcu save.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Gdy pytest uruchamia `test_openpyxl_formatowanie.py`, Python szuka modułu
`openpyxl_formatowanie`. Folder tematu nie jest w `sys.path` (liście miejsc,
gdzie Python szuka plików `.py`), więc import by się wywalił.

`conftest.py` ładuje się automatycznie przed testami i dokleja folder tematu
na początek tej listy:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` → pełna ścieżka do `conftest.py`
- `os.path.dirname(...)` → folder, w którym leży ten plik
- `sys.path.insert(0, ...)` → wstaw na początek listy poszukiwań

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie lub scenariusz.
2. **Co udaje?** — czy potrzebny plik tymczasowy / fixture? Jaki?
3. **Co sprawdzam?** — co dokładnie weryfikuje `assert`?

### Schemat: przygotuj → wywołaj → sprawdź

Przykład na temacie spoza tego kursu (dziennik ocen w pliku tekstowym):

```python
def test_dopisanie_oceny_do_dziennika(tmp_path: Path) -> None:
    """Co testuje: czy ocena dokleja się na koniec pliku dziennika.
    Co udaje: nic — tworzę prawdziwy plik tymczasowy przez tmp_path.
    Co sprawdzam: ostatnia linia pliku to nowa ocena.
    """
    # przygotuj
    p = tmp_path / "dziennik.txt"
    p.write_text("matematyka: 4\n", encoding="utf-8")

    # wywołaj
    with open(str(p), "a", encoding="utf-8") as f:
        f.write("polski: 5\n")

    # sprawdź
    linie = p.read_text(encoding="utf-8").splitlines()
    assert linie[-1] == "polski: 5"
```

W tym temacie krok „sprawdź" wygląda zwykle tak: po wywołaniu testowanej
funkcji **otwórz plik na nowo** przez `load_workbook` i obejrzyj komórki —
tak test dowodzi, że zmiany naprawdę trafiły na dysk, a nie tylko do pamięci.

### Fixture tmp_path

`tmp_path` to wbudowany fixture pytest: obiekt `Path` wskazujący czysty
folder tymczasowy, osobny dla każdego testu, sprzątany automatycznie.

```python
def test_przyklad(tmp_path: Path) -> None:
    p = tmp_path / "raport.xlsx"     # ścieżka; pliku jeszcze nie ma
    # ... przekaż str(p) do testowanej funkcji ...
```

Własne fixtures z `conftest.py` (u nas `plik_xlsx` i `df_sprzedaz`)
działają identycznie — pytest wstrzykuje je po nazwie parametru
w funkcji testowej.
