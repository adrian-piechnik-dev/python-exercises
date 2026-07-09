import logging

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from conftest import FakeDriver, FakeElement
from selenium_podstawy import (
    zadanie_01_zbuduj_opcje,
    zadanie_02_uruchom_przegladarke,
    zadanie_03_otworz_strone,
    zadanie_04_tekst_elementu,
    zadanie_05_teksty_po_klasie,
    zadanie_06_wpisz_tekst,
    zadanie_07_kliknij,
    zadanie_08_zaloguj,
    zadanie_09_poczekaj_na_element,
    zadanie_10_poczekaj_bezpiecznie,
    zadanie_11_otworz_z_dziennikiem,
    zadanie_12_scenariusz_z_finally,
)


# --- zadanie_01 ---

def test_zadanie_01_headless_dodaje_argumenty() -> None:
    """Co testuje: czy przy bezglowa=True opcje mają headless i window-size.
    Co udaje: nic — Options to czysta konfiguracja, działa bez Chrome.
    Co sprawdzam: "--headless=new" i "--window-size=1920,1080"
    są w wynik.arguments.
    """
    # TODO: wywołaj zadanie_01_zbuduj_opcje(True)
    # TODO: sprawdź "--headless=new" in wynik.arguments
    # TODO: sprawdź "--window-size=1920,1080" in wynik.arguments
    pass


def test_zadanie_01_bez_headless_tylko_rozmiar() -> None:
    """Co testuje: czy przy bezglowa=False NIE ma argumentu headless.
    Co udaje: nic — Options bez przeglądarki.
    Co sprawdzam: "--headless=new" NIE występuje, a window-size tak.
    """
    # TODO: wywołaj zadanie_01_zbuduj_opcje(False)
    # TODO: sprawdź "--headless=new" not in wynik.arguments
    # TODO: sprawdź "--window-size=1920,1080" in wynik.arguments
    pass


# --- zadanie_02 ---

def test_zadanie_02_przekazuje_sciezke_do_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy ścieżka chromedrivera trafia do Service.
    Co udaje: Service i webdriver.Chrome — zamienniki zapisują argumenty
    zamiast odpalać przeglądarkę.
    Co sprawdzam: Service dostał "C:/sterowniki/chromedriver.exe".
    """
    # TODO: przygotuj pustą listę zapamietane_sciezki = []
    # TODO: przygotuj zamiennik:
    #       def podmieniony_service(sciezka):
    #           zapamietane_sciezki.append(sciezka)
    #           return "ATRAPA_SERWISU"
    # TODO: podmień: monkeypatch.setattr(
    #           "selenium_podstawy.Service", podmieniony_service)
    # TODO: przygotuj zamiennik Chrome:
    #       def podmieniony_chrome(service=None, options=None):
    #           return FakeDriver()
    # TODO: podmień: monkeypatch.setattr(
    #           "selenium_podstawy.webdriver.Chrome", podmieniony_chrome)
    # TODO: wywołaj zadanie_02_uruchom_przegladarke(
    #           "C:/sterowniki/chromedriver.exe", None)
    # TODO: sprawdź zapamietane_sciezki[0] == "C:/sterowniki/chromedriver.exe"
    pass


def test_zadanie_02_zwraca_drivera(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy funkcja zwraca to, co dał webdriver.Chrome.
    Co udaje: Service i webdriver.Chrome — Chrome zwraca konkretną atrapę.
    Co sprawdzam: wynik is ta_sama_atrapa.
    """
    # TODO: przygotuj atrapa = FakeDriver()
    # TODO: podmień "selenium_podstawy.Service" na zamiennik
    #       zwracający "ATRAPA_SERWISU"
    # TODO: podmień "selenium_podstawy.webdriver.Chrome" na zamiennik
    #       zwracający atrapa
    # TODO: wywołaj zadanie_02_uruchom_przegladarke("C:/x/driver.exe", None)
    # TODO: sprawdź wynik is atrapa
    pass


# --- zadanie_03 ---

def test_zadanie_03_odwiedza_adres_i_zwraca_tytul() -> None:
    """Co testuje: czy funkcja otwiera podany adres i oddaje tytuł strony.
    Co udaje: przeglądarkę — FakeDriver z tytułem "Sklep Python".
    Co sprawdzam: wynik == "Sklep Python" i adres w driver.odwiedzone.
    """
    # TODO: przygotuj driver = FakeDriver(tytul="Sklep Python")
    # TODO: wywołaj zadanie_03_otworz_strone(driver, "https://sklep.pl")
    # TODO: sprawdź wynik == "Sklep Python"
    # TODO: sprawdź driver.odwiedzone == ["https://sklep.pl"]
    pass


