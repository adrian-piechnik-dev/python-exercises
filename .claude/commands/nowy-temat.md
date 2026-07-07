---
description: Generuje nowy mini-kurs cwiczeniowy dla podanego tematu
---

Temat do wygenerowania: $ARGUMENTS

PROCEDURA A — nowy temat
Nazwa pliku wejsciowa: TEMAT_SLUG (np. "listy_petle")
Zmien w promptie generatora wszystkie wystapienia nazw:
  zadania.py       -> <TEMAT_SLUG>.py
  test_zadania.py  -> test_<TEMAT_SLUG>.py
  teoria.md        -> zostaje teoria.md (bez zmian)

Dodaj sekcje "SPIRALA — zazebienie z poprzednim tematem":
  Przed napisaniem teorii, przeczytaj teoria.md poprzedniego folderu
  w cwiczenia/. Ostatnie 2-3 zadania nowego tematu musza wymagac
  UZYCIA co najmniej jednego pojecia z poprzedniego tematu
  (np. warunek if w petli, funkcja z Etapu 1 uzyta w zadaniu o listach).
  Nie tlumacz tego pojecia od nowa w teorii — tylko przypomnij
  jednym zdaniem, ze juz je znasz z <nazwa_folderu_poprzedniego>.

Struktura wyjsciowa: TYLKO cwiczenia/<temat_slug>/
  {teoria.md, conftest.py, <temat_slug>.py, test_<temat_slug>.py}
  Zadnych podfolderow src/ ani tests/.

## PLIK conftest.py — reguly (SZKIELET z TODO, nie gotowy plik):
- Sygnatura fixture/importu z type hintami gdzie dotyczy + docstring.
- `# TODO:` wskazujace dokladnie co wstawic (np. "# TODO: dodaj sys.path.insert
  wskazujacy na folder tematu, zeby test_<temat_slug>.py widzial <temat_slug>.py").
- Jesli temat wymaga fixture (np. tmp_path, plik tymczasowy) — sygnatura fixture
  z docstringiem + TODO z krokami, bez implementacji.
- Teoria w teoria.md musi wczesniej wytlumaczyc PO CO jest conftest.py i co
  robi sys.path.insert, zanim user zobaczy TODO w tym pliku.

## PLIK test_<temat_slug>.py — reguly (SZKIELET z TODO, nie gotowe testy):
- Import z <temat_slug>.py zostaje gotowy (to nie jest TODO — bez tego user
  nie wie jakich nazw funkcji szukac).
- Kazda funkcja testowa: nazwa opisowa gotowa (test_zadanie_03_...), docstring
  z 3-question recipe (co testuje? co udaje? co sprawdzam?) WYPELNIONY konkretnie
  dla tego przypadku — to jest teoria zastosowana, nie TODO.
- Cialo testu: TODO w krokach schematu przygotuj -> podmien -> wywolaj -> sprawdz,
  BEZ gotowych assertow. Przyklad:
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
- Minimum 2 testy na zadanie (typowy + brzegowy) — nazwy i docstringi obu
  gotowe, ciala oba jako TODO.

## PLIK teoria.md — rozszerzenie zakresu:
- Teoria musi pokrywac NIE TYLKO pojecia z <temat_slug>.py, ale tez wszystko
  potrzebne do samodzielnego wypelnienia TODO w conftest.py i test_<temat_slug>.py:
  * co to jest fixture / sys.path / dlaczego testy nie widza modulu bez tego
  * schemat 3 pytan (co testuje/co udaje/co sprawdzam) — wyjasnic PRZED
    pierwszym testem w pliku, jednym razem, w osobnej sekcji
  * schemat przygotuj->podmien->wywolaj->sprawdz z przykladem na temacie
    INNYM niz zadania w tym pliku (zeby user nie mial gotowca do przepisania)
  * dowolne narzedzie stdlib/pytest pierwszy raz uzyte w tym temacie
    (np. tmp_path, monkeypatch) — pelna teoria jak dla nowej biblioteki,
    zgodnie z zasada "pierwsze uzycie nowej biblioteki standardowej"