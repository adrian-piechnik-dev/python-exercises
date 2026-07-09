# Selenium — robot sterujący przeglądarką

## Co to jest Selenium?

BeautifulSoup (temat 12) czytał strony jak gazetę — statyczny HTML.
Ale nowoczesne strony to nie gazety, tylko **aplikacje**: trzeba kliknąć,
wpisać hasło, poczekać aż coś się doładuje. Selenium to robot, który
siada przed prawdziwą przeglądarką i robi w niej to, co człowiek:
otwiera strony, klika przyciski, wypełnia formularze.

Główne zastosowania: automatyzacja żmudnych czynności i **testowanie
aplikacji webowych** (robot przechodzi przez stronę i sprawdza, czy
wszystko działa).

Instalacja:

```
pip install selenium
```

Selenium steruje przeglądarką przez program-pośrednik (**chromedriver**
dla Chrome). Nowe wersje Selenium same go pobierają (Selenium Manager),
więc zwykle wystarczy mieć Chrome.

> **Jak ćwiczymy bez otwierania Chrome?** Testy w tym temacie NIE
> uruchamiają przeglądarki — funkcje dostają drivera jako argument,
> a testy podstawiają atrapę (jak FakeConnection w temacie 15).
> Twój kod jest gotowy na prawdziwego Chrome, ale testy śmigają
> w ułamku sekundy i działają wszędzie.

---

## Options — konfiguracja przeglądarki przed startem

Zanim robot uruchomi przeglądarkę, można ją skonfigurować:

```python
from selenium.webdriver.chrome.options import Options

opcje = Options()
opcje.add_argument("--headless=new")
opcje.add_argument("--window-size=1920,1080")
```

- `Options()` — pusty zestaw ustawień Chrome.
- `add_argument("--headless=new")` — tryb **bezgłowy**: przeglądarka
  pracuje bez okna (niewidzialna). Niezbędne na serwerach bez ekranu
  i przy automatyzacji w tle. `=new` to nowa, lepsza wersja trybu.
- `add_argument("--window-size=1920,1080")` — rozmiar okna; w trybie
  headless bez tego strona może dostać malutki viewport i inaczej się
  ułożyć.
- Dodane argumenty można obejrzeć w liście `opcje.arguments` —
  przyda się w testach.

### Typowe błędy początkujących

- `opcje.add_argument(headless)` — argument to string z myślnikami:
  `"--headless=new"`.
- Ustawianie opcji PO uruchomieniu przeglądarki — opcje działają tylko
  przy starcie; potem jest za późno.

---

## Service i webdriver.Chrome — start robota

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

serwis = Service("C:/sterowniki/chromedriver.exe")
driver = webdriver.Chrome(service=serwis, options=opcje)
```

- `Service(sciezka)` — opakowanie na chromedrivera: mówi Selenium,
  gdzie leży program-pośrednik (przy Selenium Manager ścieżkę można
  pominąć, ale w kursie podajemy ją jawnie — pełna kontrola).
- `webdriver.Chrome(service=..., options=...)` — uruchamia przeglądarkę
  i zwraca **drivera**: pilota do niej. Wszystko dalej robisz driverem.

### Podstawowe ruchy drivera

```python
driver.get("https://sklep.przyklad.pl")   # otwórz adres i CZEKAJ na stronę
print(driver.title)                        # tytuł karty (pasek przeglądarki)
driver.quit()                              # zamknij przeglądarkę CAŁKOWICIE
```

- `get(url)` — nawigacja; wraca, gdy strona jest zasadniczo wczytana.
- `title` — atrybut (bez nawiasów!) z tytułem bieżącej strony.
- `quit()` — gasi przeglądarkę i sprząta procesy. **Obowiązkowy** —
  bez niego po każdym uruchomieniu zostaje wiszący Chrome w pamięci.

### Typowe błędy początkujących

- `driver.title()` z nawiasami — title to atrybut, nie metoda.
- `close()` zamiast `quit()` — close zamyka jedną kartę, quit całą
  przeglądarkę; w kursie zawsze quit.

---

## try/finally — sprzątanie gwarantowane

Znasz `try/except` (temat 4) — łapanie błędów. Blok `finally` to trzeci
element układanki: kod, który wykona się **ZAWSZE** — po sukcesie,
po wyjątku, nawet po `return`:

```python
driver = webdriver.Chrome(service=serwis, options=opcje)
try:
    driver.get("https://sklep.przyklad.pl")
    return driver.title
