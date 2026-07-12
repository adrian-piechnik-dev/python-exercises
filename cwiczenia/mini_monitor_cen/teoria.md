# Teoria — mini_monitor_cen (mini-projekt M3)

Trzeci mini-projekt: składasz klocki z tematów 12 (scraping),
14-15 (SQL + psycopg2) i 13 (pytest z atrapami) w monitor cen —
program, który regularnie sprawdza ceny w sklepie internetowym,
zapisuje je do bazy i melduje, co podrożało, a co staniało.

Jak w M1 i M2: znane pojęcia tylko PRZYPOMINAM jednym zdaniem,
od zera tłumaczę wyłącznie nowości. TODO mówią CO osiągnąć
i odsyłają do wzorców — kod piszesz z głowy.

---

## 1. Co budujemy — mapa projektu

Wyobraź sobie wywiadowcę cenowego, którego sklep wysyła na patrol
do konkurencji:

1. **Zdjęcie półki** — wchodzisz do sklepu konkurencji i robisz
   zdjęcie regału (pobranie HTML strony przez requests).
2. **Odczytanie zdjęcia** — w biurze wyciągasz ze zdjęcia nazwy
   i ceny; niektóre metki są nieczytelne, te pomijasz
   (BeautifulSoup + czyszczenie tekstu ceny).
3. **Zeszyt obserwacji** — każdy odczyt wpisujesz do zeszytu
   z datą (baza danych: INSERT z parametrami %s).
4. **Meldunek** — porównujesz dzisiejszą cenę z ostatnim wpisem
   w zeszycie i meldujesz: wzrost, spadek, bez zmian, nowość
   (SELECT z ORDER BY + porównanie).

Ten sam przepływ w numerach zadań:

```
strona sklepu (piaskownica)
   │  zadanie_01 (pobranie HTML z kontrolą błędów)   ← temat 12
   ▼
surowy HTML
   │  zadanie_02 (parsowanie produktów)              ← temat 12
   │  zadanie_03 (czyszczenie tekstu ceny)           ← NOWE 1
   │  zadanie_04 (parsowanie + czyszczenie razem)
   │  zadanie_05 (patrol po wielu stronach z pauzą)  ← temat 12
   ▼
lista {"nazwa", "cena"}
   │  zadanie_06 (tabela ceny w bazie)               ← tematy 14-15
   │  zadanie_07 (zapis jednego odczytu, %s)         ← temat 15
   │  zadanie_08 (zapis hurtowy, executemany)        ← temat 15
   ▼
zeszyt obserwacji (tabela ceny)
   │  zadanie_09 (historia cen produktu)             ← tematy 14-15
   │  zadanie_10 (ostatnia zapisana cena)            ← tematy 14-15
   │  zadanie_11 (werdykt: wzrost/spadek/...)        ← temat 1
   ▼
zadanie_12 = dyrygent zapisu (HTML -> baza)
zadanie_13 = dyrygent całości (patrol -> meldunek ze statusami)
```

---

## 2. Czego NIE tłumaczymy od nowa (przypomnienia jednozdaniowe)

- **requests.get z timeout i nagłówkiem User-Agent** (przedstawiamy
  się serwerowi), `raise_for_status()`, łapanie
  `requests.RequestException`: tematy 11-12.
- **Grzeczność scrapera**: pauza `time.sleep(...)` między
  zapytaniami, żeby nie zalać serwera: temat 12.
- **BeautifulSoup(html, "html.parser")**, `find_all` po nazwie
  znacznika i klasie (`class_=...`), `find` wewnątrz znalezionego
  elementu, `.get_text()`: temat 12.
- **Kontrakt None** przy spodziewanym braku (sieć, pusty wynik):
  tematy 1, 4-5; **early return**: temat 1.
