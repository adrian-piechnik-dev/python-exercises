---
description: Review + raport dla wykonanych zadan danego tematu (z obsluga re-review i auto-commit)
---

Folder tematu do sprawdzenia: $ARGUMENTS

PROCEDURA B — review + raport

## KROK 0 — rozpoznanie trybu (pierwszy review czy re-review):
Sprawdz, czy w cwiczenia/<temat_slug>/ istnieje plik raport.md.
- NIE istnieje -> TRYB PELNY (krok 1)
- istnieje -> TRYB RE-REVIEW (krok 2)

## KROK 1 — TRYB PELNY (pierwszy review):
1. Uruchom pytest w folderze tematu; realny output pytest MUSI znalezc sie
   w raporcie (sekcja "Wynik pytest"). Jesli ktorykolwiek test czerwony —
   przerwij review, w raporcie wpisz tylko liste failujacych testow
   i komunikat "najpierw doprowadz testy do zielonych".
2. Przeczytaj WSZYSTKIE pliki uzupelniane przez usera:
   <temat_slug>.py, test_<temat_slug>.py, conftest.py.
   Sprawdz zgodnosc z checklista techniczna:
   - type hinty na kazdej funkcji (takze testowej: -> None)
   - docstring w formacie Args/Returns (Args: "Brak." gdy bez argumentow)
   - is None / is True / is False — nigdy == None / == True
   - dwie puste linie miedzy funkcjami
   - brak martwego kodu (nieuzywane importy, TODO po zrobieniu,
     zmienne utworzone i nieuzyte, zbedne pass po implementacji)
   - kontrakt funkcji: jeden typ zwracany albo None, nigdy string-jako-blad
   - kolejnosc importow: stdlib -> third-party -> local
   - w testach: schemat przygotuj -> podmien -> wywolaj -> sprawdz zachowany,
     asserty sprawdzaja to, co deklaruje docstring testu
   - dla plikow/CSV (gdy temat dotyczy): newline="", encoding="utf-8",
     zamykanie przez with
3. Przejdz do KROKU 3 (raport).

## KROK 2 — TRYB RE-REVIEW (raport.md juz istnieje):
1. Przeczytaj istniejacy raport.md i wypisz z niego liste uwag 🔴/🟡
   (numer zadania + plik + tresc uwagi).
2. Uruchom pytest w folderze tematu (zawsze, nawet w re-review —
   poprawka mogla zepsuc cos innego). Czerwony test = przerwij jak w kroku 1.
3. Sprawdz TYLKO fragmenty kodu wskazane w uwagach z poprzedniego raportu
   (te funkcje / te testy / te linie). NIE robiij ponownego pelnego audytu
   plikow bez uwag.
4. Dla kazdej uwagi z poprzedniego raportu okresl status:
   - NAPRAWIONE (poprawka zgodna z zaleceniem lub rownowazna)
   - NIENAPRAWIONE (uwaga nadal aktualna — powtorz ja w nowym raporcie)
   - NOWY PROBLEM (poprawka wprowadzila nowy blad w TYM fragmencie —
     opisz jako nowa uwage)
5. Przejdz do KROKU 3 (raport).

## KROK 3 — RAPORT (wspolny dla obu trybow):
Nadpisz raport.md w folderze tematu — nadpisuj bez pytania o potwierdzenie
(nie twor raport_2.md ani kopii zapasowej; jeden plik, zawsze aktualny stan,
historia poprzednich wersji zyje w git).
Struktura raportu:
- Data + tryb (pelny / re-review nr N)
- Wynik pytest (skopiowany realny output, min. podsumowanie X passed)
- Lista uwag 🔴🟡🟢 z numerem zadania i plikiem + konkretna poprawka
  (w re-review: takze status uwag z poprzedniej rundy)
- Werdykt: "DO POPRAWY" albo "ZALICZONE — gotowe do dalej"

## KROK 4 — AUTO-COMMIT (TYLKO gdy werdykt = ZALICZONE):
Warunek: pytest zielony ORAZ zero uwag 🔴 ORAZ zero uwag 🟡
(🟢 drobne nie blokuja zaliczenia — wypisz je w raporcie jako
"do zapamietania na przyszlosc").
Wykonaj:
1. Zaktualizuj status tematu w LISTA_TEMATOW_CWICZENIA.md na ✅ sprawdzony.
2. git add cwiczenia/<temat_slug>/ LISTA_TEMATOW_CWICZENIA.md
   (add TYLKO te sciezki — nie git add . — zeby nie wciagnac
   przypadkowych plikow spoza tematu)
3. git commit -m "Complete: <temat_slug> exercises reviewed and passed"
4. git push
5. Wypisz userowi potwierdzenie: co skomitowano i ze temat zamkniety.
Gdy werdykt = DO POPRAWY: ZADNEGO commita. Wypisz liste uwag
i czekaj na poprawki (nastepne wywolanie /review-temat wejdzie
w TRYB RE-REVIEW).

## ZASADY OGOLNE:
- Nigdy nie poprawiaj kodu usera samodzielnie podczas review —
  review wskazuje, user poprawia.
- Realny output pytest jest obowiazkowy w kazdym raporcie —
  "testy przechodza" bez outputu nie istnieje.
- Statusy w LISTA_TEMATOW_CWICZENIA.md:
  ✅ wykonany — ustaw po pierwszym review, gdy wszystkie TODO uzupelnione
  (nawet jesli sa uwagi do poprawy)
  ✅ sprawdzony — ustaw TYLKO przy werdykcie ZALICZONE (krok 4)