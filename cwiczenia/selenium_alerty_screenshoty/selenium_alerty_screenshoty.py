from pathlib import Path
from typing import Any, Optional

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def zadanie_01_zrob_zrzut(driver: Any, sciezka: Path) -> bool:
    """Zapisuje zrzut ekranu pod wskazaną ścieżką.

    Args:
        driver: uruchomiony driver przeglądarki.
        sciezka: ścieżka docelowa pliku .png jako obiekt Path.

    Returns:
        bool: True, gdy zapis się powiódł (wynik save_screenshot).
    """
    return driver.save_screenshot(str(sciezka))


def zadanie_02_zrzut_do_folderu(driver: Any, folder: Path, nazwa: str) -> Path:
    """Buduje ścieżkę zrzutu wewnątrz folderu i zapisuje tam zdjęcie.

    Args:
        driver: uruchomiony driver przeglądarki.
        folder: istniejący folder docelowy jako Path.
        nazwa: nazwa pliku zrzutu (z końcówką .png).

    Returns:
        Path: pełna ścieżka zapisanego zrzutu (folder / nazwa).
    """
    sciezka = folder / nazwa
    driver.save_screenshot(str(sciezka))
    return sciezka


def zadanie_03_przelacz_na_alert(driver: Any) -> Any:
    """Przełącza uwagę robota na alert i zwraca uchwyt do niego.

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        Any: uchwyt alertu (driver.switch_to.alert).
    """
    return driver.switch_to.alert


def zadanie_04_tekst_alertu(driver: Any) -> str:
    """Odczytuje treść komunikatu z alertu.

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        str: treść alertu (.text).
    """
    alert = driver.switch_to.alert
    return alert.text


def zadanie_05_zaakceptuj_alert(driver: Any) -> None:
    """Potwierdza alert (odpowiednik kliknięcia OK).

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        None
    """
    alert = driver.switch_to.alert
    alert.accept()


def zadanie_06_odrzuc_alert(driver: Any) -> None:
    """Odrzuca alert (odpowiednik kliknięcia Anuluj).

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        None
    """
    alert = driver.switch_to.alert
    alert.dismiss()


def zadanie_07_alert_bezpiecznie(driver: Any) -> Optional[str]:
    """Odczytuje treść alertu; brak alertu daje None zamiast wyjątku.

    Args:
        driver: uruchomiony driver przeglądarki.

    Returns:
        Optional[str]: treść alertu lub None, gdy alertu nie ma
            (złapany NoAlertPresentException).
    """
    try:
        alert = driver.switch_to.alert
        return alert.text
    except NoAlertPresentException:
        return None


def zadanie_08_poczekaj_na_alert(driver: Any, limit_sekund: float) -> Any:
    """Czeka na pojawienie się alertu i zwraca uchwyt do niego.

    Args:
        driver: uruchomiony driver przeglądarki.
        limit_sekund: maksymalny czas czekania w sekundach.

    Returns:
        Any: uchwyt alertu zwrócony przez until. Rzuca TimeoutException,
            gdy alert nie pojawi się w limicie.
    """
    return WebDriverWait(driver, limit_sekund).until(EC.alert_is_present())


def zadanie_09_potwierdz_z_czekaniem(
    driver: Any, limit_sekund: float
) -> Optional[str]:
    """Czeka na alert, odczytuje jego treść i potwierdza; brak alertu → None.

    Args:
        driver: uruchomiony driver przeglądarki.
        limit_sekund: maksymalny czas czekania w sekundach.

    Returns:
        Optional[str]: treść potwierdzonego alertu lub None po
            TimeoutException.
    """
    try:
        alert = WebDriverWait(driver, limit_sekund).until(EC.alert_is_present())
        tresc = alert.text
        alert.accept()
        return tresc
    except TimeoutException:
        return None


def zadanie_10_potwierdz_i_udokumentuj(
    driver: Any, folder: Path, limit_sekund: float
) -> Optional[Path]:
    """Czeka na alert, potwierdza go i dokumentuje stronę zrzutem ekranu.

    Args:
        driver: uruchomiony driver przeglądarki.
        folder: istniejący folder na zrzut jako Path.
        limit_sekund: maksymalny czas czekania na alert.

    Returns:
        Optional[Path]: ścieżka zapisanego zrzutu (folder /
            "po_alercie.png") lub None, gdy alert się nie pojawił
            (wtedy zrzut NIE powstaje).
    """
    try:
        alert = WebDriverWait(driver, limit_sekund).until(EC.alert_is_present())
        alert.accept()
        sciezka = folder / "po_alercie.png"
        driver.save_screenshot(str(sciezka))
        return sciezka
    except TimeoutException:
        return None
