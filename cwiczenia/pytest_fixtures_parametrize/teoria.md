# pytest zaawansowany — fixtures, parametrize, raises, approx

## O czym jest ten temat?

Do tej pory pytest był twoim narzędziem pomocniczym — pisałeś testy
z gotowych szkieletów. Teraz pytest staje się tematem głównym: poznasz
narzędzia, które zamieniają dziesięć kopiuj-wklej testów w jeden elegancki,
i nauczysz się testować rzeczy „nietestowalne": błędy, floaty i zmienne
środowiskowe.

Zadania w tym temacie to celowo **proste funkcje** (kalkulator, walidator,
czytnik konfiguracji) — cała nowa wiedza siedzi w **testach**, które do nich
napiszesz.

---

## Fixture — wielokrotny rekwizyt testowy

### Co to jest?

Fixture to przygotowany zawczasu „rekwizyt" dla testów. Zamiast w każdym
teście od nowa budować te same dane (plik, słownik, obiekt), definiujesz
je raz i pytest **wstrzykuje** je do testu przez parametr.

Używałeś już cudzych fixtures (`tmp_path`, `monkeypatch`) i gotowych
własnych (`plik_csv`, `df_osoby`). Teraz zobaczysz, jak działają od środka.

```python
import pytest


@pytest.fixture
def koszyk() -> list[str]:
    return ["jablko", "chleb"]


def test_koszyk_ma_dwa_produkty(koszyk: list[str]) -> None:
    assert len(koszyk) == 2
```

Linijka po linijce:
- `@pytest.fixture` — dekorator: „ta funkcja to rekwizyt, nie test".
- `def koszyk()` — **nazwa funkcji staje się nazwą rekwizytu**.
- Test deklaruje parametr `koszyk` — pytest widzi zgodność nazw, wywołuje
  fixture i podaje jej wynik do testu. Żadnego importu, samo dopasowanie
  nazwy.

### Skąd się wzięło?

Z lenistwa (tego dobrego): zasada DRY — Don't Repeat Yourself. Dane
przygotowane w jednym miejscu naprawia się w jednym miejscu.

### Typowe błędy początkujących

- Wywołanie fixture wprost: `koszyk()` w teście — fixtures się nie wywołuje,
  pytest robi to za ciebie; ty tylko deklarujesz parametr.
- Literówka w nazwie parametru — pytest zgłosi
  `fixture 'kosyzk' not found` z listą dostępnych fixtures (czytaj ją!).

---

## scope — jak długo żyje rekwizyt

Domyślnie pytest tworzy fixture **od nowa dla każdego testu**. Czasem to
marnotrawstwo (np. kosztowne wczytanie dużego pliku). Parametr `scope`
kontroluje długość życia:

```python
@pytest.fixture                      # scope="function" — domyślny
def kubek_jednorazowy() -> list:
    return []


@pytest.fixture(scope="module")      # jeden na cały plik testów
def dzbanek_na_spotkanie() -> dict:
    return {"jezyk": "pl"}
```

- `scope="function"` (domyślny) — nowy egzemplarz dla **każdego testu**;
  jak kubek jednorazowy. Testy nie widzą nawzajem swoich zmian — najbezpieczniej.
- `scope="module"` — jeden egzemplarz na **cały plik testowy**; jak dzbanek
  postawiony na stole na całe spotkanie. Szybciej, ale jeśli jeden test
  dopisze coś do słownika, następny to zobaczy!
- `scope="session"` — jeden egzemplarz na **całe uruchomienie pytest**
  (wszystkie pliki); jak ekspres do kawy w biurze — włączany raz dziennie.

Zasada praktyczna: domyślny `function`, chyba że rekwizyt jest drogi
w przygotowaniu i **tylko do odczytu** — wtedy `module`/`session`.

### Typowe błędy początkujących

- Modyfikowanie fixture o scope="module" w teście — kolejne testy dostają
  „zabrudzony" obiekt i failują w losowej kolejności. Współdzielone
  rekwizyty traktuj jak tylko-do-odczytu.
- `scope=module` bez cudzysłowów — `NameError`; to string: `scope="module"`.

---

## conftest.py — wspólna szafa z rekwizytami

Fixture zdefiniowana w pliku testowym działa tylko w nim. Fixture
zdefiniowana w `conftest.py` jest widoczna **we wszystkich testach
w folderze** — bez żadnego importu. Dlatego wszystkie nasze tematy
trzymają fixtures właśnie tam.

