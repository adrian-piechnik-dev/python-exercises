from pathlib import Path

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Error, Page, expect

from playwright_pytest_network import (
    zadanie_01_naglowek_strony,
    zadanie_02_podmien_strone,
    zadanie_03_podmien_api_json,
    zadanie_04_zablokuj_obrazki,
    zadanie_05_pobierz_status_api,
    zadanie_06_pobierz_json_api,
    zadanie_07_utworz_produkt_api,
    zadanie_08_polecenie_codegen,
    zadanie_09_polecenie_trace,
    zadanie_10_nagraj_trace,
    zadanie_11_przetlumacz_podmiane,
    zadanie_12_sklep_offline,
)


# --- zadanie_01 ---

def test_zadanie_01_czyta_naglowek(page: Page) -> None:
    """Co testuje: rozgrzewke — set_content + get_by_role na karcie z wtyczki.
    Co udaje: internet — HTML wstrzykniety przez set_content.
    Co sprawdzam: wynik == "Katalog" dla HTML z naglowkiem Katalog.
    """
    # TODO: przygotuj prosty HTML z jednym <h1>Katalog</h1>
    # TODO: wywolaj zadanie_01_naglowek_strony(page, html)
    # TODO: sprawdz assertem tekst
    pass


def test_zadanie_01_pusty_naglowek(page: Page) -> None:
    """Co testuje: przypadek brzegowy — pusty <h1></h1> daje pusty tekst.
    Co udaje: internet — HTML wstrzykniety przez set_content.
    Co sprawdzam: wynik == "".
    """
    # TODO: przygotuj HTML z pustym <h1></h1>
    # TODO: wywolaj funkcje i sprawdz assertem pusty string
    pass


# --- zadanie_02 ---

def test_zadanie_02_goto_dostaje_podstawiona_strone(page: Page) -> None:
    """Co testuje: czy celnik podstawia HTML pod adresem, ktorego nie ma
    w internecie — goto dziala w pelni offline.
    Co udaje: internet — celnik z route.fulfill (body + content_type).
    Co sprawdzam: po goto na "https://sklep.testowy/sklep"
    page.title() == "Atrapa".
    """
    # TODO: przygotuj HTML "<html><head><title>Atrapa</title></head></html>"
    # TODO: podmien (zarejestruj celnika) przez zadanie_02_podmien_strone
    #       na adresie "https://sklep.testowy/sklep" — PRZED goto!
    # TODO: wywolaj page.goto("https://sklep.testowy/sklep")
    # TODO: sprawdz assertem tytul strony
    pass


def test_zadanie_02_naglowek_z_podstawionej_strony_widoczny(page: Page) -> None:
    """Co testuje: czy content_type="text/html" sprawia, ze przegladarka
    RENDERUJE podstawiony HTML (a nie pokazuje go jako tekst).
    Co udaje: internet — celnik z route.fulfill.
    Co sprawdzam: get_by_role("heading") ma tekst "Sklep atrapa".
    """
    # TODO: przygotuj HTML z <h1>Sklep atrapa</h1>
    # TODO: zarejestruj celnika i wykonaj goto na podmieniony adres
    # TODO: sprawdz assertem inner_text naglowka przez get_by_role
    pass


# --- zadanie_03 ---

def test_zadanie_03_goto_pokazuje_podstawiony_json(page: Page) -> None:
    """Co testuje: czy celnik podstawia JSON pod adresem API — trik z teorii:
    goto na adres JSON pokazuje jego tresc jako tekst strony.
    Co udaje: internet — celnik z route.fulfill(json=...).
    Co sprawdzam: po goto tekst "Krakow" jest widoczny na stronie
    (expect + to_be_visible).
    """
    # TODO: podmien API przez zadanie_03_podmien_api_json na wzorcu
    #       "**/api/dane" ze slownikiem {"miasto": "Krakow"}
    # TODO: wywolaj page.goto("https://sklep.testowy/api/dane")
    # TODO: sprawdz przez expect(page.get_by_text("Krakow")).to_be_visible()
    pass


def test_zadanie_03_zwraca_none(page: Page) -> None:
    """Co testuje: kontrakt None — funkcja tylko rejestruje celnika,
    niczego nie zwraca.
    Co udaje: internet — celnik z route.fulfill.
    Co sprawdzam: wynik is None.
    """
    # TODO: wywolaj funkcje z dowolnym wzorcem i slownikiem,
    #       zapisujac wynik do zmiennej
    # TODO: sprawdz assertem, ze wynik is None
    pass


# --- zadanie_04 ---

