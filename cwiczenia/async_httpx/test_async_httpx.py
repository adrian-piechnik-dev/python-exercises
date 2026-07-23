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
    wynik = asyncio.run(zadanie_01_zwroc_powitanie("Ala"))
    assert wynik == "Czesc, Ala!"


def test_zadanie_01_wywolanie_bez_run_daje_obiekt_coroutine() -> None:
    """Co testuje: pulapke z teorii — wywolanie coroutine bez asyncio.run
    NIE zwraca tekstu, tylko obiekt-przepis.
    Co udaje: nic.
    Co sprawdzam: wynik wywolania nie jest tekstem (isinstance(..., str)
    is False); na koncu zamykam obiekt przez .close(), zeby uciszyc
    RuntimeWarning.
    """
    obiekt = zadanie_01_zwroc_powitanie("Ala")
    assert isinstance(obiekt, str) is False
    obiekt.close()


# --- zadanie_02 ---

def test_zadanie_02_zwraca_wartosc_po_spaniu() -> None:
    """Co testuje: czy coroutine po odczekaniu oddaje przekazana wartosc.
    Co udaje: nic — prawdziwe (krotkie!) spanie 0.01 s.
    Co sprawdzam: wynik == "gotowe".
    """
    wynik = asyncio.run(zadanie_02_poczekaj_i_zwroc(0.01, "gotowe"))
    assert wynik == "gotowe"


def test_zadanie_02_dziala_dla_zera_sekund() -> None:
    """Co testuje: przypadek brzegowy — spanie 0 sekund tez dziala.
    Co udaje: nic.
    Co sprawdzam: wynik == "natychmiast".
    """
    wynik = asyncio.run(zadanie_02_poczekaj_i_zwroc(0, "natychmiast"))
    assert wynik == "natychmiast"


# --- zadanie_03 ---

def test_zadanie_03_zwraca_wynik_coroutine() -> None:
    """Co testuje: czy synchroniczna brama oddaje wynik coroutine z zadania 02.
    Co udaje: nic — funkcja sama robi asyncio.run w srodku.
    Co sprawdzam: wynik == "przez-brame" (wywolanie BEZ asyncio.run w tescie!).
    """
    wynik = zadanie_03_uruchom_synchronicznie(0.01, "przez-brame")
    assert wynik == "przez-brame"


def test_zadanie_03_wynik_jest_tekstem_nie_coroutine() -> None:
    """Co testuje: czy brama zwraca gotowy tekst, a nie obiekt coroutine.
    Co udaje: nic.
    Co sprawdzam: isinstance(wynik, str) is True.
    """
    wynik = zadanie_03_uruchom_synchronicznie(0.01, "przez-brame")
    assert isinstance(wynik, str) is True


# --- zadanie_04 ---

def test_zadanie_04_zbiera_wyniki_w_kolejnosci_podania() -> None:
    """Co testuje: czy gather oddaje wyniki w kolejnosci podania coroutine,
    nawet gdy pierwsza spi dluzej niz druga.
    Co udaje: nic — dwie prawdziwe coroutine z zadania 02.
    Co sprawdzam: wynik == ["pierwszy", "drugi"] (mimo ze "drugi" konczy
    sie szybciej).
    """
    lista = [
        zadanie_02_poczekaj_i_zwroc(0.05, "pierwszy"),
        zadanie_02_poczekaj_i_zwroc(0.01, "drugi")
    ]
    wynik = asyncio.run(zadanie_04_zbierz_wyniki(lista))
    assert wynik == ["pierwszy", "drugi"]


def test_zadanie_04_pusta_lista_daje_pusta_liste() -> None:
    """Co testuje: przypadek brzegowy — gather na pustej liscie.
    Co udaje: nic.
    Co sprawdzam: wynik == [].
    """
    wynik = asyncio.run(zadanie_04_zbierz_wyniki([]))
    assert wynik == []


# --- zadanie_05 ---

def test_zadanie_05_czas_to_co_najmniej_suma_span() -> None:
    """Co testuje: czy spanie sekwencyjne trwa co najmniej sume span.
    Co udaje: nic — prawdziwe krotkie spania.
    Co sprawdzam: wynik >= 0.06 dla listy [0.03, 0.03].
    """
    wynik = asyncio.run(zadanie_05_czas_sekwencyjnie([0.03, 0.03]))
    assert wynik >= 0.06


