import json
from typing import Any

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError


class Produkt(BaseModel):
    """Model produktu w katalogu — bramkarz danych wchodzących do sklepu.

    Args:
        id: numer produktu (int).
        nazwa: nazwa produktu.
        cena: cena produktu (float).

    Returns:
        Produkt: obiekt z polami id, nazwa i cena po walidacji.
    """

    id: int
    nazwa: str
    cena: float


def zadanie_01_pobierz_katalog(url: str) -> list[dict[str, Any]] | None:
    """Pobiera pełny katalog produktów z zewnętrznego API.

    Args:
        url: adres endpointu zwracającego listę produktów jako JSON.

    Returns:
        list[dict[str, Any]] | None: sparsowana lista produktów albo None
            przy jakimkolwiek błędzie sieci lub serwera (także 4xx/5xx).
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def zadanie_02_pobierz_strony(
    url: str, liczba_stron: int,
) -> list[dict[str, Any]]:
    """Pobiera katalog strona po stronie i skleja wyniki w jedną listę.

    Args:
        url: adres endpointu przyjmującego parametr zapytania "strona".
        liczba_stron: ile stron pobrać (numeracja od 1).

    Returns:
        list[dict[str, Any]]: produkty ze wszystkich stron w jednej,
            płaskiej liście; pusta lista dla liczba_stron równego 0.
    """
    wszystkie = []
    for numer in range(1, liczba_stron + 1):
        porcja = requests.get(url, params={"strona": numer}, timeout=10)
        wszystkie.extend(porcja.json())
    return wszystkie


def zadanie_03_filtruj_dostepne(
    produkty: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Zwraca tylko produkty oznaczone jako dostępne.

    Args:
        produkty: surowa lista produktów z kluczem "dostepny" (bool).

    Returns:
        list[dict[str, Any]]: nowa lista wyłącznie z produktami,
            których "dostepny" to True.
    """
    return [produkt for produkt in produkty if produkt["dostepny"] is True]


