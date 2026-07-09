import sys
import os
import sqlite3
from typing import Iterator

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def pusta_baza() -> Iterator[sqlite3.Connection]:
    """Całkowicie pusta baza w pamięci — do testów CREATE TABLE (zadanie 1).

    Args:
        Brak.

    Returns:
        Iterator[sqlite3.Connection]: otwarte połączenie z ulotną bazą;
            zamykane automatycznie po teście (fixture z yield).
    """
    # TODO: utwórz polaczenie = sqlite3.connect(":memory:")
    # TODO: yield polaczenie
    # TODO: po yield — polaczenie.close() (sprzątanie po teście)
    pass


@pytest.fixture
def baza_z_tabela() -> Iterator[sqlite3.Connection]:
    """Baza w pamięci z pustą tabelą pracownicy — do testów INSERT (zadanie 2).

    Args:
        Brak.

    Returns:
        Iterator[sqlite3.Connection]: połączenie z bazą zawierającą pustą
            tabelę pracownicy (id, imie, miasto, pensja, dzial_id).
    """
    # TODO: utwórz polaczenie = sqlite3.connect(":memory:")
    # TODO: wykonaj polaczenie.execute z zapytaniem:
    #       CREATE TABLE pracownicy (
    #           id INTEGER PRIMARY KEY,
    #           imie TEXT,
    #           miasto TEXT,
    #           pensja INTEGER,
    #           dzial_id INTEGER
    #       )
    # TODO: yield polaczenie
    # TODO: po yield — polaczenie.close()
    pass


@pytest.fixture
def baza_z_danymi() -> Iterator[sqlite3.Connection]:
    """Baza w pamięci z tabelami pracownicy i dzialy oraz danymi —
    do testów SELECT/GROUP BY/JOIN (zadania 3-12).

    Args:
        Brak.

    Returns:
        Iterator[sqlite3.Connection]: połączenie z bazą zawierającą:
            dzialy: (1, 'IT'), (2, 'HR');
            pracownicy: Anna/Warszawa/8000/IT, Piotr/Krakow/6000/IT,
            Zofia/Warszawa/9000/HR, Marek/Krakow/5500/bez działu (NULL),
            Ewa/Warszawa/7000/IT.
    """
    # TODO: utwórz polaczenie = sqlite3.connect(":memory:")
    # TODO: wykonaj CREATE TABLE dzialy (id INTEGER PRIMARY KEY, nazwa TEXT)
    # TODO: wykonaj CREATE TABLE pracownicy (
    #           id INTEGER PRIMARY KEY,
    #           imie TEXT,
    #           miasto TEXT,
    #           pensja INTEGER,
    #           dzial_id INTEGER
    #       )
    # TODO: wykonaj INSERT INTO dzialy (id, nazwa) VALUES
    #           (1, 'IT'), (2, 'HR')
    # TODO: wykonaj INSERT INTO pracownicy
    #           (id, imie, miasto, pensja, dzial_id) VALUES
    #           (1, 'Anna', 'Warszawa', 8000, 1),
    #           (2, 'Piotr', 'Krakow', 6000, 1),
    #           (3, 'Zofia', 'Warszawa', 9000, 2),
    #           (4, 'Marek', 'Krakow', 5500, NULL),
    #           (5, 'Ewa', 'Warszawa', 7000, 1)
    # TODO: yield polaczenie
    # TODO: po yield — polaczenie.close()
    pass
