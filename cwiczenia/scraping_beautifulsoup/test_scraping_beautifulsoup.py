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
    # TODO: wywołaj zadanie_01_tytul_strony(html_strona)
    # TODO: sprawdź wynik == "Sklep Python"
    pass


def test_zadanie_01_brak_h1_zwraca_none() -> None:
    """Co testuje: kontrakt None dla strony bez nagłówka h1.
    Co udaje: nic — podaję własny minimalny HTML bez h1.
    Co sprawdzam: wynik is None.
    """
    # TODO: przygotuj html = "<html><body><p>Sama treść</p></body></html>"
    # TODO: wywołaj zadanie_01_tytul_strony(html)
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_02 ---

def test_zadanie_02_zbiera_teksty_linkow(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera teksty wszystkich znaczników a.
    Co udaje: nic — używam fixture html_strona (2 linki).
    Co sprawdzam: wynik == ["Produkty", "Kontakt"].
    """
    # TODO: wywołaj zadanie_02_teksty_linkow(html_strona)
    # TODO: sprawdź wynik == ["Produkty", "Kontakt"]
    pass


def test_zadanie_02_brak_linkow_pusta_lista() -> None:
    """Co testuje: pustą listę (nie None) dla strony bez linków.
    Co udaje: nic — podaję własny HTML bez znaczników a.
    Co sprawdzam: wynik == [].
    """
    # TODO: przygotuj html = "<html><body><h1>Tytuł</h1></body></html>"
    # TODO: wywołaj zadanie_02_teksty_linkow(html)
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_03 ---

def test_zadanie_03_zbiera_adresy_href(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera wartości atrybutu href wszystkich linków.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == ["/produkty", "/kontakt"].
    """
    # TODO: wywołaj zadanie_03_adresy_linkow(html_strona)
    # TODO: sprawdź wynik == ["/produkty", "/kontakt"]
    pass


def test_zadanie_03_link_bez_href_daje_none_na_liscie() -> None:
    """Co testuje: czy .get("href") daje None (a nie KeyError) dla linku bez href.
    Co udaje: nic — podaję własny HTML z linkiem bez atrybutu href.
    Co sprawdzam: wynik == [None].
    """
    # TODO: przygotuj html = "<html><body><a>Bez adresu</a></body></html>"
    # TODO: wywołaj zadanie_03_adresy_linkow(html)
    # TODO: sprawdź wynik == [None]
    pass


# --- zadanie_04 ---

def test_zadanie_04_znajduje_po_klasie(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera teksty divów o klasie "produkt".
    Co udaje: nic — używam fixture html_strona (2 divy tej klasy).
    Co sprawdzam: wynik == ["Klawiatura", "Myszka"].
    """
    # TODO: wywołaj zadanie_04_teksty_po_klasie(html_strona, "produkt")
    # TODO: sprawdź wynik == ["Klawiatura", "Myszka"]
    pass


def test_zadanie_04_nieistniejaca_klasa_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla klasy, której nie ma na stronie.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == [] dla klasy "promocja".
    """
    # TODO: wywołaj zadanie_04_teksty_po_klasie(html_strona, "promocja")
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_05 ---

def test_zadanie_05_znajduje_po_id(html_strona: str) -> None:
    """Co testuje: czy funkcja zwraca tekst elementu o podanym id.
    Co udaje: nic — używam fixture html_strona (p o id "stopka").
    Co sprawdzam: wynik == "Copyright 2026".
    """
    # TODO: wywołaj zadanie_05_tekst_po_id(html_strona, "stopka")
    # TODO: sprawdź wynik == "Copyright 2026"
    pass


def test_zadanie_05_brak_id_zwraca_none(html_strona: str) -> None:
    """Co testuje: kontrakt None dla id, którego nie ma na stronie.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik is None dla id "naglowek".
    """
    # TODO: wywołaj zadanie_05_tekst_po_id(html_strona, "naglowek")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_06 ---

def test_zadanie_06_selektor_klasy(html_strona: str) -> None:
    """Co testuje: czy selektor "div.produkt" zbiera teksty obu produktów.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == ["Klawiatura", "Myszka"].
    """
    # TODO: wywołaj zadanie_06_teksty_selektorem(html_strona, "div.produkt")
    # TODO: sprawdź wynik == ["Klawiatura", "Myszka"]
    pass


def test_zadanie_06_selektor_bez_dopasowan_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla selektora bez dopasowań.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == [] dla selektora "span.cena".
    """
    # TODO: wywołaj zadanie_06_teksty_selektorem(html_strona, "span.cena")
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_07 ---

def test_zadanie_07_selektor_id(html_strona: str) -> None:
    """Co testuje: czy select_one z selektorem "#stopka" zwraca tekst stopki.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik == "Copyright 2026".
    """
    # TODO: wywołaj zadanie_07_pierwszy_selektorem(html_strona, "#stopka")
    # TODO: sprawdź wynik == "Copyright 2026"
    pass


def test_zadanie_07_brak_dopasowania_zwraca_none(html_strona: str) -> None:
    """Co testuje: kontrakt None gdy selektor nic nie znajduje.
    Co udaje: nic — używam fixture html_strona.
    Co sprawdzam: wynik is None dla selektora "#cennik".
    """
    # TODO: wywołaj zadanie_07_pierwszy_selektorem(html_strona, "#cennik")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_08 ---

def test_zadanie_08_tabela_na_liste_list(html_tabela: str) -> None:
    """Co testuje: czy tabela HTML zamienia się w listę list tekstów komórek.
    Co udaje: nic — używam fixture html_tabela (2 wiersze po 2 komórki).
    Co sprawdzam: wynik == [["Anna", "30"], ["Piotr", "25"]].
    """
    # TODO: wywołaj zadanie_08_tabela_do_listy(html_tabela)
    # TODO: sprawdź wynik == [["Anna", "30"], ["Piotr", "25"]]
    pass


def test_zadanie_08_brak_tabeli_pusta_lista(html_strona: str) -> None:
    """Co testuje: pustą listę dla strony bez tabeli.
    Co udaje: nic — używam fixture html_strona (nie ma w niej table/tr).
    Co sprawdzam: wynik == [].
    """
    # TODO: wywołaj zadanie_08_tabela_do_listy(html_strona)
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_09 ---

def test_zadanie_09_zbiera_adresy_src(html_strona: str) -> None:
    """Co testuje: czy funkcja zbiera wartości src wszystkich obrazków.
    Co udaje: nic — używam fixture html_strona (2 obrazki).
    Co sprawdzam: wynik == ["/logo.png", "/baner.png"].
    """
    # TODO: wywołaj zadanie_09_adresy_obrazkow(html_strona)
    # TODO: sprawdź wynik == ["/logo.png", "/baner.png"]
    pass


def test_zadanie_09_brak_obrazkow_pusta_lista(html_tabela: str) -> None:
    """Co testuje: pustą listę dla strony bez obrazków.
    Co udaje: nic — używam fixture html_tabela (nie ma w niej img).
    Co sprawdzam: wynik == [].
    """
    # TODO: wywołaj zadanie_09_adresy_obrazkow(html_tabela)
    # TODO: sprawdź wynik == []
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_tytul_pobranej_strony(
    monkeypatch: pytest.MonkeyPatch, html_strona: str
) -> None:
    """Co testuje: czy funkcja pobiera stronę i wyciąga jej h1.
    Co udaje: requests.get — zwraca FakeResponse(200, html_strona).
    Co sprawdzam: wynik == "Sklep Python".
    """
    # TODO: przygotuj zamiennik:
    #       def podmieniony_get(url, headers=None, timeout=None):
    #           return FakeResponse(200, html_strona)
    # TODO: podmień: monkeypatch.setattr(
    #           "scraping_beautifulsoup.requests.get", podmieniony_get)
    # TODO: wywołaj zadanie_10_pobierz_tytul("https://sklep.przyklad.pl")
    # TODO: sprawdź wynik == "Sklep Python"
    pass


def test_zadanie_10_wysyla_user_agenta(
    monkeypatch: pytest.MonkeyPatch, html_strona: str
) -> None:
    """Co testuje: czy zapytanie zawiera nagłówek User-Agent (etyka scrapingu).
    Co udaje: requests.get — zamiennik ZAPISUJE otrzymane headers do listy
    i zwraca FakeResponse(200, html_strona).
    Co sprawdzam: zapisane headers zawierają klucz "User-Agent".
    """
    # TODO: przygotuj pustą listę zapamietane = []
    # TODO: przygotuj zamiennik, który robi zapamietane.append(headers)
    #       i zwraca FakeResponse(200, html_strona)
    # TODO: podmień requests.get
    # TODO: wywołaj zadanie_10_pobierz_tytul("https://sklep.przyklad.pl")
    # TODO: sprawdź "User-Agent" in zapamietane[0]
    pass


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
    # TODO: przygotuj zamiennik get zwracający FakeResponse(200, html_strona)
    # TODO: podmień "scraping_beautifulsoup.requests.get"
    # TODO: przygotuj pustą listę uspienia = [] i zamiennik:
    #       def podmieniony_sleep(sekundy):
    #           uspienia.append(sekundy)
    # TODO: podmień "scraping_beautifulsoup.time.sleep"
    # TODO: wywołaj zadanie_11_scrapuj_z_pauza(
    #           ["https://a.przyklad.pl", "https://b.przyklad.pl"], 1.5)
    # TODO: sprawdź wynik == ["Sklep Python", "Sklep Python"]
    # TODO: sprawdź uspienia == [1.5, 1.5]
    pass


def test_zadanie_11_pusta_lista_bez_zapytan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: czy pusta lista adresów daje pustą listę bez żadnego zapytania.
    Co udaje: requests.get — zamiennik ZLICZA wywołania (nie powinno być żadnego).
    Co sprawdzam: wynik == [] i zero wywołań requests.get.
    """
    # TODO: przygotuj pustą listę wywolania = [] i zamiennik get,
    #       który robi wywolania.append(url) i zwraca FakeResponse(200, "")
    # TODO: podmień "scraping_beautifulsoup.requests.get"
    # TODO: wywołaj zadanie_11_scrapuj_z_pauza([], 1.0)
    # TODO: sprawdź wynik == []
    # TODO: sprawdź wywolania == []
    pass


# --- zadanie_12 ---

def test_zadanie_12_zapisuje_linki_do_csv(
    monkeypatch: pytest.MonkeyPatch, html_strona: str, tmp_path: Path
) -> None:
    """Co testuje: czy linki z pobranej strony lądują w CSV, a wynik to ich liczba.
    Co udaje: requests.get — zwraca FakeResponse(200, html_strona).
    Co sprawdzam: wynik == 2; plik wczytany przez csv.DictReader ma 2 wiersze,
    pierwszy to {"tekst": "Produkty", "adres": "/produkty"}.
    """
    # TODO: przygotuj zamiennik get zwracający FakeResponse(200, html_strona)
    # TODO: podmień "scraping_beautifulsoup.requests.get"
    # TODO: przygotuj p = tmp_path / "linki.csv"
    # TODO: wywołaj zadanie_12_zapisz_linki_do_csv(
    #           "https://sklep.przyklad.pl", str(p)) i zapisz wynik
    # TODO: sprawdź wynik == 2
    # TODO: otwórz plik (newline="", encoding="utf-8"),
    #       wczytaj wiersze = list(csv.DictReader(f))
    # TODO: sprawdź len(wiersze) == 2
    # TODO: sprawdź wiersze[0] == {"tekst": "Produkty", "adres": "/produkty"}
    pass


def test_zadanie_12_strona_bez_linkow_zwraca_zero(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Co testuje: czy strona bez linków daje 0 i plik z samym nagłówkiem.
    Co udaje: requests.get — zwraca FakeResponse(200, HTML bez znaczników a).
    Co sprawdzam: wynik == 0; plik istnieje i ma 0 wierszy danych.
    """
    # TODO: przygotuj html = "<html><body><h1>Pusto</h1></body></html>"
    # TODO: przygotuj zamiennik get zwracający FakeResponse(200, html)
    # TODO: podmień "scraping_beautifulsoup.requests.get"
    # TODO: przygotuj p = tmp_path / "linki.csv"
    # TODO: wywołaj zadanie_12_zapisz_linki_do_csv(
    #           "https://sklep.przyklad.pl", str(p)) i zapisz wynik
    # TODO: sprawdź wynik == 0
    # TODO: otwórz plik (newline="", encoding="utf-8")
    #       i sprawdź list(csv.DictReader(f)) == []
    pass
