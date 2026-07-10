# Playwright — podstawy (wersja sync) — teoria

## 1. Co to jest Playwright?

Znasz już Selenium z tematów 17-18 — robota, który klika w przeglądarkę
za Ciebie. **Playwright** to młodszy, nowocześniejszy robot tej samej
profesji, stworzony przez Microsoft. Robi to samo (otwiera strony,
klika, wpisuje), ale ma dwie supermoce, których Selenium nie ma
wbudowanych:

1. **Sam czeka** — nie musisz pisać „poczekaj, aż przycisk się pojawi";
   robot to wie.
2. **Szuka jak człowiek** — zamiast technicznych selektorów CSS pytasz
   „znajdź PRZYCISK o nazwie Wyślij", tak jak powiedziałbyś koledze.

W tym temacie używamy wersji SYNC (synchronicznej) — zwykłe funkcje,
bez `async`/`await` (choć po temacie 23 wiesz, że wersja async istnieje).

## 2. Instalacja — UWAGA, dwa kroki!

```
pip install playwright
playwright install chromium
```

- `pip install playwright` — instaluje bibliotekę Pythona (pilota).
- `playwright install chromium` — pobiera SAMĄ PRZEGLĄDARKĘ (telewizor).
  Playwright nie używa Twojego Chrome'a — ma własną, odizolowaną kopię
  przeglądarki Chromium.

### Typowe błędy początkujących
- Pominięcie drugiego kroku → błąd `Executable doesn't exist` przy
  pierwszym uruchomieniu. Pilot bez telewizora nie działa.

## 3. Rytuał startowy — sync_playwright

Każda przygoda z Playwright zaczyna się tym samym rytuałem:

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    tytul = page.title()
    browser.close()
```

Linijka po linijce:
- `from playwright.sync_api import sync_playwright` — import wersji
  synchronicznej (jest też `async_api` — nie w tym temacie).
- `with sync_playwright() as p:` — uruchom silnik Playwright; `with`
  (znasz z plików) gwarantuje zgaszenie silnika po wyjściu z bloku.
- `p.chromium.launch(headless=True)` — odpal przeglądarkę Chromium.
  `headless=True` = „bez głowy": przeglądarka działa niewidzialnie,
  bez okna na ekranie (szybciej; tak działa się w testach i CI).
  `headless=False` pokazałoby okno — przydatne, gdy chcesz PODEJRZEĆ,
  co robot robi.
- `browser.new_page()` — otwórz nową kartę. `page` to Twój główny
  bohater: KARTA przeglądarki, na której dzieje się wszystko.
- `page.goto("https://example.com")` — wpisz adres i wciśnij Enter.
- `page.title()` — odczytaj tytuł karty (to, co widać na zakładce
  przeglądarki; w HTML siedzi w znaczniku `<title>`).
- `browser.close()` — zamknij przeglądarkę (sprzątanie).

### Strona z pliku, bez internetu — file:// i set_content

Robot umie wejść nie tylko na strony w internecie. Adres może wskazywać
plik na dysku — taki adres zaczyna się od `file://`. Obiekt `Path`
(znasz z pathlib) sam buduje taki adres metodą `.as_uri()`:

```python
from pathlib import Path

sciezka = Path("C:/strony/test.html")
adres = sciezka.as_uri()   # "file:///C:/strony/test.html"
page.goto(adres)
```

Jest też droga jeszcze krótsza — wstrzyknąć HTML prosto do karty,
bez żadnego pliku:

```python
page.set_content("<html><body><h1>Czesc!</h1></body></html>")
```

- `page.set_content(html)` — „udawaj, że wczytałaś taką stronę".
  Karta renderuje podany HTML, jakby przyszedł z internetu. Idealne
  do testów: zero sieci, pełna kontrola nad treścią.

### Typowe błędy początkujących
- Użycie `page` po `browser.close()` → błąd — zamknięta przeglądarka
  nie ma kart.
- `goto("C:/strony/test.html")` bez `file://` → robot myśli, że to
  adres internetowy, i się wywala. Używaj `.as_uri()`.
- Zdziwienie, że przy `headless=True` „nic się nie dzieje" — dzieje
  się, tylko niewidzialnie.

## 4. Locatory — szukaj jak człowiek, nie jak koparka

W Selenium szukałeś elementów technicznie: `By.ID`, `By.CSS_SELECTOR`.
Problem: gdy programista strony zmieni id z `btn-2` na `btn-3`, Twój
test umiera, choć strona dla CZŁOWIEKA wygląda tak samo.

Playwright odwraca filozofię (locator-first): opisujesz element tak,
jak widzi go użytkownik. „Przycisk z napisem Wyślij" pozostaje
przyciskiem z napisem Wyślij niezależnie od id.

