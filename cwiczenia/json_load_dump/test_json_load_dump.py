import json
from pathlib import Path

from json_load_dump import (
    zadanie_01_serializuj_slownik,
    zadanie_02_deserializuj_string,
    zadanie_03_zapisz_do_pliku,
    zadanie_04_wczytaj_z_pliku,
    zadanie_05_sformatowany_json,
    zadanie_06_serializuj_liste,
    zadanie_07_wczytaj_liste_z_pliku,
    zadanie_08_parsuj_bezpiecznie,
    zadanie_09_wczytaj_plik_bezpiecznie,
    zadanie_10_zapisz_liste_do_pliku,
    zadanie_11_dopisz_wpis,
    zadanie_12_zlicz_po_kluczu,
)


# --- zadanie_01 ---

def test_zadanie_01_zwraca_string() -> None:
    """Co testuje: czy json.dumps poprawnie serializuje słownik do stringa.
    Co udaje: nic — przekazuję słownik bezpośrednio.
    Co sprawdzam: wynik jest stringiem i po deserializacji zwraca klucz "imie" == "Anna".
    """
    # TODO: przygotuj slownik = {"imie": "Anna", "wiek": 30}
    # TODO: wywołaj zadanie_01_serializuj_slownik(slownik)
    # TODO: sprawdź isinstance(wynik, str) is True
    # TODO: sprawdź json.loads(wynik)["imie"] == "Anna"
    pass


def test_zadanie_01_liczba_zachowana_jako_int() -> None:
    """Co testuje: czy wartość liczbowa jest poprawnie serializowana (jako liczba, nie string).
    Co udaje: nic — przekazuję słownik z wartością int.
    Co sprawdzam: json.loads(wynik)["wiek"] == 30 (int, nie "30").
    """
    # TODO: przygotuj slownik = {"wiek": 30}
    # TODO: wywołaj zadanie_01_serializuj_slownik(slownik)
    # TODO: sprawdź json.loads(wynik)["wiek"] == 30
    pass


# --- zadanie_02 ---

def test_zadanie_02_zwraca_slownik() -> None:
    """Co testuje: czy json.loads poprawnie deserializuje string JSON do słownika.
    Co udaje: nic — podaję gotowy string JSON.
    Co sprawdzam: wynik to dict i wynik["imie"] == "Anna".
    """
    # TODO: przygotuj tekst = '{"imie": "Anna", "wiek": 30}'
    # TODO: wywołaj zadanie_02_deserializuj_string(tekst)
    # TODO: sprawdź isinstance(wynik, dict) is True
    # TODO: sprawdź wynik["imie"] == "Anna"
    pass


def test_zadanie_02_liczba_jako_int() -> None:
    """Co testuje: czy wartość liczbowa z JSON-a wraca jako int (nie string).
    Co udaje: nic — podaję string JSON z liczbą.
    Co sprawdzam: wynik["wiek"] == 30 i isinstance(wynik["wiek"], int) is True.
    """
    # TODO: przygotuj tekst = '{"wiek": 30}'
    # TODO: wywołaj zadanie_02_deserializuj_string(tekst)
    # TODO: sprawdź wynik["wiek"] == 30
    # TODO: sprawdź isinstance(wynik["wiek"], int) is True
    pass


# --- zadanie_03 ---

def test_zadanie_03_plik_zawiera_poprawny_json(tmp_path: Path) -> None:
    """Co testuje: czy po wywołaniu funkcji plik istnieje i zawiera poprawny JSON.
    Co udaje: nic — używam tmp_path jako cel zapisu.
    Co sprawdzam: wczytanie pliku przez json.load daje słownik z "imie" == "Anna".
    """
    # TODO: przygotuj p = tmp_path / "osoba.json" i slownik = {"imie": "Anna", "wiek": 30}
    # TODO: wywołaj zadanie_03_zapisz_do_pliku(str(p), slownik)
    # TODO: otwórz plik (encoding="utf-8") i sprawdź json.load(f)["imie"] == "Anna"
    pass


