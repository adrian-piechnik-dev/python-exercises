---
description: Generuje nowy mini-kurs cwiczeniowy dla podanego tematu
---

Temat do wygenerowania (TEMAT_SLUG): $ARGUMENTS

# PROCEDURA A — generowanie nowego tematu

## KROK 0 — zakres tematu (WIAZACY, nie improwizuj):
Przeczytaj wpis dla TEMAT_SLUG w LISTA_TEMATOW_CWICZENIA.md (root repo).
- Sekcja "Zakres" definiuje DOKLADNIE jakie pojecia pokrywa temat —
  ani mniej, ani wiecej.
- Sekcja "Zazebienie" definiuje, ktore pojecie z poprzedniego tematu
  MUSI wystapic w ostatnich 2-3 zadaniach (spirala nauki). Nie tlumacz
  tego pojecia od nowa w teorii — przypomnij jednym zdaniem, ze user
  zna je z poprzedniego tematu.
Jesli tematu nie ma na liscie — zatrzymaj sie i zapytaj usera.
Jesli status tematu to juz ✅ wygenerowany lub dalszy — zatrzymaj sie
i zapytaj usera, czy na pewno generowac ponownie.

## STRUKTURA WYJSCIOWA — TYLKO:
cwiczenia/<temat_slug>/
├── teoria.md
├── conftest.py           # szkielet z TODO
├── <temat_slug>.py       # szkielet z TODO, 10-15 zadan
└── test_<temat_slug>.py  # szkielet z TODO

Zadnych podfolderow src/ ani tests/. Zadnych innych plikow.

## PLIK teoria.md — reguly:
- Tlumacz jak 5-latkowi, ktory NIGDY nie programowal. Proste analogie
  z zycia codziennego (np. funkcja = ekspres do kawy: wsypujesz ziarna,
  dostajesz kawe).
- Pokryj DOKLADNIE tyle, ile potrzeba do wszystkich zadan i wszystkich
  TODO w conftest.py oraz test_<temat_slug>.py — nie wiecej, nie mniej.
- KAZDE pojecie uzyte w zadaniach/testach/conftest musi byc wyjasnione
  W TEORII, ZANIM sie pojawi. Nic z zewnatrz.
- Kazde nowe pojecie w schemacie: Co to jest? Skad sie wzielo?
  Dlaczego tak musi byc?
- Do kazdego pojecia sekcja "Typowe bledy poczatkujacych".
- Skladnia linijka po linijce, na PRAWDZIWYCH nazwach (nigdy
  placeholderow typu some_value, SomeException).
- PEP 8 wplataj jako element teorii, nie osobna faze.
- Teoria testowa (obowiazkowa czesc teoria.md):
  * po co jest conftest.py i co robi sys.path.insert (dlaczego testy
    nie widza modulu bez tego)
  * schemat 3 pytan (co testuje? / co udaje? / co sprawdzam?) —
    w osobnej sekcji, PRZED pierwszym odwolaniem do testow
  * schemat przygotuj -> podmien -> wywolaj -> sprawdz z przykladem
    na temacie INNYM niz zadania w tym pliku (zeby user nie mial
    gotowca do przepisania)
  * kazde narzedzie stdlib/pytest uzyte w tym temacie PIERWSZY RAZ
    (np. tmp_path, monkeypatch) — pelna teoria jak dla nowej biblioteki.

## PLIK <temat_slug>.py — reguly (JEDEN plik, 10-15 funkcji, SZKIELETY):
- Wszystkie zadania w jednym pliku, jedna funkcja = jedno zadanie.
- Nazwy funkcji ponumerowane i opisowe: zadanie_01_<opis>,
  zadanie_02_<opis>... (numer = kolejnosc/progresja).
- Na gorze pliku komentarz-spis: lista numerow zadan z jednozdaniowym
  opisem kazdego.
- Kazda funkcja: sygnatura z type hintami + docstring + komentarze # TODO:.
- Docstring w formacie:
  """Czasownik-opis co funkcja robi (jedno zdanie).

  Args:
      nazwa: co to jest.

  Returns:
      Typ: co zwraca. Gdy brak argumentow -> w Args wpisz "Brak."
  """
