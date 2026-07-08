from pathlib import Path

from pliki_tekstowe import (
    zadanie_01_czytaj_calosc,
    zadanie_02_czytaj_linie,
    zadanie_03_policz_linie,
    zadanie_04_zapisz_tekst,
    zadanie_05_zapisz_linie,
    zadanie_06_dopisz_linie,
    zadanie_07_pierwsza_linia,
    zadanie_08_szukaj_frazy,
    zadanie_09_licz_slowa,
    zadanie_10_czytaj_bezpiecznie,
    zadanie_11_skopiuj_plik,
    zadanie_12_filtruj_i_zapisz,
)


# --- zadanie 01 ---

def test_zadanie_01_zwraca_pelna_zawartosc(plik_txt: Path) -> None:
    """Co testuje: czy funkcja zwraca wszystkie znaki pliku jako jeden str.
    Co udaje: nic — uzywam prawdziwego pliku z fixture plik_txt.
    Co sprawdzam: wynik == "ala ma kota\\npies i kot\\nkot spi\\n".
    """
    wynik = zadanie_01_czytaj_calosc(str(plik_txt))
    assert wynik == "ala ma kota\npies i kot\nkot spi\n"


def test_zadanie_01_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: zachowanie gdy plik nie ma zadnej tresci.
    Co udaje: nic — uzywam pustego pliku z fixture plik_pusty.
    Co sprawdzam: wynik == "" (pusty string, nie None).
    """
    wynik = zadanie_01_czytaj_calosc(str(plik_pusty))
    assert wynik == ""


def test_zadanie_01_jedna_linia(tmp_path: Path) -> None:
    """Co testuje: poprawnosc przy pliku z dokładnie jedna linia.
    Co udaje: nic — tworze plik bezposrednio przez tmp_path.
    Co sprawdzam: wynik == "hej\\n" (linia ze znakiem nowej linii).
    """
    p = tmp_path / "x.txt"
    p.write_text("hej\n", encoding="utf-8")
    wynik = zadanie_01_czytaj_calosc(str(p))
    assert wynik == "hej\n"

# --- zadanie 02 ---

def test_zadanie_02_trzy_linie(plik_txt: Path) -> None:
    """Co testuje: czy splitlines usuwa \\n i zwraca liste stringow.
    Co udaje: nic — uzywam fixture plik_txt z trzema liniami.
    Co sprawdzam: wynik == ["ala ma kota", "pies i kot", "kot spi"].
    """
    wynik = zadanie_02_czytaj_linie(str(plik_txt))
    assert wynik == ["ala ma kota", "pies i kot", "kot spi"]


def test_zadanie_02_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: czy pusty plik daje pusta liste (nie liste z jednym pustym stringiem).
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_02_czytaj_linie(str(plik_pusty))
    assert wynik == []


def test_zadanie_02_jedna_linia(tmp_path: Path) -> None:
    """Co testuje: lista z jednym elementem dla pliku z jedna linia.
    Co udaje: nic — tworze plik przez tmp_path.
    Co sprawdzam: wynik == ["jedyna"] (bez \\n).
    """
    p = tmp_path / "x.txt"
    p.write_text("jedyna\n", encoding="utf-8")
    wynik = zadanie_02_czytaj_linie(str(p))
    assert wynik == ["jedyna"]


# --- zadanie 03 ---

def test_zadanie_03_trzy_linie(plik_txt: Path) -> None:
    """Co testuje: czy funkcja liczy linie w pliku z trescia.
    Co udaje: nic — uzywam fixture plik_txt (3 linie).
    Co sprawdzam: wynik == 3.
    """
    wynik = zadanie_03_policz_linie(str(plik_txt))
    assert wynik == 3


def test_zadanie_03_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: czy pusty plik daje 0, nie 1.
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik == 0.
    """
    wynik = zadanie_03_policz_linie(str(plik_pusty))
    assert wynik == 0


def test_zadanie_03_jedna_linia(tmp_path: Path) -> None:
    """Co testuje: dokladnie 1 dla pliku z jedna linia.
    Co udaje: nic — tworze plik przez tmp_path.
    Co sprawdzam: wynik == 1.
    """
    p = tmp_path / "x.txt"
    p.write_text("jedna\n", encoding="utf-8")
    wynik = zadanie_03_policz_linie(str(p))
    assert wynik == 1


# --- zadanie 04 ---

