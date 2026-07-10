# Zadania — async_httpx
#
# Spis zadan:
# zadanie_01 — pierwsza coroutine: powitanie z imieniem
# zadanie_02 — await asyncio.sleep i zwrot wartosci po odczekaniu
# zadanie_03 — brama miedzy swiatami: uruchom coroutine przez asyncio.run
# zadanie_04 — asyncio.gather na liscie coroutine (gwiazdka!)
# zadanie_05 — pomiar czasu spania sekwencyjnego (await po await)
# zadanie_06 — pomiar czasu spania rownoleglego (gather)
# zadanie_07 — pobierz status HTTP przez httpx.AsyncClient
# zadanie_08 — pobierz tresc strony jako tekst
# zadanie_09 — pobierz statusy wielu URL-i rownolegle
# zadanie_10 — pobierz JSON wzorcem z requests (None gdy nie 200)
# zadanie_11 — pobierz JSON-y wielu URL-i rownolegle (skala)
# zadanie_12 — wyciagnij tytul strony przez BeautifulSoup (None gdy brak)
# zadanie_13 — scraping w skali: tytuly wielu stron rownolegle

import asyncio
import time

import httpx
from bs4 import BeautifulSoup


async def zadanie_01_zwroc_powitanie(imie: str) -> str:
    """Buduje powitanie w pierwszej coroutine tego kursu.

    Args:
        imie: imie do powitania, np. "Ala".

    Returns:
        str: tekst "Czesc, <imie>!".
    """
    # TODO: zwroc f-string "Czesc, {imie}!" (bez zadnego await —
    #       coroutine nie musi czekac, zeby byc coroutine)
    pass


async def zadanie_02_poczekaj_i_zwroc(sekundy: float, wartosc: str) -> str:
    """Odczekuje asynchronicznie podany czas i zwraca wartosc.

    Args:
        sekundy: ile sekund spac (np. 0.05).
        wartosc: tekst do zwrocenia po odczekaniu.

    Returns:
        str: przekazana wartosc (po uplywie sekund).
    """
    # TODO: uzyj await asyncio.sleep(sekundy)
    # TODO: zwroc wartosc
    pass


def zadanie_03_uruchom_synchronicznie(sekundy: float, wartosc: str) -> str:
    """Uruchamia coroutine z zadania 02 ze zwyklego (synchronicznego) kodu.

    Args:
        sekundy: ile sekund spac.
        wartosc: tekst do zwrocenia.

    Returns:
        str: wynik coroutine zadanie_02_poczekaj_i_zwroc.
    """
    # TODO: to funkcja ZWYKLA (bez async) — uzyj bramy asyncio.run
    #       na wywolaniu zadanie_02_poczekaj_i_zwroc(sekundy, wartosc)
    #       i zwroc jej wynik
    pass


async def zadanie_04_zbierz_wyniki(coroutines: list) -> list:
    """Uruchamia liste coroutine rownolegle i zbiera wyniki.

    Args:
        coroutines: lista obiektow coroutine do wykonania.

    Returns:
        list: wyniki w kolejnosci podania (pusta lista dla pustego wejscia).
    """
    # TODO: uzyj await asyncio.gather z gwiazdka (*coroutines)
    # TODO: gather zwraca liste — zwroc ja (uwaga: gather oddaje
    #       swoj wlasny typ listopodobny; owin go w list(...))
    pass


async def zadanie_05_czas_sekwencyjnie(lista_sekund: list[float]) -> float:
    """Mierzy czas wykonania span JEDNO PO DRUGIM (await w petli).

    Args:
        lista_sekund: dlugosci kolejnych span, np. [0.05, 0.05].

    Returns:
        float: zmierzony czas w sekundach (w przyblizeniu suma span).
    """
    # TODO: zapisz start = time.perf_counter()
    # TODO: w petli for po lista_sekund zrob await asyncio.sleep(...)
    #       dla kazdej wartosci
    # TODO: zwroc time.perf_counter() - start
    pass


async def zadanie_06_czas_rownolegle(lista_sekund: list[float]) -> float:
    """Mierzy czas wykonania span NARAZ (gather).

    Args:
        lista_sekund: dlugosci span, np. [0.05, 0.05].

    Returns:
        float: zmierzony czas w sekundach (w przyblizeniu najdluzsze spanie).
    """
    # TODO: zapisz start = time.perf_counter()
    # TODO: zbuduj list comprehension z coroutine asyncio.sleep(s)
    #       dla kazdego s z lista_sekund
    # TODO: odpal je naraz przez await asyncio.gather(*zadania)
    # TODO: zwroc time.perf_counter() - start
    pass


