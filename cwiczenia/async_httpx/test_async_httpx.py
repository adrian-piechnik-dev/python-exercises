import asyncio

import httpx

from async_httpx import (
    zadanie_01_zwroc_powitanie,
    zadanie_02_poczekaj_i_zwroc,
    zadanie_03_uruchom_synchronicznie,
    zadanie_04_zbierz_wyniki,
    zadanie_05_czas_sekwencyjnie,
    zadanie_06_czas_rownolegle,
    zadanie_07_pobierz_status,
    zadanie_08_pobierz_tekst,
    zadanie_09_pobierz_wiele_statusow,
    zadanie_10_pobierz_json,
    zadanie_11_pobierz_wiele_jsonow,
    zadanie_12_pobierz_tytul_strony,
    zadanie_13_pobierz_wiele_tytulow,
)


# --- zadanie_01 ---

def test_zadanie_01_wita_po_imieniu() -> None:
    """Co testuje: czy coroutine buduje powitanie "Czesc, Ala!".
    Co udaje: nic — czysta coroutine, uruchamiam ja przez asyncio.run.
    Co sprawdzam: wynik == "Czesc, Ala!".
    """
    # TODO: wywolaj asyncio.run(zadanie_01_zwroc_powitanie("Ala"))
    # TODO: sprawdz assertem dokladny tekst wyniku
    pass


def test_zadanie_01_wywolanie_bez_run_daje_obiekt_coroutine() -> None:
    """Co testuje: pulapke z teorii — wywolanie coroutine bez asyncio.run
    NIE zwraca tekstu, tylko obiekt-przepis.
    Co udaje: nic.
    Co sprawdzam: wynik wywolania nie jest tekstem (isinstance(..., str)
    is False); na koncu zamykam obiekt przez .close(), zeby uciszyc
    RuntimeWarning.
    """
    # TODO: przygotuj obiekt = zadanie_01_zwroc_powitanie("Ala")
    #       (bez asyncio.run!)
    # TODO: sprawdz assertem, ze isinstance(obiekt, str) is False
    # TODO: posprzataj: obiekt.close()
    pass


# --- zadanie_02 ---

def test_zadanie_02_zwraca_wartosc_po_spaniu() -> None:
    """Co testuje: czy coroutine po odczekaniu oddaje przekazana wartosc.
    Co udaje: nic — prawdziwe (krotkie!) spanie 0.01 s.
    Co sprawdzam: wynik == "gotowe".
    """
    # TODO: wywolaj przez asyncio.run z sekundami 0.01 i wartoscia "gotowe"
    # TODO: sprawdz assertem wynik
    pass


def test_zadanie_02_dziala_dla_zera_sekund() -> None:
    """Co testuje: przypadek brzegowy — spanie 0 sekund tez dziala.
    Co udaje: nic.
    Co sprawdzam: wynik == "natychmiast".
    """
    # TODO: wywolaj przez asyncio.run z sekundami 0 i wartoscia "natychmiast"
    # TODO: sprawdz assertem wynik
    pass


# --- zadanie_03 ---

def test_zadanie_03_zwraca_wynik_coroutine() -> None:
    """Co testuje: czy synchroniczna brama oddaje wynik coroutine z zadania 02.
    Co udaje: nic — funkcja sama robi asyncio.run w srodku.
    Co sprawdzam: wynik == "przez-brame" (wywolanie BEZ asyncio.run w tescie!).
    """
    # TODO: wywolaj zadanie_03_uruchom_synchronicznie(0.01, "przez-brame")
    #       zwyczajnie, bez asyncio.run — to zwykla funkcja
    # TODO: sprawdz assertem wynik
    pass


def test_zadanie_03_wynik_jest_tekstem_nie_coroutine() -> None:
    """Co testuje: czy brama zwraca gotowy tekst, a nie obiekt coroutine.
    Co udaje: nic.
    Co sprawdzam: isinstance(wynik, str) is True.
    """
    # TODO: wywolaj funkcje z dowolnymi argumentami (male spanie!)
    # TODO: sprawdz assertem, ze wynik jest typu str
    pass


# --- zadanie_04 ---

def test_zadanie_04_zbiera_wyniki_w_kolejnosci_podania() -> None:
    """Co testuje: czy gather oddaje wyniki w kolejnosci podania coroutine,
    nawet gdy pierwsza spi dluzej niz druga.
    Co udaje: nic — dwie prawdziwe coroutine z zadania 02.
    Co sprawdzam: wynik == ["pierwszy", "drugi"] (mimo ze "drugi" konczy
    sie szybciej).
    """
    # TODO: przygotuj liste [zadanie_02_poczekaj_i_zwroc(0.05, "pierwszy"),
    #       zadanie_02_poczekaj_i_zwroc(0.01, "drugi")]
    # TODO: wywolaj asyncio.run(zadanie_04_zbierz_wyniki(lista))
    # TODO: sprawdz assertem dokladna kolejnosc wynikow
    pass


