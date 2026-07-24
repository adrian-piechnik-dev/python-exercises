from pathlib import Path

import pytest
from playwright.sync_api import expect
from playwright.sync_api import Page

from playwright_podstawy import (
    zadanie_01_pobierz_tytul,
    zadanie_02_pobierz_tekst_naglowka,
    zadanie_03_czy_tekst_widoczny,
    zadanie_04_wypelnij_pole,
    zadanie_05_zaznacz_zgode,
    zadanie_06_kliknij_przycisk,
    zadanie_07_policz_elementy,
    zadanie_08_pobierz_adres_linku,
    zadanie_09_poczekaj_na_tekst,
    zadanie_10_wyslij_formularz,
    zadanie_11_przetlumacz_selenium,
    zadanie_12_zaloguj,
)


# --- zadanie_01 ---

def test_zadanie_01_czyta_tytul_z_pliku(tmp_path: Path) -> None:
    """Co testuje: caly rytual startowy — otwarcie strony i odczyt tytulu.
    Co udaje: internet — strona to plik HTML zapisany w tmp_path,
    adres budowany przez as_uri().
    Co sprawdzam: wynik == "Moja strona".
    """
    sciezka = tmp_path / "strona.html"
    sciezka.write_text(
        "<html><head><title>Moja strona</title></head></html>",
        encoding="utf-8"
    )
    adres = sciezka.as_uri()
    wynik = zadanie_01_pobierz_tytul(adres)
    assert wynik == "Moja strona"


def test_zadanie_01_pusty_tytul_dla_strony_bez_title(tmp_path: Path) -> None:
    """Co testuje: przypadek brzegowy — strona bez znacznika <title>.
    Co udaje: internet — plik HTML bez tytulu w tmp_path.
    Co sprawdzam: wynik == "" (pusty tekst, nie None i nie blad).
    """
    sciezka = tmp_path / "strona.html"
    sciezka.write_text(
        "<html><body>x</body></html>",
        encoding="utf-8"
    )
    adres = sciezka.as_uri()
    wynik = zadanie_01_pobierz_tytul(adres)
    assert wynik == ""


# --- zadanie_02 ---

def test_zadanie_02_czyta_tekst_naglowka(strona: Page) -> None:
    """Co testuje: locator get_by_role("heading") i odczyt inner_text.
    Co udaje: internet — strona formularza z fixture (set_content).
    Co sprawdzam: wynik == "Witaj w sklepie".
    """
    wynik = zadanie_02_pobierz_tekst_naglowka(strona)
    assert wynik == "Witaj w sklepie"


def test_zadanie_02_wynik_jest_tekstem(strona: Page) -> None:
    """Co testuje: czy funkcja zwraca str (a nie locator!).
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: isinstance(wynik, str) is True.
    """
    wynik = zadanie_02_pobierz_tekst_naglowka(strona)
    assert isinstance(wynik, str)


# --- zadanie_03 ---

def test_zadanie_03_widzi_widoczny_akapit(strona: Page) -> None:
    """Co testuje: czy migawka is_visible daje True dla widocznego tekstu.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik is True dla "Najlepsze ceny w miescie".
    """
    wynik = zadanie_03_czy_tekst_widoczny(strona, "Najlepsze ceny w miescie")
    assert wynik is True


def test_zadanie_03_nie_widzi_ukrytej_promocji(strona: Page) -> None:
    """Co testuje: czy migawka daje False dla elementu ukrytego (hidden),
    ktory pojawi sie dopiero po kliknieciu.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik is False dla "Promocja: -50%".
    """
    wynik = zadanie_03_czy_tekst_widoczny(strona, "Promocja: -50%")
    assert wynik is False


# --- zadanie_04 ---

def test_zadanie_04_wpisuje_tekst_w_pole(strona: Page) -> None:
    """Co testuje: get_by_label + fill — tekst laduje w polu "Imie".
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik == "Ada" (input_value po wpisaniu).
    """
    wynik = zadanie_04_wypelnij_pole(strona, "Imie", "Ada")
    assert wynik == "Ada"


