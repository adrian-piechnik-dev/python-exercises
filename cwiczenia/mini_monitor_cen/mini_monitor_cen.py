import time
from typing import Any

import requests
from bs4 import BeautifulSoup


def zadanie_01_pobierz_html(url: str) -> str | None:
    """Pobiera surowy HTML strony sklepu.

    Args:
        url: adres strony z produktami.

    Returns:
        str | None: treść strony (response.text) albo None przy
            jakimkolwiek błędzie sieci lub serwera (także 4xx/5xx).
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Jestem Adrian"},
            timeout=5
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def zadanie_02_parsuj_produkty(html: str) -> list[dict[str, str]]:
    """Wyciąga z HTML nazwy produktów i surowe teksty cen.

    Args:
        html: treść strony; produkty to divy klasy "produkt",
            wewnątrz span klasy "nazwa" i span klasy "cena".

    Returns:
        list[dict[str, str]]: słowniki {"nazwa": ..., "cena_tekst": ...}
            w kolejności ze strony; pusta lista, gdy brak produktów.
    """
    soup = BeautifulSoup(html, "html.parser")
    produkty = soup.find_all("div", class_="produkt")
    lista_produktow = []
    for produkt in produkty:
        nazwa = produkt.find("span", class_="nazwa").get_text()
        cena = produkt.find("span", class_="cena").get_text()
        lista_produktow.append({"nazwa": nazwa, "cena_tekst": cena})
    return lista_produktow


def zadanie_03_wyczysc_cene(cena_tekst: str) -> float | None:
    """Zamienia tekst ceny ze strony na liczbę.

    Args:
        cena_tekst: surowy tekst metki, np. "99,90 zł" lub " 1 299,00 zł ".

    Returns:
        float | None: cena jako liczba albo None, gdy tekst nie jest
            czytelną ceną (np. "brak danych").
    """
    czysty = cena_tekst.strip()
    bez_waluty = czysty.replace("zł", "")
    bez_spacji = bez_waluty.replace(" ", "")
    z_kropka = bez_spacji.replace(",", ".")
    try:
        return float(z_kropka)
    except ValueError:
        return None


def zadanie_04_zbierz_ceny(html: str) -> list[dict[str, Any]]:
    """Zbiera ze strony produkty z już oczyszczonymi cenami.

    Args:
        html: treść strony sklepu (format jak w zadaniu 02).

    Returns:
        list[dict[str, Any]]: słowniki {"nazwa": str, "cena": float};
            produkty z nieczytelną ceną są POMIJANE (patrol trwa dalej).
    """
    lista_produktow = zadanie_02_parsuj_produkty(html)
    czyste_ceny_produktow = []
    for produkt in lista_produktow:
        cena = produkt["cena_tekst"]
        czysta_cena = zadanie_03_wyczysc_cene(cena)
        if czysta_cena is None:
            continue
        czyste_ceny_produktow.append({"nazwa": produkt["nazwa"], "cena": czysta_cena})

    return czyste_ceny_produktow


def zadanie_05_patroluj_strony(adresy: list[str]) -> list[dict[str, Any]]:
    """Zbiera ceny z wielu stron, robiąc pauzę między zapytaniami.

    Args:
        adresy: lista adresów stron do odwiedzenia.

    Returns:
        list[dict[str, Any]]: produkty ze wszystkich stron w jednej,
            płaskiej liście; strony, których nie udało się pobrać
            (None z zadania 01), są pomijane.
    """
    lista_cen_produktow = []
    for adres in adresy:
        html = zadanie_01_pobierz_html(adres)
        if html is None:
            continue
        czyste_ceny_produktow = zadanie_04_zbierz_ceny(html)
        lista_cen_produktow.extend(czyste_ceny_produktow)
        time.sleep(1)
    return lista_cen_produktow


def zadanie_06_utworz_tabele(polaczenie: Any) -> None:
    """Tworzy tabelę ceny — dziennik odczytów monitora.

    Args:
        polaczenie: otwarte połączenie z bazą (albo atrapa w testach).

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.execute("""
            CREATE TABLE ceny(
                id SERIAL PRIMARY KEY,
                nazwa TEXT,
                cena NUMERIC,
                data_odczytu TEXT
            )
            """
        )
    polaczenie.commit()


