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
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, html_sklep)
    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_html("https://www.exaple.pl/")
    assert wynik == html_sklep


def test_zadanie_01_zwraca_none_przy_bledzie_serwera(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: kontrakt None, gdy serwer odpowiada błędem 500.
    Co udaje: requests.get — zwraca FakeResponse(500, ""); jej
    raise_for_status rzuci HTTPError jak prawdziwa odpowiedź.
    Co sprawdzam: wynik is None (bez wyjątku na zewnątrz).
    """
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get udająca awarię serwera.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
                raise_for_status rzuci HTTPError.
        """
        return FakeResponse(500, "")
    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    wynik = zadanie_01_pobierz_html("https://www.exaple.pl/")
    assert wynik is None


# --- zadanie_02 ---

def test_zadanie_02_wyciaga_wszystkie_produkty(html_sklep: str) -> None:
    """Co testuje: parsowanie nazw i surowych tekstów cen.
    Co udaje: nic — HTML podaję wprost z fixture html_sklep (3 produkty).
    Co sprawdzam: 3 słowniki; pierwszy ma nazwę Klawiatura i cena_tekst
    "99,90 zł".
    """
    wynik = zadanie_02_parsuj_produkty(html_sklep)
    assert len(wynik) == 3
    assert wynik[0]["nazwa"] == "Klawiatura"
    assert wynik[0]["cena_tekst"] == "99,90 zł"


def test_zadanie_02_pusta_lista_gdy_brak_produktow() -> None:
    """Co testuje: zachowanie brzegowe dla strony bez produktów.
    Co udaje: nic — podaję własny minimalny HTML bez divów produktu.
    Co sprawdzam: wynik to pusta lista (nie None, nie wyjątek).
    """
    wynik = zadanie_02_parsuj_produkty("<html><body><p>Pusto</p></body></html>")
    assert wynik == []


# --- zadanie_03 ---

def test_zadanie_03_czysci_polska_metke() -> None:
    """Co testuje: pełne czyszczenie metki z walutą, spacjami i przecinkiem.
    Co udaje: nic — teksty podaję wprost.
    Co sprawdzam: "99,90 zł" daje 99.9, a " 1 299,00 zł " daje 1299.0.
    """
    wynik_1 = zadanie_03_wyczysc_cene("99,90 zł")
    assert wynik_1 == 99.9
    wynik_2 = zadanie_03_wyczysc_cene(" 1 299,00 zł ")
    assert wynik_2 == 1299.0


def test_zadanie_03_none_gdy_metka_nieczytelna() -> None:
    """Co testuje: kontrakt None dla tekstu niebędącego ceną.
    Co udaje: nic — tekst "brak danych" podaję wprost.
    Co sprawdzam: wynik is None (ValueError złapany w środku).
    """
    wynik = zadanie_03_wyczysc_cene("brak danych")
    assert wynik is None


# --- zadanie_04 ---

def test_zadanie_04_pomija_nieczytelne_ceny(html_sklep: str) -> None:
    """Co testuje: zebranie czystych cen z pominięciem zepsutej metki.
    Co udaje: nic — fixture html_sklep (Monitor ma "brak danych").
    Co sprawdzam: 2 wpisy; pierwszy to Klawiatura z ceną 99.9 (float).
    """
    wynik = zadanie_04_zbierz_ceny(html_sklep)
    assert len(wynik) == 2
    assert wynik[0]["nazwa"] == "Klawiatura"
    assert wynik[0]["cena"] == 99.9


def test_zadanie_04_pusta_strona_daje_pusta_liste() -> None:
    """Co testuje: zachowanie brzegowe dla strony bez produktów.
    Co udaje: nic — własny HTML bez divów produktu.
    Co sprawdzam: wynik to pusta lista.
    """
    wynik = zadanie_04_zbierz_ceny("<html><body><p>Pusto</p></body></html>")
    assert wynik == []


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
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, html_sklep)
    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    pauzy = []

    def podmieniony_sleep(sekundy: float) -> None:
        """Atrapa time.sleep zbierajaca czas miedzy kazdym wywolaniem do listy.

        Args:
            sekundy: czas pauzy miedzy kazdym wywolaniem requests.get.

        Returns:
            None.
        """
        pauzy.append(sekundy)
    monkeypatch.setattr("mini_monitor_cen.time.sleep", podmieniony_sleep)
    wynik = zadanie_05_patroluj_strony(
        ["https://www.exaple.pl/", "https://www.exaple.pl/"]
    )
    assert len(wynik) == 4
    assert len(pauzy) == 2