def test_zadanie_04_strona_dziala_mimo_zablokowanych_obrazkow(
    page: Page,
) -> None:
    """Co testuje: sens blokowania — strona z obrazkiem laduje sie dobrze,
    choc sam obrazek zostal ubity przez celnika.
    Co udaje: internet — celnik abort na "**/*.png" + celnik fulfill
    na strone z <img src="logo.png">.
    Co sprawdzam: naglowek strony widoczny (inner_text == "Galeria").
    """
    # TODO: zarejestruj blokade przez zadanie_04_zablokuj_obrazki(page)
    # TODO: podmien strone (zadanie_02) na adresie
    #       "https://sklep.testowy/galeria" HTML-em:
    #       "<html><body><h1>Galeria</h1><img src='logo.png'></body></html>"
    # TODO: wykonaj goto na ten adres
    # TODO: sprawdz assertem tekst naglowka
    pass


def test_zadanie_04_goto_na_png_rzuca_error(page: Page) -> None:
    """Co testuje: przypadek brzegowy — nawigacja PROSTO na zablokowany
    adres konczy sie wyjatkiem Error.
    Co udaje: internet — celnik abort.
    Co sprawdzam: page.goto("https://sklep.testowy/logo.png") w bloku
    pytest.raises(Error).
    """
    # TODO: zarejestruj blokade obrazkow
    # TODO: w bloku with pytest.raises(Error): wykonaj goto na adres .png
    pass


# --- zadanie_05 ---

