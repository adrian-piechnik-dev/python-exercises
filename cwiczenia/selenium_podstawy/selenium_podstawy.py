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
    driver.get(url)
    return driver.title


def zadanie_04_tekst_elementu(driver: Any, identyfikator: str) -> str:
    """Znajduje element po id i zwraca jego widoczny tekst.

    Args:
        driver: uruchomiony driver przeglądarki.
        identyfikator: wartość atrybutu id elementu.

    Returns:
        str: tekst elementu (.text).
    """
    element = driver.find_element(By.ID, identyfikator)
    return element.text


def zadanie_05_teksty_po_klasie(driver: Any, nazwa_klasy: str) -> list[str]:
    """Zbiera teksty wszystkich elementów o podanej klasie CSS.

    Args:
        driver: uruchomiony driver przeglądarki.
        nazwa_klasy: nazwa klasy (sama nazwa, bez kropki!).

    Returns:
        list[str]: teksty znalezionych elementów; pusta lista gdy brak.
    """
    elementy = driver.find_elements(By.CLASS_NAME, nazwa_klasy)
    return [element.text for element in elementy]


def zadanie_06_wpisz_tekst(driver: Any, id_pola: str, tekst: str) -> None:
    """Znajduje pole formularza po id i wpisuje w nie tekst.

    Args:
        driver: uruchomiony driver przeglądarki.
        id_pola: wartość atrybutu id pola tekstowego.
        tekst: tekst do wpisania.

    Returns:
        None
    """
    pole = driver.find_element(By.ID, id_pola)
    pole.send_keys(tekst)


def zadanie_07_kliknij(driver: Any, selektor: str) -> None:
    """Znajduje element selektorem CSS i klika go.

    Args:
        driver: uruchomiony driver przeglądarki.
        selektor: selektor CSS elementu (np. "button.zatwierdz").

    Returns:
        None
    """
    element = driver.find_element(By.CSS_SELECTOR, selektor)
    element.click()


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
    pole_login = driver.find_element(By.ID, "login")
    pole_login.send_keys(login)
    pole_haslo = driver.find_element(By.ID, "haslo")
    pole_haslo.send_keys(haslo)
    przycisk = driver.find_element(By.ID, "zaloguj")
    przycisk.click()


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
    waiter = WebDriverWait(driver, limit_sekund)
    return waiter.until(EC.presence_of_element_located((By.ID, identyfikator)))


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
    try:
        element = WebDriverWait(driver, limit_sekund).until(
            EC.presence_of_element_located((By.ID, identyfikator))
        )
        return element.text
    except TimeoutException:
        return None


def zadanie_11_otworz_z_dziennikiem(driver: Any, url: str) -> str:
    """Otwiera stronę, zapisując przebieg do dziennika logging.

    Args:
        driver: uruchomiony driver przeglądarki.
        url: adres strony do otwarcia.

    Returns:
        str: tytuł otwartej strony.
    """
    logger.info("Otwieram strone %s", url)
    driver.get(url)
    logger.info("Zaladowano strone o tytulu %s", driver.title)
    return driver.title


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
    driver = webdriver.Chrome(service=Service(sciezka_drivera), options=opcje)
    try:
        driver.get(url)
        return driver.title
    finally:
        driver.quit()
