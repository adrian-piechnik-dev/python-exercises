import math
from pathlib import Path
from typing import Any

import pytest
import requests

from conftest import FakeResponse
from pytest_fixtures_parametrize import (
    zadanie_01_podziel,
    zadanie_02_srednia,
    zadanie_03_kategoria_wieku,
    zadanie_04_pole_kola,
    zadanie_05_czytaj_ustawienie,
    zadanie_06_klucz_api,
    zadanie_07_waliduj_email,
    zadanie_08_cena_brutto,
    zadanie_09_wczytaj_konfiguracje,
    zadanie_10_pobierz_ustawienie,
    zadanie_11_pobierz_kurs,
    zadanie_12_pobierz_kurs_bezpiecznie,
)


# --- zadanie_01 ---

@pytest.mark.parametrize(
    "dzielna, dzielnik, oczekiwane",
    [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (1, 4, 0.25),
    ],
)
def test_zadanie_01_dzieli_poprawnie(
    dzielna: float, dzielnik: float, oczekiwane: float
) -> None:
    """Co testuje: poprawność dzielenia dla trzech par liczb (parametrize).
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wynik == pytest.approx(oczekiwane) dla każdego zestawu.
    """
    # TODO: wywołaj zadanie_01_podziel(dzielna, dzielnik)
    # TODO: sprawdź wynik == pytest.approx(oczekiwane)
    pass


def test_zadanie_01_dzielnik_zero_rzuca_wyjatek() -> None:
    """Co testuje: kontrakt wyjątku przy dzielniku równym 0.
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wywołanie z dzielnikiem 0 rzuca ValueError (pytest.raises).
    """
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_01_podziel(10, 0)
    pass


# --- zadanie_02 ---

def test_zadanie_02_liczy_srednia() -> None:
    """Co testuje: poprawność średniej dla listy [1, 2, 3].
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wynik == pytest.approx(2.0).
    """
    # TODO: wywołaj zadanie_02_srednia([1, 2, 3])
    # TODO: sprawdź wynik == pytest.approx(2.0)
    pass


def test_zadanie_02_pusta_lista_rzuca_wyjatek() -> None:
    """Co testuje: kontrakt wyjątku dla pustej listy.
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wywołanie z [] rzuca ValueError (pytest.raises).
    """
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_02_srednia([])
    pass


# --- zadanie_03 ---

@pytest.mark.parametrize(
    "wiek, oczekiwana",
    [
        (5, "dziecko"),
        (12, "dziecko"),
        (13, "nastolatek"),
        (17, "nastolatek"),
        (18, "dorosly"),
        (70, "dorosly"),
    ],
)
def test_zadanie_03_przypisuje_kategorie(wiek: int, oczekiwana: str) -> None:
    """Co testuje: kategorie dla sześciu wieków, w tym granice 12/13 i 17/18.
    Co udaje: nic — czysta funkcja.
    Co sprawdzam: wynik == oczekiwana dla każdego zestawu z parametrize.
    """
    # TODO: wywołaj zadanie_03_kategoria_wieku(wiek)
    # TODO: sprawdź wynik == oczekiwana
    pass


def test_zadanie_03_ujemny_wiek_rzuca_wyjatek() -> None:
    """Co testuje: kontrakt wyjątku dla ujemnego wieku.
    Co udaje: nic — czysta funkcja.
    Co sprawdzam: wywołanie z -1 rzuca ValueError (pytest.raises).
    """
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_03_kategoria_wieku(-1)
    pass


# --- zadanie_04 ---

def test_zadanie_04_pole_kola_dla_promienia_1() -> None:
    """Co testuje: pole koła o promieniu 1 to dokładnie pi.
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wynik == pytest.approx(math.pi) — float wymaga approx.
    """
    # TODO: wywołaj zadanie_04_pole_kola(1)
    # TODO: sprawdź wynik == pytest.approx(math.pi)
    pass


def test_zadanie_04_ujemny_promien_rzuca_wyjatek() -> None:
    """Co testuje: kontrakt wyjątku dla ujemnego promienia.
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wywołanie z -2 rzuca ValueError (pytest.raises).
    """
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_04_pole_kola(-2)
    pass


# --- zadanie_05 ---

