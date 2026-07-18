import sys
import os
from pathlib import Path
from typing import Optional

from selenium.common.exceptions import NoAlertPresentException

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeAlert:
    """Atrapa alertu JavaScript — udaje okienko i zlicza decyzje robota.

    Args:
        tekst: treść komunikatu, którą alert ma udawać (atrybut .text).
    """

    def __init__(self, tekst: str = "") -> None:
        """Przygotowuje alert-szpiega z zadaną treścią.

        Args:
            tekst: wartość udawana przez atrybut .text.

        Returns:
            None
        """
        self.text = tekst
        self.zaakceptowano = 0
        self.odrzucono = 0

    def accept(self) -> None:
        """Zlicza potwierdzenia zamiast klikać OK.

        Args:
            Brak.

        Returns:
            None
        """
        self.zaakceptowano += 1

    def dismiss(self) -> None:
        """Zlicza odrzucenia zamiast klikać Anuluj.

        Args:
            Brak.

        Returns:
            None
        """
        self.odrzucono += 1


class FakeSwitchTo:
    """Atrapa przełącznika kontekstu — udaje driver.switch_to.

    Args:
        alert: FakeAlert do zwracania albo None, gdy alertu "nie ma".
    """

    def __init__(self, alert: Optional[FakeAlert]) -> None:
        """Zapamiętuje alert (lub jego brak).

        Args:
            alert: atrapa alertu lub None.

        Returns:
            None
        """
        self._alert = alert

    @property
    def alert(self) -> FakeAlert:
        """Zwraca alert lub rzuca NoAlertPresentException — jak prawdziwy driver.

        Args:
            Brak.

        Returns:
            FakeAlert: atrapa alertu, gdy jest ustawiona.
        """
        if self._alert is None:
            raise NoAlertPresentException("brak alertu")
        return self._alert


class FakeDriver:
    """Atrapa przeglądarki — udaje drivera do zrzutów ekranu i alertów.

    Args:
        alert: FakeAlert widoczny przez switch_to.alert albo None
            (wtedy switch_to.alert rzuca NoAlertPresentException).
    """

    def __init__(self, alert: Optional[FakeAlert] = None) -> None:
        """Przygotowuje przeglądarkę-atrapę z opcjonalnym alertem.

        Args:
            alert: atrapa alertu lub None.

        Returns:
            None
        """
        self.switch_to = FakeSwitchTo(alert)
        self.zrzuty = []

    def save_screenshot(self, sciezka: str) -> bool:
        """Notuje ścieżkę zrzutu i tworzy podrobiony plik PNG.

        Args:
            sciezka: ścieżka pliku zrzutu jako STRING (jak w prawdziwym
                driverze — Path trzeba skonwertować przed wywołaniem).

        Returns:
            bool: True — jak prawdziwy driver przy udanym zapisie.
        """
        self.zrzuty.append(sciezka)
        Path(sciezka).write_bytes(b"FAKE-PNG")
        return True
