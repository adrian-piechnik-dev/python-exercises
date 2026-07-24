from playwright.sync_api import Page, expect, sync_playwright


def zadanie_01_pobierz_tytul(url: str) -> str:
    """Otwiera strone w niewidzialnej przegladarce i zwraca jej tytul.

    Args:
        url: adres strony (moze byc file:// z dysku).

    Returns:
        str: tytul strony (zawartosc znacznika <title>).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        tytul = page.title()
        browser.close()
    return tytul


def zadanie_02_pobierz_tekst_naglowka(page: Page) -> str:
    """Zwraca widoczny tekst naglowka strony.

    Args:
        page: karta przegladarki z wczytana strona.

    Returns:
        str: tekst elementu o roli "heading".
    """
    locator = page.get_by_role("heading")
    return locator.inner_text()


def zadanie_03_czy_tekst_widoczny(page: Page, tekst: str) -> bool:
    """Sprawdza migawkowo, czy podany tekst jest teraz widoczny na stronie.

    Args:
        page: karta przegladarki z wczytana strona.
        tekst: szukany widoczny tekst.

    Returns:
        bool: True gdy tekst jest teraz widoczny, False w przeciwnym razie.
    """
    locator = page.get_by_text(tekst)
    return locator.is_visible()


def zadanie_04_wypelnij_pole(page: Page, etykieta: str, tekst: str) -> str:
    """Wypelnia pole formularza wskazane etykieta i zwraca jego zawartosc.

    Args:
        page: karta przegladarki z wczytana strona.
        etykieta: tekst etykiety pola (label), np. "Imie".
        tekst: tekst do wpisania.

    Returns:
        str: aktualna zawartosc pola po wpisaniu (input_value).
    """
    locator = page.get_by_label(etykieta)
    locator.fill(tekst)
    return locator.input_value()


def zadanie_05_zaznacz_zgode(page: Page, nazwa: str) -> bool:
    """Odhacza pole wyboru o podanej nazwie i zwraca jego stan.

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczna nazwa checkboxa, np. "Akceptuje regulamin".

    Returns:
        bool: True gdy pole jest po operacji odhaczone.
    """
    locator = page.get_by_role("checkbox", name=nazwa)
    locator.check()
    return locator.is_checked()


def zadanie_06_kliknij_przycisk(page: Page, nazwa: str) -> None:
    """Klika przycisk o podanej nazwie (auto-waiting zrobi reszte).

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczny napis na przycisku, np. "Wyslij".

    Returns:
        None: funkcja wykonuje akcje, niczego nie zwraca.
    """
    locator = page.get_by_role("button", name=nazwa)
    locator.click()


def zadanie_07_policz_elementy(page: Page, rola: str) -> int:
    """Liczy elementy o podanej roli na stronie.

    Args:
        page: karta przegladarki z wczytana strona.
        rola: rola ARIA, np. "button" albo "link".

    Returns:
        int: liczba pasujacych elementow (0 gdy brak).
    """
    locator = page.get_by_role(rola)
    return locator.count()


def zadanie_08_pobierz_adres_linku(page: Page, nazwa: str) -> str | None:
    """Zwraca adres (href) linku o podanej nazwie; brak linku daje None.

    Args:
        page: karta przegladarki z wczytana strona.
        nazwa: widoczny tekst linku, np. "Kontakt".

    Returns:
        str | None: wartosc atrybutu href albo None, gdy takiego linku
            nie ma na stronie.
    """
    locator = page.get_by_role("link", name=nazwa)
    if locator.count() == 0:
        return None
    return locator.get_attribute("href")


def zadanie_09_poczekaj_na_tekst(page: Page, tekst: str) -> bool:
    """Czeka cierpliwie (expect), az podany tekst stanie sie widoczny.

    Args:
        page: karta przegladarki z wczytana strona.
        tekst: tekst, ktory MA sie pojawic (moze z opoznieniem).

    Returns:
        bool: True gdy tekst stal sie widoczny w limicie 2 sekund
            (gdy nie — expect rzuca AssertionError).
    """
    expect(page.get_by_text(tekst)).to_be_visible(timeout=2000)
    return True


def zadanie_10_wyslij_formularz(page: Page, imie: str) -> str:
    """Przechodzi caly formularz: wypelnia, odhacza zgode, klika, czyta wynik.

    Args:
        page: karta przegladarki ze strona formularza.
        imie: imie do wpisania w pole "Imie".

    Returns:
        str: tekst komunikatu (element o roli "status") po wyslaniu.
    """
    page.get_by_label("Imie").fill(imie)
    page.get_by_role("checkbox", name = "Akceptuje regulamin").check()
    page.get_by_role("button", name="Wyslij").click()
    expect(page.get_by_role("status")).to_be_visible(timeout=2000)
    return page.get_by_role("status").inner_text()


def zadanie_11_przetlumacz_selenium(pojecie: str) -> str | None:
    """Tlumaczy pojecie z Selenium na odpowiednik w Playwright.

    Args:
        pojecie: nazwa z Selenium, jedna z: "find_element", "send_keys",
            "WebDriverWait", "expected_conditions", "driver.get".

    Returns:
        str | None: odpowiednik w Playwright wedlug sciagi z teorii
            ("locatory", "fill", "auto-waiting", "expect", "page.goto");
            None dla nieznanego pojecia.
    """
    translator = {
        "find_element": "locatory",
        "send_keys": "fill",
        "WebDriverWait": "auto-waiting",
        "expected_conditions": "expect",
        "driver.get": "page.goto"
    }
    return translator.get(pojecie)


def zadanie_12_zaloguj(page: Page, login: str, haslo: str) -> str:
    """Odtwarza scenariusz logowania z tematu Selenium — teraz w Playwright.

    Args:
        page: karta przegladarki ze strona logowania.
        login: login do wpisania w pole "Login".
        haslo: haslo do wpisania w pole "Haslo".

    Returns:
        str: tekst komunikatu (rola "status") po probie logowania —
            powitanie albo informacja o blednych danych.
    """
    page.get_by_label("Login").fill(login)
    page.get_by_label("Haslo").fill(haslo)
    page.get_by_role("button", name="Zaloguj").click()
    expect(page.get_by_role("status")).to_be_visible(timeout=2000)
    return page.get_by_role("status").inner_text()