Drugi obowiązek `conftest.py` w tym kursie — doklejenie folderu tematu
do listy miejsc, w których Python szuka modułów (bez tego
`test_pytest_fixtures_parametrize.py` nie znalazłby modułu
`pytest_fixtures_parametrize`):

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` → pełna ścieżka do `conftest.py`,
- `os.path.dirname(...)` → folder, w którym leży,
- `sys.path.insert(0, ...)` → wstaw na początek listy poszukiwań.

---

## parametrize — jeden test, wiele przypadków

### Co to jest?

Chcesz sprawdzić dzielenie dla pięciu par liczb. Pięć testów
kopiuj-wklej? Nie — jeden test i tabelka przypadków:

```python
import pytest


@pytest.mark.parametrize(
    "a, b, oczekiwane",
    [
        (10, 2, 5),
        (9, 3, 3),
        (7, 7, 1),
    ],
)
def test_dzielenie(a: int, b: int, oczekiwane: int) -> None:
    assert a / b == oczekiwane
```

Linijka po linijce:
- `@pytest.mark.parametrize(...)` — dekorator nad testem (pełna ścieżka:
  `pytest.mark.parametrize`, nie samo `parametrize`).
- Pierwszy argument: **string** z nazwami parametrów rozdzielonymi
  przecinkami — muszą pasować do parametrów funkcji testowej.
- Drugi argument: **lista krotek** — każda krotka to jeden zestaw wartości,
  w kolejności jak nazwy.
- pytest uruchomi test **trzy razy** — w raporcie zobaczysz
  `test_dzielenie[10-2-5]`, `test_dzielenie[9-3-3]`, `test_dzielenie[7-7-1]`.
  Jeden padnie — pozostałe i tak się wykonają, a raport powie który.

### Typowe błędy początkujących

- `@pytest.mark.parametrize(("a", "b"), ...)` z nazwami w osobnych
  stringach zadziała, ale konwencja kursu to jeden string `"a, b"`.
- Liczba wartości w krotce ≠ liczba nazw — pytest odmówi kolekcji testów.
- Zapomniany parametr w sygnaturze testu — `fixture 'oczekiwane' not found`
  (pytest szuka fixture o tej nazwie, bo nie znalazł jej w parametrize).

---

## pytest.raises — test, że funkcja rzuca wyjątek

### Co to jest?

Dobra funkcja rzuca wyjątek przy złych danych (kontrakt z tematu 4).
Jak przetestować, że NAPRAWDĘ rzuca? Zwykły assert nie zadziała —
wyjątek przerwałby test. `pytest.raises` to łapka na wyjątki:

```python
import pytest


def test_dzielenie_przez_zero_rzuca_wyjatek() -> None:
    with pytest.raises(ValueError):
        podziel(10, 0)
```

- `with pytest.raises(ValueError):` — blok-łapka: „oczekuję, że w środku
  poleci ValueError".
- Jeśli wyjątek poleci — test **przechodzi** (łapka go złapała).
- Jeśli NIE poleci — test **pada** z komunikatem `DID NOT RAISE`.
- Jeśli poleci inny typ wyjątku — test też pada.

Wywołanie testowanej funkcji musi być **wewnątrz** bloku `with`.

### Typowe błędy początkujących

- Wywołanie funkcji przed blokiem: wyjątek poleci za wcześnie i wywali test,
  zamiast zostać złapanym.
- `pytest.raises(ValueError())` z nawiasami — podajesz klasę wyjątku,
  nie jego egzemplarz: `pytest.raises(ValueError)`.
- assert po wywołaniu w tym samym bloku `with` — kod po rzuceniu wyjątku
  się nie wykona; asserty stawiaj poza blokiem.

---

## pytest.approx — porównywanie floatów

### Co to jest?

Komputer przechowuje ułamki dziesiętne w przybliżeniu. Efekt:

```python
0.1 + 0.2 == 0.3   # False!  (0.1 + 0.2 to 0.30000000000000004)
```

Assert z `==` na floatach to loteria. `pytest.approx` porównuje
„z rozsądną tolerancją":

```python
assert 0.1 + 0.2 == pytest.approx(0.3)          # True
assert wynik == pytest.approx(123.0)
```

- `pytest.approx(oczekiwana)` — opakowanie wartości oczekiwanej;
  porównanie `==` z nim przepuszcza mikroskopijne różnice.

Zasada kursu: **każde** porównanie floatów w assertach — przez
`pytest.approx`. Inty porównuj zwykłym `==`.

W zadaniu z polem koła spotkasz `math.pi` — stałą π z modułu wbudowanego
`math` (`import math`, `math.pi` ≈ 3.14159...).

### Typowe błędy początkujących

- `pytest.approx(wynik) == oczekiwana` — approx opakowuje wartość
  **oczekiwaną**, nie obliczoną (obie strony zadziałają, ale konwencja
  i czytelne komunikaty błędów są za `wynik == pytest.approx(oczekiwana)`).
- Approx na intach — niepotrzebne; inty są dokładne.

---

## Zmienne środowiskowe i monkeypatch.setenv

### Co to są zmienne środowiskowe?

To karteczki przyklejone do systemu operacyjnego: nazwa + wartość,
widoczne dla każdego programu. Trzyma się w nich konfigurację, której
nie wolno wpisywać w kod — hasła, klucze API, tryb pracy.

W Pythonie czyta się je przez `os.environ` (moduł wbudowany `os`):

```python
import os