def test_zadanie_05_pusta_lista_konczy_sie_natychmiast() -> None:
    """Co testuje: przypadek brzegowy — brak span = czas bliski zeru.
    Co udaje: nic.
    Co sprawdzam: wynik < 0.05.
    """
    wynik = asyncio.run(zadanie_05_czas_sekwencyjnie([]))
    assert wynik < 0.05


# --- zadanie_06 ---

def test_zadanie_06_rownolegle_szybsze_niz_suma() -> None:
    """Co testuje: sedno async — dwa spania naraz trwaja krocej niz ich suma.
    Co udaje: nic — prawdziwe krotkie spania.
    Co sprawdzam: wynik < 0.1 dla listy [0.05, 0.05] (suma bylaby 0.1).
    """
    wynik = asyncio.run(zadanie_06_czas_rownolegle([0.05, 0.05]))
    assert wynik < 0.1


def test_zadanie_06_rownolegle_szybsze_niz_sekwencyjnie() -> None:
    """Co testuje: porownanie sync vs async na tych samych spaniach.
    Co udaje: nic — mierze obie wersje naprawde.
    Co sprawdzam: czas rownolegly < czas sekwencyjny dla [0.03, 0.03, 0.03].
    """
    zadania = [0.03, 0.03, 0.03]
    sekwencyjny = asyncio.run(zadanie_05_czas_sekwencyjnie(zadania))
    rownolegly = asyncio.run(zadanie_06_czas_rownolegle(zadania))
    assert rownolegly < sekwencyjny


# --- zadanie_07 ---

def test_zadanie_07_zwraca_200_dla_istniejacej_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja oddaje kod statusu odpowiedzi.
    Co udaje: internet — klient_testowy z MockTransport (adres /ok -> 200).
    Co sprawdzam: wynik == 200.
    """
    wynik = asyncio.run(
        zadanie_07_pobierz_status(klient_testowy, "https://testowy.pl/ok")
    )
    assert wynik == 200


def test_zadanie_07_zwraca_404_dla_brakujacej_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy kod bledu tez wraca bez zmian (funkcja nie ukrywa 404).
    Co udaje: internet — MockTransport (adres /brak -> 404).
    Co sprawdzam: wynik == 404.
    """
    wynik = asyncio.run(
        zadanie_07_pobierz_status(klient_testowy, "https://testowy.pl/brak")
    )
    assert wynik == 404


# --- zadanie_08 ---

