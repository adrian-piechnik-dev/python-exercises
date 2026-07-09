import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from fastapi_pydantic import (
    zadanie_01_aplikacja_powitalna,
    zadanie_02_dwa_endpointy,
    zadanie_03_parametr_sciezki,
    zadanie_04_kwadrat_liczby,
    zadanie_05_utworz_produkt,
    zadanie_06_przyjmij_produkt,
    zadanie_07_przyjmij_zamowienie,
    zadanie_08_response_model,
    zadanie_09_echo_produktu,
    zadanie_10_api_konfiguracji,
    zadanie_11_api_dodawania,
    zadanie_12_pelne_api,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_powitanie() -> None:
    """Co testuje: czy GET / odpowiada kodem 200 i powitalnym JSON-em.
    Co udaje: sieć — TestClient woła aplikację w pamięci, bez serwera.
    Co sprawdzam: status_code == 200
    i json() == {"wiadomosc": "Witaj w API"}.
    """
    # TODO: przygotuj client = TestClient(zadanie_01_aplikacja_powitalna())
    #       (nawiasy! podajesz APLIKACJĘ, nie funkcję)
    # TODO: wywołaj response = client.get("/")
    # TODO: sprawdź response.status_code == 200
    # TODO: sprawdź response.json() == {"wiadomosc": "Witaj w API"}
    pass


def test_zadanie_01_nieznana_sciezka_daje_404() -> None:
    """Co testuje: czy ścieżka bez endpointu dostaje standardowe 404.
    Co udaje: sieć — TestClient.
    Co sprawdzam: GET /nieistnieje ma status_code == 404.
    """
    # TODO: przygotuj client = TestClient(zadanie_01_aplikacja_powitalna())
    # TODO: wywołaj response = client.get("/nieistnieje")
    # TODO: sprawdź response.status_code == 404
    pass


# --- zadanie_02 ---

def test_zadanie_02_endpoint_glowny_dziala() -> None:
    """Co testuje: czy pierwszy z dwóch endpointów (GET /) odpowiada.
    Co udaje: sieć — TestClient.
    Co sprawdzam: status 200 i json() == {"wiadomosc": "Witaj w API"}.
    """
    # TODO: przygotuj client = TestClient(zadanie_02_dwa_endpointy())
    # TODO: wywołaj response = client.get("/")
    # TODO: sprawdź status 200 i treść {"wiadomosc": "Witaj w API"}
    pass


def test_zadanie_02_endpoint_o_nas_dziala() -> None:
    """Co testuje: czy drugi endpoint (GET /o-nas) współistnieje z pierwszym.
    Co udaje: sieć — TestClient.
    Co sprawdzam: status 200
    i json() == {"nazwa": "Sklep Python", "wersja": 1}.
    """
    # TODO: przygotuj client = TestClient(zadanie_02_dwa_endpointy())
    # TODO: wywołaj response = client.get("/o-nas")
    # TODO: sprawdź status 200 i treść {"nazwa": "Sklep Python", "wersja": 1}
    pass


# --- zadanie_03 ---

def test_zadanie_03_liczba_z_adresu_jako_int() -> None:
    """Co testuje: czy parametr ścieżki wraca jako int (konwersja z adresu).
    Co udaje: sieć — TestClient.
    Co sprawdzam: GET /uzytkownicy/7 daje 200 i json() == {"id": 7}
    (7 jako liczba, nie "7").
    """
    # TODO: przygotuj client = TestClient(zadanie_03_parametr_sciezki())
    # TODO: wywołaj response = client.get("/uzytkownicy/7")
    # TODO: sprawdź status 200
    # TODO: sprawdź response.json() == {"id": 7}
    pass


def test_zadanie_03_tekst_w_adresie_daje_422() -> None:
    """Co testuje: czy walidacja type hintem odrzuca tekst zamiast liczby.
    Co udaje: sieć — TestClient.
    Co sprawdzam: GET /uzytkownicy/abc ma status_code == 422.
    """
    # TODO: przygotuj client = TestClient(zadanie_03_parametr_sciezki())
    # TODO: wywołaj response = client.get("/uzytkownicy/abc")
    # TODO: sprawdź response.status_code == 422
    pass


# --- zadanie_04 ---

def test_zadanie_04_liczy_kwadrat() -> None:
    """Co testuje: czy endpoint liczy kwadrat liczby z adresu.
    Co udaje: sieć — TestClient.
    Co sprawdzam: GET /kwadrat/5 daje json() == {"wynik": 25}.
    """
    # TODO: przygotuj client = TestClient(zadanie_04_kwadrat_liczby())
    # TODO: wywołaj response = client.get("/kwadrat/5")
    # TODO: sprawdź response.json() == {"wynik": 25}
    pass


def test_zadanie_04_tekst_daje_422() -> None:
    """Co testuje: czy nie-liczba w adresie kończy się kodem 422.
    Co udaje: sieć — TestClient.
    Co sprawdzam: GET /kwadrat/xyz ma status_code == 422.
    """
    # TODO: przygotuj client = TestClient(zadanie_04_kwadrat_liczby())
    # TODO: wywołaj response = client.get("/kwadrat/xyz")
    # TODO: sprawdź response.status_code == 422
    pass


# --- zadanie_05 ---

def test_zadanie_05_tworzy_produkt_z_konwersja() -> None:
    """Co testuje: czy Pydantic tworzy obiekt i konwertuje "49" na 49.0.
    Co udaje: nic — czysta walidacja Pydantic, bez sieci.
    Co sprawdzam: wynik.nazwa == "Mysz" i wynik.cena == 49.0 (float).
    """
    # TODO: wywołaj zadanie_05_utworz_produkt("Mysz", "49")
    # TODO: sprawdź wynik.nazwa == "Mysz"
    # TODO: sprawdź wynik.cena == 49.0
    pass


def test_zadanie_05_zla_cena_rzuca_validation_error() -> None:
    """Co testuje: czy nie-liczbowa cena kończy się ValidationError.
    Co udaje: nic — czysta walidacja Pydantic.
    Co sprawdzam: wywołanie z cena="darmo" rzuca ValidationError
    (pytest.raises — temat 13).
    """
    # TODO: w bloku with pytest.raises(ValidationError):
    #       wywołaj zadanie_05_utworz_produkt("Mysz", "darmo")
    pass


# --- zadanie_06 ---

def test_zadanie_06_przyjmuje_poprawny_produkt() -> None:
    """Co testuje: czy POST z poprawnym JSON-em przechodzi walidację modelu.
    Co udaje: sieć — TestClient.
    Co sprawdzam: status 200 i json() == {"przyjeto": "Mysz"}.
    """
    # TODO: przygotuj client = TestClient(zadanie_06_przyjmij_produkt())
    # TODO: wywołaj response = client.post(
    #           "/produkty", json={"nazwa": "Mysz", "cena": 49.0})
    # TODO: sprawdź status 200 i treść {"przyjeto": "Mysz"}
    pass


def test_zadanie_06_brak_pola_daje_422() -> None:
    """Co testuje: czy JSON bez wymaganego pola cena dostaje 422.
    Co udaje: sieć — TestClient.
    Co sprawdzam: POST z {"nazwa": "Mysz"} ma status_code == 422.
    """
    # TODO: przygotuj client = TestClient(zadanie_06_przyjmij_produkt())
    # TODO: wywołaj response = client.post(
    #           "/produkty", json={"nazwa": "Mysz"})
    # TODO: sprawdź response.status_code == 422
    pass


# --- zadanie_07 ---

def test_zadanie_07_liczy_wartosc_zamowienia() -> None:
    """Co testuje: czy endpoint mnoży ilość przez cenę jednostkową.
    Co udaje: sieć — TestClient.
    Co sprawdzam: 3 sztuki po 10.0 dają json() == {"do_zaplaty": 30.0}.
    """
    # TODO: przygotuj client = TestClient(zadanie_07_przyjmij_zamowienie())
    # TODO: wywołaj response = client.post("/zamowienia", json={
    #           "nazwa": "Mysz", "ilosc": 3, "cena_jednostkowa": 10.0})
    # TODO: sprawdź response.json() == {"do_zaplaty": 30.0}
    pass


def test_zadanie_07_zla_ilosc_daje_422() -> None:
    """Co testuje: czy tekst w polu ilosc (int) odrzuca walidacja modelu.
    Co udaje: sieć — TestClient.
    Co sprawdzam: POST z ilosc="duzo" ma status_code == 422.
    """
    # TODO: przygotuj client = TestClient(zadanie_07_przyjmij_zamowienie())
    # TODO: wywołaj response = client.post("/zamowienia", json={
    #           "nazwa": "Mysz", "ilosc": "duzo", "cena_jednostkowa": 10.0})
    # TODO: sprawdź response.status_code == 422
    pass


# --- zadanie_08 ---

def test_zadanie_08_tajne_pole_nie_wychodzi() -> None:
    """Co testuje: czy response_model wycina pole spoza modelu Produkt.
    Co udaje: sieć — TestClient.
    Co sprawdzam: w odpowiedzi NIE ma klucza "tajny_kod".
    """
    # TODO: przygotuj client = TestClient(zadanie_08_response_model())
    # TODO: wywołaj response = client.get("/produkty/polecany")
    # TODO: sprawdź "tajny_kod" not in response.json()
    pass


def test_zadanie_08_pola_modelu_zostaja() -> None:
    """Co testuje: czy pola zgodne z modelem przechodzą przez filtr.
    Co udaje: sieć — TestClient.
    Co sprawdzam: json() == {"nazwa": "Klawiatura", "cena": 99.0}.
    """
    # TODO: przygotuj client = TestClient(zadanie_08_response_model())
    # TODO: wywołaj response = client.get("/produkty/polecany")
    # TODO: sprawdź response.json() == {"nazwa": "Klawiatura", "cena": 99.0}
    pass


# --- zadanie_09 ---

def test_zadanie_09_odsyla_przyjety_produkt() -> None:
    """Co testuje: czy echo zwraca dokładnie to, co przyszło (po walidacji).
    Co udaje: sieć — TestClient.
    Co sprawdzam: json() == {"nazwa": "Monitor", "cena": 899.0}.
    """
    # TODO: przygotuj client = TestClient(zadanie_09_echo_produktu())
    # TODO: wywołaj response = client.post("/produkty/echo",
    #           json={"nazwa": "Monitor", "cena": 899.0})
    # TODO: sprawdź response.json() == {"nazwa": "Monitor", "cena": 899.0}
    pass


def test_zadanie_09_puste_body_daje_422() -> None:
    """Co testuje: czy puste body nie przechodzi walidacji modelu.
    Co udaje: sieć — TestClient.
    Co sprawdzam: POST z json={} ma status_code == 422.
    """
    # TODO: przygotuj client = TestClient(zadanie_09_echo_produktu())
    # TODO: wywołaj response = client.post("/produkty/echo", json={})
    # TODO: sprawdź response.status_code == 422
    pass


# --- zadanie_10 ---

def test_zadanie_10_serwuje_zawartosc_pliku(tmp_path: Path) -> None:
    """Co testuje: czy GET /konfiguracja zwraca słownik z pliku JSON.
    Co udaje: dysk — tmp_path z własnym plikiem konfiguracji; sieć —
    TestClient.
    Co sprawdzam: json() == {"jezyk": "pl", "limit": 10}.
    """
    # TODO: przygotuj p = tmp_path / "konfiguracja.json"
    # TODO: zapisz p.write_text(json.dumps({"jezyk": "pl", "limit": 10}),
    #       encoding="utf-8")
    # TODO: przygotuj client = TestClient(zadanie_10_api_konfiguracji(str(p)))
    # TODO: wywołaj response = client.get("/konfiguracja")
    # TODO: sprawdź response.json() == {"jezyk": "pl", "limit": 10}
    pass


def test_zadanie_10_czyta_plik_przy_kazdym_zapytaniu(tmp_path: Path) -> None:
    """Co testuje: czy endpoint czyta plik na żywo (zmiana pliku = zmiana
    odpowiedzi).
    Co udaje: dysk — tmp_path; sieć — TestClient.
    Co sprawdzam: po nadpisaniu pliku drugi GET zwraca nową zawartość.
    """
    # TODO: przygotuj plik z {"jezyk": "pl"} i client jak w teście wyżej
    # TODO: wywołaj pierwszy GET i sprawdź {"jezyk": "pl"}
    # TODO: nadpisz plik: p.write_text(json.dumps({"jezyk": "en"}),
    #       encoding="utf-8")
    # TODO: wywołaj drugi GET i sprawdź {"jezyk": "en"}
    pass


# --- zadanie_11 ---

def test_zadanie_11_dopisuje_do_pliku(plik_produktow: Path) -> None:
    """Co testuje: czy POST dopisuje produkt na koniec listy w pliku.
    Co udaje: dysk — fixture plik_produktow (3 produkty); sieć — TestClient.
    Co sprawdzam: odpowiedź {"liczba": 4}, a ostatni wpis pliku to
    dodany produkt.
    """
    # TODO: przygotuj client = TestClient(
    #           zadanie_11_api_dodawania(str(plik_produktow)))
    # TODO: wywołaj response = client.post("/produkty",
    #           json={"nazwa": "Podkladka", "cena": 19.0})
    # TODO: sprawdź response.json() == {"liczba": 4}
    # TODO: otwórz plik (encoding="utf-8"), wczytaj json.load
    # TODO: sprawdź, że ostatni element listy ==
    #       {"nazwa": "Podkladka", "cena": 19.0}
    pass


def test_zadanie_11_zle_dane_nie_zmieniaja_pliku(plik_produktow: Path) -> None:
    """Co testuje: czy walidacja (422) zatrzymuje zapis — plik bez zmian.
    Co udaje: dysk — fixture plik_produktow; sieć — TestClient.
    Co sprawdzam: POST bez pola cena daje 422, a plik nadal ma 3 wpisy.
    """
    # TODO: przygotuj client = TestClient(
    #           zadanie_11_api_dodawania(str(plik_produktow)))
    # TODO: wywołaj response = client.post("/produkty",
    #           json={"nazwa": "Podkladka"})
    # TODO: sprawdź response.status_code == 422
    # TODO: otwórz plik i sprawdź len(json.load(f)) == 3
    pass


# --- zadanie_12 ---

def test_zadanie_12_get_zwraca_liste_z_pliku(klient_api: TestClient) -> None:
    """Co testuje: czy GET /produkty serwuje listę z pliku-magazynu.
    Co udaje: wszystko przygotowała fixture klient_api (specjalny fixture
    z tematu 13 — podaje gotowego klienta zamiast danych).
    Co sprawdzam: status 200, 3 produkty, pierwszy to Klawiatura.
    """
    # TODO: wywołaj response = klient_api.get("/produkty")
    # TODO: sprawdź response.status_code == 200
    # TODO: sprawdź len(response.json()) == 3
    # TODO: sprawdź response.json()[0]["nazwa"] == "Klawiatura"
    pass


def test_zadanie_12_post_potem_get_widzi_nowy_produkt(
    klient_api: TestClient,
) -> None:
    """Co testuje: pełny obieg — POST dodaje, kolejny GET już widzi 4 produkty.
    Co udaje: fixture klient_api (plik + aplikacja + klient).
    Co sprawdzam: POST daje {"liczba": 4}, a następny GET zwraca listę
    z 4 elementami zakończoną dodanym produktem.
    """
    # TODO: wywołaj response_post = klient_api.post("/produkty",
    #           json={"nazwa": "Podkladka", "cena": 19.0})
    # TODO: sprawdź response_post.json() == {"liczba": 4}
    # TODO: wywołaj response_get = klient_api.get("/produkty")
    # TODO: sprawdź len(response_get.json()) == 4
    # TODO: sprawdź response_get.json()[-1]["nazwa"] == "Podkladka"
    pass
