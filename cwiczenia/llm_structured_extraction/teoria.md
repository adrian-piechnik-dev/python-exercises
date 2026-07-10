# LLM — ekstrakcja strukturalna (prompt → JSON → dane)

> Znasz już json.loads i JSONDecodeError z tematu 7 oraz klienta API
> (nagłówki, payload, requests.post, raise_for_status) z tematu 19.
> W tym temacie nauczysz się prosić model o odpowiedź w formacie JSON
> i defensywnie ją parsować — bo model to nie baza danych i potrafi
> odpowiedzieć "po swojemu".

---

## Co to jest ekstrakcja strukturalna

Gdy pytasz model "opowiedz o Annie", dostajesz wypracowanie. Gdy potrzebujesz
DANYCH (imię, wiek — do zapisania w bazie czy CSV), wypracowanie jest
bezużyteczne. Ekstrakcja strukturalna to prośba: "przeczytaj tekst i zwróć
wynik jako FORMULARZ" — czyli JSON o ustalonych polach. Zamiast eseju
dostajesz `{"imie": "Anna", "wiek": 30}` i możesz to od razu przetworzyć.

Problem: model tylko OBIECUJE, że zwróci JSON. Czasem doklei komentarz,
owinie odpowiedź w blok markdown albo odmówi. Dlatego połowa tego tematu
to defensywne parsowanie.

---

## Prompt z szablonem JSON — podwójne klamry w f-stringu

Prompt (polecenie dla modelu) musi POKAZAĆ oczekiwany format:

```
Wyciagnij z tekstu imie i wiek. Zwroc TYLKO JSON w formacie
{"imie": "...", "wiek": 0}. Tekst: Anna ma 30 lat.
```

Chcesz zbudować taki prompt f-stringiem, wstawiając `tekst` użytkownika.
Ale f-string traktuje `{` i `}` jako "tu wstaw zmienną" — a Ty potrzebujesz
LITERALNYCH klamr w szablonie JSON. Rozwiązanie: podwójna klamra.
`{{` w f-stringu daje znak `{`, a `}}` daje znak `}`:

```python
prompt = f'Zwroc TYLKO JSON w formacie {{"imie": "...", "wiek": 0}}. Tekst: {tekst}'
```

Czytaj: `{{` → `{`, potem zwykły tekst szablonu, `}}` → `}`,
a `{tekst}` (pojedyncze klamry) to normalne wstawienie zmiennej.

Da się też budować szablon DYNAMICZNIE — z listy nazw pól. Środek szablonu
sklejasz przez `", ".join(...)` (znasz join z wcześniejszych tematów):

```python
srodek = ", ".join(f'"{pole}": "..."' for pole in pola)
prompt = f'Zwroc TYLKO JSON w formacie {{{srodek}}}. Tekst: {tekst}'
```

Uwaga na POTRÓJNĄ klamrę `{{{srodek}}}`: to `{{` (literalna klamra
otwierająca) + `{srodek}` (wstawienie zmiennej) + `}}` (literalna
zamykająca). Dla `pola = ["imie", "wiek"]` środek to
`"imie": "...", "wiek": "..."`, a cały fragment:
`{"imie": "...", "wiek": "..."}`.

### Typowe błędy — klamry w f-stringu
- Pojedyncza klamra w szablonie: `f'... {"imie": ...}'` — Python próbuje
  potraktować zawartość jako wyrażenie i rzuca błąd składni albo
  wstawia coś nieoczekiwanego. Literalna klamra ZAWSZE podwójna.
- Podwojenie także klamry wstawiającej zmienną: `{{tekst}}` — dostaniesz
  dosłownie `{tekst}` zamiast wartości zmiennej.

---

## Model owija JSON w markdown — czyszczenie odpowiedzi

Modele często zwracają JSON w bloku kodu markdown:

```
```json
{"imie": "Anna", "wiek": 30}
```
```

Takiego stringa `json.loads` NIE sparsuje — trzeba najpierw zdjąć
"opakowanie". Do tego służą metody stringów `removeprefix`
i `removesuffix` (są w Pythonie od wersji 3.9):

```python
tekst = tekst.removeprefix("```json")
tekst = tekst.removesuffix("```")
```

- `removeprefix("```json")` — jeśli string ZACZYNA SIĘ od `` ```json ``,
  zwraca string bez tego początku; jeśli NIE zaczyna się — zwraca string
  BEZ ZMIAN (żadnego wyjątku). To czyni je idealnymi do defensywnego
  czyszczenia: kod działa i dla owiniętej, i dla czystej odpowiedzi.