def test_zadanie_04_fill_nadpisuje_poprzednia_zawartosc(strona: Page) -> None:
    """Co testuje: czy fill najpierw czysci pole (roznica vs send_keys!) —
    drugie wypelnienie NIE dokleja sie do pierwszego.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: po wpisaniu "Ada", potem "Ola" — wynik == "Ola".
    """
    zadanie_04_wypelnij_pole(strona, "Imie", "Ada")
    wynik = zadanie_04_wypelnij_pole(strona, "Imie", "Ola")
    assert wynik == "Ola"


# --- zadanie_05 ---

def test_zadanie_05_odhacza_zgode(strona: Page) -> None:
    """Co testuje: akcja check na checkboxie wskazanym przez role i nazwe.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik is True dla "Akceptuje regulamin".
    """
    wynik = zadanie_05_zaznacz_zgode(strona, "Akceptuje regulamin")
    assert wynik is True


def test_zadanie_05_podwojne_check_nie_odhacza_z_powrotem(strona: Page) -> None:
    """Co testuje: czy check jest bezpieczny przy powtorzeniu (nie przelacza,
    tylko upewnia sie, ze odhaczone).
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: po dwoch wywolaniach wynik nadal is True.
    """
    zadanie_05_zaznacz_zgode(strona, "Akceptuje regulamin")
    wynik = zadanie_05_zaznacz_zgode(strona, "Akceptuje regulamin")
    assert wynik is True


# --- zadanie_06 ---

def test_zadanie_06_klik_pokazuje_komunikat(strona: Page) -> None:
    """Co testuje: czy klikniecie "Wyslij" uruchamia komunikat strony.
    Co udaje: internet — strona formularza z fixture (komunikat pojawia sie
    z opoznieniem 300 ms).
    Co sprawdzam: po kliknieciu i odczekaniu przez expect tekst
    "Dziekujemy za zgloszenie" jest widoczny (to_be_visible przechodzi).
    """
    zadanie_06_kliknij_przycisk(strona, "Wyslij")
    expect(
        strona.get_by_text("Dziekujemy za zgloszenie")).to_be_visible(timeout=2000)


