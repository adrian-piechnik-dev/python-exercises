# psycopg2 i SQLAlchemy — Python rozmawia z PostgreSQL

## Od sqlite do PostgreSQL

W temacie 14 ćwiczyłeś SQL na sqlite — bazie-notesiku żyjącym w pamięci
jednego programu. PostgreSQL to baza-**serwer**: osobny program (często na
innym komputerze), z którym łączy się wiele aplikacji naraz, z hasłami,
użytkownikami i danymi przeżywającymi restart.

SQL pozostaje ten sam (SELECT/WHERE/GROUP BY/JOIN — nic nie przepada!).
Zmienia się sposób **połączenia** — i tego dotyczy ten temat:

- `psycopg2` — sterownik: najniższy poziom, ręczne połączenia i kursory,
- `SQLAlchemy` — nakładka: „fabryka połączeń" (engine), z którą przyjaźni
  się pandas.

Instalacja obu (biblioteki zewnętrzne):

```
pip install psycopg2-binary sqlalchemy
```

(`psycopg2-binary` — wersja gotowa do użycia bez kompilatora C;
importuje się ją jako `psycopg2`.)

> **Jak ćwiczymy bez serwera?** Nie każę ci instalować PostgreSQL.
> Funkcje psycopg2 przetestujesz na **atrapach** połączeń (jak FakeResponse
> z tematu 11), a SQLAlchemy + pandas — na sqlite, bo engine obsługuje
> obie bazy identycznie. Twój kod będzie gotowy na prawdziwego Postgresa.

---

## psycopg2.connect — połączenie z serwerem

```python
import psycopg2

polaczenie = psycopg2.connect(
    host="localhost",
    dbname="sklep",
    user="anna",
    password="tajne123",
)
```

- `host` — adres serwera (`"localhost"` = ten sam komputer).
- `dbname` — nazwa bazy na serwerze (serwer może mieć ich wiele).
- `user`, `password` — logowanie; baza-serwer wymaga uwierzytelnienia.
- Zwraca obiekt połączenia — twój „telefon" do bazy.

Po pracy połączenie zamyka się przez `polaczenie.close()`.

### Typowe błędy początkujących

- `database="sklep"` — psycopg2 przyjmuje oba, ale konwencja kursu:
  `dbname`.
- Hasło w kodzie na stałe — w prawdziwych projektach hasła czyta się
  ze zmiennych środowiskowych (temat 13!); w ćwiczeniach przymykamy oko.

---

## cursor, execute, commit — rozmowa przez psycopg2

```python
kursor = polaczenie.cursor()
kursor.execute("SELECT nazwa, cena FROM produkty")
wiersze = kursor.fetchall()
```

- `polaczenie.cursor()` — tworzy kursor; w psycopg2 (inaczej niż w skrócie
  sqlite z tematu 14) kursor tworzy się **jawnie** i dopiero na nim woła
  execute.
- `fetchall()` / `fetchone()` — znasz z tematu 14: lista krotek / jedna
  krotka albo None.

### commit — zatwierdź zmiany

PostgreSQL pracuje w **transakcjach**: zmiany (INSERT/UPDATE/CREATE) są
najpierw „ołówkiem na brudno" i widzi je tylko twoje połączenie. Dopiero
`polaczenie.commit()` zapisuje je długopisem — na stałe, dla wszystkich:

```python
kursor.execute("INSERT INTO produkty (nazwa, cena) VALUES ('Mysz', 49)")
polaczenie.commit()   # bez tego INSERT przepadnie przy zamknięciu!
```

Wzorzec tego tematu dla każdej funkcji **zmieniającej** dane:
execute → **commit**. Funkcje tylko czytające (SELECT) commita nie
potrzebują.

### Typowe błędy początkujących

- Brak `commit()` po INSERT — program kończy się bez błędu, a danych
  w bazie nie ma. Najczęstszy błąd psycopg2.
