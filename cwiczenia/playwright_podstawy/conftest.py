# TODO: zaimportuj sys i os (stdlib), a nizej pytest oraz Browser i Page
#       z playwright.sync_api i sync_playwright (third-party) —
#       kolejnosc grup importow i pusta linia miedzy nimi

# TODO: dodaj sys.path.insert(0, ...) wskazujacy na folder tego tematu,
#       zeby test_playwright_podstawy.py widzial modul playwright_podstawy
#       (wzorzec: os.path.dirname(os.path.abspath(__file__)))


# Gotowe strony testowe (DANE, nie rozwiazanie — nie zmieniaj tresci,
# testy zaleza od dokladnych tekstow ponizej).

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


# TODO: udekoruj fixture dekoratorem @pytest.fixture(scope="session")
#       — jedna przegladarka na cala sesje testowa
def przegladarka():
    """Wspolna niewidzialna przegladarka dla wszystkich testow tematu.

    Args:
        Brak.

    Returns:
        Browser: uruchomiona przegladarka Chromium (headless);
            po sesji testowej zamykana w fazie sprzatania.
    """
    # TODO: uruchom silnik: p = sync_playwright().start()
    # TODO: odpal przegladarke: browser = p.chromium.launch(headless=True)
    # TODO: oddaj ja testom przez yield browser
    # TODO: po yield posprzataj: browser.close() i p.stop()
    # TODO: uzupelnij type hint zwracanej wartosci (Browser)
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture (zwykly zasieg —
#       swieza karta dla kazdego testu)
def strona(przegladarka):
    """Swieza karta ze strona formularza sklepu (HTML_FORMULARZ).

    Args:
        przegladarka: wspolna przegladarka z fixture wyzej.

    Returns:
        Page: karta z wczytana strona formularza;
            po tescie zamykana w fazie sprzatania.
    """
    # TODO: otworz karte: page = przegladarka.new_page()
    # TODO: wstrzyknij HTML: page.set_content(HTML_FORMULARZ)
    # TODO: oddaj karte testowi przez yield page
    # TODO: po yield posprzataj: page.close()
    # TODO: uzupelnij type hinty (parametr Browser, zwrot Page)
    pass


# TODO: udekoruj fixture dekoratorem @pytest.fixture
def strona_logowania(przegladarka):
    """Swieza karta ze strona logowania (HTML_LOGOWANIE).

    Args:
        przegladarka: wspolna przegladarka z fixture wyzej.

    Returns:
        Page: karta z wczytana strona logowania;
            po tescie zamykana w fazie sprzatania.
    """
    # TODO: otworz karte, wstrzyknij HTML_LOGOWANIE, yield, zamknij karte
    #       (dokladnie jak w fixture strona)
    # TODO: uzupelnij type hinty (parametr Browser, zwrot Page)
    pass
