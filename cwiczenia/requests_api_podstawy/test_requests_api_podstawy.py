import csv
import json
from pathlib import Path

import pytest
import requests

from conftest import FakeResponse
from requests_api_podstawy import (
    zadanie_01_pobierz_status,
    zadanie_02_pobierz_json,
    zadanie_03_pobierz_z_parametrami,
    zadanie_04_czy_sukces,
    zadanie_05_pobierz_z_kontrola,
    zadanie_06_pobierz_bezpiecznie,
    zadanie_07_wyslij_post,
    zadanie_08_wyslij_post_z_naglowkami,
    zadanie_09_pobierz_liste_uzytkownikow,
    zadanie_10_pobierz_pole,
    zadanie_11_zapisz_odpowiedz_do_json,
    zadanie_12_zapisz_uzytkownikow_do_csv,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_kod_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca kod statusu z odpowiedzi.
    Co udaje: requests.get — zwraca FakeResponse(200, {}).
    Co sprawdzam: wynik == 200.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_status("https://api.przyklad.pl")
    assert wynik == 200


def test_zadanie_01_zwraca_kod_404(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja przekazuje kod błędu bez zmian (nie rzuca).
    Co udaje: requests.get — zwraca FakeResponse(404, {}).
    Co sprawdzam: wynik == 404.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(404, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_status("https://api.przyklad.pl")
    assert wynik == 404


# --- zadanie_02 ---

def test_zadanie_02_zwraca_slownik(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja parsuje treść odpowiedzi do słownika.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik == {"imie": "Anna"}.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"imie": "Anna"})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_02_pobierz_json("https://api.przyklad.pl")
    assert wynik == {"imie": "Anna"}


def test_zadanie_02_pusty_slownik(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: zachowanie przy pustej (ale poprawnej) odpowiedzi JSON.
    Co udaje: requests.get — zwraca FakeResponse(200, {}).
    Co sprawdzam: wynik == {} (pusty słownik, nie None).
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_02_pobierz_json("https://api.przyklad.pl")
    assert wynik == {}


# --- zadanie_03 ---

def test_zadanie_03_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja z parametrami zwraca sparsowaną odpowiedź.
    Co udaje: requests.get — zwraca FakeResponse(200, {"wyniki": [1, 2]}).
    Co sprawdzam: wynik == {"wyniki": [1, 2]}.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"wyniki": [1, 2]})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_03_pobierz_z_parametrami("https://api.przyklad.pl", {"miasto": "Warszawa"})
    assert wynik == {"wyniki": [1, 2]}


def test_zadanie_03_przekazuje_parametry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik parametrów faktycznie trafia do requests.get.
    Co udaje: requests.get — zamiennik ZAPISUJE otrzymane params do listy
    i zwraca FakeResponse(200, {}).
    Co sprawdzam: zapisane params == {"miasto": "Warszawa"}.
    """
    zapamietane = []
    def podmieniony_get(url, params=None, timeout=None):
        zapamietane.append(params)
        return FakeResponse(200, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    zadanie_03_pobierz_z_parametrami("https://api.przyklad.pl", {"miasto": "Warszawa"})
    assert zapamietane[0] == {"miasto": "Warszawa"}


# --- zadanie_04 ---

def test_zadanie_04_true_dla_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy kod 200 daje True.
    Co udaje: requests.get — zwraca FakeResponse(200, {}).
    Co sprawdzam: wynik is True.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_04_czy_sukces("https://api.przyklad.pl")
    assert wynik is True


def test_zadanie_04_false_dla_500(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy kod 500 daje False (a nie wyjątek).
    Co udaje: requests.get — zwraca FakeResponse(500, {}).
    Co sprawdzam: wynik is False.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(500, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_04_czy_sukces("https://api.przyklad.pl")
    assert wynik is False


# --- zadanie_05 ---

def test_zadanie_05_sukces_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy przy kodzie 200 funkcja zwraca sparsowane dane.
    Co udaje: requests.get — zwraca FakeResponse(200, {"id": 1}).
    Co sprawdzam: wynik == {"id": 1}.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"id": 1})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_05_pobierz_z_kontrola("https://api.przyklad.pl")
    assert wynik == {"id": 1}


def test_zadanie_05_blad_serwera_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy przy kodzie 500 funkcja przepuszcza HTTPError.
    Co udaje: requests.get — zwraca FakeResponse(500, {}), którego
    raise_for_status rzuci HTTPError.
    Co sprawdzam: wywołanie rzuca requests.HTTPError (pytest.raises).
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(500, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    with pytest.raises(requests.HTTPError):
        zadanie_05_pobierz_z_kontrola("https://api.przyklad.pl")


# --- zadanie_06 ---

def test_zadanie_06_sukces_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy przy sukcesie funkcja zwraca dane (nie None).
    Co udaje: requests.get — zwraca FakeResponse(200, {"id": 7}).
    Co sprawdzam: wynik == {"id": 7}.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"id": 7})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_06_pobierz_bezpiecznie("https://api.przyklad.pl")
    assert wynik == {"id": 7}


def test_zadanie_06_awaria_sieci_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None przy awarii połączenia.
    Co udaje: requests.get — RZUCA requests.ConnectionError (dziecko
    RequestException), zamiast zwracać odpowiedź.
    Co sprawdzam: wynik is None (wyjątek złapany w funkcji).
    """
    def podmieniony_get(url, params=None, timeout=10):
        raise requests.ConnectionError("brak internetu")
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_06_pobierz_bezpiecznie("https://api.przyklad.pl")
    assert wynik is None


# --- zadanie_07 ---

def test_zadanie_07_zwraca_kod_201(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca kod statusu odpowiedzi na POST.
    Co udaje: requests.post — zwraca FakeResponse(201, {}).
    Co sprawdzam: wynik == 201.
    """
    def podmieniony_post(url, json=None, headers=None, timeout=None):
        return FakeResponse(201, {})
    monkeypatch.setattr("requests_api_podstawy.requests.post", podmieniony_post)
    wynik = zadanie_07_wyslij_post("https://api.przyklad.pl", {"imie": "Anna"})
    assert wynik == 201


def test_zadanie_07_przekazuje_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik danych trafia do requests.post jako json=.
    Co udaje: requests.post — zamiennik ZAPISUJE otrzymany json do listy
    i zwraca FakeResponse(201, {}).
    Co sprawdzam: zapisany json == {"imie": "Anna"}.
    """
    zapamietane = []
    def podmieniony_post(url, json=None, headers=None, timeout=None):
        zapamietane.append(json)
        return FakeResponse(201, {})
    monkeypatch.setattr("requests_api_podstawy.requests.post", podmieniony_post)
    zadanie_07_wyslij_post("https://api.przyklad.pl", {"imie": "Anna"})
    assert zapamietane[0] == {"imie": "Anna"}


# --- zadanie_08 ---

def test_zadanie_08_zwraca_odpowiedz(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca sparsowaną treść odpowiedzi na POST.
    Co udaje: requests.post — zwraca FakeResponse(201, {"id": 5}).
    Co sprawdzam: wynik == {"id": 5}.
    """
    def podmieniony_post(url, json=None, headers=None, timeout=None):
        return FakeResponse(201, {"id": 5})
    monkeypatch.setattr("requests_api_podstawy.requests.post", podmieniony_post)
    wynik = zadanie_08_wyslij_post_z_naglowkami(
        "https://api.przyklad.pl",
        {"imie": "Anna"},
        {"Authorization": "Bearer klucz"}
    )
    assert wynik == {"id": 5}


def test_zadanie_08_przekazuje_naglowki(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik nagłówków trafia do requests.post jako headers=.
    Co udaje: requests.post — zamiennik ZAPISUJE otrzymane headers do listy
    i zwraca FakeResponse(201, {}).
    Co sprawdzam: zapisane headers == {"Authorization": "Bearer klucz"}.
    """
    zapamietane = []
    def podmieniony_post(url, json=None, headers=None, timeout=None):
        zapamietane.append(headers)
        return FakeResponse(201, {})
    monkeypatch.setattr("requests_api_podstawy.requests.post", podmieniony_post)
    wynik = zadanie_08_wyslij_post_z_naglowkami(
        "https://api.przyklad.pl",
        {"imie": "Anna"},
        {"Authorization": "Bearer klucz"}
    )
    assert zapamietane[0] == {"Authorization": "Bearer klucz"}


# --- zadanie_09 ---

def test_zadanie_09_zwraca_liste(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca listę słowników z odpowiedzi.
    Co udaje: requests.get — zwraca FakeResponse(200,
    [{"imie": "Anna"}, {"imie": "Piotr"}]).
    Co sprawdzam: len(wynik) == 2 i wynik[0]["imie"] == "Anna".
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, [{"imie": "Anna"}, {"imie": "Piotr"}])
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_09_pobierz_liste_uzytkownikow("https://api.przyklad.pl")
    assert len(wynik) == 2
    assert wynik[0]["imie"] == "Anna"


def test_zadanie_09_blad_404_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy kod 404 kończy się wyjątkiem HTTPError (nie pustą listą).
    Co udaje: requests.get — zwraca FakeResponse(404, []).
    Co sprawdzam: wywołanie rzuca requests.HTTPError (pytest.raises).
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(404, [])
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    with pytest.raises(requests.HTTPError):
        zadanie_09_pobierz_liste_uzytkownikow("https://api.przyklad.pl")


# --- zadanie_10 ---

def test_zadanie_10_zwraca_wartosc_pola(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja wyciąga wartość istniejącego pola.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna", "wiek": 30}).
    Co sprawdzam: wynik == "Anna" dla pola "imie".
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"imie": "Anna", "wiek": 30})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_10_pobierz_pole("https://api.przyklad.pl", "imie")
    assert wynik == "Anna"


def test_zadanie_10_brak_pola_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None gdy pola nie ma w odpowiedzi.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik is None dla pola "email".
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"imie": "Anna", "wiek": 30})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    wynik = zadanie_10_pobierz_pole("https://api.przyklad.pl", "email")
    assert wynik is None