- **Sklejanie list `.extend()`** w pętli-akumulatorze: znasz z M2.
- **SQL**: CREATE TABLE, INSERT, SELECT z WHERE, ORDER BY (z DESC —
  malejąco), LIMIT: temat 14; **SERIAL** (autonumeracja), typy TEXT
  i NUMERIC: temat 15.
- **psycopg2-styl pracy z bazą**: `with polaczenie.cursor() as kursor:`,
  `kursor.execute(sql, krotka)` z zaślepkami `%s` (NIGDY f-string —
  SQL injection), `executemany`, `fetchall`/`fetchone` (wiersze to
  KROTKI), `polaczenie.commit()` po zapisie: temat 15.
- **Atrapa-szpieg** (FakeCursor/FakeConnection — zapisuje zapytania
  zamiast je wykonywać, test zagląda potem w notatki szpiega):
  budowałeś ją w temacie 15.
- **monkeypatch.setattr** (podmiana w module, w którym funkcja
  UŻYWA narzędzia) i **@pytest.mark.parametrize** (jeden test,
  wiele zestawów danych): tematy 11-13.
- **tmp_path**: temat 10 (tu prawie niepotrzebny — baza jest atrapą).

Jeśli coś z powyższych brzmi obco — wróć do tamtej teorii, zanim
zaczniesz.

---

## 3. NOWE pojęcie 1: czyszczenie tekstu — .replace() i .strip()

### Co to jest?

Metody stringów do sprzątania tekstu przed konwersją na liczbę:

```python
tekst = "  1 299,00 zł "
czysty = tekst.strip()                # "1 299,00 zł"
bez_waluty = czysty.replace(" zł", "")   # "1 299,00"
bez_spacji = bez_waluty.replace(" ", "")  # "1299,00"
z_kropka = bez_spacji.replace(",", ".")   # "1299.00"
liczba = float(z_kropka)                  # 1299.0
```

### Skąd się wzięło?

Strona sklepu pisze ceny DLA LUDZI: "99,90 zł" — z walutą,
przecinkiem, czasem spacjami. A `float()` czyta ceny DLA MASZYN:
kropka zamiast przecinka, żadnych liter. Ktoś musi przetłumaczyć —
i to jest właśnie czyszczenie danych, chleb powszedni każdego
scrapera.

### Dlaczego tak musi być?

- `tekst.strip()` — odcina białe znaki (spacje, entery) z OBU
  końców stringa; środka nie rusza.
- `tekst.replace(stare, nowe)` — zwraca NOWY string, w którym każde
  wystąpienie `stare` zamieniono na `nowe`. String w Pythonie jest
  niezmienny, więc wynik trzeba przypisać — `tekst.replace(...)`
  bez przypisania nic nie daje.
- `replace(",", ".")` przed `float()` — bo polski przecinek
  dziesiętny to dla `float()` błąd: `float("99,90")` rzuca
  `ValueError`. A skoro metka bywa też całkiem nieczytelna
  ("brak danych"), konwersję i tak ubezpieczasz znaną bramką
  try/except ValueError → kontrakt None (walidację z bramką
  ćwiczyłeś w M1).

### Typowe błędy początkujących

- `tekst.replace(",", ".")` bez przypisania wyniku — stringi są
  niezmienne, oryginał zostaje z przecinkiem.
- Kolejność: `float()` przed czyszczeniem — wybuch na pierwszej
  cenie z przecinkiem.
- `strip("zł")` zamiast `replace(" zł", "")` — strip zdejmuje ZNAKI
  z końców (i tylko z końców), nie napis; do usuwania napisu
  w środku/na końcu służy replace.

---

## 4. NOWE pojęcie 2: historia w bazie i „ostatni wpis"

### Co to jest?

Monitor cen NIE nadpisuje starej ceny — DOPISUJE nowy wiersz przy
każdym odczycie. Tabela `ceny` to dziennik: ta sama nazwa produktu
może wystąpić wiele razy, z różnymi datami:

