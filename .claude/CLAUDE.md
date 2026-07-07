# Kontekst projektu — ćwiczenia Python

To repo służy do generowania mini-kursów ćwiczeniowych (nie portfolio).
Każdy temat = jeden folder w cwiczenia/<temat_slug>/ z 4 plikami:
teoria_<temat_slug>.md, conftest.py, <temat_slug>.py, test_<temat_slug>.py

ZAKAZ: nie twórz podfolderów src/ ani tests/ w cwiczenia/ — struktura
jest płaska, jeden folder = jeden temat, 4 pliki.

Standardy techniczne (type hinty, docstring Args/Returns, is None,
dwie puste linie, importy stdlib→third-party→local) — zgodnie z
INSTRUKCJA_PROJEKTU.md w głównym projekcie Claude.ai (poza tym repo).

Pełne reguły generowania nowego tematu i review — patrz slash commands:
/nowy-temat, /review-temat

Lista tematów i ich zakres: patrz LISTA_TEMATOW_CWICZENIA.md w tym repo.
  Sprawdź tam status przed /nowy-temat (nie duplikuj wygenerowanych).