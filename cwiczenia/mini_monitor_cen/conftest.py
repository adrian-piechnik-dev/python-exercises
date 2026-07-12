# UWAGA (reguły mini-projektu M3): ten conftest dostajesz GOTOWY, bez TODO.
# Atrapy FakeResponse (temat 12) i FakeCursor/FakeConnection (temat 15)
# budowałeś już sam — tu są wypełnione, żebyś pisał logikę i asserty,
# nie infrastrukturę. Przeczytaj całość uważnie: w testach będziesz
# zaglądać w notatki szpiega (wykonane, wykonane_wiele, liczba_commitow).

import os
import sys
from typing import Any, Optional

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeResponse:
    """Atrapa odpowiedzi HTTP z HTML-em — udaje obiekt z requests.get.

    Args:
        status_code: kod statusu, który atrapa ma udawać (np. 200, 500).
        text: string z HTML-em udostępniany w atrybucie text.
    """

    def __init__(self, status_code: int, text: str) -> None:
        """Zapamiętuje kod statusu i HTML do udawania.

        Args:
            status_code: kod statusu HTTP.
            text: surowy HTML strony.

        Returns:
            None
        """
        self.status_code = status_code
        self.text = text

    def raise_for_status(self) -> None:
        """Rzuca requests.HTTPError przy kodach 4xx/5xx — jak prawdziwa odpowiedź.

        Args:
            Brak.

        Returns:
            None
        """
        if self.status_code >= 400:
            raise requests.HTTPError(f"kod {self.status_code}")


class FakeCursor:
    """Atrapa-szpieg kursora — notuje zapytania zamiast je wykonywać.

    Args:
        wiersze: lista krotek udawanych przy fetchall/fetchone.
    """

    def __init__(self, wiersze: list[tuple]) -> None:
        """Przygotowuje szpiega z zaprogramowanymi wierszami do zwrotu.

        Args:
            wiersze: dane udawane przy odczycie.

        Returns:
            None
        """
        self.wiersze = wiersze
        self.wykonane: list[tuple] = []
        self.wykonane_wiele: list[tuple] = []

    def execute(self, sql: str, parametry: Optional[tuple] = None) -> None:
        """Notuje zapytanie i parametry zamiast wysyłać je do bazy.

        Args:
            sql: tekst zapytania SQL.
            parametry: krotka wartości dla zaślepek %s (lub None).

        Returns:
            None
        """
        self.wykonane.append((sql, parametry))

    def executemany(self, sql: str, lista_parametrow: list[tuple]) -> None:
        """Notuje zapytanie hurtowe i listę krotek zamiast je wykonywać.

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
        if not self.wiersze:
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
    """Atrapa połączenia — wydaje wspólny FakeCursor i zlicza commity.

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
def html_sklep() -> str:
    """HTML strony sklepu z trzema produktami — jeden z nieczytelną ceną.

    Args:
        Brak.

    Returns:
        str: strona z divami klasy "produkt"; Klawiatura "99,90 zł",
            Mysz "49,00 zł", Monitor "brak danych" (odpada przy
            czyszczeniu ceny).
    """
    return """
    <html>
      <body>
        <div class="produkt">
          <span class="nazwa">Klawiatura</span>
          <span class="cena">99,90 zł</span>
        </div>
        <div class="produkt">
          <span class="nazwa">Mysz</span>
          <span class="cena">49,00 zł</span>
        </div>
        <div class="produkt">
          <span class="nazwa">Monitor</span>
          <span class="cena">brak danych</span>
        </div>
      </body>
    </html>
    """


@pytest.fixture
def polaczenie_puste() -> FakeConnection:
    """Połączenie-atrapa bez żadnych wierszy (fetchone zwróci None).

    Args:
        Brak.

    Returns:
        FakeConnection: świeża atrapa do testów zapisu i pustej historii.
    """
    return FakeConnection()


@pytest.fixture
def polaczenie_z_historia() -> FakeConnection:
    """Połączenie-atrapa z zaprogramowaną historią odczytów.

    Args:
        Brak.

    Returns:
        FakeConnection: kursor uda wiersze [(89.9, "2026-07-01"),
            (99.9, "2026-07-08")]; fetchone zwróci pierwszy z nich,
            czyli (89.9, "2026-07-01").
    """
    return FakeConnection(wiersze=[(89.9, "2026-07-01"), (99.9, "2026-07-08")])