finally:
    driver.quit()   # wykona się także, gdy get wybuchnie!
```

Analogia: wychodzisz z domu — czy dzień był udany, czy nie, drzwi
zamykasz zawsze. Bez `finally` wyjątek w `get` przeskoczyłby `quit()`
i przeglądarka wisiałaby do końca świata.

Wzorzec: **stwórz drivera PRZED try** (jak się nie uda, nie ma czego
sprzątać), pracę rób w `try`, `quit()` w `finally`.

### Typowe błędy początkujących

- `driver = webdriver.Chrome(...)` wewnątrz try z quit w finally —
  jeśli sam start się nie uda, finally zawoła quit na nieistniejącej
  zmiennej (`NameError`). Twórz drivera przed try.
- `finally` z `return` w środku — połyka wyjątki; w finally tylko
  sprzątanie.

---

## By i find_element — szukanie na stronie

Robot musi wskazać element, zanim go kliknie. Adresowanie elementów
robi się parą: **strategia** (By) + **wartość**:

```python
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, "koszyk")
przyciski = driver.find_elements(By.CLASS_NAME, "przycisk")
naglowek = driver.find_element(By.CSS_SELECTOR, "div.oferta h2")
```

- `By.ID` — po atrybucie `id` (znasz z tematu 12: id jest unikalne).
- `By.CLASS_NAME` — po klasie CSS (jedna nazwa klasy, bez kropki!).
- `By.CSS_SELECTOR` — pełne selektory CSS z tematu 12 (`div.oferta h2`,
  `#stopka`...) — najuniwersalniejsza strategia.
- `find_element` (pojedynczy) — zwraca PIERWSZY pasujący element;
  gdy nie ma żadnego — rzuca `NoSuchElementException` (nie None!).
- `find_elements` (liczba mnoga) — zwraca LISTĘ; pustą, gdy brak
  dopasowań (nie wyjątek!). Ta niesymetria to częsta pułapka.

Z elementu można wyciągnąć tekst:

```python
print(element.text)   # widoczny tekst elementu
```

### Typowe błędy początkujących

- `find_element("koszyk")` — brak strategii; zawsze para:
  `find_element(By.ID, "koszyk")`.
- `By.CLASS_NAME, "div.przycisk"` — CLASS_NAME przyjmuje samą nazwę
  klasy (`"przycisk"`); kropki i tagi to składnia CSS_SELECTOR.
- Oczekiwanie None od find_element — brak elementu to WYJĄTEK
  `NoSuchElementException`; None-owy kontrakt musisz zbudować sam
  (try/except).

---

## send_keys i click — ręce robota

```python
pole_login = driver.find_element(By.ID, "login")
pole_login.send_keys("anna")

przycisk = driver.find_element(By.ID, "zaloguj")
przycisk.click()
```

- `send_keys(tekst)` — wpisuje tekst do pola (jak stukanie w klawiaturę).
- `click()` — klika element.
- Typowy scenariusz logowania: znajdź pole → wpisz → znajdź pole → wpisz
  → znajdź przycisk → kliknij.

### Typowe błędy początkujących

- `send_keys` na przycisku albo `click` na polu tekstowym — działa
  „dziwnie"; najpierw upewnij się, CO znalazłeś.
- Zapominanie, że każde `find_element` szuka OD NOWA — element
  wygodnie złapać do zmiennej.

---

## WebDriverWait — cierpliwość robota