def test_zadanie_06_zwraca_none(strona: Page) -> None:
    """Co testuje: kontrakt None — akcja niczego nie zwraca.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_06_kliknij_przycisk(strona, "Wyslij")
    assert wynik is None


# --- zadanie_07 ---

def test_zadanie_07_liczy_przyciski(strona: Page) -> None:
    """Co testuje: count na locatorze roli — strona ma dokladnie 2 przyciski.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik == 2 dla roli "button".
    """
    wynik = zadanie_07_policz_elementy(strona, "button")
    assert wynik == 2


def test_zadanie_07_zero_dla_roli_ktorej_nie_ma(strona: Page) -> None:
    """Co testuje: przypadek brzegowy — rola nieobecna na stronie daje 0.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik == 0 dla roli "table".
    """
    wynik = zadanie_07_policz_elementy(strona, "table")
    assert wynik == 0


# --- zadanie_08 ---

def test_zadanie_08_zwraca_href_linku(strona: Page) -> None:
    """Co testuje: get_attribute — link "Kontakt" prowadzi do /kontakt.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik == "/kontakt".
    """
    wynik = zadanie_08_pobierz_adres_linku(strona, "Kontakt")
    assert wynik == "/kontakt"


def test_zadanie_08_zwraca_none_gdy_linku_brak(strona: Page) -> None:
    """Co testuje: kontrakt None — link o nieistniejacej nazwie daje None
    (przez count == 0), bez czekania i bez bledu.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik is None dla nazwy "Regulamin".
    """
    wynik = zadanie_08_pobierz_adres_linku(strona, "Regulamin")
    assert wynik is None


# --- zadanie_09 ---

def test_zadanie_09_doczeka_sie_opoznionego_tekstu(strona: Page) -> None:
    """Co testuje: sedno expect — tekst pojawia sie 700 ms po kliknieciu,
    migawka by go nie zlapala, expect cierpliwie czeka.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: po kliknieciu "Pokaz oferte" wynik is True
    dla tekstu "Promocja: -50%".
    """
    zadanie_06_kliknij_przycisk(strona, "Pokaz oferte")
    wynik = zadanie_09_poczekaj_na_tekst(strona, "Promocja: -50%")
    assert wynik is True


def test_zadanie_09_rzuca_gdy_tekst_sie_nie_pojawia(strona: Page) -> None:
    """Co testuje: przypadek brzegowy — tekst, ktory NIGDY sie nie pojawi,
    konczy sie AssertionError po uplywie timeoutu.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wywolanie w bloku pytest.raises(AssertionError).
    """
    with pytest.raises(AssertionError):
        zadanie_09_poczekaj_na_tekst(strona, "Takiego tekstu nie ma")


# --- zadanie_10 ---

def test_zadanie_10_pelny_formularz_konczy_sie_komunikatem(strona: Page) -> None:
    """Co testuje: zlozenie fill + check + click + expect w jeden scenariusz.
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: wynik == "Dziekujemy za zgloszenie".
    """
    wynik = zadanie_10_wyslij_formularz(strona, "Ada")
    assert wynik == "Dziekujemy za zgloszenie"


def test_zadanie_10_imie_zostaje_w_polu_po_wyslaniu(strona: Page) -> None:
    """Co testuje: czy scenariusz naprawde wpisal imie do pola (stan strony
    po wywolaniu funkcji).
    Co udaje: internet — strona formularza z fixture.
    Co sprawdzam: strona.get_by_label("Imie").input_value() == "Ola".
    """
    zadanie_10_wyslij_formularz(strona, "Ola")
    assert strona.get_by_label("Imie").input_value() == "Ola"


# --- zadanie_11 ---

def test_zadanie_11_tlumaczy_webdriverwait_na_autowaiting() -> None:
    """Co testuje: mapowanie pojec Selenium -> Playwright ze sciagi teorii.
    Co udaje: nic — czysta funkcja na slowniku.
    Co sprawdzam: wynik == "auto-waiting" dla "WebDriverWait"
    oraz wynik == "fill" dla "send_keys".
    """
    wynik = zadanie_11_przetlumacz_selenium("WebDriverWait")
    assert wynik == "auto-waiting"
    wynik = zadanie_11_przetlumacz_selenium("send_keys")
    assert wynik == "fill"


def test_zadanie_11_none_dla_nieznanego_pojecia() -> None:
    """Co testuje: kontrakt None — pojecie spoza sciagi daje None.
    Co udaje: nic — czysta funkcja na slowniku.
    Co sprawdzam: wynik is None dla "teleportacja".
    """
    wynik = zadanie_11_przetlumacz_selenium("teleportacja")
    assert wynik is None


# --- zadanie_12 ---

def test_zadanie_12_poprawne_dane_daja_powitanie(strona_logowania: Page) -> None:
    """Co testuje: scenariusz logowania znany z Selenium — szczesliwa sciezka.
    Co udaje: internet — strona logowania z fixture (poprawne dane:
    login "ada", haslo "tajne").
    Co sprawdzam: wynik == "Witaj, ada!".
    """
    wynik = zadanie_12_zaloguj(strona_logowania, "ada", "tajne")
    assert wynik == "Witaj, ada!"


def test_zadanie_12_bledne_haslo_daje_komunikat_bledu(
    strona_logowania: Page,
) -> None:
    """Co testuje: przypadek brzegowy logowania — zle haslo.
    Co udaje: internet — strona logowania z fixture.
    Co sprawdzam: wynik == "Bledne dane".
    """
    wynik = zadanie_12_zaloguj(strona_logowania, "ada", "zle-haslo")
    assert wynik == "Bledne dane"