**Locator** to NAMIAR na element — karteczka z opisem „szukam
przycisku Wyślij". Ważne: utworzenie locatora NICZEGO jeszcze nie
szuka (jak wypisanie karteczki nie znajduje przedmiotu). Szukanie
odbywa się dopiero, gdy locatora UŻYJESZ (klik, odczyt).

### get_by_role — po roli elementu

Każdy element strony ma ROLĘ — nazwę jego funkcji, standardową dla
wszystkich stron świata (pochodzi ze standardu dostępności ARIA,
którego używają np. czytniki ekranu dla niewidomych):

| rola | co to na stronie |
|---|---|
| `"button"` | przycisk |
| `"link"` | odnośnik `<a>` |
| `"heading"` | nagłówek `<h1>`-`<h6>` |
| `"checkbox"` | pole do odhaczenia |
| `"textbox"` | pole tekstowe do wpisywania |
| `"status"` | obszar komunikatów o stanie (np. „zapisano!") |

```python
przycisk = page.get_by_role("button", name="Wyslij")
```

- `page.get_by_role("button", ...)` — „szukam elementu o roli przycisk".
- `name="Wyslij"` — zawężenie: ten z widocznym napisem „Wyslij".
  Bez `name` locator wskaże WSZYSTKIE przyciski na stronie naraz.

### get_by_text — po widocznym tekście

```python
napis = page.get_by_text("Najlepsze ceny w miescie")
```

- „szukam elementu zawierającego ten tekst" — dokładnie tak, jak
  człowiek skanuje stronę wzrokiem. Do akapitów, komunikatów, etykiet.

### get_by_label — po etykiecie pola formularza

W HTML pole formularza ma zwykle etykietę
(`<label for="imie">Imie</label> <input id="imie">`). Człowiek mówi
„wpisz coś w pole Imie" — i dokładnie tak mówisz robotowi:

```python
pole = page.get_by_label("Imie")
```

- Playwright sam znajduje `<label>` z tym tekstem i sam przechodzi
  do POŁĄCZONEGO z nim pola `<input>`. Ty nie musisz znać żadnych id.

### Typowe błędy początkujących
- `get_by_role("h1")` — `h1` to nazwa ZNACZNIKA, nie rola. Rola
  nagłówka to `"heading"`.
- Zdziwienie, że locator „nie rzucił błędu", choć elementu nie ma —
  locator to tylko karteczka z opisem; błąd wyskoczy dopiero przy
  próbie użycia.
- `get_by_text` do przycisków — zadziała, ale `get_by_role("button",
  name=...)` jest precyzyjniejsze (tekst może wystąpić też w akapicie).

## 5. Odczytywanie — co robot widzi

Gdy masz locator, możesz odpytać element:

```python
tekst = page.get_by_role("heading").inner_text()
wartosc = page.get_by_label("Imie").input_value()
adres = page.get_by_role("link", name="Kontakt").get_attribute("href")
ile = page.get_by_role("button").count()
widac = page.get_by_text("Promocja").is_visible()
odhaczone = page.get_by_role("checkbox").is_checked()
```

- `.inner_text()` — widoczny tekst elementu (np. treść nagłówka).
- `.input_value()` — AKTUALNA zawartość pola formularza (to, co jest
  wpisane teraz, nie to, co było w HTML na starcie).
- `.get_attribute("href")` — wartość atrybutu HTML; zwraca tekst albo
  `None`, gdy element nie ma takiego atrybutu.
- `.count()` — ile elementów pasuje do namiaru (locator może wskazywać
  wiele naraz). 0 = nie ma takiego elementu — to Twój sposób na
  sprawdzenie istnienia BEZ czekania i bez błędu.
- `.is_visible()` — czy element jest TERAZ widoczny (True/False).
  Uwaga: to MIGAWKA — zdjęcie zrobione natychmiast, bez czekania.
- `.is_checked()` — czy pole wyboru jest TERAZ odhaczone.

### Typowe błędy początkujących
- `.inner_text` bez nawiasów — to metoda, wywołuj z `()`.
- `.input_value()` na przycisku (nie-polu) → błąd; to metoda pól
  formularza.
- Użycie `.is_visible()` do elementu, który POJAWI SIĘ za chwilę —
  migawka złapie „jeszcze nie ma" i odda False. Do czekania służy
  `expect` (sekcja 7).

## 6. Akcje z auto-waiting — click, fill, check

```python
page.get_by_label("Imie").fill("Ada")
page.get_by_role("checkbox", name="Akceptuje regulamin").check()
page.get_by_role("button", name="Wyslij").click()
```

- `.fill("Ada")` — wyczyść pole i wpisz tekst (odpowiednik
  `send_keys` z Selenium, ale najpierw czyści).
- `.check()` — odhacz pole wyboru (jeśli już odhaczone — nic nie psuje).
- `.click()` — kliknij.

Supermoc nr 1 w akcji: **auto-waiting**. Zanim Playwright wykona
akcję, SAM czeka, aż element będzie „zdatny do akcji" (po angielsku
actionability): doczepiony do strony, widoczny, nieruchomy (nie w
trakcie animacji), odblokowany. Pamiętasz z Selenium mozolne
`WebDriverWait(driver, 10).until(expected_conditions...)`? Tu ta
cała maszyneria jest WBUDOWANA w każdą akcję. Jeśli element nie
stanie się zdatny w limicie czasu (domyślnie 30 s) — dopiero wtedy
błąd.

