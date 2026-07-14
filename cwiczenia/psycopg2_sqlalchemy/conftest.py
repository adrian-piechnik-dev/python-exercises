import os
import sys
from pathlib import Path
from typing import Any, Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeCursor:
    """Atrapa-szpieg kursora psycopg2 — zapisuje zapytania zamiast je wykonywać.

    Args:
        wiersze: lista krotek, które atrapa uda przy fetchall/fetchone.
    """

    def __init__(self, wiersze: list[tuple]) -> None:
        """Przygotowuje szpiega z zaprogramowanymi wierszami do zwrotu.

        Args:
            wiersze: dane udawane przy odczycie.

        Returns:
            None
        """
        self.wiersze = wiersze
        self.wykonane = []
        self.wykonane_wiele = []

    def execute(self, sql: str, parametry: Optional[tuple] = None) -> None:
        """Zapisuje zapytanie i parametry zamiast wysyłać je do bazy.

        Args:
            sql: tekst zapytania SQL.
            parametry: krotka wartości dla zaślepek %s (lub None).

        Returns:
            None
        """
        self.wykonane.append((sql, parametry))

    def executemany(self, sql: str, lista_parametrow: list[tuple]) -> None:
        """Zapisuje zapytanie hurtowe i listę krotek zamiast je wykonywać.

        Args:
            sql: tekst zapytania SQL z zaślepkami %s.
            lista_parametrow: lista krotek wartości.

        Returns:
            None
        """
        self.wykonane_wiele.append((sql, lista_parametrow))

    def fetchall(self) -> list[tuple]:
        """Zwraca zaprogramowane wiersze — jak fetchall prawdziwego kursora.

        Args:
            Brak.

        Returns:
            list[tuple]: wiersze przekazane przy tworzeniu atrapy.
        """
        return self.wiersze

    def fetchone(self) -> Optional[tuple]:
        """Zwraca pierwszy zaprogramowany wiersz lub None, gdy brak wierszy.

        Args:
            Brak.

        Returns:
            Optional[tuple]: pierwszy wiersz albo None.
        """
        if self.wiersze == []:
            return None
        return self.wiersze[0]

    def __enter__(self) -> "FakeCursor":
        """Wspiera blok with — zwraca samego siebie (trafia za "as").

        Args:
            Brak.

        Returns:
            FakeCursor: ta sama atrapa.
        """
        return self

    def __exit__(self, typ: Any, wartosc: Any, slad: Any) -> None:
        """Wspiera wyjście z bloku with — nie połyka wyjątków.

        Args:
            typ: klasa ewentualnego wyjątku (lub None).
            wartosc: egzemplarz wyjątku (lub None).
            slad: ślad stosu (lub None).

        Returns:
            None
        """
        return None


class FakeConnection:
    """Atrapa połączenia psycopg2 — wydaje FakeCursor i zlicza commity.

    Args:
        wiersze: dane, które kursor-szpieg uda przy odczycie
            (domyślnie brak wierszy).
    """

    def __init__(self, wiersze: Optional[list[tuple]] = None) -> None:
        """Tworzy połączenie-atrapę z jednym kursorem-szpiegiem.

        Args:
            wiersze: wiersze do udawania przy fetch (None = pusta lista).

        Returns:
            None
        """
        if wiersze is None:
            wiersze = []
        self.kursor = FakeCursor(wiersze)
        self.liczba_commitow = 0

    def cursor(self) -> FakeCursor:
        """Zwraca kursor-szpiega — jak cursor() prawdziwego połączenia.

        Args:
            Brak.

        Returns:
            FakeCursor: współdzielona atrapa kursora.
        """
        return self.kursor

    def commit(self) -> None:
        """Zlicza wywołania commit zamiast zatwierdzać transakcję.

        Args:
            Brak.

        Returns:
            None
        """
        self.liczba_commitow += 1


@pytest.fixture
def silnik_sqlite(tmp_path: Path) -> Engine:
    """Prawdziwy engine SQLAlchemy na pliku sqlite w folderze tymczasowym.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Engine: silnik wskazujący świeżą, pustą bazę sqlite w pliku.
    """
    adres = f"sqlite:///{tmp_path / 'test.db'}"
    return create_engine(adres)
