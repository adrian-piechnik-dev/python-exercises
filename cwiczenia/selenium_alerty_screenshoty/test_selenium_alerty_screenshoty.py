from pathlib import Path

import pytest
from selenium.common.exceptions import TimeoutException

from conftest import FakeAlert, FakeDriver
from selenium_alerty_screenshoty import (
    zadanie_01_zrob_zrzut,
    zadanie_02_zrzut_do_folderu,
    zadanie_03_przelacz_na_alert,
    zadanie_04_tekst_alertu,
    zadanie_05_zaakceptuj_alert,
    zadanie_06_odrzuc_alert,
    zadanie_07_alert_bezpiecznie,
    zadanie_08_poczekaj_na_alert,
    zadanie_09_potwierdz_z_czekaniem,
    zadanie_10_potwierdz_i_udokumentuj,
)


# --- zadanie_01 ---

def test_zadanie_01_tworzy_plik_zrzutu(tmp_path: Path) -> None:
    """Co testuje: czy zrzut ląduje pod wskazaną ścieżką i funkcja zwraca True.
    Co udaje: przeglądarkę — FakeDriver (tworzy podrobiony plik PNG);
    dysk — tmp_path.
    Co sprawdzam: wynik is True i sciezka.exists() is True.
    """
    driver = FakeDriver()
    sciezka = tmp_path / "strona.png"
    wynik = zadanie_01_zrob_zrzut(driver, sciezka)
    assert wynik is True
    assert sciezka.exists() is True


def test_zadanie_01_przekazuje_sciezke_jako_string(tmp_path: Path) -> None:
    """Co testuje: czy do save_screenshot trafia STRING (konwersja Path→str).
    Co udaje: przeglądarkę — FakeDriver notujący ścieżki zrzutów.
    Co sprawdzam: driver.zrzuty[0] to str i równa się str(sciezka).
    """
    driver = FakeDriver()
    sciezka = tmp_path / "strona.png"
    zadanie_01_zrob_zrzut(driver, sciezka)
    assert isinstance(driver.zrzuty[0], str) is True
    assert driver.zrzuty[0] == str(sciezka)


# --- zadanie_02 ---

def test_zadanie_02_sklada_sciezke_i_robi_zrzut(tmp_path: Path) -> None:
    """Co testuje: czy funkcja buduje ścieżkę operatorem / i robi tam zrzut.
    Co udaje: przeglądarkę — FakeDriver; dysk — tmp_path jako folder.
    Co sprawdzam: wynik == tmp_path / "raport.png" i plik istnieje.
    """
    driver = FakeDriver()
    wynik = zadanie_02_zrzut_do_folderu(driver, tmp_path, "raport.png")
    assert wynik == tmp_path / "raport.png"
    assert wynik.exists() is True


def test_zadanie_02_zwraca_path_nie_string(tmp_path: Path) -> None:
    """Co testuje: czy funkcja zwraca obiekt Path (kontrakt typu zwrotu).
    Co udaje: przeglądarkę — FakeDriver.
    Co sprawdzam: isinstance(wynik, Path) is True.
    """
    driver = FakeDriver()
    wynik = zadanie_02_zrzut_do_folderu(driver, tmp_path, "foto.png")
    assert isinstance(wynik, Path) is True


# --- zadanie_03 ---

def test_zadanie_03_zwraca_uchwyt_alertu() -> None:
    """Co testuje: czy funkcja oddaje dokładnie ten alert, który jest na ekranie.
    Co udaje: przeglądarkę — FakeDriver z konkretnym FakeAlert.
    Co sprawdzam: wynik is przygotowany_alert.
    """
    alert = FakeAlert(tekst="Czy na pewno?")
    driver = FakeDriver(alert=alert)
    wynik = zadanie_03_przelacz_na_alert(driver)
    assert wynik is alert


def test_zadanie_03_nie_klika_niczego() -> None:
    """Co testuje: czy samo przełączenie NIE podejmuje decyzji za usera.
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: zaakceptowano == 0 i odrzucono == 0 po wywołaniu.
    """
    alert = FakeAlert()
    driver = FakeDriver(alert=alert)
    zadanie_03_przelacz_na_alert(driver)
    assert alert.zaakceptowano == 0
    assert alert.odrzucono == 0


# --- zadanie_04 ---

def test_zadanie_04_zwraca_tresc_alertu() -> None:
    """Co testuje: czy funkcja odczytuje treść komunikatu z alertu.
    Co udaje: przeglądarkę — FakeDriver z alertem o znanej treści.
    Co sprawdzam: wynik == "Usunieto produkt".
    """
    alert = FakeAlert(tekst="Usunieto produkt")
    driver = FakeDriver(alert=alert)
    wynik = zadanie_04_tekst_alertu(driver)
    assert wynik == "Usunieto produkt"


def test_zadanie_04_nie_zamyka_alertu() -> None:
    """Co testuje: czy odczyt treści zostawia alert otwarty (bez accept).
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: alert.zaakceptowano == 0 po odczycie.
    """
    alert = FakeAlert(tekst="Komunikat")
    driver = FakeDriver(alert=alert)
    zadanie_04_tekst_alertu(driver)
    assert alert.zaakceptowano == 0


# --- zadanie_05 ---

def test_zadanie_05_akceptuje_alert() -> None:
    """Co testuje: czy funkcja potwierdza alert dokładnie raz.
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: alert.zaakceptowano == 1.
    """
    alert = FakeAlert()
    driver = FakeDriver(alert=alert)
    zadanie_05_zaakceptuj_alert(driver)
    assert alert.zaakceptowano == 1


