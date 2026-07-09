# Selenium — zrzuty ekranu i alerty

## Kontynuacja tematu 17

Drivera, By, WebDriverWait i try/finally znasz z tematu 17 — tu nic się
nie zmienia: funkcje dalej dostają drivera jako argument, a testy
podstawiają atrapę. Ten temat dokłada robotowi dwie umiejętności:
**robienie zdjęć** (zrzuty ekranu) i **rozmowę z wyskakującymi
okienkami** (alertami).

---

## save_screenshot — zdjęcie tego, co widzi robot

### Po co?

Robot pracuje w tle (headless) — nie widzisz, co się dzieje. Gdy
scenariusz padnie o 3 w nocy, zrzut ekranu to twój materiał dowodowy:
JAK wyglądała strona w chwili awarii. Zrzuty robi się też do raportów
(„tak wyglądał sklep po dodaniu produktu").

```python
wynik = driver.save_screenshot("C:/zrzuty/blad_logowania.png")
print(wynik)   # True — zapis się udał
```

- `save_screenshot(sciezka)` — zapisuje aktualny widok strony do pliku
  PNG i zwraca **bool**: `True` przy sukcesie.
- Ścieżka musi kończyć się na `.png` — inne rozszerzenia Selenium
  odrzuca (z ostrzeżeniem, zapisując i tak PNG).
- **Ścieżka musi być stringiem.** I tu wchodzi zazębienie…

### Path → str — pułapka typów

Z tematu 4 znasz `pathlib.Path` — wygodne budowanie ścieżek operatorem
`/`:

```python
from pathlib import Path

folder = Path("C:/zrzuty")
sciezka = folder / "logowanie.png"     # Path — sklejanie operatorem /
```

Ale `save_screenshot` to starsze API — chce **stringa**, nie Path.
Konwersja to zwykłe `str()`:

```python
driver.save_screenshot(str(sciezka))   # Path zamieniony na string
```

Wzorzec kursu: ścieżki buduj Pathem (czytelnie, przenośnie), a do
save_screenshot podawaj `str(sciezka)`.

### Typowe błędy początkujących

- `save_screenshot(sciezka)` z gołym Path — nowsze wersje Selenium to
  przełkną, starsze nie; konwencja kursu: zawsze `str()`.
- Zrzut do nieistniejącego folderu — plik się nie zapisze
  (`save_screenshot` zwróci False); folder musi istnieć wcześniej.
- Nazwa bez `.png` — ostrzeżenie i niespodzianka w nazwie pliku.

---

## Alerty — okienka, które blokują stronę

### Co to jest?

Strona potrafi wyskoczyć z małym systemowym okienkiem: „Czy na pewno
usunąć?" z przyciskami OK/Anuluj. To **alert JavaScript** — blokuje całą
stronę, dopóki człowiek (albo robot) go nie obsłuży. Zwykłe
`find_element` go NIE widzi — alert nie jest elementem HTML, żyje
piętro wyżej, w przeglądarce.

### switch_to.alert — podejdź do okienka

```python
alert = driver.switch_to.alert
print(alert.text)    # treść okienka, np. "Czy na pewno usunac?"
alert.accept()       # kliknij OK / Tak
```

- `driver.switch_to.alert` — atrybut (bez nawiasów!): przełącza uwagę
  robota ze strony na alert i zwraca uchwyt do niego.
- `alert.text` — treść komunikatu (też atrybut).
- `alert.accept()` — potwierdź (OK / Tak / Zatwierdź).
- `alert.dismiss()` — odrzuć (Anuluj / Nie / krzyżyk).

Po `accept()`/`dismiss()` alert znika i robot wraca do strony.

### NoAlertPresentException — a jak okienka nie ma?

`driver.switch_to.alert` przy BRAKU alertu rzuca
`NoAlertPresentException`:

```python
from selenium.common.exceptions import NoAlertPresentException

try:
    alert = driver.switch_to.alert
    tresc = alert.text
except NoAlertPresentException:
    tresc = None
```

Kontrakt None przez try/except — wzorzec z tematu 4, nowy wyjątek.

### Typowe błędy początkujących

- `driver.switch_to.alert()` z nawiasami — to atrybut, nie metoda.
- Szukanie alertu przez `find_element` — alert nie jest w HTML;
  tylko `switch_to.alert`.
- `accept()` bez wcześniejszego złapania alertu do zmiennej — da się
  (`driver.switch_to.alert.accept()`), ale gdy chcesz najpierw
  przeczytać `.text`, złap alert do zmiennej raz.

---

## alert_is_present — czekanie na alert

Alert często wyskakuje z opóźnieniem (po zapisie, po odpowiedzi
serwera). `WebDriverWait` znasz z tematu 17 — tu nowy warunek,
**bez lokatora**, bo alert jest tylko jeden:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
alert.accept()
```

- `EC.alert_is_present()` — nawiasy puste! Warunek „jakikolwiek alert
  jest na ekranie"; żadnej krotki-lokatora (porównaj:
  `presence_of_element_located((By.ID, ...))` z tematu 17).
- `until(...)` zwraca **uchwyt do alertu** — od razu można
  `.text` / `.accept()`.
- Brak alertu w limicie → `TimeoutException` (znasz z tematu 17).

### Typowe błędy początkujących

- `EC.alert_is_present((By.ID, "alert"))` — ten warunek NIE przyjmuje
  lokatora; puste nawiasy.
- `EC.alert_is_present` bez nawiasów wywołania — podajesz funkcję
  zamiast warunku; `until` się wywali.

---

## Teoria testowa

### Po co conftest.py i sys.path.insert?

Jak zawsze: pytest musi znaleźć moduł `selenium_alerty_screenshoty`,
a folder tematu nie jest w `sys.path`. `conftest.py` dokleja go:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### Trzy pytania przed każdym testem

1. **Co testuje?** — konkretne zachowanie funkcji.
2. **Co udaje?** — przeglądarkę i alert: FakeDriver z FakeAlert
   (albo bez — dla scenariuszy „alertu nie ma"); dysk udaje tmp_path.
3. **Co sprawdzam?** — notatki atrap (kliknięto accept?), istnienie
   pliku zrzutu, zwróconą wartość.

### FakeDriver tego tematu

Atrapa jest prostsza niż w temacie 17 (bez find_element), za to umie
dwie nowe rzeczy:

- `save_screenshot(sciezka)` — zapisuje ścieżkę do notatek
  **i naprawdę tworzy plik** (z podrobioną zawartością) — dzięki temu
  testy sprawdzają istnienie pliku przez `Path.exists()`, jak przy
  prawdziwym driverze. Zwraca True.
- `switch_to` — obiekt z atrybutem `alert`, który zwraca FakeAlert
  albo rzuca `NoAlertPresentException` (jak prawdziwy driver).

`FakeAlert` to klasyczna atrapa-szpieg (temat 15): ma `.text`
i zlicza wywołania `accept()`/`dismiss()`.

### property — atrybut, który jest metodą w przebraniu (NOWOŚĆ)

Prawdziwe `driver.switch_to.alert` to **atrybut** (bez nawiasów),
a mimo to potrafi RZUCIĆ wyjątek. Jak? Pod spodem siedzi metoda
przebrana za atrybut — dekorator `@property`:

```python
class FakeSwitchTo:
    def __init__(self, alert):
        self._alert = alert            # None = alertu nie ma

    @property
    def alert(self):
        if self._alert is None:
            raise NoAlertPresentException("brak alertu")
        return self._alert
```

- `@property` nad metodą — od teraz `obiekt.alert` (BEZ nawiasów)
  wykonuje tę metodę i oddaje jej wynik.
- Dzięki temu atrapa zachowuje się jak oryginał: jest alert → zwraca,
  nie ma → wyjątek. Zwykły atrybut nie umiałby rzucać.

To także powód, dla którego `EC.alert_is_present()` działa na atrapie:
warunek zagląda w `driver.switch_to.alert`, łapie
`NoAlertPresentException` i czeka dalej — aż do TimeoutException.
Czekanie testujemy więc PRAWDZIWYM WebDriverWait (z krótkim limitem,
~1 sekunda).

### Schemat: przygotuj → podmień → wywołaj → sprawdź

Przykład na temacie INNYM niż zadania — domofon i atrapa zamka:

```python
# domofon.py
def wpusc_goscia(zamek, kod: str) -> bool:
    if kod == "1234":
        zamek.otworz()
        return True
    return False
```

```python
class FakeZamek:
    def __init__(self):
        self.otwarcia = 0

    def otworz(self):
        self.otwarcia += 1


def test_dobry_kod_otwiera_zamek() -> None:
    """Co testuje: czy poprawny kod otwiera zamek dokładnie raz.
    Co udaje: zamek — atrapa zlicza otwarcia zamiast ruszać ryglem.
    Co sprawdzam: wynik is True i zamek.otwarcia == 1.
    """
    # przygotuj (podmiana przez wstrzyknięcie atrapy)
    zamek = FakeZamek()

    # wywołaj
    wynik = wpusc_goscia(zamek, "1234")

    # sprawdź
    assert wynik is True
    assert zamek.otwarcia == 1
```

### tmp_path do zrzutów

Zrzuty w testach lądują w `tmp_path` (czysty folder na test) — budujesz
ścieżkę Pathem, funkcja robi „zrzut", test sprawdza `sciezka.exists()`.