def test_zadanie_03_get_przed_odczytem_tytulu() -> None:
    """Co testuje: czy funkcja NAJPIERW nawiguje (get), a potem czyta tytuł.
    Co udaje: przeglądarkę — FakeDriver.
    Co sprawdzam: po wywołaniu lista odwiedzone ma dokładnie 1 wpis.
    """
    # TODO: przygotuj driver = FakeDriver()
    # TODO: wywołaj zadanie_03_otworz_strone(driver, "https://przyklad.pl")
    # TODO: sprawdź len(driver.odwiedzone) == 1
    pass


# --- zadanie_04 ---

def test_zadanie_04_zwraca_tekst_elementu() -> None:
    """Co testuje: czy funkcja znajduje element po id i oddaje jego tekst.
    Co udaje: przeglądarkę — FakeDriver z elementem "cena" o tekście "99 zl".
    Co sprawdzam: wynik == "99 zl".
    """
    # TODO: przygotuj driver = FakeDriver(
    #           elementy={"cena": FakeElement(tekst="99 zl")})
    # TODO: wywołaj zadanie_04_tekst_elementu(driver, "cena")
    # TODO: sprawdź wynik == "99 zl"
    pass


def test_zadanie_04_brak_elementu_rzuca_wyjatek() -> None:
    """Co testuje: czy brak elementu kończy się NoSuchElementException
    (kontrakt prawdziwego drivera — nie None!).
    Co udaje: przeglądarkę — FakeDriver bez elementów.
    Co sprawdzam: wywołanie rzuca NoSuchElementException (pytest.raises).
    """
    # TODO: przygotuj driver = FakeDriver()
    # TODO: w bloku with pytest.raises(NoSuchElementException):
    #       wywołaj zadanie_04_tekst_elementu(driver, "cena")
    #       (NoSuchElementException jest już zaimportowany u góry pliku)
    pass


# --- zadanie_05 ---

def test_zadanie_05_zbiera_teksty_z_listy() -> None:
    """Co testuje: czy funkcja zbiera teksty wszystkich elementów klasy.
    Co udaje: przeglądarkę — FakeDriver z listą 2 elementów klasy "produkt".
    Co sprawdzam: wynik == ["Klawiatura", "Mysz"].
    """
    # TODO: przygotuj driver = FakeDriver(listy_elementow={
    #           "produkt": [FakeElement(tekst="Klawiatura"),
    #                       FakeElement(tekst="Mysz")]})
    # TODO: wywołaj zadanie_05_teksty_po_klasie(driver, "produkt")
    # TODO: sprawdź wynik == ["Klawiatura", "Mysz"]
    pass


def test_zadanie_05_brak_elementow_pusta_lista() -> None:
    """Co testuje: czy nieznana klasa daje pustą listę (find_elements
    nie rzuca!).
    Co udaje: przeglądarkę — FakeDriver bez list elementów.
    Co sprawdzam: wynik == [].
    """
    # TODO: przygotuj driver = FakeDriver()
    # TODO: wywołaj zadanie_05_teksty_po_klasie(driver, "promocja")
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_06 ---

def test_zadanie_06_wpisuje_tekst_w_pole() -> None:
    """Co testuje: czy tekst trafia do właściwego pola przez send_keys.
    Co udaje: przeglądarkę — FakeDriver z polem o id "szukaj".
    Co sprawdzam: pole.wpisane == ["laptop"].
    """
    # TODO: przygotuj pole = FakeElement()
    # TODO: przygotuj driver = FakeDriver(elementy={"szukaj": pole})
    # TODO: wywołaj zadanie_06_wpisz_tekst(driver, "szukaj", "laptop")
    # TODO: sprawdź pole.wpisane == ["laptop"]
    pass


def test_zadanie_06_nie_klika_pola() -> None:
    """Co testuje: czy funkcja tylko wpisuje (bez przypadkowych kliknięć).
    Co udaje: przeglądarkę — FakeDriver z polem.
    Co sprawdzam: pole.klikniecia == 0 po wywołaniu.
    """
    # TODO: przygotuj pole = FakeElement()
    # TODO: przygotuj driver = FakeDriver(elementy={"szukaj": pole})
    # TODO: wywołaj zadanie_06_wpisz_tekst(driver, "szukaj", "laptop")
    # TODO: sprawdź pole.klikniecia == 0
    pass