def zadanie_07_zapisz_cene(
    polaczenie: Any, nazwa: str, cena: float, data_odczytu: str,
) -> None:
    """Dopisuje jeden odczyt ceny do dziennika.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.
        cena: odczytana cena.
        data_odczytu: data odczytu, np. "2026-07-10".

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.execute(
            "INSERT INTO ceny (nazwa, cena, data_odczytu) VALUES (%s, %s, %s)",
            (nazwa, cena, data_odczytu)
        )
    polaczenie.commit()


def zadanie_08_zapisz_wiele_cen(
    polaczenie: Any, wpisy: list[tuple],
) -> None:
    """Dopisuje wiele odczytów jednym zapytaniem hurtowym.

    Args:
        polaczenie: otwarte połączenie z bazą.
        wpisy: lista krotek (nazwa, cena, data_odczytu).

    Returns:
        None
    """
    with polaczenie.cursor() as kursor:
        kursor.executemany(
            "INSERT INTO ceny (nazwa, cena, data_odczytu) VALUES (%s, %s, %s)",
            wpisy
        )
    polaczenie.commit()


def zadanie_09_historia_cen(polaczenie: Any, nazwa: str) -> list[tuple]:
    """Pobiera pełną historię odczytów jednego produktu.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.

    Returns:
        list[tuple]: krotki (cena, data_odczytu) posortowane rosnąco
            po dacie; pusta lista, gdy produktu nie ma w dzienniku.
    """
    with polaczenie.cursor() as kursor:
        kursor.execute("""
            SELECT cena, data_odczytu 
            FROM ceny 
            WHERE nazwa = %s 
            ORDER BY data_odczytu
            """,
            (nazwa,)
        )
        return kursor.fetchall()


def zadanie_10_ostatnia_cena(polaczenie: Any, nazwa: str) -> float | None:
    """Pobiera najświeższą zapisaną cenę produktu.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.

    Returns:
        float | None: ostatnia cena jako float albo None, gdy produktu
            nie ma jeszcze w dzienniku.
    """
    with polaczenie.cursor() as kursor:
        kursor.execute("""
            SELECT cena 
            FROM ceny 
            WHERE nazwa = %s 
            ORDER BY data_odczytu 
            DESC LIMIT 1
            """,
            (nazwa,)
        )
        wiersz = kursor.fetchone()
        if wiersz is None:
            return None
        cena = wiersz[0]
        return float(cena)


def zadanie_11_werdykt(stara: float | None, nowa: float) -> str:
    """Porównuje cenę z ostatnim wpisem i wydaje werdykt.

    Args:
        stara: ostatnia znana cena albo None, gdy produkt jest nowy.
        nowa: świeżo odczytana cena.

    Returns:
        str: "nowy produkt" (stara is None), "wzrost", "spadek"
            albo "bez zmian" — wartości domenowe, nie sygnały błędów
            (teoria, sekcja 5).
    """
    if stara is None:
        return "nowy produkt"
    if nowa > stara:
        return "wzrost"
    if nowa < stara:
        return "spadek"
    return "bez zmian"


def zadanie_12_zapisz_odczyt(
    polaczenie: Any, html: str, data_odczytu: str,
) -> int:
    """Dyrygent zapisu: parsuje stronę i zapisuje wszystkie ceny do bazy.

    Args:
        polaczenie: otwarte połączenie z bazą.
        html: treść strony sklepu.
        data_odczytu: data patrolu, np. "2026-07-10".

    Returns:
        int: liczba zapisanych wpisów; 0 gdy strona nie miała żadnej
            czytelnej ceny (wtedy nie wykonuje zapisu wcale).
    """
    produkty_oczyszczone = zadanie_04_zbierz_ceny(html)
    if not produkty_oczyszczone:
        return 0
    wpisy = [
        (produkt["nazwa"], produkt["cena"], data_odczytu)
        for produkt in produkty_oczyszczone
    ]
    zadanie_08_zapisz_wiele_cen(polaczenie, wpisy)
    return len(produkty_oczyszczone)


def zadanie_13_monitoruj(
    url: str, polaczenie: Any, data_odczytu: str,
) -> list[dict[str, Any]] | None:
    """Dyrygent całości: patrol, porównanie z historią, zapis i meldunek.

    Args:
        url: adres strony sklepu.
        polaczenie: otwarte połączenie z bazą.
        data_odczytu: data patrolu, np. "2026-07-10".

    Returns:
        list[dict[str, Any]] | None: meldunek — dla każdego produktu
            słownik {"nazwa": str, "cena": float, "status": str}
            (status z zadania 11); None, gdy strony nie udało się
            pobrać (wtedy baza zostaje nietknięta).
    """
    html = zadanie_01_pobierz_html(url)
    if html is None:
        return None
    produkty = zadanie_04_zbierz_ceny(html)
    meldunek = []
    for produkt in produkty:
        nazwa = produkt["nazwa"]
        nowa_cena = produkt["cena"]
        stara_cena = zadanie_10_ostatnia_cena(polaczenie, nazwa)
        status = zadanie_11_werdykt(stara_cena, nowa_cena)
        zadanie_07_zapisz_cene(polaczenie, nazwa, nowa_cena, data_odczytu)
        meldunek.append({
            "nazwa": nazwa,
            "cena": nowa_cena,
            "status": status
        })
    return meldunek
