import sqlite3

# --- SPIS ZADAŃ ---
# Uwaga: w tym temacie piszesz SQL — Python (sqlite3) jest tylko nośnikiem,
# który wykonuje twoje zapytania. Każda funkcja dostaje otwarte połączenie.
#
# zadanie_01 — utwórz tabelę pracownicy (CREATE TABLE)
# zadanie_02 — wstaw trzech pracowników (INSERT INTO ... VALUES)
# zadanie_03 — pobierz wszystkie wiersze (SELECT *)
# zadanie_04 — imiona pracowników z Warszawy (WHERE)
# zadanie_05 — imiona i pensje malejąco po pensji (ORDER BY DESC)
# zadanie_06 — dwoje najlepiej opłacanych (ORDER BY + LIMIT)
# zadanie_07 — liczba wszystkich pracowników (COUNT)
# zadanie_08 — średnia pensja (AVG)
# zadanie_09 — suma pensji per miasto (GROUP BY + SUM)
# zadanie_10 — miasta z co najmniej trzema pracownikami (GROUP BY + HAVING)
# zadanie_11 — pracownicy z nazwami działów (INNER JOIN)
# zadanie_12 — wszyscy pracownicy z działami lub None (LEFT JOIN)


def zadanie_01_utworz_tabele(polaczenie: sqlite3.Connection) -> None:
    """Tworzy tabelę pracownicy o pięciu kolumnach.

    Args:
        polaczenie: otwarte połączenie z bazą (bez tabel).

    Returns:
        None
    """
    # TODO: wykonaj polaczenie.execute z zapytaniem CREATE TABLE pracownicy
    #       o kolumnach: id INTEGER PRIMARY KEY, imie TEXT, miasto TEXT,
    #       pensja INTEGER, dzial_id INTEGER
    #       (pamiętaj: bez przecinka po ostatniej kolumnie)
    pass


def zadanie_02_wstaw_pracownikow(polaczenie: sqlite3.Connection) -> None:
    """Wstawia trzech pracowników do istniejącej tabeli pracownicy.

    Args:
        polaczenie: połączenie z bazą zawierającą pustą tabelę pracownicy.

    Returns:
        None
    """
    # TODO: wykonaj polaczenie.execute z zapytaniem INSERT INTO pracownicy
    #       (id, imie, miasto, pensja, dzial_id) VALUES — trzy wiersze naraz:
    #       (1, 'Anna', 'Warszawa', 8000, 1),
    #       (2, 'Piotr', 'Krakow', 6000, 1),
    #       (3, 'Zofia', 'Warszawa', 9000, 2)
    #       (teksty w apostrofach, liczby bez)
    pass


def zadanie_03_wszyscy_pracownicy(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera wszystkie wiersze tabeli pracownicy ze wszystkimi kolumnami.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: lista krotek — jedna krotka na wiersz tabeli.
    """
    # TODO: wykonaj SELECT * FROM pracownicy
    # TODO: zwróć wynik przez .fetchall()
    pass


def zadanie_04_imiona_z_warszawy(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera imiona pracowników z Warszawy.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki jednoelementowe z imionami, w kolejności z tabeli.
    """
    # TODO: wykonaj SELECT imie FROM pracownicy z warunkiem WHERE
    #       miasto = 'Warszawa' (apostrofy! pojedyncze = !)
    # TODO: zwróć wynik przez .fetchall()
    pass


def zadanie_05_pensje_malejaco(
    polaczenie: sqlite3.Connection,
) -> list[tuple]:
    """Pobiera imiona i pensje wszystkich pracowników od najwyższej pensji.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        list[tuple]: krotki (imie, pensja) posortowane malejąco po pensji.
    """
    # TODO: wykonaj SELECT imie, pensja FROM pracownicy
    #       z sortowaniem ORDER BY pensja DESC
    # TODO: zwróć wynik przez .fetchall()
    pass


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
    # TODO: wykonaj SELECT imie, pensja FROM pracownicy
    #       ORDER BY pensja DESC LIMIT 2 (LIMIT zawsze po ORDER BY)
    # TODO: zwróć wynik przez .fetchall()
    pass


def zadanie_07_liczba_pracownikow(polaczenie: sqlite3.Connection) -> int:
    """Liczy wszystkich pracowników w tabeli.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        int: liczba wierszy tabeli pracownicy.
    """
    # TODO: wykonaj SELECT COUNT(*) FROM pracownicy
    # TODO: zwróć wartość przez .fetchone()[0]
    #       ([0] — bo fetchone daje krotkę, nawet jednoelementową)
    pass


def zadanie_08_srednia_pensja(polaczenie: sqlite3.Connection) -> float:
    """Liczy średnią pensję wszystkich pracowników.

    Args:
        polaczenie: połączenie z bazą wypełnioną danymi.

    Returns:
        float: średnia wartość kolumny pensja.
    """
    # TODO: wykonaj SELECT AVG(pensja) FROM pracownicy
    # TODO: zwróć wartość przez .fetchone()[0]
    pass


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
    # TODO: wykonaj SELECT miasto, SUM(pensja) FROM pracownicy
    #       z grupowaniem GROUP BY miasto i sortowaniem ORDER BY miasto
    # TODO: zwróć wynik przez .fetchall()
    pass


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
    # TODO: wykonaj SELECT miasto, COUNT(*) FROM pracownicy
    #       GROUP BY miasto z filtrem grup HAVING COUNT(*) >= 3
    #       (HAVING, nie WHERE — filtrujemy PO agregacji)
    # TODO: zwróć wynik przez .fetchall()
    pass


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
    # TODO: wykonaj SELECT pracownicy.imie, dzialy.nazwa FROM pracownicy
    #       INNER JOIN dzialy ON pracownicy.dzial_id = dzialy.id
    # TODO: zwróć wynik przez .fetchall()
    pass


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
    # TODO: wykonaj SELECT pracownicy.imie, dzialy.nazwa FROM pracownicy
    #       LEFT JOIN dzialy ON pracownicy.dzial_id = dzialy.id
    #       (LEFT — cała lewa tabela zostaje, braki jako NULL)
    # TODO: zwróć wynik przez .fetchall()
    pass
