# RAPORT SPÓJNOŚCI: PLAN_REORGANIZACJI v3 vs CC_Cwiczenia (stan 21.07.2026)

## BLUF

**Spójne w 85% — 3 konkretne korekty w PLAN_REORGANIZACJI, żadna nie psuje logiki.** 
Statusy w LISTA_TEMATOW są aktualne; plan był pisany na podstawie wcześniejszej wersji, 
więc kilka kroków jest zdeduplikowanych albo nieaktualne. Integracja strategii portfolio 
(4 projekty P1–P4) ze ścieżką CC (M0–M4, szablony tpl-*) jest architektonicznie solidna.

---

## FAKTYCZNE STATUSY (zweryfikowane: TODO + raport.md)

### Blok 1–18: pełna gotowość
✅ tematy 1–18 wykonane i sprawdzone (wszystkie mają raport.md, zero TODO)

### Blok 19–22: **GOTOWE** (ale plan mówi "wykonaj")
| Temat | TODO | Raport | Status w LISTA | Plan każe |
|---|---|---|---|---|
| 19 llm_api_klient | 0 | ✅ | ✅ sprawdzony | Etap 1: "wykonaj" ❌ |
| 20 llm_structured_extraction | 0 | ✅ | ✅ sprawdzony | Etap 1: "wykonaj" ❌ |
| 21 docker_podstawy | 0 | ✅ | ✅ sprawdzony | Etap 5: "wykonaj" ❌ |
| 22 github_actions_ci | 0 | ✅ | ✅ sprawdzony | Etap 1.5: "wykonaj" ❌ |

### Blok 23–25: szkielety z TODO (plan OK)
| Temat | TODO | Status w LISTA | Plan każe |
|---|---|---|---|
| 23 async_httpx | 31 | ✅ wygenerowany | Etap 5: opcjonalnie ✅ |
| 24 playwright_podstawy | 36 | ✅ wygenerowany | P4: nie wspominane jawnie ✅ |
| 25 playwright_pytest_network | 28 | ✅ wygenerowany | P4: nie wspominane jawnie ✅ |

### Blok MP1–MP3: mini-projekty treningowe (plan OK)
| Mini-projekt | TODO | Status w LISTA | Plan każe |
|---|---|---|---|
| MP1 mini_raport_wydatkow | 25 | ✅ wygenerowany | Etap 3: "wykonaj" ✅ |
| MP2 mini_api_katalog | 23 | ✅ wygenerowany | nie wspominane ⚠️ |
| MP3 mini_monitor_cen | 27 | ✅ wygenerowany | Etap 5: opcjonalnie ✅ |

---

## ROZBIEŻNOŚCI I KOREKTY

### Rozbieżność 1: Etap 1 każe "wykonać" 19–20, które są gotowe

**Miejsce w planie:** sekcja "ETAP 1 — P1 `smartscraper-ai`"

```markdown
- [ ] Wykonaj tematy 19 (`llm_api_klient`) i 20 (`llm_structured_extraction`) 
      w cyklu Explore→Plan→Code→Commit
```

**Rzeczywistość:** tematy 19–20 są `✅ sprawdzony` — masz gotowy kod do ekstrakcji AI.

**Korekta:**
```markdown
- [ ] Wykorzystaj gotowy kod z tematów 19–20 (`llm_api_klient`, 
      `llm_structured_extraction`) jako moduł ekstrakcji AI do P1
- [ ] Wehikuł M0 (pełny cykl EPCC) → przenieś na `async_httpx` (temat 23) 
      zamiast powtórki 19–20
```

**Wpływ:** zmniejsza pracę w Etapie 1 (~1 dzień), ale zmienia gdzie zaliczasz M0.

---

### Rozbieżność 2: Etap 1.5 każe "wykonać" temat 22, który jest gotowy

**Miejsce:** sekcja "ETAP 1.5 — Przygotowanie pod szablony"

```markdown
- [ ] Wykonaj temat 22 (`github_actions_ci`) — szablony M1 wymagają stubu Actions
```

**Rzeczywistość:** temat 22 jest `✅ sprawdzony` — znasz workflow YAML i know-how.

**Korekta:**
```markdown
- [ ] Know-how GitHub Actions masz już (temat 22 ✅ sprawdzony). 
      Przy budowie szablonów tpl-* (Etapy 2–4) wklej stubs Actions bezpośrednio 
      z gotowego kodu — bez powtórki.
```

**Wpływ:** usuwa duplikat, skraca harmonogram.

---

### Rozbieżność 3: Etap 5 każe "wykonać" temat 21, który jest gotowy

**Miejsce:** sekcja "ETAP 5 — Docker + P5 opcjonalny"

```markdown
- [ ] Wykonaj temat 21 (`docker_podstawy`) → Dockerfile w P1 i P4
```

**Rzeczywistość:** temat 21 jest `✅ sprawdzony` — znasz Dockerfile i docker-compose.

**Korekta:**
```markdown
- [ ] Dockerfile w P1 i P4 (wiesz już ze struktury z tematu 21 ✅). 
      Przy Selenium (P4): flagi --no-sandbox/--disable-gpu per zazębienie LISTA_TEMATOW.
```

**Wpływ:** skraca Etap 5.

---

### Rozbieżność 4: Mini-projekty (MP1–MP3) nie są jasno mapowane w planie

**Miejsce:** plan wspomina MP1 (Etap 3) i MP3 (Etap 5 opcjonalnie), ale MP2 nie pojawia się.

**Rzeczywistość:** MP2 `mini_api_katalog` to też gotowy szkielet (TODO 23), logicznie byłby w Etapie 2 (budowa `tpl-fastapi`).

