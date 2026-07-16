import logging
from typing import Any, Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def zadanie_01_zbuduj_opcje(bezglowa: bool) -> Options:
    """Buduje opcje Chrome z rozmiarem okna i opcjonalnym trybem headless.

    Args:
        bezglowa: True = dodaj tryb bezokienkowy (--headless=new).

    Returns:
        Options: opcje z ustawionym --window-size=1920,1080 oraz
            --headless=new, gdy bezglowa jest True.
    """
    opcje = Options()
    if bezglowa is True:
        opcje.add_argument("--headless=new")
    opcje.add_argument("--window-size=1920,1080")
    return opcje


def zadanie_02_uruchom_przegladarke(
    sciezka_drivera: str, opcje: Options
) -> Any:
    """Uruchamia Chrome przez Service z podaną ścieżką chromedrivera.

    Args:
        sciezka_drivera: ścieżka do pliku chromedriver.
        opcje: skonfigurowane opcje Chrome (np. z zadania 1).

    Returns:
        Any: driver zwrócony przez webdriver.Chrome.
    """
    # TODO: utwórz serwis = Service(sciezka_drivera)
    # TODO: zwróć webdriver.Chrome(service=serwis, options=opcje)
    serwis = Service(sciezka_drivera)
    return webdriver.Chrome(service=serwis, options=opcje)


def zadanie_03_otworz_strone(driver: Any, url: str) -> str:
    """Otwiera stronę i zwraca jej tytuł.

    Args:
        driver: uruchomiony driver przeglądarki.
        url: adres strony do otwarcia.

    Returns:
        str: tytuł otwartej strony (driver.title).
    """
    # TODO: otwórz stronę: driver.get(url)
    # TODO: zwróć driver.title (atrybut — bez nawiasów!)
    pass


def zadanie_04_tekst_elementu(driver: Any, identyfikator: str) -> str:
    """Znajduje element po id i zwraca jego widoczny tekst.

    Args:
        driver: uruchomiony driver przeglądarki.
        identyfikator: wartość atrybutu id elementu.

    Returns:
        str: tekst elementu (.text).
    """
    # TODO: znajdź element: driver.find_element(By.ID, identyfikator)
    # TODO: zwróć element.text
    pass


def zadanie_05_teksty_po_klasie(driver: Any, nazwa_klasy: str) -> list[str]:
    """Zbiera teksty wszystkich elementów o podanej klasie CSS.

    Args:
        driver: uruchomiony driver przeglądarki.
        nazwa_klasy: nazwa klasy (sama nazwa, bez kropki!).

    Returns:
        list[str]: teksty znalezionych elementów; pusta lista gdy brak.
    """
    # TODO: znajdź elementy: driver.find_elements(By.CLASS_NAME, nazwa_klasy)
    # TODO: zwróć list comprehension z .text każdego elementu
    pass


def zadanie_06_wpisz_tekst(driver: Any, id_pola: str, tekst: str) -> None:
    """Znajduje pole formularza po id i wpisuje w nie tekst.

    Args:
        driver: uruchomiony driver przeglądarki.
        id_pola: wartość atrybutu id pola tekstowego.
        tekst: tekst do wpisania.

    Returns:
        None
    """
    # TODO: znajdź pole: driver.find_element(By.ID, id_pola)
    # TODO: wpisz tekst: pole.send_keys(tekst)
    pass


def zadanie_07_kliknij(driver: Any, selektor: str) -> None:
    """Znajduje element selektorem CSS i klika go.

    Args:
        driver: uruchomiony driver przeglądarki.
        selektor: selektor CSS elementu (np. "button.zatwierdz").

    Returns:
        None
    """
    # TODO: znajdź element: driver.find_element(By.CSS_SELECTOR, selektor)
    # TODO: kliknij: element.click()
    pass