def test_zadanie_05_nie_odrzuca() -> None:
    """Co testuje: czy akceptowanie nie miesza w liczniku odrzuceń.
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: alert.odrzucono == 0.
    """
    alert = FakeAlert()
    driver = FakeDriver(alert=alert)
    zadanie_05_zaakceptuj_alert(driver)
    assert alert.odrzucono == 0


# --- zadanie_06 ---

def test_zadanie_06_odrzuca_alert() -> None:
    """Co testuje: czy funkcja odrzuca alert dokładnie raz (dismiss).
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: alert.odrzucono == 1.
    """
    alert = FakeAlert()
    driver = FakeDriver(alert=alert)
    zadanie_06_odrzuc_alert(driver)
    assert alert.odrzucono == 1


def test_zadanie_06_nie_akceptuje() -> None:
    """Co testuje: czy odrzucanie nie potwierdza alertu przy okazji.
    Co udaje: przeglądarkę — FakeDriver z FakeAlert.
    Co sprawdzam: alert.zaakceptowano == 0.
    """
    alert = FakeAlert()
    driver = FakeDriver(alert=alert)
    zadanie_06_odrzuc_alert(driver)
    assert alert.zaakceptowano == 0


# --- zadanie_07 ---

def test_zadanie_07_zwraca_tresc_gdy_alert_jest() -> None:
    """Co testuje: czy przy obecnym alercie funkcja oddaje jego treść.
    Co udaje: przeglądarkę — FakeDriver z alertem "Zapisano zmiany".
    Co sprawdzam: wynik == "Zapisano zmiany".
    """
    driver = FakeDriver(alert=FakeAlert(tekst="Zapisano zmiany"))
    wynik = zadanie_07_alert_bezpiecznie(driver)
    assert wynik == "Zapisano zmiany"


def test_zadanie_07_brak_alertu_zwraca_none() -> None:
    """Co testuje: kontrakt None, gdy alertu nie ma (NoAlertPresentException
    złapany w funkcji — wzorzec z tematu 4).
    Co udaje: przeglądarkę — FakeDriver BEZ alertu (property rzuca wyjątek).
    Co sprawdzam: wynik is None.
    """
    driver = FakeDriver()
    wynik = zadanie_07_alert_bezpiecznie(driver)
    assert wynik is None


# --- zadanie_08 ---

def test_zadanie_08_zwraca_obecny_alert() -> None:
    """Co testuje: czy czekanie kończy się od razu, gdy alert JUŻ jest.
    Co udaje: przeglądarkę — FakeDriver z alertem; WebDriverWait jest
    PRAWDZIWY (alert_is_present działa na atrapie dzięki property).
    Co sprawdzam: wynik is przygotowany_alert.
    """
    alert = FakeAlert(tekst="Gotowe")
    driver = FakeDriver(alert=alert)
    wynik = zadanie_08_poczekaj_na_alert(driver, 2)
    assert wynik is alert


def test_zadanie_08_brak_alertu_konczy_sie_timeoutem() -> None:
    """Co testuje: czy po limicie bez alertu leci TimeoutException.
    Co udaje: przeglądarkę — FakeDriver bez alertu (property rzuca
    NoAlertPresentException, warunek czeka aż limit).
    Co sprawdzam: wywołanie z limitem 1 s rzuca TimeoutException.
    """
    driver = FakeDriver()
    with pytest.raises(TimeoutException):
        zadanie_08_poczekaj_na_alert(driver, 1)


# --- zadanie_09 ---

def test_zadanie_09_czyta_i_akceptuje() -> None:
    """Co testuje: czy funkcja oddaje treść ORAZ potwierdza alert.
    Co udaje: przeglądarkę — FakeDriver z alertem "Czy usunac konto?".
    Co sprawdzam: wynik == "Czy usunac konto?" i zaakceptowano == 1.
    """
    alert = FakeAlert(tekst="Czy usunac konto?")
    driver = FakeDriver(alert=alert)
    wynik = zadanie_09_potwierdz_z_czekaniem(driver, 2)
    assert wynik == "Czy usunac konto?"
    assert alert.zaakceptowano == 1


def test_zadanie_09_timeout_zwraca_none() -> None:
    """Co testuje: kontrakt None po TimeoutException (bez alertu w limicie).
    Co udaje: przeglądarkę — FakeDriver bez alertu.
    Co sprawdzam: wynik is None (wyjątek złapany W funkcji).
    """
    driver = FakeDriver()
    wynik = zadanie_09_potwierdz_z_czekaniem(driver, 1)
    assert wynik is None


# --- zadanie_10 ---

def test_zadanie_10_akceptuje_i_robi_zrzut(tmp_path: Path) -> None:
    """Co testuje: pełny scenariusz — potwierdzenie alertu i zrzut do folderu.
    Co udaje: przeglądarkę — FakeDriver z alertem; dysk — tmp_path.
    Co sprawdzam: wynik == tmp_path / "po_alercie.png", plik istnieje,
    zaakceptowano == 1.
    """
    alert = FakeAlert(tekst="Zapisano")
    driver = FakeDriver(alert=alert)
    wynik = zadanie_10_potwierdz_i_udokumentuj(driver, tmp_path, 2)
    assert wynik == tmp_path / "po_alercie.png"
    assert wynik.exists() is True
    assert alert.zaakceptowano == 1


def test_zadanie_10_bez_alertu_none_i_brak_zrzutu(tmp_path: Path) -> None:
    """Co testuje: czy timeout daje None i NIE zostawia pliku zrzutu.
    Co udaje: przeglądarkę — FakeDriver bez alertu; dysk — tmp_path.
    Co sprawdzam: wynik is None i (tmp_path / "po_alercie.png").exists()
    is False.
    """
    driver = FakeDriver()
    wynik = zadanie_10_potwierdz_i_udokumentuj(driver, tmp_path, 1)
    assert wynik is None
    assert (tmp_path / "po_alercie.png").exists() is False
