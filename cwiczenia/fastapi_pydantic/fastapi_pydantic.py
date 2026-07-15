import json
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel


class Produkt(BaseModel):
    """Model produktu sklepowego — bramkarz danych wejściowych.

    Args:
        nazwa: nazwa produktu.
        cena: cena produktu (Pydantic skonwertuje np. "49" na 49.0).

    Returns:
        Produkt: obiekt z polami nazwa i cena po walidacji.
    """
    nazwa: str
    cena: float


class Zamowienie(BaseModel):
    """Model zamówienia — nazwa produktu, ilość sztuk i cena jednostkowa.

    Args:
        nazwa: nazwa zamawianego produktu.
        ilosc: liczba sztuk (int).
        cena_jednostkowa: cena jednej sztuki (float).

    Returns:
        Zamowienie: obiekt zamówienia po walidacji.
    """
    nazwa: str
    ilosc: int
    cena_jednostkowa: float


def zadanie_01_aplikacja_powitalna() -> FastAPI:
    """Buduje aplikację z jednym endpointem GET / zwracającym powitanie.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET / odpowiada
            {"wiadomosc": "Witaj w API"}.
    """
    app = FastAPI()
    @app.get("/")
    def powitanie() -> dict:
        return {"wiadomosc": "Witaj w API"}
    return app


def zadanie_02_dwa_endpointy() -> FastAPI:
    """Buduje aplikację z dwoma endpointami GET: / oraz /o-nas.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET / odpowiada
            {"wiadomosc": "Witaj w API"}, a GET /o-nas odpowiada
            {"nazwa": "Sklep Python", "wersja": 1}.
    """
    app = FastAPI()
    @app.get("/")
    def powitanie() -> dict:
        return {"wiadomosc": "Witaj w API"}
    @app.get("/o-nas")
    def o_nas() -> dict:
        return {"nazwa": "Sklep Python", "wersja": 1}
    return app


def zadanie_03_parametr_sciezki() -> FastAPI:
    """Buduje aplikację z endpointem o parametrze ścieżki walidowanym jako int.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /uzytkownicy/{id_uzytkownika}
            odpowiada {"id": <int z adresu>}; tekst zamiast liczby
            w adresie daje automatyczne 422.
    """
    app = FastAPI()
    @app.get("/uzytkownicy/{id_uzytkownika}")
    def pobierz_uzytkownika(id_uzytkownika: int) -> dict:
        return {"id": id_uzytkownika}
    return app


def zadanie_04_kwadrat_liczby() -> FastAPI:
    """Buduje aplikację liczącą kwadrat liczby z parametru ścieżki.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /kwadrat/{liczba} odpowiada
            {"wynik": liczba * liczba}; parametr walidowany jako int.
    """
    app = FastAPI()
    @app.get("/kwadrat/{liczba}")
    def kwadrat(liczba: int) -> dict:
        return {"wynik": liczba * liczba}
    return app


def zadanie_05_utworz_produkt(nazwa: str, cena: object) -> Produkt:
    """Tworzy obiekt Produkt, przepuszczając dane przez walidację Pydantic.

    Args:
        nazwa: nazwa produktu.
        cena: cena — dowolna wartość; Pydantic skonwertuje lub rzuci
            ValidationError.

    Returns:
        Produkt: zwalidowany obiekt produktu. Rzuca
            pydantic.ValidationError, gdy cena nie da się skonwertować
            na float.
    """
    return Produkt(nazwa=nazwa, cena=cena)


def zadanie_06_przyjmij_produkt() -> FastAPI:
    """Buduje aplikację przyjmującą produkt POST-em z walidacją modelu.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /produkty przyjmuje w treści
            JSON pasujący do modelu Produkt i odpowiada
            {"przyjeto": <nazwa produktu>}; złe dane dają 422.
    """
    app = FastAPI()
    @app.post("/produkty")
    def dodaj_produkt(produkt: Produkt) -> dict:
        return {"przyjeto": produkt.nazwa}
    return app