def test_zadanie_04_zapisuje_tresc(tmp_path: Path) -> None:
    """Co testuje: czy plik zawiera dokladnie podana tresc po zapisie.
    Co udaje: nic — tworze sciezke przez tmp_path (plik jeszcze nie istnieje).
    Co sprawdzam: p.read_text() po zapisie == "hello world".
    """
    p = tmp_path / "wynik.txt"
    zadanie_04_zapisz_tekst(str(p), "hello world")
    assert p.read_text(encoding="utf-8") == "hello world"


def test_zadanie_04_nadpisuje_istniejacy(plik_txt: Path) -> None:
    """Co testuje: czy tryb "w" usuwa stara tresc i zastepuje nowa.
    Co udaje: nic — uzywam istniejacego plik_txt jako cel nadpisania.
    Co sprawdzam: treść == "nowa tresc" (stare linie znikneły).
    """
    zadanie_04_zapisz_tekst(str(plik_txt), "nowa tresc")
    assert plik_txt.read_text(encoding="utf-8") == "nowa tresc"


def test_zadanie_04_zapisuje_pusty_string(tmp_path: Path) -> None:
    """Co testuje: poprawnosc zapisu pustego stringa (tworzy pusty plik).
    Co udaje: nic — tworze sciezke przez tmp_path.
    Co sprawdzam: p.read_text() == "" po zapisie.
    """
    p = tmp_path / "wynik.txt"
    zadanie_04_zapisz_tekst(str(p), "")
    assert p.read_text(encoding="utf-8") == ""


# --- zadanie 05 ---

def test_zadanie_05_lista_trzech(tmp_path: Path) -> None:
    """Co testuje: czy lista linii trafia do pliku oddzielona \\n.
    Co udaje: nic — tworze sciezke przez tmp_path.
    Co sprawdzam: p.read_text() == "ala\\npies\\nkot" (bez \\n na koncu).
    """
    p = tmp_path / "wynik.txt"
    zadanie_05_zapisz_linie(str(p), ["ala", "pies", "kot"])
    assert p.read_text(encoding="utf-8") == "ala\npies\nkot"


def test_zadanie_05_pusta_lista(tmp_path: Path) -> None:
    """Co testuje: pusta lista -> pusty plik (nie crashuje).
    Co udaje: nic — tworze sciezke przez tmp_path.
    Co sprawdzam: p.read_text() == "".
    """
    p = tmp_path / "wynik.txt"
    p.write_text("")
    zadanie_05_zapisz_linie(str(p), [])
    assert p.read_text(encoding="utf-8") == ""


def test_zadanie_05_jedna_pozycja(tmp_path: Path) -> None:
    """Co testuje: lista z jednym elementem -> string bez \\n.
    Co udaje: nic — tworze sciezke przez tmp_path.
    Co sprawdzam: p.read_text() == "jedyna".
    """
    p = tmp_path / "wynik.txt"
    zadanie_05_zapisz_linie(str(p), ["jedyna"])
    assert p.read_text(encoding="utf-8") == "jedyna"


# --- zadanie 06 ---

def test_zadanie_06_dopisuje_do_pustego(tmp_path: Path) -> None:
    """Co testuje: czy tryb "a" tworzy plik gdy nie istnieje.
    Co udaje: nic — sciezka do nieistniejacego pliku w tmp_path.
    Co sprawdzam: p.read_text() == "nowa linia\\n" po dopisaniu.
    """
    p = tmp_path / "log.txt"
    zadanie_06_dopisz_linie(str(p), "nowa linia")
    assert p.read_text(encoding="utf-8") == "nowa linia\n"


def test_zadanie_06_dopisuje_do_istniejacego(plik_txt: Path) -> None:
    """Co testuje: czy stara tresc jest zachowana po dopisaniu.
    Co udaje: nic — uzywam istniejacego plik_txt.
    Co sprawdzam: tresc == oryginalna_tresc + "czwarta\\n".
    """
    oryginalna = plik_txt.read_text(encoding="utf-8")
    zadanie_06_dopisz_linie(str(plik_txt), "czwarta")
    assert plik_txt.read_text(encoding="utf-8") == oryginalna + "czwarta\n"


def test_zadanie_06_dwa_dopisania(tmp_path: Path) -> None:
    """Co testuje: dwa kolejne wywolania kumuluja wpisy.
    Co udaje: nic — tworze sciezke przez tmp_path.
    Co sprawdzam: p.read_text() == "linia1\\nlinia2\\n".
    """
    p = tmp_path / "log.txt"
    zadanie_06_dopisz_linie(str(p), "linia1")
    zadanie_06_dopisz_linie(str(p), "linia2")
    assert p.read_text(encoding="utf-8") == "linia1\nlinia2\n"