**Korekta:**
```markdown
ETAP 1.5 (po wyjaśnieniu "czemu nie powtarzamy 19–22"):
Mapowanie mini-projektów na etapy:
- MP1 (`mini_raport_wydatkow`) → trening do Etapu 3 (tpl-etl) ✅ już w planie
- MP2 (`mini_api_katalog`) → trening do Etapu 2 (tpl-fastapi) ⚠️ brakuje w planie
- MP3 (`mini_monitor_cen`) → trening do Etapu 5 opcjonalnie ✅ już w planie
```

**Wpływ:** wyjaśnia gdzie robisz MP2, nie zmienia harmonogramu (to trening, nie blokujący projekt).

---

## ZAGADNIENIE: WEHIKUŁ M0

Plan pisząc:
> Tematy 19–20 robisz JUŻ nowym workflow (plan mode, EPCC) — zalicza M0 bez osobnego zadania

**Problem:** tematy 19–20 są JUŻ gotowe ze starego workflow. Nie możesz ich "robić nowym workflow".

**Rozwiązanie:** Wehikuł M0 (zaliczenie exit criteria fundamentu: "1 temat w pełnym cyklu EPCC, 
clean review verdict, ani razu nie kodowałeś przed zatwierdzeniem planu") — przenieś na:

1. **Opcja A (rekomendowana):** temat 23 `async_httpx` (pierwsza niezrobiona rzecz, jeszcze jej nie robiłeś nowym workflow)
2. **Opcja B:** budowa `tpl-scraper` od zera w plan mode (to de facto "temat 26" — nowa treść)
3. **Opcja C:** remodelacja jednego istniejącego tematu przez plan mode (bardziej formalna, mniej praktyki)

Rekomendacja: **Opcja A** — temat 23 trzeba robić tak czy inaczej, a jednocześnie zaliczysz M0.

---

## MAPA KOREKT DO NANIESIENIA W PLAN_REORGANIZACJI.md

| Sekcja | Linia (przybliżona) | Zmiana |
|---|---|---|
| Etap 1 intro | ~218 | Usuń "Tematy 19–20 robisz JUŻ nowym workflow"; zmień na "Wykorzystaj kod z 19–20" + wyjaśnienie wehikułu M0 |
| Etap 1 checklist | ~223–224 | Zmień "Wykonaj tematy 19–20" na "Wykorzystaj kod tematów 19–20 do P1" |
| Etap 1 checklist | nowy punkt | Dodaj "Wehikuł M0: wykonaj temat 23 (`async_httpx`) w pełnym cyklu EPCC" |
| Etap 1.5 intro | ~195 | Usuń "Temat 22 wymagane do stubu Actions"; zmień na "Know-how masz, wklej stubs z kodu" |
| Etap 1.5 checklist | ~197 | Usuń checbox "Wykonaj temat 22" |
| Etap 5 intro | ~226 | Usuń "Wykonaj temat 21"; zmień na "Know-how masz, stosuj strukturę Dockerfile" |
| Etap 5 checklist | ~228 | Usuń checbox "Wykonaj temat 21" |
| Nowy punkt | po Etap 1 | Dodaj mapowanie MP1–MP3 na etapy: MP2 → Etap 2 (tpl-fastapi) |

---

## WERDYKT SPÓJNOŚCI

| Wymiar | Ocena | Notatka |
|---|---|---|
| **Architektura (4 projekty → 4 szablony)** | ✅ spójna | 1:1 mapowanie P1–P4 ↔ tpl-scraper, tpl-fastapi, tpl-etl, tpl-selenium-pom jest czyste |
| **Integracja ze ścieżką CC (M0–M4)** | ✅ spójna | Moduły i bramki (M2 weryfikacja, M3 sandbox) logicznie umieszczone; jednak wehikuł M0 wymaga podmiany |
| **Tematy 19–22** | ⚠️ duplikaty | Plan każe "wykonać", faktycznie już wykonane; 4 zbędy checboxy, 0 realnej pracy |
| **Mini-projekty MP1–MP3** | ⚠️ niejednorodne | MP1 ✅, MP3 ✅ w planie; MP2 jest ale nie wspominane; można jasniej |
| **Timeline** | ✅ realistyczny po korekcie | Duplikaty usunięte = przyspieszenie (~2–3 dni na Etapach 1, 1.5, 5) |
| **Propozycje (P1–P4)** | ✅ spójne ze strategią | Mapowanie do kategorii Useme, stawek, popytu — OK |

---

## PODSUMOWANIE: CO ROBIĆ

1. ✅ **PLAN_REORGANIZACJI.md jest fundamentalnie SPÓJNY.** Architektura (portfolio 4 projektów mapa na 4 szablony CC) 
   i integracja (M0–M4) są solidne.

2. ⚠️ **Ale wymaga 5–7 linii korekt,** nie merytorycznych:
   - Usuń "wykonaj 19–20, 21–22" (duplikaty, robisz je do innego celu — kodu do P1)
   - Przenieś wehikuł M0 z "powtórka 19–20" na "temat 23 nowy"
   - Wyjaśnij, że know-how Actions/Docker masz, tylko aplikujesz, nie uczysz się

3. ✅ **Harmonogram po korekcie = oszczędność ~2–3 dni**, spokojniej do czasu Etapu 1.

4. 🔴 **LISTA_TEMATOW jest dokładna** — statusy są aktualne, nie trzeba tam nic zmieniać.

Chcesz, żebym przepisał PLAN_REORGANIZACJI.md z tymi 5–7 liniami korekt?
