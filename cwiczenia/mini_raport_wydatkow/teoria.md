# Teoria — mini_raport_wydatkow (mini-projekt M1)

To NIE jest zwykły temat z nową biblioteką. To mini-projekt: bierzesz
klocki, które już znasz z tematów 6 (CSV), 8-9 (pandas) i 10 (openpyxl),
i składasz z nich jedną działającą całość — raport wydatków.

Dlatego ta teoria wygląda inaczej niż zwykle: większość pojęć tylko
PRZYPOMINA jednym zdaniem (znasz je, wracaj do starych teorii, gdy
czegoś zapomnisz), a od zera tłumaczy tylko kilka NOWYCH rzeczy
i — co najważniejsze — pokazuje, jak klocki łączą się w pipeline.

Uwaga do TODO w zadaniach: w mini-projekcie TODO mówią CO osiągnąć
i odsyłają do wzorca, ale NIE dyktują kodu linijka po linijce.
To celowe — piszesz logikę z głowy, nie przepisujesz.

---

## 1. Co budujemy — mapa projektu

Wyobraź sobie restaurację:

1. **Dostawa składników** — rano przyjeżdża skrzynka warzyw (plik CSV
   z wydatkami). Nie wiesz jeszcze, czy wszystko jest świeże.
2. **Kontrola jakości** — kucharz odrzuca zgniłe pomidory (wiersze
   z zepsutą kwotą, np. "abc" albo pustą).
3. **Kuchnia** — z dobrych składników powstaje danie (pandas: agregacja
   wydatków po kategoriach, procenty, sortowanie).
4. **Podanie na talerzu** — danie musi też ładnie wyglądać (openpyxl:
   pogrubione nagłówki, kolory, szerokości kolumn).

Ten sam przepływ w numerach zadań:

```
CSV na dysku
   │  zadanie_01 (wczytanie)          ← temat 6
   ▼
lista słowników (kwoty to stringi!)
   │  zadanie_02 (walidacja)          ← NOWE pojęcie 1
   ▼
lista poprawnych wierszy (kwoty to float)
   │  zadanie_03 (budowa DataFrame)   ← temat 8
   ▼
DataFrame  ──►  zadanie_04 (filtr), zadanie_05 (suma)     ← temat 8
   │  zadanie_06 (agregacja po kategorii)                 ← temat 9 + NOWE 2
   ▼
raport (kategoria / suma / srednia / liczba)
   │  zadanie_07 (procenty)           ← temat 9 + NOWE 4
   │  zadanie_08 (sortowanie)         ← NOWE pojęcie 3
   ▼
posortowany raport
   │  zadanie_09 (eksport do .xlsx)   ← temat 10
   │  zadania_10-12 (formatowanie)    ← temat 10
   ▼
gotowy raport Excel

zadanie_13 = dyrygent: wywołuje powyższe klocki po kolei.
```

---

## 2. Czego NIE tłumaczymy od nowa (przypomnienia jednozdaniowe)

Wszystko poniżej już ćwiczyłeś — tu tylko przypominajka, z którego
tematu co pochodzi:

- **csv.DictReader** + `open(..., newline="", encoding="utf-8")` —
  czytanie CSV jako słowników: temat 6. Pamiętaj: WSZYSTKO, co czyta
  DictReader, jest stringiem — nawet "120.50".
- **try/except** i kolejność wyjątków szczegółowy → ogólny: temat 4;
  `FileNotFoundError` przy otwieraniu nieistniejącego pliku: temat 5.
- **Kontrakt None** — funkcja zwraca None zamiast rzucać wyjątkiem,
  gdy "braku" się spodziewamy: tematy 1 i 5.
- **pd.DataFrame**, `df["kolumna"]`, `.sum()`, filtr boolean
  `df[df["kwota"] > 100]` i `.copy()` przeciw side effects: temat 8.
- **.groupby()**, `.agg({"kolumna": "funkcja"})`, `.assign()`
  z lambdą i method chaining: temat 9.
- **df.to_excel(sciezka, index=False)**, `.reset_index()` po groupby,
  **Font / PatternFill / Alignment**, `iter_rows`, `column_dimensions`,
  `freeze_panes` i żelazna zasada „najpierw dane (pandas), potem ozdoby
  (openpyxl), na końcu save": temat 10.

Jeśli którekolwiek z powyższych brzmi obco — otwórz teorię tamtego
tematu, zanim zaczniesz. Ta teoria zakłada, że to umiesz.

