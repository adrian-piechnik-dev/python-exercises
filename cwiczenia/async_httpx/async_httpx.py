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
    return f"Czesc, {imie}!"


async def zadanie_02_poczekaj_i_zwroc(sekundy: float, wartosc: str) -> str:
    """Odczekuje asynchronicznie podany czas i zwraca wartosc.

    Args:
        sekundy: ile sekund spac (np. 0.05).
        wartosc: tekst do zwrocenia po odczekaniu.

    Returns:
        str: przekazana wartosc (po uplywie sekund).
    """
    await asyncio.sleep(sekundy)
    return wartosc


def zadanie_03_uruchom_synchronicznie(sekundy: float, wartosc: str) -> str:
    """Uruchamia coroutine z zadania 02 ze zwyklego (synchronicznego) kodu.

    Args:
        sekundy: ile sekund spac.
        wartosc: tekst do zwrocenia.

    Returns:
        str: wynik coroutine zadanie_02_poczekaj_i_zwroc.
    """
    return asyncio.run(zadanie_02_poczekaj_i_zwroc(sekundy, wartosc))


async def zadanie_04_zbierz_wyniki(coroutines: list) -> list:
    """Uruchamia liste coroutine rownolegle i zbiera wyniki.

    Args:
        coroutines: lista obiektow coroutine do wykonania.

    Returns:
        list: wyniki w kolejnosci podania (pusta lista dla pustego wejscia).
    """
    return await asyncio.gather(*coroutines)


async def zadanie_05_czas_sekwencyjnie(lista_sekund: list[float]) -> float:
    """Mierzy czas wykonania span JEDNO PO DRUGIM (await w petli).

    Args:
        lista_sekund: dlugosci kolejnych span, np. [0.05, 0.05].

    Returns:
        float: zmierzony czas w sekundach (w przyblizeniu suma span).
    """
    start = time.perf_counter()
    for sekunda in lista_sekund:
        await asyncio.sleep(sekunda)
    return time.perf_counter() - start


async def zadanie_06_czas_rownolegle(lista_sekund: list[float]) -> float:
    """Mierzy czas wykonania span NARAZ (gather).

    Args:
        lista_sekund: dlugosci span, np. [0.05, 0.05].

    Returns:
        float: zmierzony czas w sekundach (w przyblizeniu najdluzsze spanie).
    """
    start = time.perf_counter()
    zadania = [asyncio.sleep(s) for s in lista_sekund]
    await asyncio.gather(*zadania)
    return time.perf_counter() - start


async def zadanie_07_pobierz_status(client: httpx.AsyncClient, url: str) -> int:
    """Pobiera kod statusu HTTP dla podanego adresu.

    Args:
        client: klient httpx (w testach: z podmienionym transportem).
        url: adres do odpytania.

    Returns:
        int: kod statusu odpowiedzi (np. 200 albo 404).
    """
    response = await client.get(url)
    return response.status_code


async def zadanie_08_pobierz_tekst(client: httpx.AsyncClient, url: str) -> str:
    """Pobiera tresc odpowiedzi jako tekst.

    Args:
        client: klient httpx.
        url: adres do odpytania.

    Returns:
        str: tresc odpowiedzi (response.text).
    """
    response = await client.get(url)
    return response.text


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
    zadania = [client.get(url) for url in urle]
    odpowiedzi = await asyncio.gather(*zadania)
    return [odpowiedz.status_code for odpowiedz in odpowiedzi]


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
    response = await client.get(url)
    if response.status_code != 200:
        return None
    return response.json()


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
    zadania = [zadanie_10_pobierz_json(client, url) for url in urle]
    odpowiedzi = await asyncio.gather(*zadania)
    return odpowiedzi


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
    response = await client.get(url)
    tekst = response.text
    soup = BeautifulSoup(tekst, "html.parser")
    wynik = soup.find("title")
    if wynik is None:
        return None
    return wynik.get_text()


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
    zadania = [
        zadanie_12_pobierz_tytul_strony(client, url) for url in urle
    ]
    odpowiedzi = await asyncio.gather(*zadania)
    return odpowiedzi
