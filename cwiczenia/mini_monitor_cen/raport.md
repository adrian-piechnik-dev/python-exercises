# Raport — mini_monitor_cen

**Data:** 2026-07-26
**Tryb:** re-review nr 1

---

## Wynik pytest

```
............................                                             [100%]
28 passed in 0.17s
```

28 passed — poprawki niczego nie zepsuły.

---

## Status uwag z poprzedniej rundy

| # | Zadanie | Plik | Uwaga | Status |
|---|---------|------|-------|--------|
| 1 | 06 | `mini_monitor_cen.py` | 🔴 przecinek po ostatniej kolumnie w CREATE TABLE | ✅ NAPRAWIONE |
| 2 | 04 | `test_mini_monitor_cen.py` | 🟡 brak `assert len(wynik) == 2` mimo deklaracji w docstringu | ✅ NAPRAWIONE |
| 3 | 12 | `test_mini_monitor_cen.py` | 🟡 assert nie sprawdzał daty deklarowanej w docstringu | ✅ NAPRAWIONE |
| 4 | 05 | `test_mini_monitor_cen.py` | 🟡 brak type hinta parametru `sekundy` w `podmieniony_sleep` | ✅ NAPRAWIONE |

Szczegóły weryfikacji:

**1. Zadanie 06 (`mini_monitor_cen.py:126-131`)** — `data_odczytu TEXT` bez
przecinka, nawias zamykający czysty. SQL jest teraz składniowo poprawny dla
PostgreSQL, nie tylko dla atrapy.

**2. Zadanie 04 (`test_mini_monitor_cen.py:135`)** — `assert len(wynik) == 2`
dodany przed assertami na zawartość. Test faktycznie broni teraz pomijania
nieczytelnych cen: gdyby „Monitor" przeszedł przez filtr, test padnie.

**3. Zadanie 12 (`test_mini_monitor_cen.py:430-432`)** — pełne porównanie
listy krotek razem z datą `"2026-07-10"`. Docstring i asserty się zgadzają.

**4. Zadanie 05 (`test_mini_monitor_cen.py:180`, `:224`)** —
`def podmieniony_sleep(sekundy: float) -> None:` w obu testach. Hinty
w pliku spójne.

Nowych problemów w poprawianych fragmentach nie ma.

---

## Uwagi 🟢 — do zapamiętania na przyszłość

Poza uwagami blokującymi poprawiłeś też większość drobnych z poprzedniej
rundy: nowy słownik zamiast `del` w zadaniu 04, `_` przy rozpakowaniu
krotki, puste linie przed zagnieżdżonym `def`, zawijanie długich wywołań.
Zostały trzy kosmetyki:

**A. Zadanie 05 — `mini_monitor_cen.py:111` — pauza po ostatniej stronie**

`time.sleep(1)` przeniesiony na koniec pętli — pauza przed pierwszym
zapytaniem zniknęła, to była sedno uwagi. Zostaje jednak jedna zbędna
sekunda po ostatnim adresie: patrol już nic nie pobierze, a i tak czeka.
Docelowo pauza tylko wtedy, gdy zostały jeszcze adresy — np. `enumerate`
i `if i < len(adresy) - 1`. Test przechodzi w obu wariantach (2 adresy =
2 pauzy), więc to kwestia intencji, nie poprawności.

**B. Zadanie 12 — `test_mini_monitor_cen.py:431-432` — nadmiarowy assert**

```python
assert len(parametry) == 2
assert parametry == [("Klawiatura", 99.9, ...), ("Mysz", 49.0, ...)]
```

Drugi assert zawiera w sobie pierwszy — porównanie list sprawdza i długość,
i zawartość. Zostaw sam assert na równość; krótszy test, jeden powód
awarii. (Linia 432 ma przy okazji ~95 znaków — przy zawinięciu listy na
dwie linie zmieści się w limicie.)

**C. Zadanie 10 — `mini_monitor_cen.py:214-220` — łamanie SQL i trailing
whitespace**

Przejście na `"""` z argumentami w osobnych liniach wyprostowało wcięcie.
Dwie drobnostki: `ORDER BY data_odczytu` i `DESC LIMIT 1` są rozdzielone
łamaniem linii, choć `DESC` należy do `ORDER BY` — czytelniej
`ORDER BY data_odczytu DESC` w jednej linii, `LIMIT 1` w następnej. Do tego
linie 215-218 mają spacje na końcu (trailing whitespace, flake8 W291) —
warto włączyć w edytorze przycinanie przy zapisie.

---

## Werdykt

**ZALICZONE — gotowe do dalej**

Pytest zielony (28 passed), zero uwag 🔴, zero 🟡. Mini-projekt M3 zamknięty:
scraping + czyszczenie danych + PostgreSQL + testy z atrapą sieci i bazy
złożone w jeden działający pipeline z konsekwentnym kontraktem None
na całej długości.
