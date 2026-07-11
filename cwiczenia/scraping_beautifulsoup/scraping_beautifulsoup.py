import csv
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


def zadanie_01_tytul_strony(html: str) -> Optional[str]:
    """Zwraca tekst pierwszego nagłówka h1 lub None, gdy strona nie ma h1.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        Optional[str]: treść znacznika h1 lub None przy jego braku.
    """
    soup = BeautifulSoup(html, "html.parser")
    naglowek = soup.find("h1")
    if naglowek is None:
        return None
    return naglowek.text


def zadanie_02_teksty_linkow(html: str) -> list[str]:
    """Zbiera teksty wszystkich linków (znaczników a) ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[str]: teksty linków w kolejności ze strony; pusta lista gdy brak.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [link.text for link in soup.find_all("a")]


def zadanie_03_adresy_linkow(html: str) -> list[Optional[str]]:
    """Zbiera adresy (atrybut href) wszystkich linków ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[Optional[str]]: wartości href w kolejności ze strony; pusta lista gdy brak.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [link.get("href") for link in soup.find_all("a")]


def zadanie_04_teksty_po_klasie(html: str, klasa: str) -> list[str]:
    """Zbiera teksty wszystkich znaczników div o podanej klasie.

    Args:
        html: surowy HTML strony jako string.
        klasa: nazwa klasy CSS do wyszukania (np. "produkt").

    Returns:
        list[str]: teksty pasujących divów; pusta lista gdy brak dopasowań.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [element.text for element in soup.find_all("div", class_=klasa)]


def zadanie_05_tekst_po_id(html: str, identyfikator: str) -> Optional[str]:
    """Zwraca tekst elementu o podanym id lub None, gdy takiego elementu nie ma.

    Args:
        html: surowy HTML strony jako string.
        identyfikator: wartość atrybutu id do wyszukania (np. "stopka").

    Returns:
        Optional[str]: treść elementu lub None przy braku dopasowania.
    """
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find(id=identyfikator)
    if element is None:
        return None
    return element.text


def zadanie_06_teksty_selektorem(html: str, selektor: str) -> list[str]:
    """Zbiera teksty wszystkich elementów pasujących do selektora CSS.

    Args:
        html: surowy HTML strony jako string.
        selektor: selektor CSS (np. "div.produkt", "#stopka", "a").

    Returns:
        list[str]: teksty pasujących elementów (get_text ze strip=True);
            pusta lista gdy brak dopasowań.
    """
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select(selektor)
    return [e.get_text(strip=True) for e in element]


def zadanie_07_pierwszy_selektorem(html: str, selektor: str) -> Optional[str]:
    """Zwraca tekst pierwszego elementu pasującego do selektora CSS lub None.

    Args:
        html: surowy HTML strony jako string.
        selektor: selektor CSS (np. "#stopka", "div.opis").

    Returns:
        Optional[str]: tekst pierwszego dopasowania lub None gdy brak.
    """
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select_one(selektor)
    if element is None:
        return None
    return element.get_text(strip=True)


def zadanie_08_tabela_do_listy(html: str) -> list[list[str]]:
    """Zamienia pierwszą tabelę HTML na listę list tekstów komórek.

    Args:
        html: surowy HTML strony z tabelą (tr/td) jako string.

    Returns:
        list[list[str]]: jeden element listy = jeden wiersz tabeli
            (lista tekstów komórek td); pusta lista gdy tabeli brak.
    """
    soup = BeautifulSoup(html, "html.parser")
    wiersze = []
    for tr in soup.find_all("tr"):
        komorki = [td.text for td in tr.find_all("td")]
        wiersze.append(komorki)
    return wiersze


def zadanie_09_adresy_obrazkow(html: str) -> list[Optional[str]]:
    """Zbiera adresy (atrybut src) wszystkich obrazków ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[Optional[str]]: wartości src w kolejności ze strony; pusta lista gdy brak.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [img.get("src") for img in soup.find_all("img")]


def zadanie_10_pobierz_tytul(url: str) -> Optional[str]:
    """Pobiera stronę (przedstawiając się User-Agentem) i zwraca tekst jej h1.

    Args:
        url: adres strony do pobrania.

    Returns:
        Optional[str]: treść nagłówka h1 lub None, gdy strona nie ma h1.
    """
    naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    response = requests.get(url, headers=naglowki, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    naglowek = soup.find("h1")
    if naglowek is None:
        return None
    return naglowek.text


def zadanie_11_scrapuj_z_pauza(adresy: list[str], pauza: float) -> list[str]:
    """Pobiera kolejno strony z listy, robiąc pauzę po każdym zapytaniu,
    i zbiera teksty ich nagłówków h1.

    Args:
        adresy: lista adresów stron do pobrania.
        pauza: liczba sekund pauzy po każdym zapytaniu (rate limiting).

    Returns:
        list[str]: teksty nagłówków h1 kolejnych stron; pusta lista
            dla pustej listy adresów.
    """
    naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    tytuly = []
    for url in adresy:
        response = requests.get(url, headers=naglowki, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tytuly.append(soup.find("h1").text)
        time.sleep(pauza)
    return tytuly


def zadanie_12_zapisz_linki_do_csv(url: str, sciezka: str) -> int:
    """Pobiera stronę, wyciąga wszystkie linki i zapisuje je do pliku CSV.

    Args:
        url: adres strony do pobrania.
        sciezka: ścieżka do pliku wynikowego .csv (kolumny: tekst, adres).

    Returns:
        int: liczba zapisanych linków (wierszy danych, bez nagłówka).
    """
    naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    response = requests.get(url, headers=naglowki, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    lista = []
    for a in soup.find_all("a"):
        lista.append({"tekst": a.text, "adres": a.get("href")})
    with open(sciezka, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tekst", "adres"])
        writer.writeheader()
        writer.writerows(lista)
    return len(lista)