---

## 3. NOWE pojęcie 1: walidacja danych — bramka jakości

### Co to jest?

Walidacja to sprawdzenie danych PRZED użyciem: „czy to, co dostałem,
w ogóle nadaje się do liczenia?". Jak bramkarz w klubie — wpuszcza
tylko tych z ważnym biletem, resztę odsyła, ale impreza trwa dalej.

### Skąd się wzięło?

Pliki CSV tworzą ludzie i inne programy — a te się mylą. W kolumnie
z kwotą potrafi wylądować "abc", pusty string albo wartość ujemna.
DictReader tego NIE sprawdza — odda ci każdy śmieć jako string.

### Dlaczego tak musi być?

Bo `float("abc")` rzuca `ValueError` — i bez bramki jeden zepsuty
wiersz wywala cały program. Wzorzec: próbujesz skonwertować, a gdy
się nie da — pomijasz TEN JEDEN wiersz i idziesz dalej:

```python
poprawne = []
for wiersz in wiersze:
    try:
        ocena = float(wiersz["ocena"])
    except ValueError:
        continue
    if ocena > 0:
        wiersz["ocena"] = ocena
        poprawne.append(wiersz)
```

Linijka po linijce (przykład na ocenach uczniów, NIE na wydatkach):

- `try:` — „spróbuj, może się uda" (znasz z tematu 4).
- `float(wiersz["ocena"])` — konwersja stringa "4.5" na liczbę 4.5.
  Dla "abc" i "" poleci `ValueError`.
- `except ValueError: continue` — łapiemy TYLKO błąd konwersji
  i przechodzimy do następnego wiersza pętli. `continue` znaczy
  „porzuć ten obieg pętli, weź kolejny element".
- `if ocena > 0:` — druga bramka: liczba poprawna technicznie,
  ale bez sensu biznesowo (ocena zerowa/ujemna) też odpada.
- `wiersz["ocena"] = ocena` — podmieniamy string na float, żeby
  dalej w pipeline nie trzeba było konwertować drugi raz.

### Typowe błędy początkujących

- `except Exception:` zamiast `except ValueError:` — łapiesz za dużo
  i ukrywasz prawdziwe bugi (np. literówkę w nazwie klucza).
- Walidacja przez `wiersz["ocena"].isdigit()` — zawiedzie dla "4.5"
  (kropka to nie cyfra). Do liczb z kropką: tylko próba `float()`.
- Zwracanie stringa "błędne dane" zamiast pominięcia wiersza —
  łamie kontrakt funkcji (jeden typ zwracany, znasz od tematu 1).
- Zapomnienie o `continue` — zepsuty wiersz i tak trafia do wyniku.

---

## 4. NOWE pojęcie 2: nazwana agregacja w .agg()

### Co to jest?

Rozszerzenie znanego ci `.agg()`: zamiast słownika podajesz argumenty
nazwane, gdzie NAZWA argumentu = nazwa nowej kolumny wyniku,
a wartość to para `("kolumna_źródłowa", "funkcja")`:

```python
wynik = df.groupby("klasa").agg(
    srednia=("ocena", "mean"),
    liczba=("ocena", "count"),
)
```

(Przykład na ocenach w klasach — twoje zadania mają inne kolumny.)

### Skąd się wzięło?

Znana ci forma słownikowa `.agg({"ocena": "mean"})` ma ograniczenie:
wynikowa kolumna zawsze nazywa się jak źródłowa. A co, gdy z JEDNEJ
kolumny chcesz trzy statystyki naraz (suma, średnia, liczba)?
Słownik `{"ocena": ["mean", "count"]}` tworzy koszmarne podwójne
nagłówki. Twórcy pandas dodali więc (w wersji 0.25) nazwaną agregację.

### Dlaczego tak musi być?

- `srednia=` — to będzie NAZWA kolumny w wyniku. Ty ją wybierasz,
  więc raport od razu ma czytelne polskie nagłówki.
- `("ocena", "mean")` — krotka: skąd brać dane i co z nimi zrobić.
  Musi być krotka w nawiasach okrągłych — tak twórcy pandas
  odróżniają „źródło + funkcja" od zwykłej wartości.
- Wynik dalej trzyma grupy w indeksie — przed eksportem do Excela
  potrzebujesz `.reset_index()` (znasz z tematu 10).

### Typowe błędy początkujących