# --- zadanie_07 ---

def test_zadanie_07_klika_element() -> None:
    """Co testuje: czy funkcja klika element wskazany selektorem CSS.
    Co udaje: przeglądarkę — FakeDriver z przyciskiem pod selektorem
    "button.zatwierdz".
    Co sprawdzam: przycisk.klikniecia == 1.
    """
    # TODO: przygotuj przycisk = FakeElement()
    # TODO: przygotuj driver = FakeDriver(
    #           elementy={"button.zatwierdz": przycisk})
    # TODO: wywołaj zadanie_07_kliknij(driver, "button.zatwierdz")
    # TODO: sprawdź przycisk.klikniecia == 1
    pass


def test_zadanie_07_klika_dokladnie_raz() -> None:
    """Co testuje: czy funkcja nie klika wielokrotnie.
    Co udaje: przeglądarkę — FakeDriver z przyciskiem.
    Co sprawdzam: po jednym wywołaniu klikniecia == 1 (nie 2).
    """
    # TODO: przygotuj przycisk = FakeElement()
    # TODO: przygotuj driver = FakeDriver(elementy={"a.link": przycisk})
    # TODO: wywołaj zadanie_07_kliknij(driver, "a.link") JEDEN raz
    # TODO: sprawdź przycisk.klikniecia == 1
    pass


# --- zadanie_08 ---

def test_zadanie_08_wypelnia_oba_pola() -> None:
    """Co testuje: czy login i hasło trafiają do właściwych pól.
    Co udaje: przeglądarkę — FakeDriver z polami "login", "haslo"
    i przyciskiem "zaloguj".
    Co sprawdzam: pole_login.wpisane == ["anna"]
    i pole_haslo.wpisane == ["tajne123"].
    """
    # TODO: przygotuj pole_login = FakeElement(), pole_haslo = FakeElement(),
    #       przycisk = FakeElement()
    # TODO: przygotuj driver = FakeDriver(elementy={
    #           "login": pole_login, "haslo": pole_haslo,
    #           "zaloguj": przycisk})
    # TODO: wywołaj zadanie_08_zaloguj(driver, "anna", "tajne123")
    # TODO: sprawdź pole_login.wpisane == ["anna"]
    # TODO: sprawdź pole_haslo.wpisane == ["tajne123"]
    pass


def test_zadanie_08_klika_przycisk_logowania() -> None:
    """Co testuje: czy scenariusz kończy się kliknięciem przycisku zaloguj.
    Co udaje: przeglądarkę — FakeDriver jak w teście wyżej.
    Co sprawdzam: przycisk.klikniecia == 1.
    """
    # TODO: przygotuj trzy FakeElementy i FakeDriver jak w teście wyżej
    # TODO: wywołaj zadanie_08_zaloguj(driver, "anna", "tajne123")
    # TODO: sprawdź przycisk.klikniecia == 1
    pass


# --- zadanie_09 ---

def test_zadanie_09_zwraca_obecny_element() -> None:
    """Co testuje: czy czekanie kończy się natychmiast, gdy element JEST.
    Co udaje: przeglądarkę — FakeDriver z elementem "wyniki";
    WebDriverWait jest PRAWDZIWY (działa na atrapie!).
    Co sprawdzam: wynik is przygotowany_element.
    """
    # TODO: przygotuj element = FakeElement(tekst="10 wynikow")
    # TODO: przygotuj driver = FakeDriver(elementy={"wyniki": element})
    # TODO: wywołaj zadanie_09_poczekaj_na_element(driver, "wyniki", 2)
    # TODO: sprawdź wynik is element
    pass


def test_zadanie_09_brak_elementu_konczy_sie_timeoutem() -> None:
    """Co testuje: czy po limicie czekania leci TimeoutException.
    Co udaje: przeglądarkę — FakeDriver BEZ elementu "wyniki"
    (find_element rzuca NoSuchElementException, wait ponawia aż limit).
    Co sprawdzam: wywołanie z limitem 1 s rzuca TimeoutException.
    """
    # TODO: przygotuj driver = FakeDriver()
    # TODO: w bloku with pytest.raises(TimeoutException):
    #       wywołaj zadanie_09_poczekaj_na_element(driver, "wyniki", 1)
    #       (limit 1 sekunda — test chwilę potrwa, tak ma być)
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_tekst_gdy_element_jest() -> None:
    """Co testuje: czy przy obecnym elemencie funkcja zwraca jego tekst.
    Co udaje: przeglądarkę — FakeDriver z elementem "komunikat".
    Co sprawdzam: wynik == "Zapisano".
    """
    # TODO: przygotuj driver = FakeDriver(
    #           elementy={"komunikat": FakeElement(tekst="Zapisano")})
    # TODO: wywołaj zadanie_10_poczekaj_bezpiecznie(driver, "komunikat", 2)
    # TODO: sprawdź wynik == "Zapisano"
    pass