- `kursor.commit()` — commit należy do **połączenia**, nie kursora.

---

## with — context manager od środka

`with` znasz od tematu o plikach: gwarantuje posprzątanie. Teraz zajrzymy
pod maskę, bo będziesz budować własne obiekty do `with`.

Obiekt nadaje się do `with`, jeśli ma dwie specjalne metody:

- `__enter__(self)` — wywoływana przy wejściu w blok; to, co zwróci,
  trafia za `as`,
- `__exit__(self, typ, wartosc, slad)` — wywoływana przy wyjściu z bloku
  (nawet po błędzie!); trzy parametry opisują ewentualny wyjątek.

Kursor psycopg2 jest takim obiektem, więc pisze się:

```python
with polaczenie.cursor() as kursor:
    kursor.execute("SELECT * FROM produkty")
    wiersze = kursor.fetchall()
# tu kursor już zamknięty — with zawołał __exit__
```

To wzorzec wszystkich funkcji w tym temacie: `with polaczenie.cursor()
as kursor:` zamiast luzem wiszącego kursora.

### Typowe błędy początkujących

- Używanie kursora **po** bloku with — kursor już zamknięty, dostaniesz
  błąd; wszystko, co potrzebuje kursora (execute, fetch), rób w środku.
- Mylenie poziomów: `with` zamyka **kursor**, nie połączenie —
  `polaczenie.commit()` może (i powinien) stać po bloku with.

---

## Zapytania parametryzowane — %s zamiast sklejania

### Dlaczego to najważniejsza sekcja tego tematu?

Wyobraź sobie, że budujesz zapytanie f-stringiem z danych od użytkownika:

```python
kursor.execute(f"SELECT * FROM uzytkownicy WHERE imie = '{imie}'")  # ŹLE!
```

Jeśli ktoś w polu „imię" wpisze `'; DROP TABLE uzytkownicy; --`,
twoje zapytanie zamieni się w DWA zapytania — drugie **kasuje tabelę**.
Ten atak nazywa się SQL injection i od dekad jest na szczycie listy
najgroźniejszych dziur bezpieczeństwa.

### Jak robić dobrze: %s + krotka

```python
kursor.execute(
    "SELECT * FROM uzytkownicy WHERE imie = %s",
    (imie,),
)
```