- `srednia="ocena", "mean"` bez nawiasów krotki — SyntaxError albo
  zupełnie inne znaczenie. Para musi być w `(...)`.
- `srednia=("mean", "ocena")` — odwrócona kolejność; najpierw
  kolumna, potem funkcja.
- Zapomniany `.reset_index()` przed `to_excel(index=False)` —
  nazwy grup znikają z raportu (dokładnie ta pułapka z tematu 10).

---

## 5. NOWE pojęcie 3: .sort_values() — sortowanie tabeli

### Co to jest?

Metoda DataFrame układająca wiersze według wartości wskazanej kolumny:

```python
posortowane = df.sort_values("ocena", ascending=False)
```

### Skąd się wzięło?

Raport „kategorie wydatków" jest czytelny dopiero, gdy największe
pozycje są na górze — jak lista przebojów: nikt nie zaczyna od
miejsca czterdziestego.

### Dlaczego tak musi być?

- `"ocena"` — nazwa kolumny, po której sortujemy.
- `ascending=False` — malejąco (od największej). Domyślnie jest
  `ascending=True`, czyli rosnąco — bo po angielsku *ascending*
  znaczy „wznoszący".
- `sort_values` zwraca NOWY DataFrame — oryginał zostaje nietknięty.
  To ta sama filozofia „bez side effects", którą znasz z `.copy()`
  w temacie 8: metody pandas domyślnie nie psują danych wejściowych.

### Typowe błędy początkujących

- Wywołanie `df.sort_values("ocena")` bez przypisania wyniku —
  posortowana tabela przepada, `df` się nie zmienia.
- `ascending=False` pominięte, gdy chcesz „od największego" —
  dostajesz odwrotną kolejność i raport wygląda na zepsuty.
- Sortowanie po kolumnie ze stringami zamiast liczb — "9" wyląduje
  za "10", bo stringi sortują się znak po znaku. Dlatego walidacja
  (pojęcie 1) konwertuje kwoty na float ZANIM zbudujesz DataFrame.

---

## 6. NOWE pojęcie 4: .round() na kolumnie

### Co to jest?

Metoda zaokrąglająca każdą liczbę w kolumnie (Series) do zadanej
liczby miejsc po przecinku:

```python
df["procent_frekwencji"].round(1)   # 35.31847... -> 35.3
```

### Skąd się wzięło?

Udział procentowy z dzielenia prawie nigdy nie wychodzi okrągły —
a raport z wartością 35.31847915426253 wygląda nieprofesjonalnie.

### Dlaczego tak musi być?

- `.round(1)` — jedna cyfra po przecinku; `.round(0)` — pełne liczby.
- Działa na CAŁEJ kolumnie naraz (jak `.sum()` — jedna komenda,
  wszystkie wiersze), zwraca nową kolumnę, oryginał bez zmian.
- Świetnie łączy się z `.assign()` z tematu 9: w lambdzie liczysz
  udział i od razu go zaokrąglasz.

### Typowe błędy początkujących

- `.round(1)` na całym DataFrame zamiast na kolumnie — zadziała, ale
  zaokrągli WSZYSTKIE kolumny liczbowe, także te, których nie chcesz.
- Mylenie z wbudowanym `round(x, 1)` — tamto działa na pojedynczej
  liczbie; na kolumnie używaj metody `.round(1)`.

---

## 7. Sekcja przekrojowa: jak klocki tworzą pipeline

To najważniejsza lekcja tego mini-projektu — dotyczy KAŻDEGO
przyszłego programu, nie tylko wydatków.

### Małe funkcje + jeden dyrygent

Każde z zadań 01-12 to mały, samodzielny klocek: robi JEDNĄ rzecz,
da się go zrozumieć i przetestować osobno. Zadanie 13 to dyrygent —
sam nic nie liczy, tylko wywołuje klocki we właściwej kolejności
i podaje wynik jednego jako wejście następnego.

Analogia: dyrygent orkiestry nie gra na żadnym instrumencie —
ale bez niego skrzypce i trąbka grają każde swoje.

### Kontrakt None płynie przez pipeline

Klocek czytający plik (zadanie 01) zwraca None, gdy pliku nie ma.
Dyrygent (zadanie 13) musi to sprawdzić NA POCZĄTKU: jeśli wczytanie
dało None — cały raport nie ma sensu, więc dyrygent też zwraca None
(early return, znasz z tematu 1). Błąd z brzegu pipeline'u przepływa
na jego koniec, zamiast wybuchać w środku.