def test_zadanie_05_czyta_ustawiona_zmienna(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: odczyt wartości ustawionej zmiennej środowiskowej.
    Co udaje: zmienną KOLOR_MOTYWU — setenv ustawia "ciemny" na czas testu.
    Co sprawdzam: wynik == "ciemny".
    """
    # TODO: podmień: monkeypatch.setenv("KOLOR_MOTYWU", "ciemny")
    # TODO: wywołaj zadanie_05_czytaj_ustawienie("KOLOR_MOTYWU")
    # TODO: sprawdź wynik == "ciemny"
    pass


def test_zadanie_05_brak_zmiennej_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None dla nieustawionej zmiennej.
    Co udaje: brak zmiennej KOLOR_MOTYWU — delenv usuwa ją na czas testu.
    Co sprawdzam: wynik is None.
    """
    # TODO: podmień: monkeypatch.delenv("KOLOR_MOTYWU", raising=False)
    # TODO: wywołaj zadanie_05_czytaj_ustawienie("KOLOR_MOTYWU")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_06 ---

def test_zadanie_06_zwraca_klucz_ze_srodowiska(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: odczyt klucza API z ustawionej zmiennej środowiskowej.
    Co udaje: zmienną API_KLUCZ — setenv ustawia "sekret-123" na czas testu.
    Co sprawdzam: wynik == "sekret-123".
    """
    # TODO: podmień: monkeypatch.setenv("API_KLUCZ", "sekret-123")
    # TODO: wywołaj zadanie_06_klucz_api()
    # TODO: sprawdź wynik == "sekret-123"
    pass


def test_zadanie_06_brak_klucza_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt wyjątku, gdy zmienna API_KLUCZ nie istnieje.
    Co udaje: brak zmiennej API_KLUCZ — delenv usuwa ją na czas testu.
    Co sprawdzam: wywołanie rzuca ValueError (pytest.raises).
    """
    # TODO: podmień: monkeypatch.delenv("API_KLUCZ", raising=False)
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_06_klucz_api()
    pass


# --- zadanie_07 ---

@pytest.mark.parametrize(
    "email, oczekiwane",
    [
        ("anna@przyklad.pl", True),
        ("piotr.nowak@firma.com", True),
        ("bez-malpy.pl", False),
        ("bez@kropki", False),
    ],
)
def test_zadanie_07_waliduje_adresy(email: str, oczekiwane: bool) -> None:
    """Co testuje: walidację czterech adresów — dwóch dobrych i dwóch złych.
    Co udaje: nic — czysta funkcja.
    Co sprawdzam: wynik is oczekiwane dla każdego zestawu z parametrize.
    """
    # TODO: wywołaj zadanie_07_waliduj_email(email)
    # TODO: sprawdź wynik is oczekiwane
    pass


def test_zadanie_07_pusty_string_daje_false() -> None:
    """Co testuje: zachowanie dla pustego stringa (przypadek brzegowy).
    Co udaje: nic — czysta funkcja.
    Co sprawdzam: wynik is False.
    """
    # TODO: wywołaj zadanie_07_waliduj_email("")
    # TODO: sprawdź wynik is False
    pass


# --- zadanie_08 ---

@pytest.mark.parametrize(
    "netto, stawka, oczekiwana",
    [
        (100.0, 0.23, 123.0),
        (200.0, 0.08, 216.0),
        (50.0, 0.0, 50.0),
    ],
)
def test_zadanie_08_liczy_brutto(
    netto: float, stawka: float, oczekiwana: float
) -> None:
    """Co testuje: cenę brutto dla trzech stawek VAT (w tym 0%).
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wynik == pytest.approx(oczekiwana) — floaty wymagają approx.
    """
    # TODO: wywołaj zadanie_08_cena_brutto(netto, stawka)
    # TODO: sprawdź wynik == pytest.approx(oczekiwana)
    pass


def test_zadanie_08_ujemne_netto_rzuca_wyjatek() -> None:
    """Co testuje: kontrakt wyjątku dla ujemnej ceny netto.
    Co udaje: nic — czysta funkcja liczbowa.
    Co sprawdzam: wywołanie z netto=-10 rzuca ValueError (pytest.raises).
    """
    # TODO: w bloku with pytest.raises(ValueError):
    #       wywołaj zadanie_08_cena_brutto(-10, 0.23)
    pass


# --- zadanie_09 ---

def test_zadanie_09_wczytuje_konfiguracje(plik_konfiguracyjny: Path) -> None:
    """Co testuje: wczytanie całego słownika konfiguracji z pliku.
    Co udaje: nic — fixture plik_konfiguracyjny tworzy prawdziwy plik tymczasowy.
    Co sprawdzam: wynik == {"jezyk": "pl", "limit": 10}.
    """
    # TODO: wywołaj zadanie_09_wczytaj_konfiguracje(str(plik_konfiguracyjny))
    # TODO: sprawdź wynik == {"jezyk": "pl", "limit": 10}
    pass


def test_zadanie_09_liczba_wraca_jako_int(plik_konfiguracyjny: Path) -> None:
    """Co testuje: czy wartość liczbowa z JSON-a wraca jako int (nie string).
    Co udaje: nic — używam fixture plik_konfiguracyjny.
    Co sprawdzam: wynik["limit"] == 10 i isinstance(wynik["limit"], int) is True.
    """
    # TODO: wywołaj zadanie_09_wczytaj_konfiguracje(str(plik_konfiguracyjny))
    # TODO: sprawdź wynik["limit"] == 10
    # TODO: sprawdź isinstance(wynik["limit"], int) is True
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_wartosc_ustawienia(
    konfiguracja_globalna: dict[str, Any],
) -> None:
    """Co testuje: odczyt istniejącego ustawienia ze słownika konfiguracji.
    Co udaje: nic — fixture konfiguracja_globalna (scope="module",
    współdzielona przez cały plik, tylko-do-odczytu).
    Co sprawdzam: wynik == "pl" dla klucza "jezyk".
    """
    # TODO: wywołaj zadanie_10_pobierz_ustawienie(konfiguracja_globalna, "jezyk")
    # TODO: sprawdź wynik == "pl"
    pass


def test_zadanie_10_brak_klucza_zwraca_none(
    konfiguracja_globalna: dict[str, Any],
) -> None:
    """Co testuje: kontrakt None dla nieistniejącego ustawienia.
    Co udaje: nic — ta sama fixture module-scope co w teście wyżej
    (pytest utworzył ją tylko raz na cały plik).
    Co sprawdzam: wynik is None dla klucza "motyw".
    """
    # TODO: wywołaj zadanie_10_pobierz_ustawienie(konfiguracja_globalna, "motyw")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_11 ---

def test_zadanie_11_zwraca_kurs_jako_float(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: pobranie i konwersję kursu z odpowiedzi API.
    Co udaje: requests.get — zwraca FakeResponse(200, {"kurs": 4.25})
    (mock jak w temacie 11).
    Co sprawdzam: wynik == pytest.approx(4.25).
    """
    # TODO: przygotuj zamiennik:
    #       def podmieniony_get(url, timeout=None):
    #           return FakeResponse(200, {"kurs": 4.25})
    # TODO: podmień: monkeypatch.setattr(
    #           "pytest_fixtures_parametrize.requests.get", podmieniony_get)
    # TODO: wywołaj zadanie_11_pobierz_kurs("https://api.przyklad.pl/eur")
    # TODO: sprawdź wynik == pytest.approx(4.25)
    pass


def test_zadanie_11_blad_serwera_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy funkcja przepuszcza HTTPError przy kodzie 500.
    Co udaje: requests.get — zwraca FakeResponse(500, {}), którego
    raise_for_status rzuci HTTPError.
    Co sprawdzam: wywołanie rzuca requests.HTTPError (pytest.raises + mock).
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(500, {})
    # TODO: podmień "pytest_fixtures_parametrize.requests.get"
    # TODO: w bloku with pytest.raises(requests.HTTPError):
    #       wywołaj zadanie_11_pobierz_kurs("https://api.przyklad.pl/eur")
    pass


# --- zadanie_12 ---

def test_zadanie_12_sukces_zwraca_kurs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy przy sukcesie funkcja zwraca kurs (nie None).
    Co udaje: requests.get — zwraca FakeResponse(200, {"kurs": 3.98}).
    Co sprawdzam: wynik == pytest.approx(3.98).
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"kurs": 3.98})
    # TODO: podmień "pytest_fixtures_parametrize.requests.get"
    # TODO: wywołaj zadanie_12_pobierz_kurs_bezpiecznie(
    #           "https://api.przyklad.pl/usd")
    # TODO: sprawdź wynik == pytest.approx(3.98)
    pass


def test_zadanie_12_awaria_sieci_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None przy awarii połączenia (try/except z tematu 4).
    Co udaje: requests.get — RZUCA requests.ConnectionError zamiast
    zwracać odpowiedź.
    Co sprawdzam: wynik is None (wyjątek złapany w funkcji, nie w teście).
    """
    # TODO: przygotuj zamiennik, który zamiast return robi:
    #       raise requests.ConnectionError("brak internetu")
    # TODO: podmień "pytest_fixtures_parametrize.requests.get"
    # TODO: wywołaj zadanie_12_pobierz_kurs_bezpiecznie(
    #           "https://api.przyklad.pl/usd")
    # TODO: sprawdź wynik is None
    pass
