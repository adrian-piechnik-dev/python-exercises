import pytest

from conftest import FakeConnection, FakeResponse
from mini_monitor_cen import (
    zadanie_01_pobierz_html,
    zadanie_02_parsuj_produkty,
    zadanie_03_wyczysc_cene,
    zadanie_04_zbierz_ceny,
    zadanie_05_patroluj_strony,
    zadanie_06_utworz_tabele,
    zadanie_07_zapisz_cene,
    zadanie_08_zapisz_wiele_cen,
    zadanie_09_historia_cen,
    zadanie_10_ostatnia_cena,
    zadanie_11_werdykt,
    zadanie_12_zapisz_odczyt,
    zadanie_13_monitoruj,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_html_strony(
    monkeypatch: pytest.MonkeyPatch, html_sklep: str,
) -> None:
    """Co testuje: pobranie treści strony przy zdrowym serwerze.
    Co udaje: requests.get w module tematu — zwraca FakeResponse(200,
    html_sklep).
    Co sprawdzam: wynik to dokładnie HTML z atrapy.
    """
    # TODO: przygotuj podmienioną funkcję zwracającą atrapę z kodem 200
    #       i HTML-em z fixture (podmiana requests.get W MODULE
    #       mini_monitor_cen — wzorzec z tematów 11-12; pamiętaj, że
    #       prawdziwe wywołanie dostaje url, headers i timeout)
    # TODO: wywołaj testowaną funkcję z dowolnym adresem
    # TODO: sprawdź, że wynik równa się HTML-owi z fixture
    pass


def test_zadanie_01_zwraca_none_przy_bledzie_serwera(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None, gdy serwer odpowiada błędem 500.
    Co udaje: requests.get — zwraca FakeResponse(500, ""); jej
    raise_for_status rzuci HTTPError jak prawdziwa odpowiedź.
    Co sprawdzam: wynik is None (bez wyjątku na zewnątrz).
    """
    # TODO: przygotuj podmienioną funkcję zwracającą atrapę z kodem 500
    # TODO: podmień requests.get w module tematu i wywołaj funkcję
    # TODO: sprawdź kontrakt None
    pass


# --- zadanie_02 ---

def test_zadanie_02_wyciaga_wszystkie_produkty(html_sklep: str) -> None:
    """Co testuje: parsowanie nazw i surowych tekstów cen.
    Co udaje: nic — HTML podaję wprost z fixture html_sklep (3 produkty).
    Co sprawdzam: 3 słowniki; pierwszy ma nazwę Klawiatura i cena_tekst
    "99,90 zł".
    """
    # TODO: wywołaj testowaną funkcję na fixture
    # TODO: sprawdź liczbę produktów oraz oba pola pierwszego słownika
    pass


def test_zadanie_02_pusta_lista_gdy_brak_produktow() -> None:
    """Co testuje: zachowanie brzegowe dla strony bez produktów.
    Co udaje: nic — podaję własny minimalny HTML bez divów produktu.
    Co sprawdzam: wynik to pusta lista (nie None, nie wyjątek).
    """
    # TODO: przygotuj html = "<html><body><p>Pusto</p></body></html>"
    # TODO: wywołaj testowaną funkcję i sprawdź wynik
    pass


# --- zadanie_03 ---

def test_zadanie_03_czysci_polska_metke() -> None:
    """Co testuje: pełne czyszczenie metki z walutą, spacjami i przecinkiem.
    Co udaje: nic — teksty podaję wprost.
    Co sprawdzam: "99,90 zł" daje 99.9, a " 1 299,00 zł " daje 1299.0.
    """
    # TODO: wywołaj testowaną funkcję dla obu tekstów z docstringa
    # TODO: sprawdź oba wyniki
    pass


def test_zadanie_03_none_gdy_metka_nieczytelna() -> None:
    """Co testuje: kontrakt None dla tekstu niebędącego ceną.
    Co udaje: nic — tekst "brak danych" podaję wprost.
    Co sprawdzam: wynik is None (ValueError złapany w środku).
    """
    # TODO: wywołaj testowaną funkcję z tekstem "brak danych"
    # TODO: sprawdź kontrakt None
    pass


# --- zadanie_04 ---

def test_zadanie_04_pomija_nieczytelne_ceny(html_sklep: str) -> None:
    """Co testuje: zebranie czystych cen z pominięciem zepsutej metki.
    Co udaje: nic — fixture html_sklep (Monitor ma "brak danych").
    Co sprawdzam: 2 wpisy; pierwszy to Klawiatura z ceną 99.9 (float).
    """
    # TODO: wywołaj testowaną funkcję na fixture
    # TODO: sprawdź liczbę wpisów oraz nazwę i cenę pierwszego
    pass


def test_zadanie_04_pusta_strona_daje_pusta_liste() -> None:
    """Co testuje: zachowanie brzegowe dla strony bez produktów.
    Co udaje: nic — własny HTML bez divów produktu.
    Co sprawdzam: wynik to pusta lista.
    """
    # TODO: przygotuj minimalny HTML bez produktów
    # TODO: wywołaj testowaną funkcję i sprawdź wynik
    pass


# --- zadanie_05 ---

def test_zadanie_05_zbiera_ceny_z_wielu_stron_z_pauza(
    monkeypatch: pytest.MonkeyPatch, html_sklep: str,
) -> None:
    """Co testuje: patrol po 2 stronach — sklejanie wyników i pauzy.
    Co udaje: requests.get (atrapa 200 z html_sklep dla każdej strony)
    ORAZ time.sleep w module tematu (licznik zamiast czekania — test
    nie może trwać sekund).
    Co sprawdzam: 4 wpisy (2 strony po 2 czytelne ceny) i sleep
    wywołany 2 razy.
    """
    # TODO: przygotuj podmieniony get (atrapa 200 z fixture) oraz
    #       podmieniony sleep dopisujący sekundy do listy-licznika
    #       (wzorzec szpiega z teorii, sekcja 6)
    # TODO: podmień OBIE rzeczy w module mini_monitor_cen
    # TODO: wywołaj testowaną funkcję z listą 2 adresów
    # TODO: sprawdź długość wyniku i liczbę zanotowanych pauz
    pass


def test_zadanie_05_pusta_lista_adresow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: zachowanie brzegowe — brak adresów do patrolu.
    Co udaje: requests.get i time.sleep — żadne nie powinno być użyte.
    Co sprawdzam: wynik to pusta lista.
    """
    # TODO: podmień get i sleep dowolnymi atrapami
    # TODO: wywołaj testowaną funkcję z pustą listą i sprawdź wynik
    pass


# --- zadanie_06 ---

def test_zadanie_06_wykonuje_create_table(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: czy funkcja zleca utworzenie tabeli ceny.
    Co udaje: bazę — atrapa FakeConnection podana argumentem (nic
    nie podmieniam monkeypatchem).
    Co sprawdzam: w notatkach szpiega (kursor.wykonane) jest jedno
    zapytanie zawierające "CREATE TABLE" i "ceny".
    """
    # TODO: wywołaj testowaną funkcję z atrapą z fixture
    # TODO: zajrzyj w polaczenie_puste.kursor.wykonane — sprawdź liczbę
    #       zapisów i treść zapytania (operator in działa na stringach)
    pass


def test_zadanie_06_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po utworzeniu tabeli.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    # TODO: wywołaj testowaną funkcję z atrapą
    # TODO: sprawdź licznik commitów
    pass


# --- zadanie_07 ---

def test_zadanie_07_insert_z_parametrami(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zapis odczytu zapytaniem parametryzowanym.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: zanotowane zapytanie zawiera "INSERT" oraz "%s",
    a parametry to krotka ("Klawiatura", 99.9, "2026-07-10").
    """
    # TODO: wywołaj testowaną funkcję z atrapą i danymi z docstringa
    # TODO: rozpakuj zanotowaną krotkę (sql, parametry) z wykonane
    # TODO: sprawdź treść zapytania i krotkę parametrów
    pass


def test_zadanie_07_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po zapisie odczytu.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    # TODO: wywołaj testowaną funkcję z atrapą i dowolnymi danymi
    # TODO: sprawdź licznik commitów
    pass


# --- zadanie_08 ---

def test_zadanie_08_executemany_z_lista_krotek(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zapis hurtowy wielu odczytów naraz.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: w wykonane_wiele jest jeden zapis, a jego lista
    parametrów to dokładnie 2 przekazane krotki.
    """
    # TODO: przygotuj listę 2 krotek (nazwa, cena, data_odczytu)
    # TODO: wywołaj testowaną funkcję z atrapą
    # TODO: zajrzyj w kursor.wykonane_wiele i sprawdź zapis
    pass


def test_zadanie_08_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po zapisie hurtowym.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    # TODO: wywołaj testowaną funkcję z atrapą i listą 1 krotki
    # TODO: sprawdź licznik commitów
    pass


# --- zadanie_09 ---

def test_zadanie_09_zwraca_historie_produktu(
    polaczenie_z_historia: FakeConnection,
) -> None:
    """Co testuje: pobranie pełnej historii odczytów produktu.
    Co udaje: bazę — atrapa z zaprogramowanymi 2 wierszami historii.
    Co sprawdzam: wynik to dokładnie 2 zaprogramowane krotki, a nazwa
    poszła do zapytania jako parametr %s (nie wklejona w SQL).
    """
    # TODO: wywołaj testowaną funkcję z atrapą i nazwą "Klawiatura"
    # TODO: sprawdź, że wynik to 2 krotki z fixture
    # TODO: rozpakuj zanotowane zapytanie i sprawdź: "%s" w SQL,
    #       parametry == ("Klawiatura",)
    pass


def test_zadanie_09_pusta_lista_gdy_brak_historii(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zachowanie brzegowe — produkt bez żadnych odczytów.
    Co udaje: bazę — pusta atrapa (fetchall zwróci pustą listę).
    Co sprawdzam: wynik to pusta lista (nie None).
    """
    # TODO: wywołaj testowaną funkcję z pustą atrapą
    # TODO: sprawdź, że wynik to dokładnie pusta lista
    pass


# --- zadanie_10 ---

def test_zadanie_10_zwraca_ostatnia_cene_jako_float(
    polaczenie_z_historia: FakeConnection,
) -> None:
    """Co testuje: pobranie najświeższej ceny produktu.
    Co udaje: bazę — atrapa; jej fetchone zwróci (89.9, "2026-07-01").
    Co sprawdzam: wynik == 89.9 i jest typu float.
    """
    # TODO: wywołaj testowaną funkcję z atrapą i dowolną nazwą
    # TODO: sprawdź wartość oraz typ wyniku (isinstance)
    pass


def test_zadanie_10_none_gdy_produkt_nowy(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: kontrakt None dla produktu spoza dziennika.
    Co udaje: bazę — pusta atrapa (fetchone zwróci None).
    Co sprawdzam: wynik is None (bez TypeError z fetchone[0]).
    """
    # TODO: wywołaj testowaną funkcję z pustą atrapą
    # TODO: sprawdź kontrakt None
    pass


# --- zadanie_11 ---

@pytest.mark.parametrize(
    "stara, nowa, oczekiwany",
    [
        (99.9, 105.0, "wzrost"),
        (99.9, 89.9, "spadek"),
        (99.9, 99.9, "bez zmian"),
    ],
)
def test_zadanie_11_werdykt_dla_znanych_cen(
    stara: float, nowa: float, oczekiwany: str,
) -> None:
    """Co testuje: werdykt dla trzech układów cen (zazębienie: temat 13 —
    parametrize przebiega tym testem trzykrotnie, raz na zestaw).
    Co udaje: nic — liczby podaje dekorator.
    Co sprawdzam: wynik równa się oczekiwanemu statusowi z zestawu.
    """
    # TODO: wywołaj testowaną funkcję z parametrami stara i nowa
    # TODO: porównaj wynik z parametrem oczekiwany
    pass


def test_zadanie_11_nowy_produkt_gdy_brak_starej_ceny() -> None:
    """Co testuje: werdykt dla produktu bez historii.
    Co udaje: nic — starą cenę podaję wprost jako None.
    Co sprawdzam: wynik == "nowy produkt".
    """
    # TODO: wywołaj testowaną funkcję ze starą ceną None i dowolną nową
    # TODO: sprawdź werdykt
    pass


# --- zadanie_12 ---

def test_zadanie_12_zapisuje_czytelne_ceny_hurtem(
    polaczenie_puste: FakeConnection, html_sklep: str,
) -> None:
    """Co testuje: dyrygenta zapisu — z HTML prosto do bazy.
    Co udaje: bazę — atrapa FakeConnection (HTML jest prawdziwy,
    z fixture; Monitor odpada przy czyszczeniu).
    Co sprawdzam: wynik == 2, a w wykonane_wiele wylądowały dokładnie
    2 krotki z datą "2026-07-10".
    """
    # TODO: wywołaj testowaną funkcję z atrapą, fixture i datą
    #       "2026-07-10"
    # TODO: sprawdź zwróconą liczbę
    # TODO: zajrzyj w wykonane_wiele — sprawdź liczbę krotek w zapisie
    pass


def test_zadanie_12_zero_bez_dotykania_bazy(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zachowanie brzegowe — strona bez czytelnych cen.
    Co udaje: bazę — atrapa; HTML bez produktów podaję wprost.
    Co sprawdzam: wynik == 0, wykonane_wiele puste i zero commitów.
    """
    # TODO: przygotuj minimalny HTML bez produktów
    # TODO: wywołaj testowaną funkcję z atrapą
    # TODO: sprawdź wynik, pustkę w wykonane_wiele i licznik commitów
    pass


# --- zadanie_13 ---

def test_zadanie_13_melduje_statusy_produktow(
    monkeypatch: pytest.MonkeyPatch,
    polaczenie_z_historia: FakeConnection,
    html_sklep: str,
) -> None:
    """Co testuje: pełny pipeline — patrol, porównanie, zapis, meldunek.
    Co udaje: requests.get (atrapa 200 z html_sklep) i bazę (atrapa
    z historią — każdy produkt dostanie starą cenę 89.9).
    Co sprawdzam: meldunek ma 2 wpisy; Klawiatura (99.9) ma status
    "wzrost", Mysz (49.0) ma status "spadek".
    """
    # TODO: podmień requests.get w module tematu atrapą z fixture
    # TODO: wywołaj testowaną funkcję z atrapą bazy i datą "2026-07-10"
    # TODO: sprawdź długość meldunku oraz statusy obu wpisów
    pass


def test_zadanie_13_none_i_baza_nietknieta_gdy_siec_padla(
    monkeypatch: pytest.MonkeyPatch,
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: propagację kontraktu None przy awarii sieci.
    Co udaje: requests.get — atrapa z kodem 500; bazę — pusta atrapa.
    Co sprawdzam: wynik is None, a szpieg nie zanotował ŻADNEGO
    zapytania (baza nietknięta).
    """
    # TODO: podmień requests.get atrapą z kodem 500
    # TODO: wywołaj testowaną funkcję
    # TODO: sprawdź kontrakt None oraz pustkę w wykonane
    #       i wykonane_wiele
    pass