```
id | nazwa      | cena   | data_odczytu
 1 | Klawiatura |  99.90 | 2026-07-01
 2 | Klawiatura |  89.90 | 2026-07-08
```

„Ostatnią cenę" wyciągasz zapytaniem, które znasz z tematu 14 —
sortowanie malejąco po dacie i tylko pierwszy wiersz:

```sql
SELECT cena FROM ceny WHERE nazwa = %s
ORDER BY data_odczytu DESC LIMIT 1
```

### Skąd się wzięło?

Gdybyś nadpisywał, po tygodniu wiedziałbyś tylko TYLE, ile kosztuje
dziś — a cały sens monitora to porównanie z przeszłością. Dziennik
(zapis przyrostowy) to standardowy wzorzec: tak działają logi,
historia konta w banku, rejestr temperatur.

### Dlaczego tak musi być?

- `WHERE nazwa = %s` — historia JEDNEGO produktu; parametr zawsze
  przez zaślepkę (temat 15).
- `ORDER BY data_odczytu DESC` — najświeższy wpis na górze.
- `LIMIT 1` + `fetchone()` — interesuje nas tylko ten najświeższy;
  fetchone zwraca KROTKĘ (np. `(89.90,)`) albo None, gdy produktu
  jeszcze nie ma w zeszycie — i to None jest dla nas informacją:
  „nowy produkt".
- Wartość z kolumny NUMERIC warto rzutować wbudowanym `float(...)`,
  żeby kontrakt funkcji (float albo None) był czysty niezależnie
  od typu, jakim baza oddaje liczby.

### Typowe błędy początkujących

- Brak `DESC` — dostajesz NAJSTARSZĄ cenę i raport kłamie.
- `fetchone()[0]` bez sprawdzenia None — dla nowego produktu
  TypeError; najpierw sprawdź `wiersz is None`.
- Nadpisywanie (UPDATE) zamiast dopisywania (INSERT) — tracisz
  historię, a z nią cały sens monitora.

---

## 5. Sekcja przekrojowa: architektura monitora

### Werdykt to wartość domenowa, nie błąd

