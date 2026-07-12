# Spis zadań (mini-projekt M3 — pipeline: scraping -> baza danych -> raport zmian):
# 01 — pobranie HTML strony sklepu z kontrolą błędów (None przy awarii)
# 02 — parsowanie produktów z HTML (nazwa + surowy tekst ceny)
# 03 — czyszczenie tekstu ceny do float (None gdy nieczytelna)
# 04 — zebranie czystych cen ze strony (parsowanie + czyszczenie, pomija zepsute)
# 05 — patrol po wielu stronach z pauzą między zapytaniami
# 06 — utworzenie tabeli ceny w bazie (dziennik odczytów)
# 07 — zapis jednego odczytu ceny (INSERT z %s + commit)
# 08 — zapis hurtowy wielu odczytów (executemany + commit)
# 09 — historia cen produktu (SELECT + fetchall)
# 10 — ostatnia zapisana cena produktu (ORDER BY DESC + LIMIT 1, None gdy brak)
# 11 — werdykt zmiany ceny: wzrost / spadek / bez zmian / nowy produkt
# 12 — dyrygent zapisu: z HTML prosto do bazy (zwraca liczbę wpisów)
# 13 — dyrygent całości: patrol + porównanie + zapis + meldunek ze statusami

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
    # TODO: pobierz stronę grzecznym scraperem z tematu 12 — przedstaw
    #       się nagłówkiem User-Agent, ustaw timeout, skontroluj kod
    #       odpowiedzi
    # TODO: awarię sieci/serwera obsłuż kontraktem None (wspólnego
    #       rodzica wyjątków sieciowych znasz z tematu 11)
    pass


def zadanie_02_parsuj_produkty(html: str) -> list[dict[str, str]]:
    """Wyciąga z HTML nazwy produktów i surowe teksty cen.

    Args:
        html: treść strony; produkty to divy klasy "produkt",
            wewnątrz span klasy "nazwa" i span klasy "cena".

    Returns:
        list[dict[str, str]]: słowniki {"nazwa": ..., "cena_tekst": ...}
            w kolejności ze strony; pusta lista, gdy brak produktów.
    """
    # TODO: sparsuj HTML i znajdź wszystkie divy produktów
    #       (find_all z klasą — temat 12)
    # TODO: z każdego diva wyciągnij tekst obu spanów (find wewnątrz
    #       elementu + get_text — temat 12) i zbuduj słownik
    pass


def zadanie_03_wyczysc_cene(cena_tekst: str) -> float | None:
    """Zamienia tekst ceny ze strony na liczbę.

    Args:
        cena_tekst: surowy tekst metki, np. "99,90 zł" lub " 1 299,00 zł ".

    Returns:
        float | None: cena jako liczba albo None, gdy tekst nie jest
            czytelną ceną (np. "brak danych").
    """
    # TODO: wysprzątaj tekst wzorcem z teorii (sekcja 3): białe znaki
    #       z końców, napis waluty, spacje w środku, przecinek na kropkę
    # TODO: konwersję ubezpiecz bramką znaną z M1 — nieczytelna metka
    #       to kontrakt None, nie wyjątek
    pass


def zadanie_04_zbierz_ceny(html: str) -> list[dict[str, Any]]:
    """Zbiera ze strony produkty z już oczyszczonymi cenami.

    Args:
        html: treść strony sklepu (format jak w zadaniu 02).

    Returns:
        list[dict[str, Any]]: słowniki {"nazwa": str, "cena": float};
            produkty z nieczytelną ceną są POMIJANE (patrol trwa dalej).
    """
    # TODO: połącz dwa gotowe klocki: parsowanie (zadanie 02)
    #       i czyszczenie (zadanie 03)
    # TODO: produkt, którego cena wyszła None, pomiń — do wyniku
    #       trafiają tylko czytelne metki
    pass


def zadanie_05_patroluj_strony(adresy: list[str]) -> list[dict[str, Any]]:
    """Zbiera ceny z wielu stron, robiąc pauzę między zapytaniami.

    Args:
        adresy: lista adresów stron do odwiedzenia.

    Returns:
        list[dict[str, Any]]: produkty ze wszystkich stron w jednej,
            płaskiej liście; strony, których nie udało się pobrać
            (None z zadania 01), są pomijane.
    """
    # TODO: dla każdego adresu: pauza grzecznościowa 1 sekundy
    #       (temat 12), pobranie HTML (zadanie 01), zebranie cen
    #       (zadanie 04)
    # TODO: nieudane pobranie pomiń; udane porcje doklejaj do
    #       akumulatora (pułapkę append vs extend znasz z M2)
    pass


