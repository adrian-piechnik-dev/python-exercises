from pathlib import Path
from typing import Any, Optional

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- SPIS ZADAŃ ---
# Funkcje dostają drivera jako argument (testy podstawiają atrapę) —
# jak w temacie 17.
#
# zadanie_01 — zrób zrzut ekranu pod wskazaną ścieżką (Path → str!)
# zadanie_02 — zbuduj ścieżkę zrzutu w folderze i zrób zdjęcie
# zadanie_03 — przełącz się na alert (switch_to.alert)
# zadanie_04 — odczytaj treść alertu (.text)
# zadanie_05 — zaakceptuj alert (accept)
# zadanie_06 — odrzuć alert (dismiss)
# zadanie_07 — odczytaj alert bezpiecznie (brak alertu → None)
# zadanie_08 — poczekaj na alert (WebDriverWait + alert_is_present)
# zadanie_09 — poczekaj, przeczytaj i potwierdź (Timeout → None)
# zadanie_10 — scenariusz: potwierdź alert i udokumentuj zrzutem


def zadanie_01_zrob_zrzut(driver: Any, sciezka: Path) -> bool:
    """Zapisuje zrzut ekranu pod wskazaną ścieżką.

    Args:
        driver: uruchomiony driver przeglądarki.
        sciezka: ścieżka docelowa pliku .png jako obiekt Path.

    Returns:
        bool: True, gdy zapis się powiódł (wynik save_screenshot).
    """
    # TODO: zwróć driver.save_screenshot(str(sciezka))
    #       — save_screenshot chce STRINGA, stąd konwersja str(Path)
    pass


def zadanie_02_zrzut_do_folderu(driver: Any, folder: Path, nazwa: str) -> Path:
    """Buduje ścieżkę zrzutu wewnątrz folderu i zapisuje tam zdjęcie.

    Args:
        driver: uruchomiony driver przeglądarki.
        folder: istniejący folder docelowy jako Path.
        nazwa: nazwa pliku zrzutu (z końcówką .png).

    Returns:
        Path: pełna ścieżka zapisanego zrzutu (folder / nazwa).
    """
    # TODO: zbuduj sciezka = folder / nazwa (operator / z tematu 4)
    # TODO: zrób zrzut: driver.save_screenshot(str(sciezka))
    # TODO: return sciezka
    pass


def zadanie_03_przelacz_na_alert(driver: Any) -> Any:
    """Przełącza uwagę robota na alert i zwraca uchwyt do niego.

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        Any: uchwyt alertu (driver.switch_to.alert).
    """
    # TODO: zwróć driver.switch_to.alert (atrybut — bez nawiasów!)
    pass


def zadanie_04_tekst_alertu(driver: Any) -> str:
    """Odczytuje treść komunikatu z alertu.

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        str: treść alertu (.text).
    """
    # TODO: złap alert = driver.switch_to.alert
    # TODO: zwróć alert.text
    pass


def zadanie_05_zaakceptuj_alert(driver: Any) -> None:
    """Potwierdza alert (odpowiednik kliknięcia OK).

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        None
    """
    # TODO: złap alert = driver.switch_to.alert
    # TODO: potwierdź: alert.accept()
    pass


def zadanie_06_odrzuc_alert(driver: Any) -> None:
    """Odrzuca alert (odpowiednik kliknięcia Anuluj).

    Args:
        driver: uruchomiony driver przeglądarki (alert jest na ekranie).

    Returns:
        None
    """
    # TODO: złap alert = driver.switch_to.alert
    # TODO: odrzuć: alert.dismiss()
    pass


def zadanie_07_alert_bezpiecznie(driver: Any) -> Optional[str]:
    """Odczytuje treść alertu; brak alertu daje None zamiast wyjątku.

    Args:
        driver: uruchomiony driver przeglądarki.

    Returns:
        Optional[str]: treść alertu lub None, gdy alertu nie ma
            (złapany NoAlertPresentException).
    """
    # TODO: użyj try/except NoAlertPresentException (kontrakt None —
    #       wzorzec z tematu 4)
    # TODO: w try: złap alert = driver.switch_to.alert
    #       i return alert.text
    # TODO: w except NoAlertPresentException: return None
    pass


def zadanie_08_poczekaj_na_alert(driver: Any, limit_sekund: float) -> Any:
    """Czeka na pojawienie się alertu i zwraca uchwyt do niego.

    Args:
        driver: uruchomiony driver przeglądarki.
        limit_sekund: maksymalny czas czekania w sekundach.

    Returns:
        Any: uchwyt alertu zwrócony przez until. Rzuca TimeoutException,
            gdy alert nie pojawi się w limicie.
    """
    # TODO: zwróć WebDriverWait(driver, limit_sekund).until(
    #           EC.alert_is_present())
    #       — puste nawiasy: ten warunek NIE przyjmuje lokatora!
    pass


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
    # TODO: użyj try/except TimeoutException
    # TODO: w try: alert = WebDriverWait(driver, limit_sekund).until(
    #           EC.alert_is_present())
    #       potem: tresc = alert.text, alert.accept(), return tresc
    #       (treść czytaj PRZED accept — po nim alert znika!)
    # TODO: w except TimeoutException: return None
    pass


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
    # TODO: użyj try/except TimeoutException
    # TODO: w try: poczekaj na alert przez WebDriverWait + alert_is_present
    #       i potwierdź go przez .accept()
    # TODO: dalej w try: zbuduj sciezka = folder / "po_alercie.png",
    #       zrób zrzut driver.save_screenshot(str(sciezka))
    #       i return sciezka
    # TODO: w except TimeoutException: return None
    pass