Strony ładują się w kawałkach: klikniesz „szukaj", a wyniki pojawiają
się po sekundzie. Robot bez cierpliwości szuka elementu NATYCHMIAST
i wywala się, bo jeszcze go nie ma. `WebDriverWait` to czekanie
z limitem:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

czekacz = WebDriverWait(driver, 10)
element = czekacz.until(
    EC.presence_of_element_located((By.ID, "wyniki"))
)
```

- `WebDriverWait(driver, 10)` — czekaj maksymalnie 10 sekund,
  sprawdzając co pół sekundy.
- `until(warunek)` — powtarzaj sprawdzanie, aż warunek się spełni;
  wtedy zwróć znaleziony element.
- `EC.presence_of_element_located(lokator)` — warunek „element jest
  w HTML strony". Konwencja importu: `as EC` (wszyscy tak piszą).
- Lokator to **krotka** `(By.ID, "wyniki")` — nawiasy podwójne
  w wywołaniu: zewnętrzne od funkcji, wewnętrzne od krotki!

### TimeoutException — cierpliwość się skończyła

Gdy limit minie, a elementu nie ma, WebDriverWait rzuca
`TimeoutException`:

```python
from selenium.common.exceptions import TimeoutException

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "wyniki"))
    )
except TimeoutException:
    element = None
```

Kontrakt None przez try/except znasz z tematu 4 — tu tylko nowy wyjątek.

### Typowe błędy początkujących

- `EC.presence_of_element_located(By.ID, "wyniki")` — zjedzone nawiasy
  krotki; lokator to JEDEN argument-krotka: `((By.ID, "wyniki"))`.
- `time.sleep(10)` zamiast WebDriverWait — śpisz zawsze 10 sekund,
  nawet gdy element pojawił się po pół sekundy; wait kończy od razu.

---

## logging — dziennik pokładowy programu (NOWOŚĆ w stdlib)

### Po co, skoro jest print?

Robot klika w tle (headless) na serwerze — nie widzisz, co robi.
Gdy coś padnie o 3 w nocy, potrzebujesz **dziennika**: co się działo,
w jakiej kolejności, z jakimi danymi. `print` to za mało: nie ma
poziomów ważności, czasu, ani wyłącznika. `logging` (moduł wbudowany)
ma wszystko.

### Logger i poziomy

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("szczegół techniczny: %s", dane)
logger.info("Otwieram strone %s", url)
logger.warning("strona wolno odpowiada")
logger.error("nie udalo sie zaladowac strony")
```

- `logging.getLogger(__name__)` — daje logger nazwany jak twój moduł
  (`__name__` to nazwa pliku widziana przez Pythona). Po nazwie
  w dzienniku wiadomo, KTO pisał. Tworzy się go raz, na górze modułu,
  zaraz po importach.
- Poziomy od najcichszego: `debug` (szczegóły dla programisty),
  `info` (normalne wydarzenia), `warning` (niepokojące, ale działa),
  `error` (coś się nie udało).

### Wstawianie wartości: %s i przecinek (nie f-string!)

```python
logger.info("Otwieram strone %s", url)        # DOBRZE
logger.info(f"Otwieram strone {url}")          # ŹLE (w logging)
```

Zaślepka `%s` + wartość po przecinku — logging sam sklei tekst,
ale **tylko jeśli wpis faktycznie trafia do dziennika**. F-string
skleja ZAWSZE, nawet gdy logowanie wyłączone — marnuje pracę. To
konwencja logging (nie myl z `%s` z psycopg2 — zbieżność przypadkowa).

### basicConfig — włącznik dziennika

Sam logger pisze „do szuflady". Żeby wpisy było widać na ekranie,
program GŁÓWNY (nie moduł-biblioteka!) włącza dziennik raz:

```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
```

- `level=logging.INFO` — pokazuj INFO i ważniejsze (bez debug).
- Umieszczasz to w bloku `if __name__ == "__main__":` (temat 4) —
  konfiguruje ten, kto URUCHAMIA program; moduły tylko piszą do loggera.
  W testach dziennik przechwytuje pytest — bez żadnej konfiguracji.

