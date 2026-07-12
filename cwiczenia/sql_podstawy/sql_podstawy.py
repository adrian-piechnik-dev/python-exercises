import sqlite3


def zadanie_01_utworz_tabele(polaczenie: sqlite3.Connection) -> None:
    """Tworzy tabelę pracownicy o pięciu kolumnach.

    Args:
        polaczenie: otwarte połączenie z bazą (bez tabel).

    Returns:
        None
    """
    polaczenie.execute(
        """
        CREATE TABLE pracownicy (
            id INTEGER PRIMARY KEY,
            imie TEXT,
            miasto TEXT,
            pensja INTEGER,
            dzial_id INTEGER
        )
        """
    )


def zadanie_02_wstaw_pracownikow(polaczenie: sqlite3.Connection) -> None:
    """Wstawia trzech pracowników do istniejącej tabeli pracownicy.

    Args:
        polaczenie: połączenie z bazą zawierającą pustą tabelę pracownicy.

    Returns:
        None
    """
    polaczenie.execute(
        """
        INSERT INTO pracownicy
        (id, imie, miasto, pensja, dzial_id) VALUES
        (1, 'Anna', 'Warszawa', 8000, 1),
        (2, 'Piotr', 'Krakow', 6000, 1),
        (3, 'Zofia', 'Warszawa', 9000, 2)
        """
    )


def zadanie_03_wszyscy_pracownicy(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera wszystkie wiersze tabeli pracownicy ze wszystkimi kolumnami.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: lista krotek — jedna krotka na wiersz tabeli.
    """
    return polaczenie.execute("SELECT * FROM pracownicy").fetchall()


def zadanie_04_imiona_z_warszawy(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera imiona pracowników z Warszawy.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki jednoelementowe z imionami, w kolejności z tabeli.
    """
    return polaczenie.execute(
        "SELECT imie FROM pracownicy WHERE miasto = 'Warszawa'"
    ).fetchall()


def zadanie_05_pensje_malejaco(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera imiona i pensje wszystkich pracowników od najwyższej pensji.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki (imie, pensja) posortowane malejąco po pensji.
    """
    return polaczenie.execute(
        "SELECT imie, pensja FROM pracownicy ORDER BY pensja DESC"
    ).fetchall()


def zadanie_06_najlepiej_oplacani(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera dwoje najlepiej opłacanych pracowników (imię i pensja).

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: dokładnie 2 krotki (imie, pensja) — najwyższe pensje
            na początku.
    """
    return polaczenie.execute(
        "SELECT imie, pensja FROM pracownicy ORDER BY pensja DESC LIMIT 2"
    ).fetchall()


def zadanie_07_liczba_pracownikow(polaczenie: sqlite3.Connection) -> int:
    """Liczy wszystkich pracowników w tabeli.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        int: liczba wierszy tabeli pracownicy.
    """
    return polaczenie.execute(
        "SELECT COUNT(*) FROM pracownicy"
    ).fetchone()[0]


def zadanie_08_srednia_pensja(polaczenie: sqlite3.Connection) -> float:
    """Liczy średnią pensję wszystkich pracowników.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        float: średnia wartość kolumny pensja.
    """
    return polaczenie.execute("SELECT AVG(pensja) FROM pracownicy").fetchone()[0]


def zadanie_09_suma_pensji_po_miescie(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Liczy sumę pensji w każdym mieście, posortowaną alfabetycznie po mieście.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki (miasto, suma_pensji) po jednej na miasto,
            w kolejności alfabetycznej miast.
    """
    return polaczenie.execute(
        "SELECT miasto, SUM(pensja) FROM pracownicy GROUP BY miasto ORDER BY miasto"
    ).fetchall()


def zadanie_10_miasta_z_trojka(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Znajduje miasta zatrudniające co najmniej trzech pracowników.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki (miasto, liczba_pracownikow) tylko dla miast
            z co najmniej 3 pracownikami.
    """
    return polaczenie.execute(
        "SELECT miasto, COUNT(*) FROM pracownicy GROUP BY miasto HAVING COUNT(*) >= 3"
    ).fetchall()


def zadanie_11_pracownicy_z_dzialami(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Łączy pracowników z nazwami ich działów — tylko przypisani do działu.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi (pracownicy + dzialy).

    Returns:
        list[tuple]: krotki (imie, nazwa_dzialu); pracownicy bez działu
            (dzial_id NULL) nie pojawiają się w wyniku.
    """
    return polaczenie.execute(
        """
        SELECT pracownicy.imie, dzialy.nazwa
        FROM pracownicy INNER JOIN dzialy ON pracownicy.dzial_id = dzialy.id
        """
    ).fetchall()


def zadanie_12_wszyscy_z_dzialami(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Łączy WSZYSTKICH pracowników z nazwami działów; brak działu daje None.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi (pracownicy + dzialy).

    Returns:
        list[tuple]: krotki (imie, nazwa_dzialu lub None) — po jednej
            dla każdego pracownika, także nieprzypisanego do działu.
    """
    return polaczenie.execute(
        """
        SELECT pracownicy.imie, dzialy.nazwa
        FROM pracownicy
        LEFT JOIN dzialy ON pracownicy.dzial_id = dzialy.id
        """
    ).fetchall()
