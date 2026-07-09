import csv
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

# --- SPIS ZADAŃ ---
# zadanie_01 — wyciągnij tekst pierwszego nagłówka h1 (find + .text)
# zadanie_02 — zbierz teksty wszystkich linków (find_all)
# zadanie_03 — zbierz adresy href wszystkich linków (.get("href"))
# zadanie_04 — zbierz teksty elementów o podanej klasie (class_)
# zadanie_05 — znajdź element po id; brak elementu → None
# zadanie_06 — zbierz teksty pasujące do selektora CSS (select)
# zadanie_07 — pierwszy element selektora CSS lub None (select_one)
# zadanie_08 — zamień tabelę HTML na listę list (tr/td)
# zadanie_09 — zbierz adresy src wszystkich obrazków
# zadanie_10 — pobierz stronę z User-Agentem i zwróć tytuł h1
#              (zazębienie: requests z tematu 11)
# zadanie_11 — scrapuj listę adresów z pauzą między zapytaniami (time.sleep)
# zadanie_12 — pobierz stronę i zapisz linki do CSV (zazębienie: temat 6)


def zadanie_01_tytul_strony(html: str) -> Optional[str]:
    """Zwraca tekst pierwszego nagłówka h1 lub None, gdy strona nie ma h1.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        Optional[str]: treść znacznika h1 lub None przy jego braku.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: znajdź nagłówek: naglowek = soup.find("h1")
    # TODO: jeśli naglowek is None — return None
    # TODO: w przeciwnym razie return naglowek.text
    pass


def zadanie_02_teksty_linkow(html: str) -> list[str]:
    """Zbiera teksty wszystkich linków (znaczników a) ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[str]: teksty linków w kolejności ze strony; pusta lista gdy brak.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: zwróć list comprehension: [link.text for link in soup.find_all("a")]
    pass


def zadanie_03_adresy_linkow(html: str) -> list[str]:
    """Zbiera adresy (atrybut href) wszystkich linków ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[str]: wartości href w kolejności ze strony; pusta lista gdy brak.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: zwróć list comprehension z link.get("href")
    #       dla każdego linku z soup.find_all("a")
    pass


def zadanie_04_teksty_po_klasie(html: str, klasa: str) -> list[str]:
    """Zbiera teksty wszystkich znaczników div o podanej klasie.

    Args:
        html: surowy HTML strony jako string.
        klasa: nazwa klasy CSS do wyszukania (np. "produkt").

    Returns:
        list[str]: teksty pasujących divów; pusta lista gdy brak dopasowań.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: znajdź elementy: soup.find_all("div", class_=klasa)
    #       — pamiętaj o podkreśleniu w class_!
    # TODO: zwróć listę tekstów znalezionych elementów
    pass


def zadanie_05_tekst_po_id(html: str, identyfikator: str) -> Optional[str]:
    """Zwraca tekst elementu o podanym id lub None, gdy takiego elementu nie ma.

    Args:
        html: surowy HTML strony jako string.
        identyfikator: wartość atrybutu id do wyszukania (np. "stopka").

    Returns:
        Optional[str]: treść elementu lub None przy braku dopasowania.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: znajdź element: element = soup.find(id=identyfikator)
    # TODO: jeśli element is None — return None; inaczej return element.text
    pass


def zadanie_06_teksty_selektorem(html: str, selektor: str) -> list[str]:
    """Zbiera teksty wszystkich elementów pasujących do selektora CSS.

    Args:
        html: surowy HTML strony jako string.
        selektor: selektor CSS (np. "div.produkt", "#stopka", "a").

    Returns:
        list[str]: teksty pasujących elementów (get_text ze strip=True);
            pusta lista gdy brak dopasowań.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: znajdź elementy: soup.select(selektor)
    # TODO: zwróć listę element.get_text(strip=True) dla każdego elementu
    pass