# --- zadanie 07 ---

def test_zadanie_07_zwraca_pierwsza(plik_txt: Path) -> None:
    """Co testuje: czy pierwsza linia jest zwracana bez \\n.
    Co udaje: nic — uzywam fixture plik_txt (pierwsza linia: "ala ma kota").
    Co sprawdzam: wynik == "ala ma kota".
    """
    wynik = zadanie_07_pierwsza_linia(str(plik_txt))
    assert wynik == "ala ma kota"


def test_zadanie_07_pusty_plik_zwraca_none(plik_pusty: Path) -> None:
    """Co testuje: czy pusty plik zwraca None (nie "" ani IndexError).
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_07_pierwsza_linia(str(plik_pusty))
    assert wynik is None


def test_zadanie_07_jedna_linia(tmp_path: Path) -> None:
    """Co testuje: plik z jedna linia -> zwraca ten element.
    Co udaje: nic — tworze plik przez tmp_path.
    Co sprawdzam: wynik == "jedyna".
    """
    p = tmp_path / "x.txt"
    p.write_text("jedyna\n", encoding="utf-8")
    wynik = zadanie_07_pierwsza_linia(str(p))
    assert wynik == "jedyna"


# --- zadanie 08 ---

def test_zadanie_08_fraza_w_jednej_linii(plik_txt: Path) -> None:
    """Co testuje: filtrowanie — tylko linie zawierajace fraze sa zwracane.
    Co udaje: nic — uzywam plik_txt; "pies" wystepuje w jednej linii.
    Co sprawdzam: wynik == ["pies i kot"].
    """
    wynik = zadanie_08_szukaj_frazy(str(plik_txt), "pies")
    assert wynik == ["pies i kot"]


def test_zadanie_08_fraza_we_wszystkich(plik_txt: Path) -> None:
    """Co testuje: fraza w kazdej linii -> wszystkie linie w wyniku.
    Co udaje: nic — uzywam plik_txt; "kot" jest w 3 z 3 linii.
    Co sprawdzam: wynik == ["ala ma kota", "pies i kot", "kot spi"].
    """
    wynik = zadanie_08_szukaj_frazy(str(plik_txt), "kot")
    assert wynik == ["ala ma kota", "pies i kot", "kot spi"]


def test_zadanie_08_fraza_nie_istnieje(plik_txt: Path) -> None:
    """Co testuje: brak dopasowania -> pusta lista (nie None, nie blad).
    Co udaje: nic — uzywam plik_txt; "zebra" nie wystepuje w zadnej linii.
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_08_szukaj_frazy(str(plik_txt), "zebra")
    assert wynik == []


def test_zadanie_08_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: pusty plik -> pusta lista (nie blad).
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik == [].
    """
    wynik = zadanie_08_szukaj_frazy(str(plik_pusty), "ala")
    assert wynik == []


# --- zadanie 09 ---

def test_zadanie_09_osiem_slow(plik_txt: Path) -> None:
    """Co testuje: czy funkcja sumuje slowa ze wszystkich linii.
    Co udaje: nic — uzywam plik_txt ("ala ma kota" + "pies i kot" + "kot spi" = 8 slow).
    Co sprawdzam: wynik == 8.
    """
    wynik = zadanie_09_licz_slowa(str(plik_txt))
    assert wynik == 8


def test_zadanie_09_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: pusty plik -> 0 (nie blad, nie 1).
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik == 0.
    """
    wynik = zadanie_09_licz_slowa(str(plik_pusty))
    assert wynik == 0


def test_zadanie_09_jedno_slowo(tmp_path: Path) -> None:
    """Co testuje: plik z jednym slowem -> 1.
    Co udaje: nic — tworze plik przez tmp_path.
    Co sprawdzam: wynik == 1.
    """
    p = tmp_path / "x.txt"
    p.write_text("slowo\n", encoding="utf-8")
    wynik = zadanie_09_licz_slowa(str(p))
    assert wynik == 1


# --- zadanie 10 ---

def test_zadanie_10_istniejacy_plik(plik_txt: Path) -> None:
    """Co testuje: normalne czytanie zwraca str z trescia.
    Co udaje: nic — uzywam fixture plik_txt.
    Co sprawdzam: wynik == "ala ma kota\\npies i kot\\nkot spi\\n".
    """
    wynik = zadanie_10_czytaj_bezpiecznie(str(plik_txt))
    assert wynik == "ala ma kota\npies i kot\nkot spi\n"


