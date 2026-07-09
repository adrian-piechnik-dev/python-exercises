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
    # TODO: przygotuj zamiennik:
    #       def podmieniony_get(url, params=None, timeout=None):
    #           return FakeResponse(200, {})
    # TODO: podmień: monkeypatch.setattr(
    #           "requests_api_podstawy.requests.get", podmieniony_get)
    # TODO: wywołaj zadanie_01_pobierz_status("https://api.przyklad.pl")
    # TODO: sprawdź wynik == 200
    pass


def test_zadanie_01_zwraca_kod_404(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja przekazuje kod błędu bez zmian (nie rzuca).
    Co udaje: requests.get — zwraca FakeResponse(404, {}).
    Co sprawdzam: wynik == 404.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(404, {})
    # TODO: podmień requests.get jak w teście wyżej
    # TODO: wywołaj zadanie_01_pobierz_status("https://api.przyklad.pl")
    # TODO: sprawdź wynik == 404
    pass


# --- zadanie_02 ---

def test_zadanie_02_zwraca_slownik(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja parsuje treść odpowiedzi do słownika.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik == {"imie": "Anna"}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"imie": "Anna"})
    # TODO: podmień requests.get przez monkeypatch.setattr
    # TODO: wywołaj zadanie_02_pobierz_json("https://api.przyklad.pl")
    # TODO: sprawdź wynik == {"imie": "Anna"}
    pass