- `%s` — zaślepka w SQL; psycopg2 sam wstawi tam wartość, **bezpiecznie
  opakowaną** (żaden tekst nie „ucieknie" poza wartość).
- Drugi argument execute — **krotka wartości**, po jednej na każde `%s`,
  w kolejności występowania.
- Krotka jednoelementowa ma przecinek: `(imie,)` — bez niego to tylko
  nawiasy wokół zmiennej.
- `%s` używa się dla KAŻDEGO typu (tekst, liczba) — to nie jest
  formatowanie stringów Pythona, mimo mylącego wyglądu.

Dwie zaślepki:

```python
kursor.execute(
    "INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)",
    ("Klawiatura", 99.0),
)
```

### Typowe błędy początkujących

- f-string albo `+` do sklejania SQL z danymi — dziura bezpieczeństwa;
  **zawsze** %s.
- `execute(sql, imie)` — drugi argument musi być krotką (lub listą),
  nawet dla jednej wartości: `(imie,)`.
- `'%s'` w apostrofach w SQL — psycopg2 sam dba o apostrofy; zaślepka
  stoi goła: `= %s`.

---

## executemany — wiele wierszy jednym ruchem

Pętla z execute dla 500 wierszy = 500 okrążeń do bazy. `executemany`
robi to hurtem:

```python
produkty = [
    ("Klawiatura", 99.0),
    ("Mysz", 49.0),
    ("Monitor", 899.0),
]
kursor.executemany(
    "INSERT INTO produkty (nazwa, cena) VALUES (%s, %s)",
    produkty,
)
polaczenie.commit()
```

- Pierwszy argument: jedno zapytanie z `%s`.
- Drugi: **lista krotek** — zapytanie wykona się raz na każdą krotkę.

### Typowe błędy początkujących

- `executemany` z jedną krotką zamiast listy krotek — dostaniesz błąd
  albo wstawianie „po literce"; drugi argument to lista.

---

## psycopg2.Error — gdy serwer odmawia

Serwer może być wyłączony, hasło złe, sieć zerwana. Wszystkie błędy
psycopg2 dziedziczą po `psycopg2.Error` — łapiesz przodka, łapiesz
wszystko (dokładnie jak `requests.RequestException` w temacie 11):

```python
import psycopg2
from typing import Optional


def polacz_bezpiecznie(host: str, dbname: str) -> Optional[object]:
    try:
        return psycopg2.connect(host=host, dbname=dbname)
    except psycopg2.Error:
        return None
```

Kontrakt znasz z tematu 4: sukces → wartość, problem → `None`,
nigdy string-jako-błąd.

### Typowe błędy początkujących

- `except Error` bez przedrostka — `NameError`; pełna ścieżka
  `psycopg2.Error`.

---

## SQLAlchemy — fabryka połączeń dla pandas

### create_engine

psycopg2 to ręczna skrzynia biegów. `SQLAlchemy` daje automat: **engine** —
obiekt, który sam otwiera i oddaje połączenia, gdy ktoś (np. pandas)
o nie poprosi.

```python
from sqlalchemy import create_engine

silnik = create_engine("postgresql://anna:tajne123@localhost/sklep")
```

- Argument to **adres bazy** (URL) w formacie:
  `dialekt://uzytkownik:haslo@host/baza`.
- Ten sam mechanizm obsługuje różne bazy — zmienia się tylko dialekt:
  - PostgreSQL: `"postgresql://anna:tajne123@localhost/sklep"`,
  - sqlite (plik, bez serwera): `"sqlite:///C:/dane/test.db"` —
    trzy ukośniki, potem ścieżka pliku; loginu i hasła brak, bo to
    zwykły plik.

Dzięki temu w testach podstawiamy sqlite, a w produkcji PostgreSQL —
kod funkcji nie zmienia się ani o literę.

### pandas: to_sql i read_sql

pandas (tematy 8-9) umie gadać z bazą przez engine — DataFrame w obie
strony:

```python
import pandas as pd

df.to_sql("produkty", silnik, index=False, if_exists="replace")
df2 = pd.read_sql("SELECT * FROM produkty", silnik)
```

`to_sql` — DataFrame → tabela w bazie:
- `"produkty"` — nazwa tabeli (utworzy ją sam, z kolumn DataFrame),
- `silnik` — engine z create_engine,
- `index=False` — nie zapisuj indeksu jako kolumny (znasz z `to_excel`,
  temat 10),
- `if_exists="replace"` — jeśli tabela istnieje, zastąp ją (inne opcje:
  `"append"` — dopisz, `"fail"` — błąd; w kursie używamy `"replace"`).

`read_sql` — zapytanie SQL → DataFrame:
- pierwszy argument: dowolny SELECT (cały twój SQL z tematu 14 działa!),
- zwraca DataFrame z kolumnami jak w wyniku zapytania.

### Typowe błędy początkujących

- `df.to_sql(silnik, "produkty")` — kolejność: najpierw nazwa tabeli,
  potem engine.
- Zapomniane `index=False` — w tabeli ląduje śmieciowa kolumna `index`.
- `sqlite://plik.db` — za mało ukośników; plik lokalny to `sqlite:///`
  (trzy).

---

## Zazębienie w zadaniach 10-12

DataFrame i łańcuch `groupby → agg → reset_index` znasz z tematów 9-10 —
tu tylko przypomnienie jednym zdaniem: `df.groupby("miasto")
.agg({"sprzedaz": "sum"}).reset_index()` daje tabelkę miasto/suma
o zwykłych kolumnach. W zadaniu 12 taki raport polecisz prosto do bazy
przez `to_sql`.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak zawsze: pytest musi znaleźć moduł `psycopg2_sqlalchemy`, a folder
tematu nie jest w `sys.path`. `conftest.py` dokleja go na początek:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie funkcji.
2. **Co udaje?** — tu aż dwa światy: dla psycopg2 udajemy CAŁE połączenie
   (atrapy FakeConnection/FakeCursor), dla SQLAlchemy nic nie udajemy —
   engine dostaje prawdziwego sqlite w pliku tymczasowym.
3. **Co sprawdzam?** — wysłane zapytanie/parametry (atrapa je zapamiętała)
   albo zawartość bazy (odczyt przez read_sql).

### Atrapa-szpieg: FakeConnection i FakeCursor

Prawdziwej bazy nie ma, więc skąd wiadomo, że funkcja działa? Sprawdzamy,
**co funkcja chciała wysłać**. Atrapa zapisuje każde wywołanie do listy —
to ten sam chwyt, co zapamiętywanie `params`/`headers` w temacie 11,
ale ubrany w klasę:

```python
class FakeCursor:
    def __init__(self, wiersze):
        self.wiersze = wiersze        # co udawać przy fetch
        self.wykonane = []            # szpieg: zapis każdego execute

    def execute(self, sql, parametry=None):
        self.wykonane.append((sql, parametry))

    def fetchall(self):
        return self.wiersze

    def __enter__(self):
        return self                   # to trafia za "as" w with

    def __exit__(self, typ, wartosc, slad):
        return None                   # nie połykaj wyjątków
```

`__enter__`/`__exit__` — znasz z sekcji o with: dzięki nim atrapa
przeżyje `with polaczenie.cursor() as kursor:` dokładnie jak prawdziwy
kursor. `FakeConnection` analogicznie: `cursor()` zwraca szpiega,
`commit()` zlicza wywołania.

W teście zaglądasz szpiegowi w notatki:

```python
sql, parametry = polaczenie.kursor.wykonane[0]
assert "%s" in sql
assert parametry == ("Klawiatura", 99.0)
```

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania — wysyłacz SMS-ów:

```python
# powiadomienia.py
def wyslij_alarm(klient_sms, numer: str) -> None:
    klient_sms.wyslij(numer, "ALARM: temperatura za wysoka")
```

```python
class FakeKlientSms:
    def __init__(self):
        self.wyslane = []

    def wyslij(self, numer, tresc):
        self.wyslane.append((numer, tresc))


def test_wyslij_alarm_wysyla_na_wlasciwy_numer() -> None:
    """Co testuje: czy alarm idzie na podany numer z właściwą treścią.
    Co udaje: klienta SMS — atrapa-szpieg zapisuje wysyłki zamiast słać.
    Co sprawdzam: lista wyslane zawiera (numer, treść z 'ALARM').
    """
    # przygotuj (podmiana przez wstrzyknięcie atrapy jako argument)
    klient = FakeKlientSms()

    # wywołaj
    wyslij_alarm(klient, "500600700")

    # sprawdź
    assert klient.wyslane[0][0] == "500600700"
    assert "ALARM" in klient.wyslane[0][1]
```

Zauważ: tu nie trzeba monkeypatcha — funkcja **dostaje** zależność jako
argument, więc podmiana to po prostu podanie atrapy. Tak samo działa
większość zadań tego tematu (funkcje dostają `polaczenie`). Monkeypatch
(`"psycopg2_sqlalchemy.psycopg2.connect"`) potrzebny jest tylko tam,
gdzie funkcja sama tworzy połączenie (zadania 1 i 7).

### Fixture silnika sqlite (dla zadań 9-12)

W `conftest.py` przygotujesz fixture z prawdziwym engine wskazującym
plik w `tmp_path` — baza powstaje na czas testu i znika z folderem
tymczasowym:

```python
silnik = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
```