wartosc = os.environ.get("TRYB_PRACY")   # str albo None, gdy nie ustawiona
```

- `os.environ` zachowuje się jak słownik — `.get(nazwa)` zwraca wartość
  lub `None` (wzorzec z tematu 3).

### Jak to przetestować? monkeypatch.setenv / delenv

Test nie może zależeć od tego, co akurat jest ustawione na twoim
komputerze. `monkeypatch` (znasz `setattr` z tematów 11-12) ma do tego
dwie dodatkowe metody:

```python
def test_czyta_tryb_pracy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRYB_PRACY", "testowy")      # ustaw na czas testu
    ...


def test_brak_zmiennej(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRYB_PRACY", raising=False)  # usuń na czas testu
    ...
```

- `setenv(nazwa, wartosc)` — ustawia zmienną; po teście pytest przywraca
  stan sprzed.
- `delenv(nazwa, raising=False)` — usuwa zmienną; `raising=False` znaczy
  „nie krzycz, jeśli i tak jej nie było" (bez tego — błąd, gdy zmienna
  nie istnieje).

### Typowe błędy początkujących

- `os.environ["TRYB_PRACY"] = "testowy"` wprost w teście — zmiana zostaje
  po teście i psuje inne testy; od tego jest monkeypatch, który sprząta.
- `setenv("TRYB_PRACY", 5)` — wartości zmiennych środowiskowych to zawsze
  **stringi**.

---

## Zazębienie: mock requests i pytest.raises w akcji

Z tematu 11 znasz podmianę `requests.get` przez `monkeypatch.setattr`
i atrapę `FakeResponse` (status_code, `.json()`, `.raise_for_status()`) —
w `conftest.py` czeka jej szkielet, a testy zadań 11-12 używają jej
dokładnie jak wtedy. Nowość: teraz połączysz mock z `pytest.raises`
(czy funkcja przepuszcza `requests.HTTPError`?) i z `pytest.approx`
(kursy walut to floaty). Kontrakt None przy `RequestException` —
wzorzec try/except z tematu 4.

---

## Teoria testowa

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie lub przypadek.
2. **Co udaje?** — fixture z danymi? podmieniony requests? ustawiona
   zmienna środowiskowa?
3. **Co sprawdzam?** — równość (approx dla floatów), wyjątek (raises),
   None (is None)?

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania — funkcja zwracająca powitanie
zależne od zmiennej środowiskowej z imieniem:

```python
# powitania.py
import os


def przywitaj() -> str:
    imie = os.environ.get("IMIE_UZYTKOWNIKA")
    if imie is None:
        return "Witaj, nieznajomy!"
    return f"Witaj, {imie}!"
```

```python
def test_przywitaj_uzywa_imienia(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy powitanie zawiera imię ze zmiennej środowiskowej.
    Co udaje: zmienną IMIE_UZYTKOWNIKA — setenv ustawia "Kasia" na czas testu.
    Co sprawdzam: wynik == "Witaj, Kasia!".
    """
    # przygotuj + podmień
    monkeypatch.setenv("IMIE_UZYTKOWNIKA", "Kasia")

    # wywołaj
    wynik = przywitaj()

    # sprawdź
    assert wynik == "Witaj, Kasia!"
```

W tym temacie „podmień" przybiera trzy postaci: `setenv`/`delenv`
(zmienne środowiskowe), `setattr` (requests) albo nic (czyste funkcje
liczbowe).