Zadanie 11 zwraca status: "wzrost", "spadek", "bez zmian" albo
"nowy produkt". Czy to nie łamie zakazu „string jako błąd"? NIE —
zakaz dotyczy sygnalizowania AWARII stringiem (np. return "błąd
pliku"). Tu string to normalna, słownikowa odpowiedź funkcji
(jak nazwa koloru czy dzień tygodnia) — każda z czterech wartości
jest poprawnym wynikiem, żaden nie oznacza problemu. Awarie w tym
projekcie dalej sygnalizuje None (sieć padła) lub wyjątek.

### Funkcje bazodanowe dostają połączenie z zewnątrz

Zadania 06-10 i 12-13 przyjmują `polaczenie` jako argument, zamiast
same się łączyć. To celowe (znasz to z tematu 15): funkcja, która
dostaje połączenie, jest testowalna — test podaje atrapę-szpiega
i żadna prawdziwa baza nie jest potrzebna. Otwieranie połączenia
to obowiązek programu głównego, nie klocków.

### Kontrakt None płynie przez pipeline (jak w M1 i M2)

Gdy pobranie HTML zawiedzie (zadanie 01 → None), dyrygent całości
(zadanie 13) przerywa się early returnem i zwraca None — ZANIM
cokolwiek trafi do bazy. Nieczytelna metka pojedynczego produktu
to za to NIE awaria — ten jeden produkt się pomija (zadanie 04),
patrol trwa dalej.

---

## 6. Teoria testowa

### Po co conftest.py i sys.path.insert — przypomnienie

pytest odpalany z głównego folderu repo nie widzi modułu
`mini_monitor_cen.py`; `sys.path.insert(0, ...)` w conftest.py
dopisuje folder tematu do miejsc, w których Python szuka modułów.
conftest.py to też dom fixture i klas pomocniczych — pytest wczytuje
go automatycznie.

**Jak w M1 i M2: conftest dostajesz GOTOWY, bez TODO.** Są tam trzy
atrapy, które znasz z wcześniejszych tematów: FakeResponse (temat 12,
wersja z .text), FakeCursor i FakeConnection (temat 15 — tym razem
wypełnione, przeczytaj i porównaj ze swoją wersją). Przeczytaj
conftest uważnie: testując, będziesz zaglądać w notatki szpiega
(`kursor.wykonane`, `kursor.wykonane_wiele`, `liczba_commitow`).

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

1. **Co testuję?** — który klocek i który jego obowiązek.
2. **Co udaję?** — sieć (podmiana requests.get), czas (podmiana
   time.sleep) albo bazę (atrapa połączenia podana argumentem).
3. **Co sprawdzam?** — konkretny assert: wynik funkcji ALBO notatki
   szpiega (co zostało zapisane do „bazy").

Docstringi testów mają te odpowiedzi wypełnione — przekładasz je
na kod.

### Schemat przygotuj → podmień → wywołaj → sprawdź

Przykład na INNYM temacie niż ten projekt — funkcja `zaparz_herbate`,
która pod spodem czeka `time.sleep(180)`; test nie może czekać
3 minut, więc podmienia czekanie licznikiem:

```python
def test_zaparz_herbate_czeka_i_zwraca_napar(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pauzy = []                                     # przygotuj
    def podmieniony_sleep(sekundy):                # przygotuj
        pauzy.append(sekundy)
    monkeypatch.setattr(                           # podmień
        "kuchnia.time.sleep", podmieniony_sleep
    )
    wynik = zaparz_herbate("earl grey")            # wywołaj
    assert wynik == "napar: earl grey"             # sprawdź
    assert pauzy == [180]                          # sprawdź
```

Zwróć uwagę na dwie rzeczy: podmieniamy `time.sleep` W MODULE
`kuchnia` (tam, gdzie funkcja go używa — zasada z tematów 11-13),
a lista `pauzy` robi ze zwykłej funkcji szpiega: test sprawdza
nie tylko wynik, ale i to, CZY oraz JAK czekano. Dokładnie tak samo
podmienisz `time.sleep` i `requests.get` w module tego tematu.

Testy funkcji bazodanowych są prostsze — nic nie podmieniasz
monkeypatchem, bo atrapę połączenia podajesz po prostu argumentem
(po to właśnie klocki dostają połączenie z zewnątrz).

### Parametrize — przypomnienie (zazębienie z tematem 13)

Jeden z testów zadania 11 ma gotowy dekorator
`@pytest.mark.parametrize` z trzema zestawami danych — ten sam test
przebiega trzykrotnie, raz na zestaw. Mechanizm znasz z tematu 13;
tu tylko wypełniasz ciało korzystając z nazw parametrów z dekoratora.

### Gotowe atrapy i fixture w conftest.py tego projektu

| Nazwa                   | Co daje                                                  |
|-------------------------|----------------------------------------------------------|
| `FakeResponse`          | atrapa odpowiedzi HTTP: status_code, text, raise_for_status() |
| `FakeCursor`            | kursor-szpieg: notuje execute/executemany, udaje fetchall/fetchone, wspiera with |
| `FakeConnection`        | połączenie-atrapa: wydaje wspólny kursor, zlicza commity |
| `html_sklep`            | HTML strony sklepu: 3 produkty, w tym Monitor z nieczytelną ceną |
| `polaczenie_puste`      | FakeConnection bez żadnych wierszy (fetchone da None)    |
| `polaczenie_z_historia` | FakeConnection z zaprogramowaną ostatnią ceną (89.9,)    |

Dane kontrolne (sprawdź sam w conftest.py): Klawiatura "99,90 zł"
(po czyszczeniu 99.9), Mysz "49,00 zł" (49.0), Monitor "brak danych"
(odpada przy czyszczeniu).