async def zadanie_07_pobierz_status(client: httpx.AsyncClient, url: str) -> int:
    """Pobiera kod statusu HTTP dla podanego adresu.

    Args:
        client: klient httpx (w testach: z podmienionym transportem).
        url: adres do odpytania.

    Returns:
        int: kod statusu odpowiedzi (np. 200 albo 404).
    """
    # TODO: wykonaj response = await client.get(url)
    # TODO: zwroc response.status_code
    pass


async def zadanie_08_pobierz_tekst(client: httpx.AsyncClient, url: str) -> str:
    """Pobiera tresc odpowiedzi jako tekst.

    Args:
        client: klient httpx.
        url: adres do odpytania.

    Returns:
        str: tresc odpowiedzi (response.text).
    """
    # TODO: wykonaj await client.get(url) i zwroc pole .text odpowiedzi
    pass


async def zadanie_09_pobierz_wiele_statusow(
    client: httpx.AsyncClient, urle: list[str]
) -> list[int]:
    """Pobiera kody statusow wielu adresow rownolegle.

    Args:
        client: klient httpx.
        urle: lista adresow do odpytania.

    Returns:
        list[int]: kody statusow w kolejnosci podania adresow
            (pusta lista dla pustego wejscia).
    """
    # TODO: zbuduj list comprehension z coroutine client.get(url)
    #       dla kazdego url z urle
    # TODO: odpal naraz przez await asyncio.gather(*zadania)
    # TODO: zwroc liste pol .status_code kolejnych odpowiedzi
    #       (list comprehension)
    pass


async def zadanie_10_pobierz_json(
    client: httpx.AsyncClient, url: str
) -> dict | None:
    """Pobiera JSON wzorcem znanym z requests; blad sygnalizuje przez None.

    Args:
        client: klient httpx.
        url: adres do odpytania.

    Returns:
        dict | None: slownik z response.json() przy statusie 200,
            None przy kazdym innym statusie.
    """
    # TODO: wykonaj response = await client.get(url)
    # TODO: jesli response.status_code != 200 — zwroc None
    # TODO: w przeciwnym razie zwroc response.json()
    pass


async def zadanie_11_pobierz_wiele_jsonow(
    client: httpx.AsyncClient, urle: list[str]
) -> list[dict | None]:
    """Pobiera JSON-y wielu adresow rownolegle (skala wzorca z zadania 10).

    Args:
        client: klient httpx.
        urle: lista adresow do odpytania.

    Returns:
        list[dict | None]: wynik zadania 10 dla kazdego adresu,
            w kolejnosci podania (None na pozycjach bledow).
    """
    # TODO: zbuduj list comprehension z coroutine
    #       zadanie_10_pobierz_json(client, url) dla kazdego url
    # TODO: odpal naraz przez await asyncio.gather(*zadania)
    #       i zwroc wynik jako liste
    pass


async def zadanie_12_pobierz_tytul_strony(
    client: httpx.AsyncClient, url: str
) -> str | None:
    """Pobiera strone i wyciaga tekst znacznika <title>.

    Args:
        client: klient httpx.
        url: adres strony HTML.

    Returns:
        str | None: tekst tytulu strony albo None, gdy strona
            nie ma znacznika <title>.
    """
    # TODO: pobierz tekst strony (await client.get, pole .text)
    # TODO: sparsuj przez BeautifulSoup(tekst, "html.parser")
    # TODO: znajdz znacznik przez soup.find("title")
    # TODO: jesli wynik find is None — zwroc None
    # TODO: w przeciwnym razie zwroc jego .get_text()
    pass


async def zadanie_13_pobierz_wiele_tytulow(
    client: httpx.AsyncClient, urle: list[str]
) -> list[str | None]:
    """Scrapuje tytuly wielu stron rownolegle (scraping w skali).

    Args:
        client: klient httpx.
        urle: lista adresow stron HTML.

    Returns:
        list[str | None]: tytuly w kolejnosci podania adresow
            (None na pozycjach stron bez <title>).
    """
    # TODO: zbuduj list comprehension z coroutine
    #       zadanie_12_pobierz_tytul_strony(client, url) dla kazdego url
    # TODO: odpal naraz przez await asyncio.gather(*zadania)
    #       i zwroc wynik jako liste
    pass