- `removesuffix("```")` — to samo, ale dla końcówki.
- Obie metody ZWRACAJĄ NOWY string (stringi są niezmienne) — wynik trzeba
  przypisać albo od razu zwrócić.

Pełne czyszczenie wymaga jeszcze `strip()` (usuwa białe znaki i entery
z obu końców) — PRZED zdjęciem prefiksu (żeby prefiks był naprawdę
na początku) i PO zdjęciu (bo po `` ```json `` zostaje enter):

```python
czysty = (
    tekst
    .strip()
    .removeprefix("```json")
    .removeprefix("```")
    .removesuffix("```")
    .strip()
)
```

Drugi `removeprefix("```")` łapie przypadek, gdy model otworzył blok
samym `` ``` `` bez słowa `json`.

### Typowe błędy — czyszczenie markdown
- `tekst.strip("```json")` — `strip` z argumentem usuwa ZNAKI z podanego
  zbioru (każde `` ` ``, `j`, `s`, `o`, `n` z obu końców!), nie prefiks.
  Do prefiksu służy `removeprefix`.
- Zapomnienie o przypisaniu: `tekst.removeprefix("```json")` w osobnej
  linii bez `tekst =` — string się nie zmienia.
- Brak `strip()` po zdjęciu prefiksu — zostaje `\n` na początku
  (akurat `json.loads` go toleruje, ale porównania w testach już nie).

---

## Dwie warstwy błędu JSON

W odpowiedzi API JSON występuje na DWÓCH poziomach i każdy psuje się inaczej:

**Warstwa 1 — struktura odpowiedzi API (koperta).** Serwer zwraca słownik,
w którym tekst modelu siedzi pod `dane["content"][0]["text"]` — znasz to
z tematu 19. Gdy serwer zwróci błąd, klucza `"content"` nie ma (`KeyError`)
albo lista bloków jest pusta (`IndexError`).

**Warstwa 2 — treść wygenerowana przez model.** Nawet gdy koperta jest
poprawna, TEKST w środku może nie być JSON-em — model mógł odmówić albo
dopisać komentarz. `json.loads` (temat 7) rzuca wtedy
`json.JSONDecodeError`:

```python
try:
    dane = json.loads(tekst)
except json.JSONDecodeError:
    return None
```

Obie warstwy obsługujesz OSOBNO, bo psują się z innych powodów i łapiesz
inne wyjątki. Kontrakt obu funkcji: słownik albo `None` — nigdy
string-jako-błąd.

### Typowe błędy — dwie warstwy
- Jeden wielki try łapiący `Exception` na wszystko — nie wiesz, CO się
  zepsuło (koperta czy treść), i połykasz też błędy programistyczne.
- Łapanie `JSONDecodeError` przy sięganiu do `dane["content"]` — tam
  grożą `KeyError`/`IndexError`; `JSONDecodeError` rzuca tylko `json.loads`.

---

## Klient API — przypomnienie z tematu 19

Zapytanie do modelu budujesz i wysyłasz dokładnie tak jak w temacie 19:
nagłówki (`x-api-key`, `anthropic-version: 2023-06-01`,
`content-type: application/json`), payload (`model`, `max_tokens`,
`messages` z rolą `user`), `requests.post(url, headers=..., json=...,
timeout=30)`, potem `raise_for_status()` i `.json()`. W tym temacie
klient to tylko jeden krok potoku — nowością jest to, co robisz
z odpowiedzią.

---

## Teoria testowa

conftest.py i `sys.path.insert` znasz z poprzednich tematów — dzięki nim
testy widzą moduł `llm_structured_extraction.py`.

### Schemat 3 pytań

1. **Co testuje?** — jaką konkretną wartość lub efekt sprawdzam
2. **Co udaje?** — co podmieniam zamiast prawdziwego środowiska
3. **Co sprawdzam?** — jakie twierdzenie zawiera assert

### mock — unittest.mock.patch i MagicMock

W temacie 19 podmieniałeś funkcje przez `monkeypatch`. Teraz poznasz
`patch` z modułu `unittest.mock` (stdlib) — drugie, bardzo popularne
narzędzie do podmian, wygodniejsze, gdy atrapa ma coś ZWRACAĆ.

```python
from unittest.mock import patch
```

`patch` używasz jako context managera (blok `with`, znasz z plików):

```python
with patch("kuchnia.odczytaj") as atrapa:
    atrapa.return_value = 150.0
    wynik = czy_wlaczyc_piekarnik()
```

Linijka po linijce:
- `patch("kuchnia.odczytaj")` — na czas bloku `with` podmienia
  `odczytaj` w module `kuchnia` na obiekt MagicMock; po wyjściu z bloku
  oryginał wraca automatycznie (jak przy monkeypatch),
- `as atrapa` — dostajesz ten MagicMock do ręki,
- `atrapa.return_value = 150.0` — ustawiasz, co atrapa ZWRÓCI, gdy
  testowany kod ją wywoła.

**MagicMock** to obiekt-kameleon: każdy atrybut i każda metoda, o którą
go poprosisz, powstaje automatycznie i też jest MagicMockiem. Dzięki temu
można łańcuchowo skonfigurować głębsze wywołania:

```python
with patch("requests.post") as atrapa_post:
    atrapa_post.return_value.json.return_value = {"content": []}
```

Czytaj od lewej: `atrapa_post.return_value` to obiekt, który zwróci
`requests.post(...)` (udawana odpowiedź); jego metoda `.json()` ma
zwrócić `{"content": []}`. Wywołanie `raise_for_status()` na MagicMocku
po prostu przejdzie (auto-utworzona metoda nic nie robi) — sukces gratis.

MagicMock pamięta też, JAK go wywołano: `atrapa.call_args.kwargs` to
słownik argumentów nazwanych ostatniego wywołania, np.
`atrapa_post.call_args.kwargs["timeout"]` da `30`, jeśli testowany kod
przekazał `timeout=30`.

### patch "tam gdzie używane" — najważniejsza reguła mocka

String w `patch("...")` to adres miejsca, w którym testowany kod
WYSZUKUJE nazwę w momencie wywołania — nie miejsca, gdzie funkcję
zdefiniowano. Przykład z INNEJ dziedziny:

```python
# plik czujnik.py
def odczytaj() -> float:
    ...  # czyta prawdziwy sprzęt


# plik kuchnia.py
from czujnik import odczytaj


def czy_wlaczyc_piekarnik() -> bool:
    """Włącza piekarnik poniżej 180 stopni.

    Args:
        Brak.

    Returns:
        bool: True, gdy odczyt temperatury jest mniejszy niż 180.0.
    """
    return odczytaj() < 180.0
```

Przez `from czujnik import odczytaj` moduł `kuchnia` ma WŁASNĄ nazwę
`odczytaj`. Patchowanie `"czujnik.odczytaj"` nic nie da — `kuchnia`
dalej trzyma starą referencję. Poprawnie: `patch("kuchnia.odczytaj")` —
tam, gdzie nazwa jest używana.

Schemat przygotuj → podmień → wywołaj → sprawdź w komplecie:

```python
def test_piekarnik_wlacza_sie_przy_niskiej_temperaturze() -> None:
    """Co testuje: decyzję o włączeniu piekarnika poniżej progu.
    Co udaje: odczyt czujnika — patch w module kuchnia, return_value=150.0.
    Co sprawdzam: funkcja zwraca True.
    """
    # przygotuj + podmień
    with patch("kuchnia.odczytaj") as atrapa:
        atrapa.return_value = 150.0

        # wywołaj
        wynik = czy_wlaczyc_piekarnik()

    # sprawdź
    assert wynik is True
```

A kiedy `patch("requests.post")` jednak działa? Gdy testowany moduł robi
`import requests` i woła `requests.post(...)` — wtedy nazwa `post` jest
wyszukiwana NA MODULE `requests` w chwili wywołania, a właśnie ją
podmieniłeś. Reguła jest jedna i ta sama: patchuj tam, gdzie nazwa jest
szukana.

W tym temacie użyjesz obu wariantów:
- `patch("requests.post")` — dla funkcji wysyłającej zapytanie
  (moduł robi `import requests`),
- `patch("llm_structured_extraction.zadanie_10_zapytaj_model")` — dla
  funkcji-potoków, które wołają klienta po nazwie ze swojego modułu.

### Typowe błędy — mock
- Patchowanie modułu definiującego zamiast używającego przy from-import —
  atrapa wisi w próżni, prawdziwa funkcja dalej działa.
- Konfigurowanie `return_value` PO wywołaniu testowanej funkcji —
  kolejność: podmień i skonfiguruj, dopiero potem wywołaj.
- `atrapa.return_value.json = {...}` zamiast
  `atrapa.return_value.json.return_value = {...}` — `json` to METODA,
  więc ustawiasz jej `return_value`, nie ją samą.
- Wywołanie testowanej funkcji POZA blokiem `with` — patch już cofnięty,
  poleciało prawdziwe żądanie.