def zadanie_07_przyjmij_zamowienie() -> FastAPI:
    """Buduje aplikację liczącą wartość zamówienia przyjętego POST-em.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /zamowienia przyjmuje model
            Zamowienie i odpowiada
            {"do_zaplaty": ilosc * cena_jednostkowa}.
    """
    app = FastAPI()
    @app.post("/zamowienia")
    def zloz_zamowienie(zamowienie: Zamowienie) -> dict:
        return {"do_zaplaty": zamowienie.ilosc * zamowienie.cena_jednostkowa}
    return app


def zadanie_08_response_model() -> FastAPI:
    """Buduje aplikację, w której response_model wycina tajne pole odpowiedzi.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której GET /produkty/polecany odpowiada
            wyłącznie polami modelu Produkt (nazwa, cena), mimo że
            endpoint zwraca też pole "tajny_kod".
    """
    app = FastAPI()
    @app.get("/produkty/polecany", response_model=Produkt)
    def polecany() -> dict:
        return {"nazwa": "Klawiatura", "cena": 99.0, "tajny_kod": "X99"}
    return app


def zadanie_09_echo_produktu() -> FastAPI:
    """Buduje aplikację-echo: POST zwraca przyjęty produkt przez response_model.

    Args:
        Brak.

    Returns:
        FastAPI: aplikacja, której POST /produkty/echo przyjmuje model
            Produkt i odsyła go z powrotem (response_model=Produkt).
    """
    app = FastAPI()
    @app.post("/produkty/echo", response_model=Produkt)
    def produkt_echo(produkt: Produkt) -> Produkt:
        return produkt
    return app


def zadanie_10_api_konfiguracji(sciezka: str) -> FastAPI:
    """Buduje aplikację serwującą zawartość pliku JSON pod GET /konfiguracja.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON ze słownikiem.

    Returns:
        FastAPI: aplikacja, której GET /konfiguracja odpowiada
            zawartością pliku (czytaną przy każdym zapytaniu).
    """
    app = FastAPI()
    @app.get("/konfiguracja")
    def konfiguracja() -> dict[str, Any]:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    return app


def zadanie_11_api_dodawania(sciezka: str) -> FastAPI:
    """Buduje aplikację dopisującą produkt POST-em do listy w pliku JSON.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z listą produktów.

    Returns:
        FastAPI: aplikacja, której POST /produkty dopisuje przyjęty
            produkt na koniec listy w pliku i odpowiada
            {"liczba": <nowa długość listy>}.
    """
    app = FastAPI()
    @app.post("/produkty")
    def dodaj_produkt(produkt: Produkt) -> dict:
        with open(sciezka, "r", encoding="utf-8") as old:
            produkty = json.load(old)
        produkty.append(produkt.model_dump())
        with open(sciezka, "w", encoding="utf-8") as new:
            json.dump(produkty, new)
        return {"liczba": len(produkty)}
    return app


def zadanie_12_pelne_api(sciezka: str) -> FastAPI:
    """Buduje pełne API produktów: GET zwraca listę, POST dodaje do pliku.

    Args:
        sciezka: ścieżka do istniejącego pliku JSON z listą produktów.

    Returns:
        FastAPI: aplikacja z GET /produkty (lista z pliku)
            i POST /produkty (walidacja modelem Produkt, dopisanie
            do pliku, odpowiedź {"liczba": <nowa długość>}).
    """
    app = FastAPI()
    @app.get("/produkty")
    def wczytane_produkty() -> list:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    @app.post("/produkty")
    def dodaj_produkt(produkt: Produkt) -> dict:
        with open(sciezka, "r", encoding="utf-8") as old:
            produkty = json.load(old)
        produkty.append(produkt.model_dump())
        with open(sciezka, "w", encoding="utf-8") as new:
            json.dump(produkty, new)
        return {"liczba": len(produkty)}
    return app