def test_zadanie_10_timeout_zwraca_none() -> None:
    """Co testuje: kontrakt None po TimeoutException (try/except z tematu 4).
    Co udaje: przeglądarkę — FakeDriver bez elementu.
    Co sprawdzam: wynik is None (wyjątek złapany W funkcji, nie w teście).
    """
    # TODO: przygotuj driver = FakeDriver()
    # TODO: wywołaj zadanie_10_poczekaj_bezpiecznie(driver, "komunikat", 1)
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_11 ---

def test_zadanie_11_loguje_adres_strony(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Co testuje: czy funkcja zapisuje otwierany adres do dziennika.
    Co udaje: przeglądarkę — FakeDriver; dziennik podsłuchuje caplog.
    Co sprawdzam: "https://sklep.pl" występuje w caplog.text.
    """
    # TODO: włącz podsłuch: caplog.set_level(logging.INFO)
    # TODO: przygotuj driver = FakeDriver(tytul="Sklep")
    # TODO: wywołaj zadanie_11_otworz_z_dziennikiem(driver, "https://sklep.pl")
    # TODO: sprawdź "https://sklep.pl" in caplog.text
    pass


def test_zadanie_11_zwraca_tytul_i_loguje_go(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Co testuje: czy funkcja oddaje tytuł strony i odnotowuje go w dzienniku.
    Co udaje: przeglądarkę — FakeDriver z tytułem "Sklep Python".
    Co sprawdzam: wynik == "Sklep Python" i tytuł w caplog.text.
    """
    # TODO: włącz podsłuch: caplog.set_level(logging.INFO)
    # TODO: przygotuj driver = FakeDriver(tytul="Sklep Python")
    # TODO: wywołaj zadanie_11_otworz_z_dziennikiem(driver, "https://sklep.pl")
    # TODO: sprawdź wynik == "Sklep Python"
    # TODO: sprawdź "Sklep Python" in caplog.text
    pass


# --- zadanie_12 ---

def test_zadanie_12_zamyka_przegladarke_po_sukcesie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy po udanym scenariuszu przeglądarka jest zamknięta.
    Co udaje: Service i webdriver.Chrome — Chrome zwraca FakeDriver.
    Co sprawdzam: wynik to tytuł atrapy, a driver.zamknieto is True.
    """
    # TODO: przygotuj atrapa = FakeDriver(tytul="Sklep Python")
    # TODO: podmień "selenium_podstawy.Service" na zamiennik zwracający
    #       "ATRAPA_SERWISU"
    # TODO: podmień "selenium_podstawy.webdriver.Chrome" na zamiennik
    #       (service=None, options=None) zwracający atrapa
    # TODO: wywołaj zadanie_12_scenariusz_z_finally(
    #           "C:/x/driver.exe", None, "https://sklep.pl")
    # TODO: sprawdź wynik == "Sklep Python"
    # TODO: sprawdź atrapa.zamknieto is True
    pass


def test_zadanie_12_zamyka_przegladarke_mimo_bledu(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy finally domyka przeglądarkę TAKŻE po awarii strony.
    Co udaje: Chrome zwraca FakeDriver(blad_przy_get=True) — get rzuca
    RuntimeError.
    Co sprawdzam: wyjątek wylatuje z funkcji (pytest.raises), ALE
    atrapa.zamknieto is True — quit zadziałał mimo błędu.
    """
    # TODO: przygotuj atrapa = FakeDriver(blad_przy_get=True)
    # TODO: podmień Service i webdriver.Chrome jak w teście wyżej
    #       (Chrome zwraca atrapa)
    # TODO: w bloku with pytest.raises(RuntimeError):
    #       wywołaj zadanie_12_scenariusz_z_finally(
    #           "C:/x/driver.exe", None, "https://sklep.pl")
    # TODO: PO bloku with sprawdź atrapa.zamknieto is True
    pass