### Typowe błędy początkujących
- Ręczne wstawianie `time.sleep(2)` przed akcjami „na wszelki
  wypadek" — nawyk z Selenium; w Playwright to martwy balast,
  akcje same czekają.
- `.fill()` na checkboxie albo `.check()` na polu tekstowym —
  akcja musi pasować do rodzaju elementu.

## 7. expect + to_be_visible — asercja, która umie czekać

Do SPRAWDZANIA stanu strony Playwright daje własne asercje:

```python
from playwright.sync_api import expect


expect(page.get_by_text("Dziekujemy za zgloszenie")).to_be_visible()
expect(page.get_by_text("Promocja")).to_be_visible(timeout=2000)
```

- `expect(locator)` — „mam oczekiwanie wobec tego elementu".
- `.to_be_visible()` — „…że będzie widoczny". Kluczowe: expect
  CZEKA i PONAWIA sprawdzenie, aż się uda albo minie limit czasu.
  Strona pokazuje komunikat pół sekundy po kliknięciu? `is_visible()`
  (migawka) odda False, a `expect(...).to_be_visible()` cierpliwie
  poczeka i przejdzie.
- `timeout=2000` — własny limit w MILISEKUNDACH (2000 = 2 sekundy);
  domyślnie 5 sekund.
- Gdy limit minie, a elementu nie widać — expect rzuca
  `AssertionError` (ten sam typ błędu co zwykły assert).

Mapowanie na Selenium: `expect` to odpowiednik
`WebDriverWait + expected_conditions.visibility_of_element_located` —
w jednej czytelnej linijce.

### Typowe błędy początkujących
- `assert locator.is_visible()` tam, gdzie element dopiero się
  pojawi — migotliwy (flaky) test. Do „pojawi się" służy expect.
- `timeout=2` w sekundach — to MILISEKUNDY; 2 = 0.002 s i natychmiastowa
  porażka.
- Zapomnienie importu `expect` z `playwright.sync_api`.

## 8. Ściąga: Selenium → Playwright (zazębienie z tematów 17-18)

Wszystkie te pojęcia znasz z Selenium — tu tylko mapa przejścia:

| Selenium (tematy 17-18) | Playwright (ten temat) |
|---|---|
| `find_element(By.ID, ...)` / `By.CSS_SELECTOR` | locatory: `get_by_role` / `get_by_text` / `get_by_label` |
| `send_keys("Ada")` | `fill("Ada")` (najpierw czyści pole!) |
| `WebDriverWait(driver, 10).until(...)` | auto-waiting — wbudowane w każdą akcję |
| `expected_conditions.visibility_of_...` | `expect(...).to_be_visible()` |
| `driver.get(url)` | `page.goto(url)` |
| `driver.title` | `page.title()` |

## 9. Teoria testowa

### Po co jest conftest.py i co robi sys.path.insert

Gdy pytest uruchamia `test_playwright_podstawy.py`, ten plik robi
`from playwright_podstawy import ...`. Python szuka modułów tylko
w miejscach z listy `sys.path` — a folderu tematu tam nie ma (pytest
bywa uruchamiany z głównego folderu repo). Dlatego w `conftest.py`
(plik wczytywany przez pytest automatycznie, przed testami) dopisujemy
folder tematu na początek listy:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

- `os.path.abspath(__file__)` — pełna ścieżka do conftest.py,
- `os.path.dirname(...)` — utnij nazwę pliku, zostaw folder,
- `sys.path.insert(0, ...)` — wstaw folder na pozycję 0, żeby wygrał
  z innymi miejscami poszukiwań.

### Schemat 3 pytań — zanim napiszesz jakikolwiek test

W docstringu każdego testu odpowiadasz na trzy pytania:

1. **Co testuję?** — którą funkcję i które jej zachowanie.
2. **Co udaję?** — czego nie robię naprawdę (u nas: prawdziwych stron
   internetowych — zastępuje je HTML wstrzyknięty przez `set_content`)
   i czym to zastępuję.