### Typowe błędy początkujących

- f-string w logger.info — działa, ale psuje sens leniwego sklejania;
  w kursie zawsze `%s` + przecinek.
- `logging.info(...)` wprost zamiast własnego loggera — pisze do
  anonimowego root-loggera; twórz `logger = logging.getLogger(__name__)`.
- `basicConfig` w module-bibliotece — konfigurację narzuca się każdemu,
  kto zaimportuje twój plik; basicConfig tylko pod `__main__`.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak zawsze: pytest musi znaleźć moduł `selenium_podstawy`; conftest.py
dokleja folder tematu na początek `sys.path`:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie funkcji.
2. **Co udaje?** — przeglądarkę: FakeDriver/FakeElement zamiast Chrome;
   czasem też `webdriver.Chrome` przez monkeypatch (gdy funkcja sama
   tworzy drivera).
3. **Co sprawdzam?** — notatki szpiega (co robot chciał zrobić) albo
   zwróconą wartość.

### FakeDriver i FakeElement — przeglądarka-atrapa

Wzorzec atrapy-szpiega znasz z tematu 15 (FakeConnection zapisujący
zapytania). Tu tak samo: `FakeElement` udaje element strony (ma `.text`,
zapisuje `send_keys` i `click`), a `FakeDriver` udaje przeglądarkę
(pamiętane elementy, zapis odwiedzanych adresów, flaga po `quit`).

Kluczowy szczegół: `find_element` atrapy dla nieznanego lokatora
**rzuca `NoSuchElementException`** — dokładnie jak prawdziwy driver.
Dzięki temu prawdziwy `WebDriverWait` działa na atrapie: odpytuje
`find_element` w kółko i albo dostaje element, albo po limicie rzuca
`TimeoutException`. Czekanie testujemy więc NAPRAWDĘ (z krótkim limitem,
np. 1 sekunda, żeby test nie mielił).

### caplog — podsłuch dziennika (NOWY fixture pytest)

Jak sprawdzić, że funkcja zapisała coś do logging? Pytest ma wbudowany
fixture `caplog` — przechwytuje wpisy dziennika na czas testu:

```python
def test_przyklad(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)          # od jakiego poziomu łapać
    funkcja_ktora_loguje()
    assert "Otwieram strone" in caplog.text  # caplog.text = sklejone wpisy
```

- `caplog.set_level(logging.INFO)` — na początku testu: łap INFO wzwyż.
- `caplog.text` — wszystkie przechwycone wpisy jako jeden string;
  sprawdzasz w nim fragmenty przez `in`.

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania — automat parkingowy i atrapa
szlabanu:

```python
# parking.py
def wpusc_auto(szlaban, numer_rejestracyjny: str) -> None:
    szlaban.podnies()
    szlaban.wyswietl(numer_rejestracyjny)
```

```python
class FakeSzlaban:
    def __init__(self):
        self.podniesiony = False
        self.wyswietlone = []

    def podnies(self):
        self.podniesiony = True

    def wyswietl(self, tekst):
        self.wyswietlone.append(tekst)


def test_wpusc_auto_podnosi_szlaban() -> None:
    """Co testuje: czy wpuszczenie auta podnosi szlaban i pokazuje numer.
    Co udaje: szlaban — atrapa zapisuje ruchy zamiast ruszać silnikiem.
    Co sprawdzam: podniesiony is True i numer na wyświetlaczu.
    """
    # przygotuj (podmiana przez wstrzyknięcie atrapy)
    szlaban = FakeSzlaban()

    # wywołaj
    wpusc_auto(szlaban, "WA12345")

    # sprawdź
    assert szlaban.podniesiony is True
    assert szlaban.wyswietlone == ["WA12345"]
```

Większość zadań dostaje drivera jako argument — podmiana to podanie
atrapy. Monkeypatch (`"selenium_podstawy.webdriver.Chrome"`) potrzebny
tylko tam, gdzie funkcja sama uruchamia przeglądarkę (zadania 2 i 12).