def test_zadanie_05_pusta_lista_adresow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Co testuje: zachowanie brzegowe — brak adresów do patrolu.
    Co udaje: requests.get i time.sleep — żadne nie powinno być użyte.
    Co sprawdzam: wynik to pusta lista.
    """
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200.
        """
        return FakeResponse(200, "")
    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    pauzy = []

    def podmieniony_sleep(sekundy: float) -> None:
        """Atrapa time.sleep zbierajaca czas miedzy kazdym wywolaniem do listy.

        Args:
            sekundy: czas pauzy miedzy kazdym wywolaniem requests.get.

        Returns:
            None.
        """
        pauzy.append(sekundy)
    monkeypatch.setattr("mini_monitor_cen.time.sleep", podmieniony_sleep)
    wynik = zadanie_05_patroluj_strony([])
    assert wynik == []
    assert pauzy == []


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
    zadanie_06_utworz_tabele(polaczenie_puste)
    assert len(polaczenie_puste.kursor.wykonane) == 1
    sql, _ = polaczenie_puste.kursor.wykonane[0]
    assert "CREATE TABLE" in sql
    assert "ceny" in sql


def test_zadanie_06_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po utworzeniu tabeli.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    zadanie_06_utworz_tabele(polaczenie_puste)
    assert polaczenie_puste.liczba_commitow == 1


# --- zadanie_07 ---

