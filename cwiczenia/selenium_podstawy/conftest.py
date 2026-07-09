import sys
import os
from typing import Optional

from selenium.common.exceptions import NoSuchElementException

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeElement:
    """Atrapa elementu strony — udaje wynik find_element prawdziwego drivera.

    Args:
        tekst: widoczny tekst, który element ma udawać (atrybut .text).
    """

    def __init__(self, tekst: str = "") -> None:
        """Przygotowuje element-szpiega z zadanym tekstem.

        Args:
            tekst: wartość udawana przez atrybut .text.

        Returns:
            None
        """
        # TODO: zapisz tekst w atrybucie self.text
        # TODO: utwórz pustą listę self.wpisane (zapisy send_keys)
        # TODO: utwórz licznik self.klikniecia = 0
        pass

    def send_keys(self, tekst: str) -> None:
        """Zapisuje wpisany tekst zamiast stukać w klawiaturę.

        Args:
            tekst: tekst, który robot chciał wpisać.

        Returns:
            None
        """
        # TODO: dopisz tekst do self.wpisane
        pass

    def click(self) -> None:
        """Zlicza kliknięcia zamiast klikać naprawdę.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: zwiększ self.klikniecia o 1
        pass


class FakeDriver:
    """Atrapa przeglądarki — udaje drivera Selenium i notuje polecenia.

    Args:
        elementy: słownik {wartosc_lokatora: FakeElement} dla find_element.
        listy_elementow: słownik {wartosc_lokatora: lista FakeElement}
            dla find_elements.
        tytul: tytuł strony udawany przez atrybut .title.
        blad_przy_get: gdy True, metoda get rzuca RuntimeError
            (do testowania try/finally).
    """

    def __init__(
        self,
        elementy: Optional[dict] = None,
        listy_elementow: Optional[dict] = None,
        tytul: str = "Strona testowa",
        blad_przy_get: bool = False,
    ) -> None:
        """Przygotowuje przeglądarkę-atrapę z zadanymi elementami.

        Args:
            elementy: elementy znajdowane przez find_element.
            listy_elementow: listy znajdowane przez find_elements.
            tytul: udawany tytuł strony.
            blad_przy_get: czy get ma udawać awarię.

        Returns:
            None
        """
        # TODO: zapisz self.elementy = elementy if elementy is not None else {}
        # TODO: zapisz self.listy_elementow analogicznie (pusty dict gdy None)
        # TODO: zapisz self.title = tytul
        # TODO: zapisz self.blad_przy_get = blad_przy_get
        # TODO: utwórz pustą listę self.odwiedzone (zapisy get)
        # TODO: utwórz flagę self.zamknieto = False (ustawi ją quit)
        pass

    def get(self, url: str) -> None:
        """Zapisuje odwiedzany adres; przy fladze blad_przy_get udaje awarię.

        Args:
            url: adres, który robot chciał otworzyć.

        Returns:
            None
        """
        # TODO: jeśli self.blad_przy_get is True —
        #       raise RuntimeError("strona nie odpowiada")
        # TODO: dopisz url do self.odwiedzone
        pass

    def find_element(self, by: str, wartosc: str) -> FakeElement:
        """Zwraca zapamiętany element lub rzuca NoSuchElementException.

        Args:
            by: strategia szukania (np. By.ID) — atrapa jej nie sprawdza.
            wartosc: wartość lokatora (klucz w słowniku elementy).

        Returns:
            FakeElement: element przypisany do wartości lokatora.
        """
        # TODO: jeśli wartosc jest w self.elementy — zwróć self.elementy[wartosc]
        # TODO: w przeciwnym razie — raise NoSuchElementException(wartosc)
        #       (dokładnie jak prawdziwy driver; dzięki temu WebDriverWait
        #       działa na atrapie!)
        pass

    def find_elements(self, by: str, wartosc: str) -> list[FakeElement]:
        """Zwraca zapamiętaną listę elementów lub pustą listę.

        Args:
            by: strategia szukania — atrapa jej nie sprawdza.
            wartosc: wartość lokatora (klucz w słowniku listy_elementow).

        Returns:
            list[FakeElement]: lista elementów; pusta gdy lokator nieznany.
        """
        # TODO: zwróć self.listy_elementow.get(wartosc, [])
        #       (find_elements nie rzuca — pusta lista, jak w prawdziwym)
        pass

    def quit(self) -> None:
        """Ustawia flagę zamknięcia zamiast gasić przeglądarkę.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: ustaw self.zamknieto = True
        pass
