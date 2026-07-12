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
        # TODO: zapisz wiersze w atrybucie self.wiersze
        # TODO: utwórz pustą listę self.wykonane (zapisy execute)
        # TODO: utwórz pustą listę self.wykonane_wiele (zapisy executemany)
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
        # TODO: dopisz krotkę (sql, parametry) do self.wykonane
        self.wykonane.append((sql, parametry))

    def executemany(self, sql: str, lista_parametrow: list[tuple]) -> None:
        """Zapisuje zapytanie hurtowe i listę krotek zamiast je wykonywać.

        Args:
            sql: tekst zapytania SQL z zaślepkami %s.
            lista_parametrow: lista krotek wartości.

        Returns:
            None
        """
        # TODO: dopisz krotkę (sql, lista_parametrow) do self.wykonane_wiele
        self.wykonane_wiele.append((sql, lista_parametrow))

    def fetchall(self) -> list[tuple]:
        """Zwraca zaprogramowane wiersze — jak fetchall prawdziwego kursora.

        Args:
            Brak.

        Returns:
            list[tuple]: wiersze przekazane przy tworzeniu atrapy.
        """
        # TODO: zwróć self.wiersze
        return self.wiersze

    def fetchone(self) -> Optional[tuple]:
        """Zwraca pierwszy zaprogramowany wiersz lub None, gdy brak wierszy.

        Args:
            Brak.

        Returns:
            Optional[tuple]: pierwszy wiersz albo None.
        """
        # TODO: jeśli self.wiersze jest puste — return None
        # TODO: w przeciwnym razie zwróć self.wiersze[0]
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
        # TODO: return self
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
        # TODO: return None
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
        # TODO: jeśli wiersze is None — użyj pustej listy
        # TODO: utwórz self.kursor = FakeCursor(wiersze)
        #       (jeden współdzielony kursor, żeby test mógł zajrzeć w zapisy)
        # TODO: utwórz licznik self.liczba_commitow = 0
        pass

    def cursor(self) -> FakeCursor:
        """Zwraca kursor-szpiega — jak cursor() prawdziwego połączenia.

        Args:
            Brak.

        Returns:
            FakeCursor: współdzielona atrapa kursora.
        """
        # TODO: return self.kursor
        pass

    def commit(self) -> None:
        """Zlicza wywołania commit zamiast zatwierdzać transakcję.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: zwiększ self.liczba_commitow o 1
        pass


@pytest.fixture
def silnik_sqlite(tmp_path: Path) -> Engine:
    """Prawdziwy engine SQLAlchemy na pliku sqlite w folderze tymczasowym.

    Args:
        tmp_path: wstrzykiwany przez pytest katalog tymczasowy.

    Returns:
        Engine: silnik wskazujący świeżą, pustą bazę sqlite w pliku.
    """
    # TODO: zbuduj adres = f"sqlite:///{tmp_path / 'test.db'}"
    #       (trzy ukośniki — plik lokalny)
    # TODO: return create_engine(adres)
    pass
