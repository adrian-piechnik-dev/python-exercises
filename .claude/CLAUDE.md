# Kontekst projektu — cwiczenia Python

To repo sluzy do generowania mini-kursow cwiczeniowych (nie portfolio).
Kazdy temat = jeden folder w cwiczenia/<temat_slug>/ z 4 plikami:
teoria.md, conftest.py, <temat_slug>.py, test_<temat_slug>.py

## ZAKAZY:
- Nie tworz podfolderow src/ ani tests/ w cwiczenia/ — struktura jest
  plaska, jeden folder = jeden temat, 4 pliki.
- Nigdy nie poprawiaj kodu usera samodzielnie podczas review — review
  wskazuje, user poprawia.
- Nigdy nie wypelniaj TODO za usera w szkieletach.

## STANDARDY TECHNICZNE (egzekwuj we wszystkich generowanych plikach):
- Type hinty na kazdej funkcji (takze testowej: -> None).
- Docstring w formacie Args/Returns; gdy funkcja bez argumentow,
  w Args wpisz "Brak." (nie zostawiaj pustej sekcji).
- is None / is True / is False — nigdy == None / == True.
- Dwie puste linie miedzy funkcjami (i przed pierwsza funkcja po importach).
- Kolejnosc importow: stdlib -> third-party -> local, grupy oddzielone
  pusta linia.
- Kontrakt funkcji: jeden typ zwracany albo None — nigdy string-jako-blad.
  Sygnalizacja bledu przez wyjatek lub None.
- Bez martwego kodu (nieuzywane importy, puste sekcje docstringa).
- Dla plikow CSV: open(..., newline=""), encoding="utf-8".

## KONWENCJA GIT (dla auto-commitow z /review-temat i pracy w repo):
- Commit messages po angielsku, tryb rozkazujacy ("Add csv exercises",
  nie "added csv exercises").
- git add TYLKO konkretnych sciezek — nigdy git add .
- Push po kazdym zamknietym temacie (repo synchronizowane miedzy
  dwoma komputerami).

## WORKFLOW:
Pelne reguly generowania nowego tematu i review — patrz slash commands:
/nowy-temat, /review-temat

Lista tematow, ich zakres i statusy: LISTA_TEMATOW_CWICZENIA.md w tym repo.
Przed /nowy-temat sprawdz tam status (nie duplikuj wygenerowanych).
Po /nowy-temat i /review-temat aktualizuj statusy zgodnie z zasada
auto-odhaczania opisana w tym pliku listy.