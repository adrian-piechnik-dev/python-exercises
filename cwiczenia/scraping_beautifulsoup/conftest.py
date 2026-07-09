import sys
import os

import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FakeResponse:
    """Atrapa odpowiedzi HTTP z HTML-em — udaje obiekt zwracany przez requests.get.

    Args:
        status_code: kod statusu, który atrapa ma udawać (np. 200, 404).
        text: string z HTML-em, który atrapa udostępni w atrybucie text.
    """

    def __init__(self, status_code: int, text: str) -> None:
        """Zapamiętuje kod statusu i HTML do udawania.

        Args:
            status_code: kod statusu HTTP.
            text: surowy HTML strony.

        Returns:
            None
        """
        # TODO: zapisz status_code w atrybucie self.status_code
        # TODO: zapisz text w atrybucie self.text (bez podkreślenia —
        #       prawdziwa odpowiedź requests też ma atrybut .text)
        pass

    def raise_for_status(self) -> None:
        """Rzuca requests.HTTPError przy kodach 4xx/5xx — jak prawdziwa odpowiedź.

        Args:
            Brak.

        Returns:
            None
        """
        # TODO: jeśli self.status_code >= 400 —
        #       raise requests.HTTPError(f"kod {self.status_code}")
        pass


@pytest.fixture
def html_strona() -> str:
    """HTML przykładowej strony sklepu — do zadań parsujących (1-7, 9).

    Args:
        Brak.

    Returns:
        str: strona z nagłówkiem h1, dwoma linkami, dwoma divami klasy
            "produkt", divem klasy "opis", akapitem o id "stopka"
            i dwoma obrazkami.
    """
    # TODO: zwróć poniższy HTML jako string (przepisz dokładnie):
    #       <html>
    #         <body>
    #           <h1>Sklep Python</h1>
    #           <a href="/produkty">Produkty</a>
    #           <a href="/kontakt">Kontakt</a>
    #           <div class="produkt">Klawiatura</div>
    #           <div class="produkt">Myszka</div>
    #           <div class="opis">Sklep z akcesoriami</div>
    #           <p id="stopka">Copyright 2026</p>
    #           <img src="/logo.png">
    #           <img src="/baner.png">
    #         </body>
    #       </html>
    #       Wskazówka: użyj potrójnych cudzysłowów \"\"\"...\"\"\" na
    #       wieloliniowy string.
    pass


@pytest.fixture
def html_tabela() -> str:
    """HTML z tabelą dwóch osób — do zadania 8.

    Args:
        Brak.

    Returns:
        str: strona z tabelą 2x2: wiersz Anna/30 i wiersz Piotr/25.
    """
    # TODO: zwróć poniższy HTML jako string (przepisz dokładnie):
    #       <html>
    #         <body>
    #           <table>
    #             <tr><td>Anna</td><td>30</td></tr>
    #             <tr><td>Piotr</td><td>25</td></tr>
    #           </table>
    #         </body>
    #       </html>
    pass