def test_zadanie_02_pusty_slownik(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: zachowanie przy pustej (ale poprawnej) odpowiedzi JSON.
    Co udaje: requests.get — zwraca FakeResponse(200, {}).
    Co sprawdzam: wynik == {} (pusty słownik, nie None).
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_02_pobierz_json("https://api.przyklad.pl")
    # TODO: sprawdź wynik == {}
    pass


# --- zadanie_03 ---

def test_zadanie_03_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja z parametrami zwraca sparsowaną odpowiedź.
    Co udaje: requests.get — zwraca FakeResponse(200, {"wyniki": [1, 2]}).
    Co sprawdzam: wynik == {"wyniki": [1, 2]}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"wyniki": [1, 2]})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_03_pobierz_z_parametrami(
    #           "https://api.przyklad.pl", {"miasto": "Warszawa"})
    # TODO: sprawdź wynik == {"wyniki": [1, 2]}
    pass


def test_zadanie_03_przekazuje_parametry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik parametrów faktycznie trafia do requests.get.
    Co udaje: requests.get — zamiennik ZAPISUJE otrzymane params do listy
    i zwraca FakeResponse(200, {}).
    Co sprawdzam: zapisane params == {"miasto": "Warszawa"}.
    """
    # TODO: przygotuj pustą listę zapamietane = []
    # TODO: przygotuj zamiennik, który robi zapamietane.append(params)
    #       i zwraca FakeResponse(200, {})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_03_pobierz_z_parametrami(
    #           "https://api.przyklad.pl", {"miasto": "Warszawa"})
    # TODO: sprawdź zapamietane[0] == {"miasto": "Warszawa"}
    pass


# --- zadanie_04 ---

def test_zadanie_04_true_dla_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy kod 200 daje True.
    Co udaje: requests.get — zwraca FakeResponse(200, {}).
    Co sprawdzam: wynik is True.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_04_czy_sukces("https://api.przyklad.pl")
    # TODO: sprawdź wynik is True
    pass


def test_zadanie_04_false_dla_500(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy kod 500 daje False (a nie wyjątek).
    Co udaje: requests.get — zwraca FakeResponse(500, {}).
    Co sprawdzam: wynik is False.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(500, {})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_04_czy_sukces("https://api.przyklad.pl")
    # TODO: sprawdź wynik is False
    pass


# --- zadanie_05 ---

def test_zadanie_05_sukces_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy przy kodzie 200 funkcja zwraca sparsowane dane.
    Co udaje: requests.get — zwraca FakeResponse(200, {"id": 1}).
    Co sprawdzam: wynik == {"id": 1}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"id": 1})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_05_pobierz_z_kontrola("https://api.przyklad.pl")
    # TODO: sprawdź wynik == {"id": 1}
    pass


def test_zadanie_05_blad_serwera_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy przy kodzie 500 funkcja przepuszcza HTTPError.
    Co udaje: requests.get — zwraca FakeResponse(500, {}), którego
    raise_for_status rzuci HTTPError.
    Co sprawdzam: wywołanie rzuca requests.HTTPError (pytest.raises).
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(500, {})
    # TODO: podmień requests.get
    # TODO: w bloku with pytest.raises(requests.HTTPError):
    #       wywołaj zadanie_05_pobierz_z_kontrola("https://api.przyklad.pl")
    pass


# --- zadanie_06 ---

def test_zadanie_06_sukces_zwraca_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy przy sukcesie funkcja zwraca dane (nie None).
    Co udaje: requests.get — zwraca FakeResponse(200, {"id": 7}).
    Co sprawdzam: wynik == {"id": 7}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"id": 7})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_06_pobierz_bezpiecznie("https://api.przyklad.pl")
    # TODO: sprawdź wynik == {"id": 7}
    pass


def test_zadanie_06_awaria_sieci_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None przy awarii połączenia.
    Co udaje: requests.get — RZUCA requests.ConnectionError (dziecko
    RequestException), zamiast zwracać odpowiedź.
    Co sprawdzam: wynik is None (wyjątek złapany w funkcji).
    """
    # TODO: przygotuj zamiennik, który zamiast return robi:
    #       raise requests.ConnectionError("brak internetu")
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_06_pobierz_bezpiecznie("https://api.przyklad.pl")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_07 ---

def test_zadanie_07_zwraca_kod_201(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca kod statusu odpowiedzi na POST.
    Co udaje: requests.post — zwraca FakeResponse(201, {}).
    Co sprawdzam: wynik == 201.
    """
    # TODO: przygotuj zamiennik:
    #       def podmieniony_post(url, json=None, headers=None, timeout=None):
    #           return FakeResponse(201, {})
    # TODO: podmień: monkeypatch.setattr(
    #           "requests_api_podstawy.requests.post", podmieniony_post)
    # TODO: wywołaj zadanie_07_wyslij_post(
    #           "https://api.przyklad.pl", {"imie": "Anna"})
    # TODO: sprawdź wynik == 201
    pass


def test_zadanie_07_przekazuje_dane(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik danych trafia do requests.post jako json=.
    Co udaje: requests.post — zamiennik ZAPISUJE otrzymany json do listy
    i zwraca FakeResponse(201, {}).
    Co sprawdzam: zapisany json == {"imie": "Anna"}.
    """
    # TODO: przygotuj pustą listę zapamietane = []
    # TODO: przygotuj zamiennik, który robi zapamietane.append(json)
    #       i zwraca FakeResponse(201, {})
    # TODO: podmień requests.post
    # TODO: wywołaj zadanie_07_wyslij_post(
    #           "https://api.przyklad.pl", {"imie": "Anna"})
    # TODO: sprawdź zapamietane[0] == {"imie": "Anna"}
    pass


# --- zadanie_08 ---

def test_zadanie_08_zwraca_odpowiedz(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca sparsowaną treść odpowiedzi na POST.
    Co udaje: requests.post — zwraca FakeResponse(201, {"id": 5}).
    Co sprawdzam: wynik == {"id": 5}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(201, {"id": 5})
    # TODO: podmień requests.post
    # TODO: wywołaj zadanie_08_wyslij_post_z_naglowkami(
    #           "https://api.przyklad.pl", {"imie": "Anna"},
    #           {"Authorization": "Bearer klucz"})
    # TODO: sprawdź wynik == {"id": 5}
    pass


def test_zadanie_08_przekazuje_naglowki(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy słownik nagłówków trafia do requests.post jako headers=.
    Co udaje: requests.post — zamiennik ZAPISUJE otrzymane headers do listy
    i zwraca FakeResponse(201, {}).
    Co sprawdzam: zapisane headers == {"Authorization": "Bearer klucz"}.
    """
    # TODO: przygotuj pustą listę zapamietane = []
    # TODO: przygotuj zamiennik, który robi zapamietane.append(headers)
    #       i zwraca FakeResponse(201, {})
    # TODO: podmień requests.post
    # TODO: wywołaj zadanie_08_wyslij_post_z_naglowkami(
    #           "https://api.przyklad.pl", {"imie": "Anna"},
    #           {"Authorization": "Bearer klucz"})
    # TODO: sprawdź zapamietane[0] == {"Authorization": "Bearer klucz"}
    pass


# --- zadanie_09 ---

def test_zadanie_09_zwraca_liste(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja zwraca listę słowników z odpowiedzi.
    Co udaje: requests.get — zwraca FakeResponse(200,
    [{"imie": "Anna"}, {"imie": "Piotr"}]).
    Co sprawdzam: len(wynik) == 2 i wynik[0]["imie"] == "Anna".
    """
    # TODO: przygotuj zamiennik zwracający
    #       FakeResponse(200, [{"imie": "Anna"}, {"imie": "Piotr"}])
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_09_pobierz_liste_uzytkownikow("https://api.przyklad.pl")
    # TODO: sprawdź len(wynik) == 2 i wynik[0]["imie"] == "Anna"
    pass


def test_zadanie_09_blad_404_rzuca_wyjatek(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy kod 404 kończy się wyjątkiem HTTPError (nie pustą listą).
    Co udaje: requests.get — zwraca FakeResponse(404, []).
    Co sprawdzam: wywołanie rzuca requests.HTTPError (pytest.raises).
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(404, [])
    # TODO: podmień requests.get
    # TODO: w bloku with pytest.raises(requests.HTTPError):
    #       wywołaj zadanie_09_pobierz_liste_uzytkownikow("https://api.przyklad.pl")
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_wartosc_pola(monkeypatch: pytest.MonkeyPatch) -> None:
    """Co testuje: czy funkcja wyciąga wartość istniejącego pola.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna", "wiek": 30}).
    Co sprawdzam: wynik == "Anna" dla pola "imie".
    """
    # TODO: przygotuj zamiennik zwracający
    #       FakeResponse(200, {"imie": "Anna", "wiek": 30})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_10_pobierz_pole("https://api.przyklad.pl", "imie")
    # TODO: sprawdź wynik == "Anna"
    pass


def test_zadanie_10_brak_pola_zwraca_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None gdy pola nie ma w odpowiedzi.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik is None dla pola "email".
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"imie": "Anna"})
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_10_pobierz_pole("https://api.przyklad.pl", "email")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_11 ---

def test_zadanie_11_zapisuje_dane_do_pliku(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy pobrane dane lądują w pliku JSON i funkcja zwraca True.
    Co udaje: requests.get — zwraca FakeResponse(200, {"imie": "Anna"}).
    Co sprawdzam: wynik is True; plik po wczytaniu przez json.load
    zawiera {"imie": "Anna"}.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, {"imie": "Anna"})
    # TODO: podmień requests.get
    # TODO: przygotuj p = tmp_path / "kopia.json"
    # TODO: wywołaj zadanie_11_zapisz_odpowiedz_do_json(
    #           "https://api.przyklad.pl", str(p)) i zapisz wynik
    # TODO: sprawdź wynik is True
    # TODO: otwórz plik (encoding="utf-8") i sprawdź
    #       json.load(f) == {"imie": "Anna"}
    pass


def test_zadanie_11_blad_serwera_nie_tworzy_pliku(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy przy kodzie 500 wyjątek leci PRZED zapisem pliku.
    Co udaje: requests.get — zwraca FakeResponse(500, {}).
    Co sprawdzam: wywołanie rzuca requests.HTTPError, a plik nie istnieje.
    """
    # TODO: przygotuj zamiennik zwracający FakeResponse(500, {})
    # TODO: podmień requests.get
    # TODO: przygotuj p = tmp_path / "kopia.json"
    # TODO: w bloku with pytest.raises(requests.HTTPError):
    #       wywołaj zadanie_11_zapisz_odpowiedz_do_json(
    #           "https://api.przyklad.pl", str(p))
    # TODO: sprawdź p.exists() is False
    pass


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
    # TODO: przygotuj zamiennik zwracający FakeResponse(200, [
    #           {"imie": "Anna", "wiek": "30"},
    #           {"imie": "Piotr", "wiek": "25"},
    #       ])
    # TODO: podmień requests.get
    # TODO: przygotuj p = tmp_path / "uzytkownicy.csv"
    # TODO: wywołaj zadanie_12_zapisz_uzytkownikow_do_csv(
    #           "https://api.przyklad.pl", str(p)) i zapisz wynik
    # TODO: sprawdź wynik == 2
    # TODO: otwórz plik (newline="", encoding="utf-8"),
    #       wczytaj wiersze = list(csv.DictReader(f))
    # TODO: sprawdź len(wiersze) == 2 i wiersze[0]["imie"] == "Anna"
    pass


def test_zadanie_12_naglowki_z_kluczy_slownika(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy nagłówki CSV pochodzą z kluczy pierwszego słownika.
    Co udaje: requests.get — zwraca FakeResponse(200,
    [{"imie": "Anna", "wiek": "30"}]).
    Co sprawdzam: fieldnames wczytanego pliku == ["imie", "wiek"].
    """
    # TODO: przygotuj zamiennik zwracający
    #       FakeResponse(200, [{"imie": "Anna", "wiek": "30"}])
    # TODO: podmień requests.get
    # TODO: przygotuj p = tmp_path / "uzytkownicy.csv"
    # TODO: wywołaj zadanie_12_zapisz_uzytkownikow_do_csv(
    #           "https://api.przyklad.pl", str(p))
    # TODO: otwórz plik (newline="", encoding="utf-8"),
    #       utwórz reader = csv.DictReader(f)
    # TODO: sprawdź list(reader.fieldnames) == ["imie", "wiek"]
    pass