3. **Co sprawdzam?** — jaki konkretnie assert kończy test.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Cztery fazy ciała testu (faza „podmień" bywa pusta). Przykład
z INNEJ dziedziny niż ten temat — funkcja licząca punkty w grze
w kręgle:

```python
def test_strike_daje_dziesiec_punktow() -> None:
    """Co testuje: czy zbicie wszystkich kregli daje 10 punktow.
    Co udaje: nic — czysta funkcja na liczbach.
    Co sprawdzam: wynik == 10.
    """
    zbite_kregle = [10]                    # przygotuj
    wynik = policz_punkty(zbite_kregle)    # wywołaj
    assert wynik == 10                     # sprawdź
```

W tym temacie faza „podmień" to wstrzyknięcie testowego HTML-a do
prawdziwej (ale niewidzialnej, headless) przeglądarki — funkcje
działają na karcie z NASZĄ treścią zamiast na cudzej stronie WWW.

### Fixture z yield — przygotuj, oddaj, POSPRZĄTAJ

Fixture znasz z poprzednich tematów: funkcja z `@pytest.fixture`,
której wynik pytest wstrzykuje do testu. Nowość: fixture z **yield**,
czyli z fazą sprzątania. Przeglądarki nie wolno tylko otworzyć —
trzeba ją też ZAMKNĄĆ, nawet gdy test się wywali:

```python
import pytest


@pytest.fixture
def kalkulator_z_plikiem():
    plik = otworz_plik_obliczen()   # przygotowanie (przed testem)
    yield plik                      # ODDAJ wartosc testowi i CZEKAJ
    plik.close()                    # sprzatanie (po tescie, ZAWSZE)
```

- `yield plik` — w tym miejscu fixture „zamarza": oddaje wartość
  testowi i czeka, aż test się skończy. To jak wypożyczalnia nart:
  wydaje sprzęt (yield), klient jeździ (test), sprzęt WRACA do
  serwisu (kod po yield) — nawet jeśli klient się wywrócił (test
  czerwony).
- kod PO yield wykonuje się po teście zawsze — to odpowiednik
  zamykania pliku w `finally`.

### scope="session" — jedna przeglądarka na wszystkie testy

Domyślnie pytest buduje fixture OD NOWA dla każdego testu. Odpalanie
przeglądarki trwa ~sekundę — 24 testy × sekunda = zmarnowane pół
minuty. Rozwiązanie: powiedz pytestowi, żeby zbudował fixture RAZ
i dzielił ją między testami:

```python
@pytest.fixture(scope="session")
def przegladarka():
    ...
```

- `scope="session"` — „żyj przez całą sesję testową": jedna
  przeglądarka od pierwszego do ostatniego testu. Karty (`page`)
  wciąż tworzymy świeże per test (są tanie) — dzielimy tylko drogi
  silnik. To jak jedna wypożyczalnia nart na cały sezon, ale każdy
  klient dostaje świeżo naostrzone narty.

Uwaga: silnik Playwright w fixture uruchamiamy bez `with` — przez
parę `sync_playwright().start()` / `.stop()`:

```python
p = sync_playwright().start()   # to samo co wejscie w blok with
browser = p.chromium.launch(headless=True)
yield browser
browser.close()
p.stop()                        # to samo co wyjscie z bloku with
```

- `with` nie przeżyje rozcięcia na „przed testem / po teście",
  a para `.start()`/`.stop()` — tak: start przed yield, stop po.

### pytest.raises — przypomnienie

Znasz z tematu o wyjątkach: `with pytest.raises(AssertionError):`
oznacza „ten blok MUSI rzucić taki wyjątek — jeśli nie rzuci, test
oblewa". Przyda się do sprawdzenia, że `expect` z krótkim timeoutem
naprawdę oblewa, gdy elementu nie ma.

### tmp_path i as_uri — plik HTML do testu zadania 01

`tmp_path` znasz: świeży folder tymczasowy od pytest. W teście
zadania 01 zapiszesz w nim plik `.html` (przez `write_text(...,
encoding="utf-8")`) i zamienisz ścieżkę na adres `file://` metodą
`.as_uri()` — dokładnie jak w sekcji 3.

### Typowe błędy początkujących
- Otwieranie przeglądarki w każdym teście z osobna zamiast we fixture —
  testy trwają wieki.
- Brak sprzątania po yield — po testach wiszą procesy przeglądarek.
- Testowanie na prawdziwej stronie WWW — jutro zmienią treść i test
  padnie bez winy kodu. `set_content` daje pełną kontrolę.

## 10. Co dalej

W zadaniach przejdziesz drogę: rytuał startowy i tytuł strony →
locatory (rola, tekst, etykieta) → odczyty (tekst, wartość, atrybut,
liczność, widoczność) → akcje z auto-waiting (fill, check, click) →
expect na elemencie pojawiającym się z opóźnieniem → pełny scenariusz
formularza — a na finał tłumacz pojęć Selenium→Playwright i scenariusz
logowania, który w temacie 17 pisałeś w Selenium.
