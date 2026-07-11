import csv
from pathlib import Path

import pytest

from conftest import FakeResponse
from scraping_beautifulsoup import (
    zadanie_01_tytul_strony,
    zadanie_02_teksty_linkow,
    zadanie_03_adresy_linkow,
    zadanie_04_teksty_po_klasie,
    zadanie_05_tekst_po_id,
    zadanie_06_teksty_selektorem,
    zadanie_07_pierwszy_selektorem,
    zadanie_08_tabela_do_listy,
    zadanie_09_adresy_obrazkow,
    zadanie_10_pobierz_tytul,
    zadanie_11_scrapuj_z_pauza,
    zadanie_12_zapisz_linki_do_csv,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_tekst_h1(html_strona: str) -> None:
    """Co testuje: czy funkcja wyciąga treść nagłówka h1.
    Co udaje: nic — HTML podaję bezpośrednio jako string (fixture html_strona).
    Co sprawdzam: wynik == "Sklep Python".
    """
    wynik = zadanie_01_tytul_strony(html_strona)
    assert wynik == "Sklep Python"


def test_zadanie_01_brak_h1_zwraca_none() -> None:
    """Co testuje: kontrakt None dla strony bez nagłówka h1.
    Co udaje: nic — podaję własny minimalny HTML bez h1.
    Co sprawdzam: wynik is None.
    """
    html = "<html><body><p>Sama treść</p></body></html>"
    wynik = zadanie_01_tytul_strony(html)
    assert wynik is None


# --- zadanie_02 ---

def test_zadanie_02_zbiera_teksty_linkow(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera teksty wszystkich znaczników a.
    Co udaje: nic — używam fixture html_strona (2 linki).
    Co sprawdzam: wynik == ["Produkty", "Kontakt"].
    """
    wynik = zadanie_02_teksty_linkow(html_strona)
    assert wynik == ["Produkty", "Kontakt"]


def test_zadanie_02_brak_linkow_pusta_lista() -> None:
    """Co testuje: pustą listę (nie None) dla strony bez linków.
    Co udaje: nic — podaję własny HTML bez znaczników a.
    Co sprawdzam: wynik == [].
    """
    html = "<html><body><h1>Tytuł</h1></body></html>"
    wynik = zadanie_02_teksty_linkow(html)
    assert wynik == []


# --- zadanie_03 ---

def test_zadanie_03_zbiera_adresy_href(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera wartości atrybutu href wszystkich linków.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == ["/produkty", "/kontakt"].
    """
    wynik = zadanie_03_adresy_linkow(html_strona)
    assert wynik == ["/produkty", "/kontakt"]


def test_zadanie_03_link_bez_href_daje_none_na_liscie() -> None:
    """Co testuje: czy .get("href") daje None (a nie KeyError) dla linku bez href.
    Co udaje: nic — podaję własny HTML z linkiem bez atrybutu href.
    Co sprawdzam: wynik == [None].
    """
    html = "<html><body><a>Bez adresu</a></body></html>"
    wynik = zadanie_03_adresy_linkow(html)
    assert wynik == [None]


# --- zadanie_04 ---

def test_zadanie_04_znajduje_po_klasie(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera teksty divów o klasie "produkt".
    Co udaje: nic — używam fixture html_strona (2 divy tej klasy).
    Co sprawdzam: wynik == ["Klawiatura", "Myszka"].
    """
    wynik = zadanie_04_teksty_po_klasie(html_strona, "produkt")
    assert wynik == ["Klawiatura", "Myszka"]


def test_zadanie_04_nieistniejaca_klasa_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla klasy, której nie ma na stronie.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == [] dla klasy "promocja".
    """
    wynik = zadanie_04_teksty_po_klasie(html_strona, "promocja")
    assert wynik == []


# --- zadanie_05 ---

def test_zadanie_05_znajduje_po_id(html_strona: str) -> None:
    """Co testuje: czy funkcja zwraca tekst elementu o podanym id.
    Co udaje: nic — używam fixture html_strona (p o id "stopka").
    Co sprawdzam: wynik == "Copyright 2026".
    """
    wynik = zadanie_05_tekst_po_id(html_strona, "stopka")
    assert wynik == "Copyright 2026"


def test_zadanie_05_brak_id_zwraca_none(html_strona: str) -> None:
    """Co testuje: kontrakt None dla id, którego nie ma na stronie.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik is None dla id "naglowek".
    """
    wynik = zadanie_05_tekst_po_id(html_strona, "naglowek")
    assert wynik is None


# --- zadanie_06 ---

def test_zadanie_06_selektor_klasy(html_strona: str) -> None:
    """Co testuje: czy selektor "div.produkt" zbiera teksty obu produktów.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == ["Klawiatura", "Myszka"].
    """
    wynik = zadanie_06_teksty_selektorem(html_strona, "div.produkt")
    assert wynik == ["Klawiatura", "Myszka"]


def test_zadanie_06_selektor_bez_dopasowan_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla selektora bez dopasowań.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == [] dla selektora "span.cena".
    """
    wynik = zadanie_06_teksty_selektorem(html_strona, "span.cena")
    assert wynik == []


# --- zadanie_07 ---

def test_zadanie_07_selektor_id(html_strona: str) -> None:
    """Co testuje: czy select_one z selektorem "#stopka" zwraca tekst stopki.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == "Copyright 2026".
    """
    wynik = zadanie_07_pierwszy_selektorem(html_strona, "#stopka")
    assert wynik == "Copyright 2026"


def test_zadanie_07_brak_dopasowania_zwraca_none(html_strona: str) -> None:
    """Co testuje: kontrakt None gdy selektor nic nie znajduje.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik is None dla selektora "#cennik".
    """
    wynik = zadanie_07_pierwszy_selektorem(html_strona, "#cennik")
    assert wynik is None


# --- zadanie_08 ---

def test_zadanie_08_tabela_na_liste_list(html_tabela: str) -> None:
    """Co testuje: czy tabela HTML zamienia się w listę list tekstów komórek.
    Co udaje: nic — używam fixture html_tabela (2 wiersze po 2 komórki).
    Co sprawdzam: wynik == [["Anna", "30"], ["Piotr", "25"]].
    """
    wynik = zadanie_08_tabela_do_listy(html_tabela)
    assert wynik == [["Anna", "30"], ["Piotr", "25"]]


def test_zadanie_08_brak_tabeli_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla strony bez tabeli.
    Co udaje: nic — używam fixture html_strona (nie ma w niej table/tr).
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_08_tabela_do_listy(html_strona)
    assert wynik == []


# --- zadanie_09 ---

def test_zadanie_09_zbiera_adresy_src(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera wartości src wszystkich obrazków.
    Co udaje: nic — używam fixture html_strona (2 obrazki).
    Co sprawdzam: wynik == ["/logo.png", "/baner.png"].
    """
    wynik = zadanie_09_adresy_obrazkow(html_strona)
    assert wynik == ["/logo.png", "/baner.png"]


def test_zadanie_09_brak_obrazkow_pusta_lista(html_tabela: str) -> None:
    """Co testuje: pustą listę dla strony bez obrazków.
    Co udaje: nic — używam fixture html_tabela (nie ma w niej img).
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_09_adresy_obrazkow(html_tabela)
    assert wynik == []


# --- zadanie_10 ---

def test_zadanie_10_zwraca_tytul_pobranej_strony(
    monkeypatch: pytest.MonkeyPatch, html_strona: str
) -> None:
    """Co testuje: czy funkcja pobiera stronę i wyciąga jej h1.
    Co udaje: requests.get — zwraca FakeResponse(200, html_strona).
    Co sprawdzam: wynik == "Sklep Python".
    """
    def podmieniony_get(url, headers=None, timeout=None):
        return FakeResponse(200, html_strona)
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    wynik = zadanie_10_pobierz_tytul("https://sklep.przyklad.pl")
    assert wynik == "Sklep Python"


def test_zadanie_10_wysyla_user_agenta(
    monkeypatch: pytest.MonkeyPatch, html_strona: str
) -> None:
    """Co testuje: czy zapytanie zawiera nagłówek User-Agent (etyka scrapingu).
    Co udaje: requests.get — zamiennik ZAPISUJE otrzymane headers do listy
    i zwraca FakeResponse(200, html_strona).
    Co sprawdzam: zapisane headers zawierają klucz "User-Agent".
    """
    zapamietane = []
    def podmieniony_get(url, headers=None, timeout=None):
        zapamietane.append(headers)
        return FakeResponse(200, html_strona)
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    zadanie_10_pobierz_tytul("https://sklep.przyklad.pl")
    assert "User-Agent" in zapamietane[0]


# --- zadanie_11 ---

def test_zadanie_11_zbiera_tytuly_i_spi_po_kazdym(
    monkeypatch: pytest.MonkeyPatch, html_strona: str
) -> None:
    """Co testuje: czy funkcja zbiera h1 z każdej strony i śpi po każdym zapytaniu.
    Co udaje: requests.get — zwraca FakeResponse(200, html_strona);
    time.sleep — zamiennik zapisuje wywołania do listy zamiast spać.
    Co sprawdzam: wynik == ["Sklep Python", "Sklep Python"]
    i time.sleep wywołany 2 razy z wartością 1.5.
    """
    def podmieniony_get(url, headers=None, timeout=None):
        return FakeResponse(200, html_strona)
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    uspienia = []
    def podmieniony_sleep(sekundy):
        uspienia.append(sekundy)
    monkeypatch.setattr("scraping_beautifulsoup.time.sleep", podmieniony_sleep)
    wynik = zadanie_11_scrapuj_z_pauza(
        ["https://a.przyklad.pl", "https://b.przyklad.pl"], 1.5
    )
    assert wynik == ["Sklep Python", "Sklep Python"]
    assert uspienia == [1.5, 1.5]


def test_zadanie_11_pusta_lista_bez_zapytan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy pusta lista adresów daje pustą listę bez żadnego zapytania.
    Co udaje: requests.get — zamiennik ZLICZA wywołania (nie powinno być żadnego).
    Co sprawdzam: wynik == [] i zero wywołań requests.get.
    """
    wywolania = []
    def podmieniony_get(url, headers=None, timeout=None):
        wywolania.append(url)
        return FakeResponse(200, "")
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    wynik = zadanie_11_scrapuj_z_pauza([], 1.0)
    assert wynik == []
    assert wywolania == []


# --- zadanie_12 ---

def test_zadanie_12_zapisuje_linki_do_csv(
    monkeypatch: pytest.MonkeyPatch, html_strona: str, tmp_path: Path
) -> None:
    """Co testuje: czy linki z pobranej strony lądują w CSV, a wynik to ich liczba.
    Co udaje: requests.get — zwraca FakeResponse(200, html_strona).
    Co sprawdzam: wynik == 2; plik wczytany przez csv.DictReader ma 2 wiersze,
    pierwszy to {"tekst": "Produkty", "adres": "/produkty"}.
    """
    def podmieniony_get(url, headers=None, timeout=None):
        return FakeResponse(200, html_strona)
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    p = tmp_path / "linki.csv"
    wynik = zadanie_12_zapisz_linki_do_csv("https://sklep.przyklad.pl", str(p))
    assert wynik == 2
    with open(str(p), "r", newline="", encoding="utf-8") as f:
        wiersze = list(csv.DictReader(f))
        assert len(wiersze) == 2
        assert wiersze[0] == {"tekst": "Produkty", "adres": "/produkty"}


def test_zadanie_12_strona_bez_linkow_zwraca_zero(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy strona bez linków daje 0 i plik z samym nagłówkiem.
    Co udaje: requests.get — zwraca FakeResponse(200, HTML bez znaczników a).
    Co sprawdzam: wynik == 0; plik istnieje i ma 0 wierszy danych.
    """
    html = "<html><body><h1>Pusto</h1></body></html>"
    def podmieniony_get(url, headers=None, timeout=None):
        return FakeResponse(200, html)
    monkeypatch.setattr("scraping_beautifulsoup.requests.get", podmieniony_get)
    p = tmp_path / "linki.csv"
    wynik = zadanie_12_zapisz_linki_do_csv("https://sklep.przyklad.pl", str(p))
    assert wynik == 0
    with open(str(p), "r", newline="", encoding="utf-8") as f:
        assert list(csv.DictReader(f)) == []