- # TODO: wskazuja DOKLADNIE co napisac w danym miejscu, krok po kroku,
  z konkretna wskazowka (metoda/wzorzec do uzycia), bezposrednio przed
  pass/..., np.:
      # TODO: uzyj slownik.get(klucz, domyslna)
      pass
- ZADNEGO kodu rozwiazania — kazda funkcja konczy sie pass lub ...
- Funkcja sygnalizujaca brak wartosci -> kontrakt na None (docstring
  to opisuje), nie string-jako-blad.

## PLIK conftest.py — reguly (SZKIELET z TODO):
- Sygnatura fixture/importu z type hintami gdzie dotyczy + docstring.
- # TODO: wskazujace dokladnie co wstawic (np. "# TODO: dodaj
  sys.path.insert wskazujacy na folder tematu, zeby test_<temat_slug>.py
  widzial <temat_slug>.py").
- Jesli temat wymaga fixture (np. plik tymczasowy) — sygnatura fixture
  z docstringiem + TODO z krokami, bez implementacji.

## PLIK test_<temat_slug>.py — reguly (SZKIELET z TODO):
- Import z <temat_slug>.py zostaje GOTOWY (nie TODO — bez tego user
  nie wie jakich nazw funkcji szukac).
- Grupuj testy per zadanie w kolejnosci jak w <temat_slug>.py;
  oddzielaj komentarzem-naglowkiem (# --- zadanie_01 ---).
- Kazda funkcja testowa: nazwa opisowa GOTOWA
  (test_zadanie_03_zwraca_none_gdy_pusta_lista), docstring
  z 3-question recipe WYPELNIONY konkretnie dla tego przypadku.
- Cialo testu: TODO w krokach schematu przygotuj -> podmien ->
  wywolaj -> sprawdz, BEZ gotowych assertow. Przyklad:
  ```python
  def test_zadanie_01_zwraca_none_gdy_plik_nie_istnieje() -> None:
      """Co testuje: kontrakt funkcji przy braku pliku.
      Co udaje: nic — uzywam prawdziwej nieistniejacej sciezki.
      Co sprawdzam: funkcja zwraca None zamiast rzucac wyjatek.
      """
      # TODO: przygotuj sciezke do pliku, ktory na pewno nie istnieje
      # TODO: wywolaj testowana funkcje z ta sciezka
      # TODO: sprawdz (assert ... is None) ze wynik to None
      pass
  ```
- Minimum 2 testy na zadanie (typowy + brzegowy) — nazwy i docstringi
  obu gotowe, ciala oba jako TODO.
- Testy NIE wymagaja zadnej wiedzy spoza teoria.md.

## REGULY KONSTRUKCJI ZADAN:
- Kazde zadanie rozwiazywalne WYLACZNIE na podstawie teoria.md.
- Rosnaca trudnosc, plynna progresja: zadanie_01 = najprostsze pojecie
  tematu, ostatnie = zlozenie kilku pojec w jednej funkcji.
- Ostatnie 2-3 zadania realizuja zazebienie z KROKU 0.
- Jedno zadanie = jedno male skupienie (nie upychaj 3 pojec w zadanie_02).

## STANDARDY TECHNICZNE:
Egzekwuj standardy z CLAUDE.md (type hinty, docstring Args/Returns,
is None, dwie puste linie, importy stdlib -> third-party -> local,
kontrakt None, brak martwego kodu, newline="" dla CSV).

## KROK KONCOWY:
1. Zmien status TEMAT_SLUG w LISTA_TEMATOW_CWICZENIA.md
   z ⬜ na ✅ wygenerowany (edytuj plik bezposrednio, bez pytania).
2. Wypisz komende do uruchomienia testow:
   pytest cwiczenia/<temat_slug>/test_<temat_slug>.py -v
3. Jednym zdaniem potwierdz, ile zadan wygenerowales.