def test_zadanie_03_nadpisuje_istniejacy_plik(tmp_path: Path) -> None:
    """Co testuje: czy funkcja nadpisuje plik gdy już istnieje.
    Co udaje: nic — tworzę plik z innymi danymi przed wywołaniem.
    Co sprawdzam: po wywołaniu plik zawiera nowe dane (nie stare).
    """
    # TODO: przygotuj p = tmp_path / "osoba.json"
    # TODO: zapisz do p stary słownik przez p.write_text(json.dumps({"stare": "dane"}), encoding="utf-8")
    # TODO: wywołaj zadanie_03_zapisz_do_pliku(str(p), {"imie": "Piotr"})
    # TODO: otwórz plik i sprawdź json.load(f) == {"imie": "Piotr"} (nie stare dane)
    pass


# --- zadanie_04 ---

def test_zadanie_04_zwraca_slownik(plik_json_slownik: Path) -> None:
    """Co testuje: czy json.load poprawnie wczytuje słownik z pliku.
    Co udaje: nic — używam fixture plik_json_slownik.
    Co sprawdzam: wynik["imie"] == "Anna".
    """
    # TODO: wywołaj zadanie_04_wczytaj_z_pliku(str(plik_json_slownik))
    # TODO: sprawdź wynik["imie"] == "Anna"
    pass


def test_zadanie_04_liczba_wczytana_jako_int(plik_json_slownik: Path) -> None:
    """Co testuje: czy wartość liczbowa wczytana z pliku jest int (nie string).
    Co udaje: nic — używam fixture plik_json_slownik (zawiera "wiek": 30).
    Co sprawdzam: wynik["wiek"] == 30 i isinstance(wynik["wiek"], int) is True.
    """
    # TODO: wywołaj zadanie_04_wczytaj_z_pliku(str(plik_json_slownik))
    # TODO: sprawdź wynik["wiek"] == 30
    # TODO: sprawdź isinstance(wynik["wiek"], int) is True
    pass


# --- zadanie_05 ---

def test_zadanie_05_zwraca_string_z_wcieciami() -> None:
    """Co testuje: czy json.dumps z indent=2 produkuje wieloliniowy string.
    Co udaje: nic — przekazuję słownik bezpośrednio.
    Co sprawdzam: wynik jest stringiem i zawiera znak nowej linii (efekt indent).
    """
    # TODO: przygotuj slownik = {"imie": "Anna", "wiek": 30}
    # TODO: wywołaj zadanie_05_sformatowany_json(slownik, 2)
    # TODO: sprawdź isinstance(wynik, str) is True
    # TODO: sprawdź "\n" in wynik (indent dodaje nowe linie)
    pass


def test_zadanie_05_wynik_parsuje_sie_do_oryginalu() -> None:
    """Co testuje: czy sformatowany JSON po deserializacji daje oryginalny słownik.
    Co udaje: nic — przekazuję słownik bezpośrednio.
    Co sprawdzam: json.loads(wynik) == slownik (round-trip bez straty danych).
    """
    # TODO: przygotuj slownik = {"imie": "Anna", "wiek": 30}
    # TODO: wywołaj zadanie_05_sformatowany_json(slownik, 4)
    # TODO: sprawdź json.loads(wynik) == slownik
    pass


# --- zadanie_06 ---

def test_zadanie_06_zwraca_string() -> None:
    """Co testuje: czy json.dumps poprawnie serializuje listę słowników.
    Co udaje: nic — przekazuję listę bezpośrednio.
    Co sprawdzam: wynik jest stringiem i json.loads(wynik) ma 2 elementy.
    """
    # TODO: przygotuj lista = [{"imie": "Anna"}, {"imie": "Piotr"}]
    # TODO: wywołaj zadanie_06_serializuj_liste(lista)
    # TODO: sprawdź isinstance(wynik, str) is True
    # TODO: sprawdź len(json.loads(wynik)) == 2
    pass