def test_zadanie_05_status_200_dla_produktow(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: zapytanie GET do budki-serwera przez request_context.
    Co udaje: prawdziwe API — lokalna budka-serwer z fixture.
    Co sprawdzam: wynik == 200 dla adresu <serwer>/produkty.
    """
    # TODO: zbuduj adres f"{serwer_api}/produkty"
    # TODO: wywolaj zadanie_05_pobierz_status_api(api, adres)
    # TODO: sprawdz assertem status 200
    pass


def test_zadanie_05_status_404_dla_nieznanej_sciezki(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: przypadek brzegowy — nieznana sciezka daje 404.
    Co udaje: prawdziwe API — lokalna budka-serwer.
    Co sprawdzam: wynik == 404 dla adresu <serwer>/nie-ma-takiej.
    """
    # TODO: zbuduj adres nieistniejacej sciezki i wywolaj funkcje
    # TODO: sprawdz assertem status 404
    pass


# --- zadanie_06 ---

def test_zadanie_06_zwraca_slownik_produktu(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: wzorzec z requests — ok daje slownik z JSON-a.
    Co udaje: prawdziwe API — budka-serwer (GET /produkt/1).
    Co sprawdzam: wynik == {"id": 1, "nazwa": "kubek"}.
    """
    # TODO: wywolaj zadanie_06_pobierz_json_api dla adresu /produkt/1
    # TODO: sprawdz assertem caly slownik
    pass


def test_zadanie_06_zwraca_none_dla_404(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: kontrakt None — status 404 daje None, nie wyjatek.
    Co udaje: prawdziwe API — budka-serwer (GET /produkt/999 nie istnieje).
    Co sprawdzam: wynik is None.
    """
    # TODO: wywolaj funkcje dla adresu /produkt/999
    # TODO: sprawdz assertem, ze wynik is None
    pass


# --- zadanie_07 ---

def test_zadanie_07_post_zwraca_201(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: POST nowego produktu do budki-serwera.
    Co udaje: prawdziwe API — budka-serwer (POST /produkty -> 201).
    Co sprawdzam: wynik == 201.
    """
    # TODO: wywolaj zadanie_07_utworz_produkt_api dla adresu /produkty
    #       ze slownikiem {"nazwa": "szklanka"}
    # TODO: sprawdz assertem status 201
    pass


def test_zadanie_07_post_w_zle_miejsce_zwraca_404(
    api: APIRequestContext, serwer_api: str,
) -> None:
    """Co testuje: przypadek brzegowy — POST na nieznana sciezke daje 404.
    Co udaje: prawdziwe API — budka-serwer.
    Co sprawdzam: wynik == 404 dla adresu /zamowienia.
    """
    # TODO: wywolaj funkcje dla adresu /zamowienia z dowolnym slownikiem
    # TODO: sprawdz assertem status 404
    pass


# --- zadanie_08 ---

def test_zadanie_08_sklada_komende_codegen() -> None:
    """Co testuje: budowanie komendy codegen dla adresu.
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik == "playwright codegen https://example.com".
    """
    # TODO: wywolaj zadanie_08_polecenie_codegen("https://example.com")
    # TODO: sprawdz assertem cala komende
    pass


def test_zadanie_08_komenda_zaczyna_sie_od_playwright() -> None:
    """Co testuje: czy komenda wywoluje narzedzie playwright (prefiks).
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik.startswith("playwright codegen ") is True.
    """
    # TODO: wywolaj funkcje z dowolnym adresem
    # TODO: sprawdz assertem prefiks przez startswith
    pass


# --- zadanie_09 ---

def test_zadanie_09_sklada_komende_show_trace() -> None:
    """Co testuje: budowanie komendy otwierajacej nagranie.
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik == "playwright show-trace nagranie.zip".
    """
    # TODO: wywolaj zadanie_09_polecenie_trace("nagranie.zip")
    # TODO: sprawdz assertem cala komende
    pass


def test_zadanie_09_sciezka_pliku_trafia_na_koniec() -> None:
    """Co testuje: czy inna sciezka pliku laduje na koncu komendy.
    Co udaje: nic — czysta funkcja na tekstach.
    Co sprawdzam: wynik.endswith("wyniki/test.zip") is True.
    """
    # TODO: wywolaj funkcje ze sciezka "wyniki/test.zip"
    # TODO: sprawdz assertem koncowke przez endswith
    pass


# --- zadanie_10 ---

def test_zadanie_10_tworzy_plik_z_nagraniem(
    context: BrowserContext, tmp_path: Path,
) -> None:
    """Co testuje: czy nagrywanie trace konczy sie plikiem .zip na dysku.
    Co udaje: docelowy folder — tmp_path od pytest.
    Co sprawdzam: wynik is True i plik istnieje.
    """
    # TODO: przygotuj sciezke str(tmp_path / "nagranie.zip")
    # TODO: wywolaj zadanie_10_nagraj_trace(context, sciezka)
    # TODO: sprawdz assertem wynik is True
    # TODO: sprawdz assertem istnienie pliku ((tmp_path / "nagranie.zip")
    #       .exists() is True)
    pass


def test_zadanie_10_nagranie_nie_jest_puste(
    context: BrowserContext, tmp_path: Path,
) -> None:
    """Co testuje: czy zapisany plik ma niezerowy rozmiar (naprawde cos
    nagrano, nie pusty plik).
    Co udaje: docelowy folder — tmp_path.
    Co sprawdzam: rozmiar pliku > 0 (przez .stat().st_size).
    """
    # TODO: wywolaj funkcje ze sciezka w tmp_path
    # TODO: sprawdz assertem, ze (sciezka).stat().st_size > 0
    pass


# --- zadanie_11 ---

def test_zadanie_11_tlumaczy_stare_podmiany() -> None:
    """Co testuje: mape zazebienia — stare narzedzia podmiany na nowe.
    Co udaje: nic — czysta funkcja na slowniku.
    Co sprawdzam: "monkeypatch.setattr" -> "page.route"
    oraz "side_effect" -> "route.abort".
    """
    # TODO: wywolaj zadanie_11_przetlumacz_podmiane("monkeypatch.setattr")
    #       i sprawdz assertem wynik
    # TODO: wywolaj funkcje dla "side_effect" i sprawdz assertem wynik
    pass


def test_zadanie_11_none_dla_nieznanego_narzedzia() -> None:
    """Co testuje: kontrakt None — narzedzie spoza sciagi daje None.
    Co udaje: nic — czysta funkcja na slowniku.
    Co sprawdzam: wynik is None dla "czarna-magia".
    """
    # TODO: wywolaj funkcje z nazwa spoza slownika
    # TODO: sprawdz assertem, ze wynik is None
    pass


# --- zadanie_12 ---

def test_zadanie_12_sklep_offline_rysuje_produkty(
    page: Page, html_sklepu: str,
) -> None:
    """Co testuje: final — strona i jej API podstawione przez celnikow,
    skrypt strony pobiera dane i rysuje liste, funkcja czyta nazwy.
    Co udaje: internet — dwaj celnicy (HTML + JSON).
    Co sprawdzam: wynik == ["kubek", "talerz"].
    """
    # TODO: przygotuj produkty: [{"nazwa": "kubek"}, {"nazwa": "talerz"}]
    # TODO: wywolaj zadanie_12_sklep_offline(page, html_sklepu, produkty)
    # TODO: sprawdz assertem cala liste nazw
    pass


def test_zadanie_12_pusta_lista_produktow_daje_pusta_liste(
    page: Page, html_sklepu: str,
) -> None:
    """Co testuje: przypadek brzegowy — API zwraca pusta liste, sklep
    rysuje pusta liste (i nic nie wybucha).
    Co udaje: internet — dwaj celnicy (HTML + JSON z pusta lista).
    Co sprawdzam: wynik == [].
    """
    # TODO: wywolaj funkcje z pusta lista produktow
    # TODO: sprawdz assertem, ze wynik to pusta lista
    pass