def test_zadanie_10_brak_pliku_zwraca_none() -> None:
    """Co testuje: kontrakt try/except — None zamiast FileNotFoundError.
    Co udaje: nic — uzywam sciezki do pliku ktory na pewno nie istnieje.
    Co sprawdzam: wynik is None.
    """
    wynik = zadanie_10_czytaj_bezpiecznie("/niestniejacy/plik.txt")
    assert wynik is None


def test_zadanie_10_pusty_plik(plik_pusty: Path) -> None:
    """Co testuje: pusty istniejacy plik zwraca "" nie None.
    Co udaje: nic — uzywam fixture plik_pusty.
    Co sprawdzam: wynik == "".
    """
    wynik = zadanie_10_czytaj_bezpiecznie(str(plik_pusty))
    assert wynik == ""


# --- zadanie 11 ---

def test_zadanie_11_kopiuje_zawartosc(plik_txt: Path, tmp_path: Path) -> None:
    """Co testuje: czy plik docelowy ma identyczna tresc co zrodlowy, a wynik to True.
    Co udaje: nic — uzywam plik_txt jako zrodla i tmp_path jako celu.
    Co sprawdzam: wynik is True i cel.read_text() == zrodlo.read_text().
    """
    cel = tmp_path / "kopia.txt"
    wynik = zadanie_11_skopiuj_plik(str(plik_txt), str(cel))
    assert wynik is True
    assert cel.read_text(encoding="utf-8") == plik_txt.read_text(encoding="utf-8")


def test_zadanie_11_brak_zrodla_zwraca_false(tmp_path: Path) -> None:
    """Co testuje: False zamiast FileNotFoundError gdy plik zrodlowy nie istnieje.
    Co udaje: nic — uzywam nieistniejącej sciezki jako zrodla.
    Co sprawdzam: wynik is False.
    """
    cel = tmp_path / "kopia.txt"
    wynik = zadanie_11_skopiuj_plik("nieistniejacy.txt", str(cel))
    assert wynik is False


def test_zadanie_11_kopia_pusty_plik(plik_pusty: Path, tmp_path: Path) -> None:
    """Co testuje: kopiowanie pustego pliku dziala i zwraca True.
    Co udaje: nic — uzywam fixture plik_pusty jako zrodla.
    Co sprawdzam: wynik is True i cel.read_text() == "".
    """
    cel = tmp_path / "kopia.txt"
    wynik = zadanie_11_skopiuj_plik(str(plik_pusty), str(cel))
    assert wynik is True
    assert cel.read_text(encoding="utf-8") == ""


# --- zadanie 12 ---

def test_zadanie_12_filtruje_i_zapisuje(plik_txt: Path, tmp_path: Path) -> None:
    """Co testuje: poprawna liczba zapisanych linii i ich tresc w pliku wyjsciowym.
    Co udaje: nic — uzywam plik_txt; "pies" wystepuje w jednej linii.
    Co sprawdzam: wynik == 1 i cel.read_text() == "pies i kot".
    """
    cel = tmp_path / "wynik.txt"
    wynik = zadanie_12_filtruj_i_zapisz(str(plik_txt), str(cel), "pies")
    assert wynik == 1
    assert cel.read_text(encoding="utf-8") == "pies i kot"


def test_zadanie_12_brak_dopasowania(plik_txt: Path, tmp_path: Path) -> None:
    """Co testuje: zwraca 0 gdy zadna linia nie zawiera frazy.
    Co udaje: nic — uzywam plik_txt; "zebra" nie wystepuje.
    Co sprawdzam: wynik == 0.
    """
    cel = tmp_path / "wynik.txt"
    wynik = zadanie_12_filtruj_i_zapisz(str(plik_txt), str(cel), "zebra")
    assert wynik == 0


def test_zadanie_12_brak_pliku_wejsciowego(tmp_path: Path) -> None:
    """Co testuje: 0 zamiast FileNotFoundError gdy plik wejsciowy nie istnieje.
    Co udaje: nic — uzywam nieistniejącej sciezki jako pliku wejsciowego.
    Co sprawdzam: wynik == 0.
    """
    cel = tmp_path / "wynik.txt"
    wynik = zadanie_12_filtruj_i_zapisz("/nieistniejacy.txt", str(cel), "ala")
    assert wynik == 0