def zadanie_08_zaloguj(driver: Any, login: str, haslo: str) -> None:
    """Wypełnia formularz logowania i klika przycisk zaloguj.

    Zakłada stronę z polami o id "login" i "haslo" oraz przyciskiem
    o id "zaloguj".

    Args:
        driver: uruchomiony driver przeglądarki.
        login: nazwa użytkownika do wpisania.
        haslo: hasło do wpisania.

    Returns:
        None
    """
    # TODO: znajdź pole By.ID "login" i wpisz login przez send_keys
    # TODO: znajdź pole By.ID "haslo" i wpisz haslo przez send_keys
    # TODO: znajdź przycisk By.ID "zaloguj" i kliknij go
    pass


def zadanie_09_poczekaj_na_element(
    driver: Any, identyfikator: str, limit_sekund: float
) -> Any:
    """Czeka na pojawienie się elementu o podanym id i zwraca go.

    Args:
        driver: uruchomiony driver przeglądarki.
        identyfikator: wartość atrybutu id oczekiwanego elementu.
        limit_sekund: maksymalny czas czekania w sekundach.

    Returns:
        Any: znaleziony element. Rzuca TimeoutException, gdy element
            nie pojawi się w limicie.
    """
    # TODO: utwórz czekacza: WebDriverWait(driver, limit_sekund)
    # TODO: zwróć wynik czekacz.until(
    #           EC.presence_of_element_located((By.ID, identyfikator)))
    #       — lokator to KROTKA (podwójne nawiasy!)
    pass


def zadanie_10_poczekaj_bezpiecznie(
    driver: Any, identyfikator: str, limit_sekund: float
) -> Optional[str]:
    """Czeka na element i zwraca jego tekst; brak elementu w limicie daje None.

    Args:
        driver: uruchomiony driver przeglądarki.
        identyfikator: wartość atrybutu id oczekiwanego elementu.
        limit_sekund: maksymalny czas czekania w sekundach.

    Returns:
        Optional[str]: tekst elementu lub None po TimeoutException.
    """
    # TODO: użyj try/except TimeoutException (kontrakt None — temat 4)
    # TODO: w try: element = WebDriverWait(driver, limit_sekund).until(
    #           EC.presence_of_element_located((By.ID, identyfikator)))
    #       i return element.text
    # TODO: w except TimeoutException: return None
    pass


def zadanie_11_otworz_z_dziennikiem(driver: Any, url: str) -> str:
    """Otwiera stronę, zapisując przebieg do dziennika logging.

    Args:
        driver: uruchomiony driver przeglądarki.
        url: adres strony do otwarcia.

    Returns:
        str: tytuł otwartej strony.
    """
    # TODO: zapisz do dziennika zamiar: logger.info("Otwieram strone %s", url)
    #       (%s + przecinek — NIE f-string!)
    # TODO: otwórz stronę: driver.get(url)
    # TODO: zapisz sukces: logger.info("Zaladowano strone o tytule %s",
    #       driver.title)
    # TODO: zwróć driver.title
    pass


def zadanie_12_scenariusz_z_finally(
    sciezka_drivera: str, opcje: Options, url: str
) -> str:
    """Uruchamia przeglądarkę, odczytuje tytuł strony i GWARANTUJE zamknięcie.

    Args:
        sciezka_drivera: ścieżka do pliku chromedriver.
        opcje: skonfigurowane opcje Chrome.
        url: adres strony do odwiedzenia.

    Returns:
        str: tytuł odwiedzonej strony; przeglądarka zostaje zamknięta
            (quit) nawet gdy otwieranie strony rzuci wyjątek.
    """
    # TODO: utwórz drivera PRZED try:
    #       driver = webdriver.Chrome(service=Service(sciezka_drivera),
    #                                 options=opcje)
    # TODO: w bloku try: driver.get(url) i return driver.title
    # TODO: w bloku finally: driver.quit()
    #       (finally wykona się zawsze — po sukcesie i po wyjątku)
    pass