def zadanie_06_utworz_tabele(polaczenie: Any) -> None:
    """Tworzy tabelę ceny — dziennik odczytów monitora.

    Args:
        polaczenie: otwarte połączenie z bazą (albo atrapa w testach).

    Returns:
        None
    """
    # TODO: w bloku with na kursorze wykonaj utworzenie tabeli:
    #       CREATE TABLE ceny (
    #           id SERIAL PRIMARY KEY,
    #           nazwa TEXT,
    #           cena NUMERIC,
    #           data_odczytu TEXT
    #       )
    #       (wzorzec pracy z kursorem znasz z tematu 15)
    # TODO: po bloku with zatwierdź zmianę
    pass


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
    # TODO: w bloku with na kursorze wykonaj INSERT do tabeli ceny
    #       (kolumny nazwa, cena, data_odczytu) — wartości WYŁĄCZNIE
    #       przez zaślepki %s i krotkę parametrów (temat 15; pamiętaj,
    #       dlaczego f-string w SQL to przestępstwo)
    # TODO: po bloku with zatwierdź zmianę
    pass


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
    # TODO: jak zadanie 07, ale hurtem — metodę kursora do wielu
    #       krotek naraz znasz z tematu 15
    # TODO: po bloku with zatwierdź zmianę
    pass


def zadanie_09_historia_cen(polaczenie: Any, nazwa: str) -> list[tuple]:
    """Pobiera pełną historię odczytów jednego produktu.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.

    Returns:
        list[tuple]: krotki (cena, data_odczytu) posortowane rosnąco
            po dacie; pusta lista, gdy produktu nie ma w dzienniku.
    """
    # TODO: w bloku with wykonaj SELECT cena, data_odczytu z filtrem
    #       WHERE po nazwie (parametr przez %s) i sortowaniem po dacie
    # TODO: zwróć wszystkie wiersze (metoda odczytu wielu wierszy —
    #       temat 15); odczyt nie wymaga commita
    pass


def zadanie_10_ostatnia_cena(polaczenie: Any, nazwa: str) -> float | None:
    """Pobiera najświeższą zapisaną cenę produktu.

    Args:
        polaczenie: otwarte połączenie z bazą.
        nazwa: nazwa produktu.

    Returns:
        float | None: ostatnia cena jako float albo None, gdy produktu
            nie ma jeszcze w dzienniku.
    """
    # TODO: zbuduj zapytanie o „ostatni wpis" wzorcem z teorii
    #       (sekcja 4) i pobierz jeden wiersz
    # TODO: brak wiersza obsłuż kontraktem None; wartość z wiersza
    #       rzutuj na float (teoria, sekcja 4 — pułapka fetchone[0])
    pass


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
    # TODO: rozstrzygnij cztery przypadki łańcuchem warunków z early
    #       returnem (temat 1); zacznij od przypadku nowego produktu
    #       (porównanie z None — pamiętaj o is)
    pass


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
    # TODO: zbierz czyste ceny gotowym klockiem (zadanie 04)
    # TODO: gdy lista pusta — zakończ early returnem zerem, bez
    #       dotykania bazy
    # TODO: zbuduj listę krotek (nazwa, cena, data_odczytu) i zapisz
    #       hurtem gotowym klockiem (zadanie 08); zwróć liczbę wpisów
    pass


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
    # TODO: pobierz HTML (zadanie 01); awarię propaguj kontraktem None
    #       ZANIM cokolwiek trafi do bazy (teoria, sekcja 5)
    # TODO: zbierz czyste ceny (zadanie 04) i dla każdego produktu:
    #       ostatnia cena z dziennika (zadanie 10) -> werdykt
    #       (zadanie 11) -> zapis nowego odczytu (zadanie 07) ->
    #       wpis do meldunku
    # TODO: zwróć meldunek jako listę słowników
    pass
