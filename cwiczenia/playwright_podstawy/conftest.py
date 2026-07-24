import os
import sys

import pytest
from playwright.sync_api import Browser, Page, sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HTML_FORMULARZ = """
<html>
<head><title>Sklep testowy</title></head>
<body>
  <h1>Witaj w sklepie</h1>
  <p>Najlepsze ceny w miescie</p>
  <a href="/kontakt">Kontakt</a>
  <a href="/o-nas">O nas</a>
  <form>
    <label for="imie">Imie</label>
    <input id="imie" type="text">
    <input id="zgoda" type="checkbox">
    <label for="zgoda">Akceptuje regulamin</label>
    <button type="button" id="wyslij">Wyslij</button>
    <button type="button" id="oferta">Pokaz oferte</button>
  </form>
  <div role="status" id="komunikat" hidden></div>
  <div id="promocja" hidden>Promocja: -50%</div>
  <script>
    document.getElementById("wyslij").addEventListener("click", function () {
      setTimeout(function () {
        var k = document.getElementById("komunikat");
        k.textContent = "Dziekujemy za zgloszenie";
        k.hidden = false;
      }, 300);
    });
    document.getElementById("oferta").addEventListener("click", function () {
      setTimeout(function () {
        document.getElementById("promocja").hidden = false;
      }, 700);
    });
  </script>
</body>
</html>
"""

HTML_LOGOWANIE = """
<html>
<head><title>Logowanie</title></head>
<body>
  <h1>Panel logowania</h1>
  <form>
    <label for="login">Login</label>
    <input id="login" type="text">
    <label for="haslo">Haslo</label>
    <input id="haslo" type="password">
    <button type="button" id="zaloguj">Zaloguj</button>
  </form>
  <div role="status" id="wynik" hidden></div>
  <script>
    document.getElementById("zaloguj").addEventListener("click", function () {
      setTimeout(function () {
        var login = document.getElementById("login").value;
        var haslo = document.getElementById("haslo").value;
        var wynik = document.getElementById("wynik");
        if (login === "ada" && haslo === "tajne") {
          wynik.textContent = "Witaj, ada!";
        } else {
          wynik.textContent = "Bledne dane";
        }
        wynik.hidden = false;
      }, 300);
    });
  </script>
</body>
</html>
"""


@pytest.fixture(scope="session")
def przegladarka() -> Browser:
    """Wspolna niewidzialna przegladarka dla wszystkich testow tematu.

    Args:
        Brak.

    Returns:
        Browser: uruchomiona przegladarka Chromium (headless);
            po sesji testowej zamykana w fazie sprzatania.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    yield browser
    browser.close()
    p.stop()


@pytest.fixture
def strona(przegladarka: Browser) -> Page:
    """Swieza karta ze strona formularza sklepu (HTML_FORMULARZ).

    Args:
        przegladarka: wspolna przegladarka z fixture wyzej.

    Returns:
        Page: karta z wczytana strona formularza;
            po tescie zamykana w fazie sprzatania.
    """
    page = przegladarka.new_page()
    page.set_content(HTML_FORMULARZ)
    yield page
    page.close()


@pytest.fixture
def strona_logowania(przegladarka: Browser) -> Page:
    """Swieza karta ze strona logowania (HTML_LOGOWANIE).

    Args:
        przegladarka: wspolna przegladarka z fixture wyzej.

    Returns:
        Page: karta z wczytana strona logowania;
            po tescie zamykana w fazie sprzatania.
    """
    page = przegladarka.new_page()
    page.set_content(HTML_LOGOWANIE)
    yield page
    page.close()