### Kolejność: dane → ozdoby → save

Przypomnienie żelaznej zasady z tematu 10, bo w zadaniu 13 łatwo
o potknięcie: najpierw pandas zapisuje DANE (`to_excel`), dopiero
potem openpyxl otwiera plik i dodaje OZDOBY, a każda funkcja
ozdabiająca kończy się `wb.save(...)`. Odwrotna kolejność = pandas
nadpisuje plik i formatowanie znika.

---

## 8. Teoria testowa

### Po co jest conftest.py i sys.path.insert?

Wiesz to z poprzednich tematów, więc tylko szybkie przypomnienie:
pytest uruchamiany z głównego folderu repo nie wie, gdzie leży
`mini_raport_wydatkow.py` — `sys.path.insert(0, ...)` w conftest.py
dopisuje folder tematu do listy miejsc, w których Python szuka
modułów, dzięki czemu `import` w pliku testowym działa. conftest.py
to też dom dla fixture — pytest wczytuje go automatycznie, bez
importowania.

**Ważna różnica w tym projekcie:** conftest.py dostajesz GOTOWY,
bez TODO. To świadoma decyzja reguł mini-projektu: dane testowe
(przykładowy CSV, DataFrame'y, plik Excela) są żmudne do wpisywania,
a niczego nowego nie uczą — ty masz pisać LOGIKĘ. Przeczytaj
conftest.py uważnie: musisz WIEDZIEĆ, co jest w danych, żeby pisać
sensowne asserty.

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

1. **Co testuję?** — który klocek i który jego obowiązek
   (np. „walidacja odrzuca wiersz z kwotą, której nie da się
   skonwertować").
2. **Co udaję?** — czego nie chcę używać naprawdę (tu: prawie nic —
   pliki tworzymy w tmp_path, więc są prawdziwe, tylko tymczasowe).
3. **Co sprawdzam?** — jaki konkretny assert kończy test
   (np. „w wyniku zostały dokładnie 2 wiersze").

Docstringi testów w tym projekcie mają te trzy odpowiedzi już
wypełnione — twoim zadaniem jest przełożyć je na kod.

### Schemat przygotuj → podmień → wywołaj → sprawdź

Przykład na INNYM temacie niż wydatki (funkcja `policz_linie`,
która zwraca liczbę linii pliku tekstowego albo None, gdy pliku brak):

```python
def test_policz_linie_zwraca_liczbe_linii(tmp_path: Path) -> None:
    plik = tmp_path / "notatki.txt"                  # przygotuj
    plik.write_text("a\nb\nc\n", encoding="utf-8")   # przygotuj
    wynik = policz_linie(str(plik))                  # wywołaj
    assert wynik == 3                                # sprawdź
```

Kroku „podmień" tu nie ma — niczego nie udajemy, bo tmp_path daje
prawdziwy, bezpieczny plik. W tym projekcie będzie tak samo:
większość testów to przygotuj → wywołaj → sprawdź.

### tmp_path — przypomnienie

Znasz z tematu 10: pytest wstrzykuje świeży, pusty katalog tymczasowy
dla KAŻDEGO testu z osobna; po teście system go sprząta; obiekt jest
typu `Path`, więc ścieżki budujesz przez `/`, a do funkcji
przyjmujących string przekazujesz `str(sciezka)`.

### Gotowe fixture w conftest.py tego projektu

| Fixture        | Co daje                                                        |
|----------------|----------------------------------------------------------------|
| `wydatki_csv`  | Path do poprawnego CSV: 7 wierszy, kolumny data/kategoria/opis/kwota |
| `brudne_wiersze` | lista 5 słowników: 2 poprawne, 3 do odrzucenia (kwota "abc", pusta, ujemna) |
| `df_wydatki`   | gotowy DataFrame 7 wydatków (kwoty już jako float)             |
| `df_raport`    | gotowy zagregowany raport: kategoria/suma/srednia/liczba, NIEposortowany |
| `raport_xlsx`  | Path do gotowego pliku .xlsx z nagłówkami i 3 wierszami raportu |

Liczby kontrolne (przydadzą się w assertach — policz sam dla pewności,
dane są w conftest.py): suma wszystkich kwot z `wydatki_csv`
i `df_wydatki` to 739.0; sumy kategorii: jedzenie 261.0,
transport 290.0, rozrywka 188.0.