def test_zadanie_08_zwraca_tresc_odpowiedzi(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja oddaje tekst odpowiedzi.
    Co udaje: internet — MockTransport (adres /ok -> tekst "ok").
    Co sprawdzam: wynik == "ok".
    """
    wynik = asyncio.run(
        zadanie_08_pobierz_tekst(klient_testowy, "https://testowy.pl/ok")
    )
    assert wynik == "ok"


def test_zadanie_08_zwraca_html_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy dla strony HTML wraca pelny kod z tagiem <title>.
    Co udaje: internet — MockTransport (adres /strona -> HTML z tytulem).
    Co sprawdzam: "<title>" in wynik.
    """
    wynik = asyncio.run(
        zadanie_08_pobierz_tekst(klient_testowy, "https://testowy.pl/strona")
    )
    assert "<title>" in wynik


# --- zadanie_09 ---

def test_zadanie_09_statusy_w_kolejnosci_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy statusy wracaja w kolejnosci podania adresow.
    Co udaje: internet — MockTransport (/ok -> 200, /brak -> 404).
    Co sprawdzam: wynik == [200, 404, 200].
    """
    urle = [
        "https://testowy.pl/ok",
        "https://testowy.pl/brak",
        "https://testowy.pl/ok",
    ]
    wynik = asyncio.run(zadanie_09_pobierz_wiele_statusow(klient_testowy, urle))
    assert wynik == [200, 404, 200]


def test_zadanie_09_pusta_lista_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: przypadek brzegowy — brak adresow = pusta lista statusow.
    Co udaje: internet — MockTransport (nieuzyty).
    Co sprawdzam: wynik == [].
    """
    urle = []
    wynik = asyncio.run(zadanie_09_pobierz_wiele_statusow(klient_testowy, urle))
    assert wynik == []


# --- zadanie_10 ---

def test_zadanie_10_zwraca_slownik_dla_statusu_200(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: wzorzec z requests — status 200 daje slownik z JSON-a.
    Co udaje: internet — MockTransport (/dane -> 200 + json z miastem).
    Co sprawdzam: wynik == {"miasto": "Krakow", "sprzedaz": 200}.
    """
    wynik = asyncio.run(
        zadanie_10_pobierz_json(klient_testowy, "https://testowy.pl/dane")
    )
    assert wynik == {"miasto": "Krakow", "sprzedaz": 200}


def test_zadanie_10_zwraca_none_dla_statusu_404(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: kontrakt None — status inny niz 200 daje None, nie wyjatek.
    Co udaje: internet — MockTransport (/brak -> 404).
    Co sprawdzam: wynik is None.
    """
    wynik = asyncio.run(
        zadanie_10_pobierz_json(klient_testowy, "https://testowy.pl/brak")
    )
    assert wynik is None


# --- zadanie_11 ---

def test_zadanie_11_jsony_w_kolejnosci_adresow(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy rownolegle pobieranie JSON-ow zachowuje kolejnosc.
    Co udaje: internet — MockTransport (/dane -> slownik).
    Co sprawdzam: wynik == [slownik, slownik] dla dwoch adresow /dane.
    """
    urle = [
        "https://testowy.pl/dane",
        "https://testowy.pl/dane"
    ]
    wynik = asyncio.run(
        zadanie_11_pobierz_wiele_jsonow(klient_testowy, urle)
    )
    assert wynik == [
        {"miasto": "Krakow", "sprzedaz": 200},
        {"miasto": "Krakow", "sprzedaz": 200}
    ]


def test_zadanie_11_none_na_pozycji_bledu(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy blad jednego adresu nie psuje pozostalych —
    None laduje na wlasciwej pozycji.
    Co udaje: internet — MockTransport (/dane -> 200, /brak -> 404).
    Co sprawdzam: wynik[0] to slownik, wynik[1] is None, wynik[2] to slownik.
    """
    urle = [
        "https://testowy.pl/dane",
        "https://testowy.pl/brak",
        "https://testowy.pl/dane"
    ]
    wynik = asyncio.run(
        zadanie_11_pobierz_wiele_jsonow(klient_testowy, urle)
    )
    assert isinstance(wynik[0], dict)
    assert wynik[1] is None
    assert isinstance(wynik[2], dict)


# --- zadanie_12 ---

def test_zadanie_12_wyciaga_tytul_strony(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy funkcja pobiera strone i oddaje tekst z <title>.
    Co udaje: internet — MockTransport (/strona -> HTML z tytulem
    "Testowa strona").
    Co sprawdzam: wynik == "Testowa strona".
    """
    wynik = asyncio.run(
        zadanie_12_pobierz_tytul_strony(klient_testowy, "https://testowy.pl/strona")
    )
    assert wynik == "Testowa strona"


def test_zadanie_12_zwraca_none_gdy_strona_bez_tytulu(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: kontrakt None — strona bez znacznika <title> daje None.
    Co udaje: internet — MockTransport (/pusta -> HTML bez title).
    Co sprawdzam: wynik is None.
    """
    wynik = asyncio.run(
        zadanie_12_pobierz_tytul_strony(klient_testowy, "https://testowy.pl/pusta")
    )
    assert wynik is None


# --- zadanie_13 ---

def test_zadanie_13_tytuly_wielu_stron_w_kolejnosci(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: scraping w skali — tytuly dwoch stron w kolejnosci adresow.
    Co udaje: internet — MockTransport (/strona i /strona2 z roznymi tytulami).
    Co sprawdzam: wynik == ["Testowa strona", "Druga strona"].
    """
    urle = [
        "https://testowy.pl/strona",
        "https://testowy.pl/strona2"
    ]
    wynik = asyncio.run(
        zadanie_13_pobierz_wiele_tytulow(klient_testowy, urle)
    )
    assert wynik == ["Testowa strona", "Druga strona"]


def test_zadanie_13_none_dla_strony_bez_tytulu_w_srodku(
    klient_testowy: httpx.AsyncClient,
) -> None:
    """Co testuje: czy strona bez tytulu w srodku listy daje None na swojej
    pozycji, nie psujac reszty.
    Co udaje: internet — MockTransport (/strona, /pusta, /strona2).
    Co sprawdzam: wynik == ["Testowa strona", None, "Druga strona"].
    """
    urle = [
        "https://testowy.pl/strona",
        "https://testowy.pl/pusta",
        "https://testowy.pl/strona2"
    ]
    wynik = asyncio.run(
        zadanie_13_pobierz_wiele_tytulow(klient_testowy, urle)
    )
    assert wynik == ["Testowa strona", None, "Druga strona"]
