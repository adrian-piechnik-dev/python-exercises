# Review — funkcje_return_warunki

## Testy

```
52 passed in 0.09s
```

## Checklista techniczna

| Kryterium               | Wynik |
|-------------------------|-------|
| Type hinty              | ✅ wszystkie funkcje |
| Docstring Args/Returns  | ✅ wszystkie funkcje |
| `is None` (nie `== None`) | ✅ brak porównań == None |
| Kontrakt funkcji (None jako sygnał, nie string) | ✅ |
| Brak martwego kodu      | ✅ |
| Dwie puste linie między funkcjami | 🟡 patrz niżej |

## Uwagi

🟡 **zadanie_11 → zadanie_12 (linia 195–197):** tylko jedna pusta linia zamiast wymaganych dwóch.

```python
    # linia 195
        return False
                        ← jedna pusta linia
def zadanie_12_kategoria_bmi(...):   # linia 197
```

Poprawka: dodaj jedną pustą linię między tymi funkcjami.

## Ocena

Jeden drobny błąd PEP 8 (brak drugiej pustej linii). Logika, type hinty,
docstringi i kontrakt None — bez zastrzeżeń. Po poprawce: **gotowe do dalej**.