def zadanie_07_pierwszy_selektorem(html: str, selektor: str) -> Optional[str]:
    """Zwraca tekst pierwszego elementu pasującego do selektora CSS lub None.

    Args:
        html: surowy HTML strony jako string.
        selektor: selektor CSS (np. "#stopka", "div.opis").

    Returns:
        Optional[str]: tekst pierwszego dopasowania lub None gdy brak.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: znajdź element: element = soup.select_one(selektor)
    # TODO: jeśli element is None — return None;
    #       inaczej return element.get_text(strip=True)
    pass


def zadanie_08_tabela_do_listy(html: str) -> list[list[str]]:
    """Zamienia pierwszą tabelę HTML na listę list tekstów komórek.

    Args:
        html: surowy HTML strony z tabelą (tr/td) jako string.

    Returns:
        list[list[str]]: jeden element listy = jeden wiersz tabeli
            (lista tekstów komórek td); pusta lista gdy tabeli brak.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: utwórz pustą listę wiersze = []
    # TODO: dla każdego tr w soup.find_all("tr"):
    #       zbuduj listę [td.text for td in tr.find_all("td")]
    #       i dodaj ją do wiersze przez .append
    # TODO: return wiersze
    pass


def zadanie_09_adresy_obrazkow(html: str) -> list[str]:
    """Zbiera adresy (atrybut src) wszystkich obrazków ze strony.

    Args:
        html: surowy HTML strony jako string.

    Returns:
        list[str]: wartości src w kolejności ze strony; pusta lista gdy brak.
    """
    # TODO: utwórz soup = BeautifulSoup(html, "html.parser")
    # TODO: zwróć list comprehension z img.get("src")
    #       dla każdego img z soup.find_all("img")
    pass


def zadanie_10_pobierz_tytul(url: str) -> Optional[str]:
    """Pobiera stronę (przedstawiając się User-Agentem) i zwraca tekst jej h1.

    Args:
        url: adres strony do pobrania.

    Returns:
        Optional[str]: treść nagłówka h1 lub None, gdy strona nie ma h1.
    """
    # TODO: przygotuj naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    # TODO: wywołaj requests.get(url, headers=naglowki, timeout=10)
    #       (wzorzec z tematu 11)
    # TODO: wywołaj response.raise_for_status()
    # TODO: utwórz soup = BeautifulSoup(response.text, "html.parser")
    #       — response.text, nie response.json()!
    # TODO: znajdź h1; jeśli is None — return None; inaczej return jego .text
    pass


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
    # TODO: przygotuj naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    # TODO: utwórz pustą listę tytuly = []
    # TODO: dla każdego url w adresy:
    #       - requests.get(url, headers=naglowki, timeout=10)
    #       - response.raise_for_status()
    #       - soup = BeautifulSoup(response.text, "html.parser")
    #       - dodaj soup.find("h1").text do tytuly
    #       - time.sleep(pauza) — pauza PO każdym zapytaniu
    # TODO: return tytuly
    pass


def zadanie_12_zapisz_linki_do_csv(url: str, sciezka: str) -> int:
    """Pobiera stronę, wyciąga wszystkie linki i zapisuje je do pliku CSV.

    Args:
        url: adres strony do pobrania.
        sciezka: ścieżka do pliku wynikowego .csv (kolumny: tekst, adres).

    Returns:
        int: liczba zapisanych linków (wierszy danych, bez nagłówka).
    """
    # TODO: przygotuj naglowki = {"User-Agent": "KursPython/1.0 (nauka scrapingu)"}
    # TODO: wywołaj requests.get(url, headers=naglowki, timeout=10)
    #       i response.raise_for_status()
    # TODO: utwórz soup = BeautifulSoup(response.text, "html.parser")
    # TODO: zbuduj listę słowników:
    #       [{"tekst": a.text, "adres": a.get("href")}
    #        for a in soup.find_all("a")]
    # TODO: otwórz plik: open(sciezka, "w", newline="", encoding="utf-8")
    #       w bloku with (newline="" — wzorzec CSV z tematu 6)
    # TODO: utwórz writer = csv.DictWriter(f, fieldnames=["tekst", "adres"]),
    #       wywołaj writer.writeheader() i writer.writerows(lista)
    # TODO: zwróć len(listy)
    pass