def test_zadanie_06_pierwszy_element_zachowany() -> None:
    """Co testuje: czy po serializacji i deserializacji pierwszy element listy jest niezmieniony.
    Co udaje: nic — przekazuję listę bezpośrednio.
    Co sprawdzam: json.loads(wynik)[0]["imie"] == "Anna".
    """
    # TODO: przygotuj lista = [{"imie": "Anna", "wiek": 30}, {"imie": "Piotr", "wiek": 25}]
    # TODO: wywołaj zadanie_06_serializuj_liste(lista)
    # TODO: sprawdź json.loads(wynik)[0]["imie"] == "Anna"
    pass


# --- zadanie_07 ---

def test_zadanie_07_zwraca_liste_trzech_elementow(plik_json_lista: Path) -> None:
    """Co testuje: czy json.load wczytuje listę słowników z pliku.
    Co udaje: nic — używam fixture plik_json_lista (3 osoby).
    Co sprawdzam: wynik to lista z 3 elementami.
    """
    # TODO: wywołaj zadanie_07_wczytaj_liste_z_pliku(str(plik_json_lista))
    # TODO: sprawdź isinstance(wynik, list) is True
    # TODO: sprawdź len(wynik) == 3
    pass


def test_zadanie_07_pierwszy_element_to_anna(plik_json_lista: Path) -> None:
    """Co testuje: czy pierwszy element wczytanej listy ma poprawne dane.
    Co udaje: nic — używam fixture plik_json_lista.
    Co sprawdzam: wynik[0]["imie"] == "Anna" i wynik[0]["wiek"] == 30.
    """
    # TODO: wywołaj zadanie_07_wczytaj_liste_z_pliku(str(plik_json_lista))
    # TODO: sprawdź wynik[0]["imie"] == "Anna"
    # TODO: sprawdź wynik[0]["wiek"] == 30
    pass


# --- zadanie_08 ---

def test_zadanie_08_poprawny_json_zwraca_slownik() -> None:
    """Co testuje: czy funkcja zwraca słownik gdy tekst jest poprawnym JSON-em.
    Co udaje: nic — podaję poprawny string JSON.
    Co sprawdzam: wynik["imie"] == "Anna" (nie None).
    """
    # TODO: przygotuj tekst = '{"imie": "Anna", "wiek": 30}'
    # TODO: wywołaj zadanie_08_parsuj_bezpiecznie(tekst)
    # TODO: sprawdź wynik["imie"] == "Anna"
    pass


def test_zadanie_08_niepoprawny_json_zwraca_none() -> None:
    """Co testuje: kontrakt None gdy tekst nie jest poprawnym JSON-em.
    Co udaje: nic — podaję niepoprawny string.
    Co sprawdzam: wynik is None (nie wyjątek JSONDecodeError).
    """
    # TODO: przygotuj tekst = "to nie jest json"
    # TODO: wywołaj zadanie_08_parsuj_bezpiecznie(tekst)
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_09 ---

def test_zadanie_09_istniejacy_plik_zwraca_liste(plik_json_lista: Path) -> None:
    """Co testuje: czy funkcja wczytuje listę gdy plik istnieje i jest poprawny.
    Co udaje: nic — używam fixture plik_json_lista (3 osoby).
    Co sprawdzam: wynik to lista z 3 elementami (nie None).
    """
    # TODO: wywołaj zadanie_09_wczytaj_plik_bezpiecznie(str(plik_json_lista))
    # TODO: sprawdź len(wynik) == 3
    pass


def test_zadanie_09_brak_pliku_zwraca_none() -> None:
    """Co testuje: kontrakt None gdy plik nie istnieje.
    Co udaje: nic — używam ścieżki do pliku, który na pewno nie istnieje.
    Co sprawdzam: wynik is None (nie wyjątek FileNotFoundError).
    """
    # TODO: wywołaj zadanie_09_wczytaj_plik_bezpiecznie("nieistniejacy_plik.json")
    # TODO: sprawdź wynik is None
    pass


# --- zadanie_10 ---