def test_zadanie_04_pusta_lista_daje_pusta_liste() -> None:
    """Co testuje: przypadek brzegowy — gather na pustej liscie.
    Co udaje: nic.
    Co sprawdzam: wynik == [].
    """
    # TODO: wywolaj asyncio.run(zadanie_04_zbierz_wyniki([]))
    # TODO: sprawdz assertem, ze wynik to pusta lista
    pass


# --- zadanie_05 ---

def test_zadanie_05_czas_to_co_najmniej_suma_span() -> None:
    """Co testuje: czy spanie sekwencyjne trwa co najmniej sume span.
    Co udaje: nic — prawdziwe krotkie spania.
    Co sprawdzam: wynik >= 0.06 dla listy [0.03, 0.03].
    """
    # TODO: wywolaj przez asyncio.run z lista [0.03, 0.03]
    # TODO: sprawdz assertem, ze zmierzony czas >= 0.06
    pass


def test_zadanie_05_pusta_lista_konczy_sie_natychmiast() -> None:
    """Co testuje: przypadek brzegowy — brak span = czas bliski zeru.
    Co udaje: nic.
    Co sprawdzam: wynik < 0.05.
    """
    # TODO: wywolaj przez asyncio.run z pusta lista
    # TODO: sprawdz assertem, ze czas < 0.05
    pass


# --- zadanie_06 ---

def test_zadanie_06_rownolegle_szybsze_niz_suma() -> None:
    """Co testuje: sedno async — dwa spania naraz trwaja krocej niz ich suma.
    Co udaje: nic — prawdziwe krotkie spania.
    Co sprawdzam: wynik < 0.1 dla listy [0.05, 0.05] (suma bylaby 0.1).
    """
    # TODO: wywolaj przez asyncio.run z lista [0.05, 0.05]
    # TODO: sprawdz assertem, ze zmierzony czas < 0.1
    pass


def test_zadanie_06_rownolegle_szybsze_niz_sekwencyjnie() -> None:
    """Co testuje: porownanie sync vs async na tych samych spaniach.
    Co udaje: nic — mierze obie wersje naprawde.
    Co sprawdzam: czas rownolegly < czas sekwencyjny dla [0.03, 0.03, 0.03].
    """
    # TODO: przygotuj liste [0.03, 0.03, 0.03]
    # TODO: zmierz czas sekwencyjny (asyncio.run na zadaniu 05)
    # TODO: zmierz czas rownolegly (asyncio.run na zadaniu 06)
    # TODO: sprawdz assertem, ze rownolegly < sekwencyjny
    pass


# --- zadanie_07 ---

def test_zadanie_07_zwraca_200_dla_istniejacej_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja oddaje kod statusu odpowiedzi.
    Co udaje: internet — klient_testowy z MockTransport (adres /ok -> 200).
    Co sprawdzam: wynik == 200.
    """
    # TODO: wywolaj przez asyncio.run zadanie_07_pobierz_status
    #       z klientem i adresem "https://testowy.pl/ok"
    # TODO: sprawdz assertem, ze wynik == 200
    pass


def test_zadanie_07_zwraca_404_dla_brakujacej_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy kod bledu tez wraca bez zmian (funkcja nie ukrywa 404).
    Co udaje: internet — MockTransport (adres /brak -> 404).
    Co sprawdzam: wynik == 404.
    """
    # TODO: wywolaj funkcje z adresem "https://testowy.pl/brak"
    # TODO: sprawdz assertem, ze wynik == 404
    pass


# --- zadanie_08 ---