def zadanie_04_wybierz_pola(
    produkty: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Przycina każdy produkt do trzech pól: id, nazwa, cena.

    Args:
        produkty: lista produktów z nadmiarowymi polami (np. magazyn).

    Returns:
        list[dict[str, Any]]: nowa lista słowników zawierających
            WYŁĄCZNIE klucze id, nazwa i cena.
    """
    return [
        {"id": p["id"], "nazwa": p["nazwa"], "cena": p["cena"]}
        for p in produkty
    ]


def zadanie_05_znajdz_produkt(
    produkty: list[dict[str, Any]], id_produktu: int,
) -> dict[str, Any] | None:
    """Wyszukuje produkt o podanym id.

    Args:
        produkty: lista produktów z kluczem "id".
        id_produktu: szukany numer produktu.

    Returns:
        dict[str, Any] | None: pierwszy produkt o pasującym id
            albo None, gdy takiego nie ma.
    """
    for produkt in produkty:
        if id_produktu == produkt["id"]:
            return produkt
    return None


def zadanie_06_zapisz_katalog(
    produkty: list[dict[str, Any]], sciezka: str,
) -> bool:
    """Zapisuje katalog produktów do pliku JSON.

    Args:
        produkty: lista produktów do zapisania.
        sciezka: ścieżka do pliku wynikowego .json.

    Returns:
        bool: True po pomyślnym zapisie pliku.
    """
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(produkty, f, indent=2)
    return True


def zadanie_07_wczytaj_katalog(sciezka: str) -> list[dict[str, Any]] | None:
    """Wczytuje katalog produktów z pliku JSON.

    Args:
        sciezka: ścieżka do pliku .json z listą produktów.

    Returns:
        list[dict[str, Any]] | None: lista produktów albo None, gdy plik
            nie istnieje LUB jego treść nie jest poprawnym JSON-em.
    """
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def zadanie_08_waliduj_produkt(dane: dict[str, Any]) -> Produkt | None:
    """Przepuszcza słownik przez bramkarza Pydantic.

    Args:
        dane: słownik z (potencjalnie) polami produktu.

    Returns:
        Produkt | None: zwalidowany obiekt Produkt albo None, gdy dane
            nie przechodzą walidacji modelu.
    """
    try:
        return Produkt(**dane)
    except ValidationError:
        return None


def zadanie_09_api_listy(sciezka: str) -> FastAPI:
    """Buduje aplikację serwującą listę produktów z pliku pod GET /produkty.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której GET /produkty odpowiada zawartością
            pliku (czytaną przy każdym zapytaniu).
    """
    app = FastAPI()

    @app.get("/produkty")
    def zwroc_produkty() -> list[dict]:
        """Zwraca listę produktów.

        Args:
            Brak.

        Returns:
            list[dict]: Lista produktów.
        """
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)

    return app


def zadanie_10_api_szczegolow(sciezka: str) -> FastAPI:
    """Buduje aplikację z GET /produkty/{id_produktu} zwracającym jeden produkt.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której GET /produkty/{id_produktu} odpowiada
            produktem o podanym id albo kodem 404, gdy go nie ma;
            tekst zamiast liczby w adresie daje automatyczne 422.
    """
    app = FastAPI()

    @app.get("/produkty/{id_produktu}")
    def zwroc_produkt(id_produktu: int) -> dict:
        """Zwraca szczegóły jednego produktu albo 404.

        Args:
            id_produktu: numer produktu z adresu URL.

        Returns:
            dict: produkt o podanym id.
        """
        produkty = zadanie_07_wczytaj_katalog(sciezka)
        if produkty is None:
            raise HTTPException(status_code=500, detail="Katalog niedostępny")
        produkt = zadanie_05_znajdz_produkt(produkty, id_produktu)
        if produkt is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono produktu")
        return produkt

    return app


def zadanie_11_api_dodawania(sciezka: str) -> FastAPI:
    """Buduje aplikację z POST /produkty dopisującym produkt do pliku.

    Args:
        sciezka: ścieżka do istniejącego pliku .json z listą produktów.

    Returns:
        FastAPI: aplikacja, której POST /produkty przyjmuje JSON pasujący
            do modelu Produkt (złe dane = automatyczne 422), dopisuje
            produkt do pliku i odpowiada {"liczba": <nowa długość listy>}.
    """
    app = FastAPI()

    @app.post("/produkty")
    def dodaj_produkt(produkt: Produkt) -> dict:
        """Dodaje produkt do katalogu.

        Args:
            produkt: obiekt produktu do dodania.

        Returns:
            dict: Słownik z długością listy katalogu.
        """
        produkty = zadanie_07_wczytaj_katalog(sciezka)
        if produkty is None:
            raise HTTPException(status_code=500, detail="Katalog niedostępny")
        produkt_dict = produkt.model_dump()
        produkty.append(produkt_dict)
        zadanie_06_zapisz_katalog(produkty, sciezka)
        return {"liczba": len(produkty)}

    return app


def zadanie_12_zbuduj_katalog(url: str, sciezka: str) -> bool | None:
    """Dyrygent zaopatrzenia: pobiera, czyści i zapisuje katalog na dysk.

    Args:
        url: adres endpointu zewnętrznego API z produktami.
        sciezka: ścieżka do wynikowego pliku .json katalogu.

    Returns:
        bool | None: True po zapisaniu czystego katalogu; None, gdy
            zewnętrzne API zawiodło (wtedy plik w ogóle nie powstaje).
    """
    produkty = zadanie_01_pobierz_katalog(url)
    if produkty is None:
        return None
    przefiltrowane_produkty = zadanie_03_filtruj_dostepne(produkty)
    przyciete_produkty = zadanie_04_wybierz_pola(przefiltrowane_produkty)
    zadanie_06_zapisz_katalog(przyciete_produkty, sciezka)
    return True


def zadanie_13_pelne_api(url: str, sciezka: str) -> FastAPI | None:
    """Dyrygent całości: zaopatruje sklep i buduje pełne API katalogu.

    Args:
        url: adres endpointu zewnętrznego API z produktami.
        sciezka: ścieżka do pliku .json, w którym wyląduje katalog.

    Returns:
        FastAPI | None: aplikacja z trzema endpointami — GET /produkty
            (lista z pliku), GET /produkty/{id_produktu} (szczegóły
            albo 404) i POST /produkty (walidacja modelem, dopisanie
            do pliku) — albo None, gdy zaopatrzenie się nie powiodło.
    """
    zaopatrzenie = zadanie_12_zbuduj_katalog(url, sciezka)
    if zaopatrzenie is None:
        return None
    app = FastAPI()

    @app.get("/produkty")
    def zwroc_produkty() -> list[dict]:
        """Zwraca listę produktów.

        Args:
            Brak.

        Returns:
            list[dict]: Lista produktów.
        """
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)

    @app.get("/produkty/{id_produktu}")
    def zwroc_produkt(id_produktu: int) -> dict:
        """Zwraca szczegóły jednego produktu albo 404.

        Args:
            id_produktu: numer produktu z adresu URL.

        Returns:
            dict: produkt o podanym id.
        """
        produkty = zadanie_07_wczytaj_katalog(sciezka)
        if produkty is None:
            raise HTTPException(status_code=500, detail="Katalog niedostępny")
        produkt = zadanie_05_znajdz_produkt(produkty, id_produktu)
        if produkt is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono produktu")
        return produkt

    @app.post("/produkty")
    def dodaj_produkt(produkt: Produkt) -> dict:
        """Dodaje produkt do katalogu.

        Args:
            produkt: obiekt produktu do dodania.

        Returns:
            dict: Słownik z długością listy katalogu.
        """
        produkty = zadanie_07_wczytaj_katalog(sciezka)
        if produkty is None:
            raise HTTPException(status_code=500, detail="Katalog niedostępny")
        produkt_dict = produkt.model_dump()
        produkty.append(produkt_dict)
        zadanie_06_zapisz_katalog(produkty, sciezka)
        return {"liczba": len(produkty)}

    return app