# --- zadanie_11 ---

def test_zadanie_11_zapisuje_dane_do_pliku(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy pobrane dane lądują w pliku JSON i funkcja zwraca True.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik is True; plik po wczytaniu przez json.load
    zawiera {"imie": "Anna"}.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200, {"imie": "Anna"})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    p = tmp_path / "kopia.json"
    wynik = zadanie_11_zapisz_odpowiedz_do_json("https://api.przyklad.pl", str(p))
    assert wynik is True
    with open(str(p), "r", encoding="utf-8") as f:
        assert json.load(f) == {"imie": "Anna"}


def test_zadanie_11_blad_serwera_nie_tworzy_pliku(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy przy kodzie 500 wyjątek leci PRZED zapisem pliku.
    Co udaje: requests.get — zwraca FakeResponse(500, {}).
    Co sprawdzam: wywołanie rzuca requests.HTTPError, a plik nie istnieje.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(500, {})
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    p = tmp_path / "kopia.json"
    with pytest.raises(requests.HTTPError):
        zadanie_11_zapisz_odpowiedz_do_json("https://api.przyklad.pl", str(p))


# --- zadanie_12 ---

def test_zadanie_12_zapisuje_csv_i_zwraca_liczbe(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy lista użytkowników ląduje w CSV, a wynik to liczba wierszy.
    Co udaje: requests.get — zwraca FakeResponse(200, [
    {"imie": "Anna", "wiek": "30"}, {"imie": "Piotr", "wiek": "25"}]).
    Co sprawdzam: wynik == 2; plik wczytany przez csv.DictReader ma 2 wiersze
    i pierwszy to Anna.
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(
            200, [{"imie": "Anna", "wiek": "30"}, {"imie": "Piotr", "wiek": "25"}]
        )
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    p = tmp_path / "uzytkownicy.csv"
    wynik = zadanie_12_zapisz_uzytkownikow_do_csv("https://api.przyklad.pl", str(p))
    assert wynik == 2
    with open(str(p),"r", newline="", encoding="utf-8") as f:
        wiersze = list(csv.DictReader(f))
        assert len(wiersze) == 2
        assert wiersze[0]["imie"] == "Anna"


def test_zadanie_12_naglowki_z_kluczy_slownika(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy nagłówki CSV pochodzą z kluczy pierwszego słownika.
    Co udaje: requests.get — zwraca FakeResponse(200,
    [{"imie": "Anna", "wiek": "30"}]).
    Co sprawdzam: fieldnames wczytanego pliku == ["imie", "wiek"].
    """
    def podmieniony_get(url, params=None, timeout=None):
        return FakeResponse(200,[{"imie": "Anna", "wiek": "30"}])
    monkeypatch.setattr("requests_api_podstawy.requests.get", podmieniony_get)
    p = tmp_path / "uzytkownicy.csv"
    zadanie_12_zapisz_uzytkownikow_do_csv("https://api.przyklad.pl", str(p))
    with open(str(p), "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert list(reader.fieldnames) == ["imie", "wiek"]