def test_zadanie_07_insert_z_parametrami(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zapis odczytu zapytaniem parametryzowanym.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: zanotowane zapytanie zawiera "INSERT" oraz "%s",
    a parametry to krotka ("Klawiatura", 99.9, "2026-07-10").
    """
    zadanie_07_zapisz_cene(polaczenie_puste, "Klawiatura", 99.9, "2026-07-10")
    sql, parametry = polaczenie_puste.kursor.wykonane[0]
    assert "INSERT" in sql
    assert "%s" in sql
    assert parametry == ("Klawiatura", 99.9, "2026-07-10")


def test_zadanie_07_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po zapisie odczytu.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    zadanie_07_zapisz_cene(polaczenie_puste, "Klawiatura", 99.9, "2026-07-10")
    assert polaczenie_puste.liczba_commitow == 1


# --- zadanie_08 ---

def test_zadanie_08_executemany_z_lista_krotek(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zapis hurtowy wielu odczytów naraz.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: w wykonane_wiele jest jeden zapis, a jego lista
    parametrów to dokładnie 2 przekazane krotki.
    """
    wpisy = [
        ("Klawiatura", 99.9, "2026-07-10"),
        ("Mysz", 49.0, "2026-07-10"),
    ]
    zadanie_08_zapisz_wiele_cen(polaczenie_puste, wpisy)
    assert len(polaczenie_puste.kursor.wykonane_wiele) == 1
    _, parametry = polaczenie_puste.kursor.wykonane_wiele[0]
    assert parametry == wpisy


def test_zadanie_08_zatwierdza_zmiane(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: commit po zapisie hurtowym.
    Co udaje: bazę — atrapa FakeConnection.
    Co sprawdzam: liczba_commitow atrapy wynosi 1.
    """
    wpisy = [
        ("Klawiatura", 99.9, "2026-07-10"),
        ("Mysz", 49.0, "2026-07-10"),
    ]
    zadanie_08_zapisz_wiele_cen(polaczenie_puste, wpisy)
    assert polaczenie_puste.liczba_commitow == 1


# --- zadanie_09 ---

def test_zadanie_09_zwraca_historie_produktu(
    polaczenie_z_historia: FakeConnection,
) -> None:
    """Co testuje: pobranie pełnej historii odczytów produktu.
    Co udaje: bazę — atrapa z zaprogramowanymi 2 wierszami historii.
    Co sprawdzam: wynik to dokładnie 2 zaprogramowane krotki, a nazwa
    poszła do zapytania jako parametr %s (nie wklejona w SQL).
    """
    wynik = zadanie_09_historia_cen(polaczenie_z_historia, "Klawiatura")
    assert wynik == polaczenie_z_historia.kursor.wiersze
    sql, parametry = polaczenie_z_historia.kursor.wykonane[0]
    assert "%s" in sql
    assert parametry == ("Klawiatura",)


def test_zadanie_09_pusta_lista_gdy_brak_historii(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zachowanie brzegowe — produkt bez żadnych odczytów.
    Co udaje: bazę — pusta atrapa (fetchall zwróci pustą listę).
    Co sprawdzam: wynik to pusta lista (nie None).
    """
    wynik = zadanie_09_historia_cen(polaczenie_puste, "Klawiatura")
    assert wynik == []


# --- zadanie_10 ---

def test_zadanie_10_zwraca_ostatnia_cene_jako_float(
    polaczenie_z_historia: FakeConnection,
) -> None:
    """Co testuje: pobranie najświeższej ceny produktu.
    Co udaje: bazę — atrapa; jej fetchone zwróci (89.9, "2026-07-01").
    Co sprawdzam: wynik == 89.9 i jest typu float.
    """
    wynik = zadanie_10_ostatnia_cena(polaczenie_z_historia, "Klawiatura")
    assert wynik == 89.9
    assert isinstance(wynik, float)


def test_zadanie_10_none_gdy_produkt_nowy(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: kontrakt None dla produktu spoza dziennika.
    Co udaje: bazę — pusta atrapa (fetchone zwróci None).
    Co sprawdzam: wynik is None (bez TypeError z fetchone[0]).
    """
    wynik = zadanie_10_ostatnia_cena(polaczenie_puste, "Klawiatura")
    assert wynik is None


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
    wynik = zadanie_11_werdykt(stara, nowa)
    assert wynik == oczekiwany


def test_zadanie_11_nowy_produkt_gdy_brak_starej_ceny() -> None:
    """Co testuje: werdykt dla produktu bez historii.
    Co udaje: nic — starą cenę podaję wprost jako None.
    Co sprawdzam: wynik == "nowy produkt".
    """
    wynik = zadanie_11_werdykt(None, 99.9)
    assert wynik == "nowy produkt"


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
    wynik = zadanie_12_zapisz_odczyt(polaczenie_puste, html_sklep, "2026-07-10")
    assert wynik == 2
    assert len(polaczenie_puste.kursor.wykonane_wiele) == 1
    _, parametry = polaczenie_puste.kursor.wykonane_wiele[0]
    assert len(parametry) == 2
    assert parametry == [("Klawiatura", 99.9, "2026-07-10"), ("Mysz", 49.0, "2026-07-10")]


def test_zadanie_12_zero_bez_dotykania_bazy(
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: zachowanie brzegowe — strona bez czytelnych cen.
    Co udaje: bazę — atrapa; HTML bez produktów podaję wprost.
    Co sprawdzam: wynik == 0, wykonane_wiele puste i zero commitów.
    """
    html = "<html><body><p>Pusto</p></body></html>"
    wynik = zadanie_12_zapisz_odczyt(polaczenie_puste, html, "2026-07-10")
    assert wynik == 0
    assert polaczenie_puste.kursor.wykonane_wiele == []
    assert polaczenie_puste.liczba_commitow == 0


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
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get zwracająca zdrową odpowiedź z fixture.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 200 i danymi z fixture.
        """
        return FakeResponse(200, html_sklep)

    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    wynik = zadanie_13_monitoruj(
        "http://www.example.pl", polaczenie_z_historia, "2026-07-10"
    )
    assert len(wynik) == 2
    assert wynik == [
        {"nazwa": "Klawiatura", "cena": 99.9, "status": "wzrost"},
        {"nazwa": "Mysz", "cena": 49.0, "status": "spadek"}
    ]


def test_zadanie_13_none_i_baza_nietknieta_gdy_siec_padla(
    monkeypatch: pytest.MonkeyPatch,
    polaczenie_puste: FakeConnection,
) -> None:
    """Co testuje: propagację kontraktu None przy awarii sieci.
    Co udaje: requests.get — atrapa z kodem 500; bazę — pusta atrapa.
    Co sprawdzam: wynik is None, a szpieg nie zanotował ŻADNEGO
    zapytania (baza nietknięta).
    """
    def podmieniony_get(
            url: str,
            headers: dict | None = None,
            timeout: int | None = None,
    ) -> FakeResponse:
        """Atrapa requests.get udająca awarię serwera.

        Args:
            url: ignorowany adres.
            headers: ignorowane parametry zapytania.
            timeout: ignorowany limit czasu.

        Returns:
            FakeResponse: atrapa z kodem 500 i pustymi danymi — jej
                raise_for_status rzuci HTTPError.
        """
        return FakeResponse(500, "")

    monkeypatch.setattr("mini_monitor_cen.requests.get", podmieniony_get)
    wynik = zadanie_13_monitoruj(
        "http://www.example.pl", polaczenie_puste, "2026-07-10"
    )
    assert wynik is None
    assert polaczenie_puste.kursor.wykonane_wiele == []
    assert polaczenie_puste.kursor.wykonane == []