def test_zadanie_08_zwraca_tresc_odpowiedzi(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja oddaje tekst odpowiedzi.
    Co udaje: internet — MockTransport (adres /ok -> tekst "ok").
    Co sprawdzam: wynik == "ok".
    """
    # TODO: wywolaj przez asyncio.run z adresem "https://testowy.pl/ok"
    # TODO: sprawdz assertem tekst wyniku
    pass


def test_zadanie_08_zwraca_html_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy dla strony HTML wraca pelny kod z tagiem <title>.
    Co udaje: internet — MockTransport (adres /strona -> HTML z tytulem).
    Co sprawdzam: "<title>" in wynik.
    """
    # TODO: wywolaj funkcje z adresem "https://testowy.pl/strona"
    # TODO: sprawdz assertem, ze "<title>" wystepuje w wyniku
    pass


# --- zadanie_09 ---

def test_zadanie_09_statusy_w_kolejnosci_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy statusy wracaja w kolejnosci podania adresow.
    Co udaje: internet — MockTransport (/ok -> 200, /brak -> 404).
    Co sprawdzam: wynik == [200, 404, 200].
    """
    # TODO: przygotuj liste adresow: /ok, /brak, /ok
    #       (pelne adresy https://testowy.pl/...)
    # TODO: wywolaj przez asyncio.run zadanie_09_pobierz_wiele_statusow
    # TODO: sprawdz assertem cala liste wynikow
    pass


def test_zadanie_09_pusta_lista_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: przypadek brzegowy — brak adresow = pusta lista statusow.
    Co udaje: internet — MockTransport (nieuzyty).
    Co sprawdzam: wynik == [].
    """
    # TODO: wywolaj funkcje z pusta lista adresow
    # TODO: sprawdz assertem, ze wynik to pusta lista
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_slownik_dla_statusu_200(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: wzorzec z requests — status 200 daje slownik z JSON-a.
    Co udaje: internet — MockTransport (/dane -> 200 + json z miastem).
    Co sprawdzam: wynik == {"miasto": "Krakow", "sprzedaz": 200}.
    """
    # TODO: wywolaj przez asyncio.run z adresem "https://testowy.pl/dane"
    # TODO: sprawdz assertem caly slownik
    pass


def test_zadanie_10_zwraca_none_dla_statusu_404(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: kontrakt None — status inny niz 200 daje None, nie wyjatek.
    Co udaje: internet — MockTransport (/brak -> 404).
    Co sprawdzam: wynik is None.
    """
    # TODO: wywolaj funkcje z adresem "https://testowy.pl/brak"
    # TODO: sprawdz assertem, ze wynik is None
    pass


# --- zadanie_11 ---

def test_zadanie_11_jsony_w_kolejnosci_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy rownolegle pobieranie JSON-ow zachowuje kolejnosc.
    Co udaje: internet — MockTransport (/dane -> slownik).
    Co sprawdzam: wynik == [slownik, slownik] dla dwoch adresow /dane.
    """
    # TODO: przygotuj liste dwoch adresow /dane
    # TODO: wywolaj przez asyncio.run zadanie_11_pobierz_wiele_jsonow
    # TODO: sprawdz assertem, ze wynik to dwa identyczne slowniki z miastem
    pass


def test_zadanie_11_none_na_pozycji_bledu(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy blad jednego adresu nie psuje pozostalych —
    None laduje na wlasciwej pozycji.
    Co udaje: internet — MockTransport (/dane -> 200, /brak -> 404).
    Co sprawdzam: wynik[0] to slownik, wynik[1] is None, wynik[2] to slownik.
    """
    # TODO: przygotuj liste adresow: /dane, /brak, /dane
    # TODO: wywolaj funkcje przez asyncio.run
    # TODO: sprawdz trzema assertami pozycje 0, 1 i 2
    pass


# --- zadanie_12 ---

def test_zadanie_12_wyciaga_tytul_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja pobiera strone i oddaje tekst z <title>.
    Co udaje: internet — MockTransport (/strona -> HTML z tytulem
    "Testowa strona").
    Co sprawdzam: wynik == "Testowa strona".
    """
    # TODO: wywolaj przez asyncio.run z adresem "https://testowy.pl/strona"
    # TODO: sprawdz assertem dokladny tytul
    pass


def test_zadanie_12_zwraca_none_gdy_strona_bez_tytulu(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: kontrakt None — strona bez znacznika <title> daje None.
    Co udaje: internet — MockTransport (/pusta -> HTML bez title).
    Co sprawdzam: wynik is None.
    """
    # TODO: wywolaj funkcje z adresem "https://testowy.pl/pusta"
    # TODO: sprawdz assertem, ze wynik is None
    pass


# --- zadanie_13 ---

def test_zadanie_13_tytuly_wielu_stron_w_kolejnosci(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: scraping w skali — tytuly dwoch stron w kolejnosci adresow.
    Co udaje: internet — MockTransport (/strona i /strona2 z roznymi tytulami).
    Co sprawdzam: wynik == ["Testowa strona", "Druga strona"].
    """
    # TODO: przygotuj liste adresow /strona i /strona2
    # TODO: wywolaj przez asyncio.run zadanie_13_pobierz_wiele_tytulow
    # TODO: sprawdz assertem cala liste tytulow
    pass


def test_zadanie_13_none_dla_strony_bez_tytulu_w_srodku(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy strona bez tytulu w srodku listy daje None na swojej
    pozycji, nie psujac reszty.
    Co udaje: internet — MockTransport (/strona, /pusta, /strona2).
    Co sprawdzam: wynik == ["Testowa strona", None, "Druga strona"].
    """
    # TODO: przygotuj liste adresow: /strona, /pusta, /strona2
    # TODO: wywolaj funkcje przez asyncio.run
    # TODO: sprawdz assertem cala liste (z None w srodku)
    pass