def test_zadanie_10_plik_zawiera_liste(tmp_path: Path) -> None:
    """Co testuje: czy po wywołaniu funkcji plik zawiera poprawną listę JSON.
    Co udaje: nic — używam tmp_path jako cel zapisu.
    Co sprawdzam: wczytanie pliku przez json.load daje listę z 2 elementami.
    """
    # TODO: przygotuj p = tmp_path / "lista.json"
    # TODO: przygotuj lista = [{"imie": "Anna"}, {"imie": "Piotr"}]
    # TODO: wywołaj zadanie_10_zapisz_liste_do_pliku(str(p), lista)
    # TODO: otwórz plik (encoding="utf-8") i sprawdź len(json.load(f)) == 2
    pass


def test_zadanie_10_pusta_lista_tworzy_plik(tmp_path: Path) -> None:
    """Co testuje: czy pusta lista tworzy plik bez błędu i zawartość to [].
    Co udaje: nic — używam tmp_path.
    Co sprawdzam: wczytanie pliku daje [] (pusta lista, nie None ani błąd).
    """
    # TODO: przygotuj p = tmp_path / "lista.json"
    # TODO: wywołaj zadanie_10_zapisz_liste_do_pliku(str(p), [])
    # TODO: otwórz plik (encoding="utf-8") i sprawdź json.load(f) == []
    pass


# --- zadanie_11 ---

def test_zadanie_11_lista_rosnie_o_jeden(plik_json_lista: Path) -> None:
    """Co testuje: czy nowy słownik pojawia się w pliku po dopisaniu.
    Co udaje: nic — używam fixture plik_json_lista (3 osoby).
    Co sprawdzam: po wywołaniu lista w pliku ma 4 elementy.
    """
    # TODO: przygotuj nowy_wpis = {"imie": "Marek", "wiek": 28, "miasto": "Gdansk"}
    # TODO: wywołaj zadanie_11_dopisz_wpis(str(plik_json_lista), nowy_wpis)
    # TODO: otwórz plik (encoding="utf-8") i sprawdź len(json.load(f)) == 4
    pass


def test_zadanie_11_nowy_wpis_na_koncu(plik_json_lista: Path) -> None:
    """Co testuje: czy nowy wpis trafia na koniec listy (a nie na początku).
    Co udaje: nic — używam fixture plik_json_lista.
    Co sprawdzam: ostatni element listy to dopisany słownik z "imie" == "Marek".
    """
    # TODO: przygotuj nowy_wpis = {"imie": "Marek", "wiek": 28, "miasto": "Gdansk"}
    # TODO: wywołaj zadanie_11_dopisz_wpis(str(plik_json_lista), nowy_wpis)
    # TODO: otwórz plik (encoding="utf-8") i sprawdź json.load(f)[-1]["imie"] == "Marek"
    pass


# --- zadanie_12 ---

def test_zadanie_12_zlicza_po_miescie(plik_json_lista: Path) -> None:
    """Co testuje: czy funkcja poprawnie zlicza wpisy według wartości klucza "miasto".
    Co udaje: nic — używam fixture plik_json_lista (Warszawa×2, Krakow×1).
    Co sprawdzam: wynik == {"Warszawa": 2, "Krakow": 1}.
    """
    # TODO: wywołaj zadanie_12_zlicz_po_kluczu(str(plik_json_lista), "miasto")
    # TODO: sprawdź wynik == {"Warszawa": 2, "Krakow": 1}
    pass


def test_zadanie_12_pusta_lista_zwraca_pusty_slownik(tmp_path: Path) -> None:
    """Co testuje: czy plik z pustą listą JSON daje pusty słownik (nie błąd).
    Co udaje: nic — tworzę plik z "[]" przez tmp_path.
    Co sprawdzam: wynik == {}.
    """
    # TODO: przygotuj p = tmp_path / "pusta.json"
    # TODO: p.write_text("[]", encoding="utf-8")
    # TODO: wywołaj zadanie_12_zlicz_po_kluczu(str(p), "miasto")
    # TODO: sprawdź wynik == {}
    pass
