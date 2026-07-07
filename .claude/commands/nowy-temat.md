---
description: Generuje nowy mini-kurs ćwiczeniowy dla podanego tematu
---

Temat do wygenerowania: $ARGUMENTS

PROCEDURA A — nowy temat
Nazwa pliku wejściowa: TEMAT_SLUG (np. "listy_petle")
Zmień w promptie generatora wszystkie wystąpienia nazw:
  zadania.py       → <TEMAT_SLUG>.py
  test_zadania.py  → test_<TEMAT_SLUG>.py
  teoria.md        → zostaje teoria.md (bez zmian)
Dodaj sekcję "SPIRALA — zazębienie z poprzednim tematem":
  Przed napisaniem teorii, przeczytaj teoria.md poprzedniego folderu
  w cwiczenia/. Ostatnie 2-3 zadania nowego tematu muszą wymagać
  UŻYCIA co najmniej jednego pojęcia z poprzedniego tematu
  (np. warunek if w pętli, funkcja z Etapu 1 użyta w zadaniu o listach).
  Nie tłumacz tego pojęcia od nowa w teorii — tylko przypomnij
  jednym zdaniem, że już je znasz z <nazwa_folderu_poprzedniego>.
Struktura wyjściowa: TYLKO cwiczenia/<temat_slug>/
  {teoria.md, conftest.py, <temat_slug>.py, test_<temat_slug>.py}
  Żadnych podfolderów src/ ani tests/.