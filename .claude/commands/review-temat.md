---
description: Review + raport dla wykonanych zadań danego tematu
---

Folder tematu do sprawdzenia: $ARGUMENTS

PROCEDURA B — review + raport
Po zgłoszeniu "zadania wykonane, testy zielone":
1. Uruchom pytest w folderze tematu, wklej realny output.
2. Przeczytaj <temat_slug>.py — sprawdź zgodność z checklistą techniczną
   z INSTRUKCJI_PROJEKTU.md (type hinty, docstring Args/Returns,
   is None, dwie puste linie, brak martwego kodu, kontrakt funkcji).
3. Wygeneruj raport.md w folderze tematu:
   - jeśli OK: 3-4 linijki podsumowania + "gotowe do dalej"
   - jeśli nie: lista 🔴🟡🟢 z numerem zadania + konkretna poprawka