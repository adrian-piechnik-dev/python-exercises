from typing import Optional


def zadanie_01_przywitaj(imie: str) -> str:
    """Zwraca tekst powitalny zawierający podane imię.

    Args:
        imie: imię osoby do przywitania.

    Returns:
        str: tekst w formacie "Cześć, {imie}!".
    """
    return f"Cześć, {imie}!"


def zadanie_02_suma_dwoch(a: int, b: int) -> int:
    """Zwraca sumę dwóch liczb całkowitych.

    Args:
        a: pierwsza liczba.
        b: druga liczba.

    Returns:
        int: suma a + b.
    """
    return a + b


def zadanie_03_czy_parzysta(liczba: int) -> bool:
    """Sprawdza, czy podana liczba jest parzysta.

    Args:
        liczba: liczba całkowita do sprawdzenia.

    Returns:
        bool: True gdy liczba parzysta (reszta z dzielenia przez 2 = 0), False w przeciwnym razie.
    """
    if liczba % 2 == 0:
        return True
    return False


def zadanie_04_wieksza_z_dwoch(a: int, b: int) -> int:
    """Zwraca większą z dwóch liczb; gdy są równe, zwraca a.

    Args:
        a: pierwsza liczba.
        b: druga liczba.

    Returns:
        int: większa z dwóch liczb.
    """
    if a >= b:
        return a
    else:
        return b


def zadanie_05_znak_liczby(liczba: int) -> str:
    """Określa, czy liczba jest ujemna, zerem lub dodatnia.

    Args:
        liczba: liczba całkowita do sprawdzenia.

    Returns:
        str: "ujemna" gdy liczba < 0, "zero" gdy liczba == 0, "dodatnia" gdy liczba > 0.
    """
    if liczba < 0:
        return "ujemna"
    elif liczba == 0:
        return "zero"
    else:
        return "dodatnia"


def zadanie_06_opis_dnia(numer: int) -> Optional[str]:
    """Zwraca polską nazwę dnia tygodnia dla numeru od 1 do 7.

    Args:
        numer: numer dnia (1 = poniedziałek, 2 = wtorek, ..., 7 = niedziela).

    Returns:
        Optional[str]: nazwa dnia tygodnia lub None gdy numer spoza zakresu 1–7.
    """
    if numer == 1:
        return "poniedziałek"
    elif numer == 2:
        return "wtorek"
    elif numer == 3:
        return "środa"
    elif numer == 4:
        return "czwartek"
    elif numer == 5:
        return "piątek"
    elif numer == 6:
        return "sobota"
    elif numer == 7:
        return "niedziela"
    else:
        return None


def zadanie_07_ocena_slowna(punkty: int) -> Optional[str]:
    """Zwraca ocenę słowną na podstawie liczby punktów w skali 0–100.

    Args:
        punkty: wynik egzaminu z zakresu 0–100.

    Returns:
        Optional[str]: "celujący" gdy >= 90, "dobry" gdy >= 75, "dostateczny" gdy >= 50,
            "niedostateczny" gdy >= 0, None gdy punkty spoza zakresu 0–100.
    """
    if punkty < 0 or punkty > 100:
        return None
    if punkty >= 90:
        return "celujący"
    elif punkty >= 75:
        return "dobry"
    elif punkty >= 50:
        return "dostateczny"
    else:
        return "niedostateczny"


def zadanie_08_podziel(a: float, b: float) -> Optional[float]:
    """Dzieli dwie liczby. Gdy dzielnik wynosi zero, zwraca None.

    Args:
        a: dzielna.
        b: dzielnik.

    Returns:
        Optional[float]: wynik a / b lub None gdy b == 0.
    """
    if b == 0:
        return None
    return a / b


def zadanie_09_kategoria_wieku(wiek: int) -> Optional[str]:
    """Zwraca kategorię wiekową dla podanego wieku.

    Args:
        wiek: wiek w latach (oczekiwany >= 0).

    Returns:
        Optional[str]: "niepełnoletni" gdy 0–17, "dorosły" gdy 18–64,
            "senior" gdy >= 65, None gdy wiek < 0.
    """
    if wiek < 0:
        return None
    if wiek <= 17:
        return "niepełnoletni"
    elif wiek <= 64:
        return "dorosły"
    else:
        return "senior"


def zadanie_10_opis_temperatury(temperatura: float) -> str:
    """Zwraca słowny opis zakresu temperatury w stopniach Celsjusza.

    Args:
        temperatura: temperatura w stopniach Celsjusza.

    Returns:
        str: "mróz" gdy < 0, "chłodno" gdy 0–14, "przyjemnie" gdy 15–24, "gorąco" gdy >= 25.
    """
    if temperatura < 0:
        return "mróz"
    elif temperatura < 15:
        return "chłodno"
    elif temperatura < 25:
        return "przyjemnie"
    else:
        return "gorąco"


def zadanie_11_czy_kwalifikuje(wiek: int, wzrost: int) -> Optional[bool]:
    """Sprawdza kwalifikację zawodnika: wymagany wiek >= 18 i wzrost >= 160 cm.

    Args:
        wiek: wiek zawodnika w latach.
        wzrost: wzrost zawodnika w centymetrach.

    Returns:
        Optional[bool]: True gdy oba warunki spełnione, False gdy przynajmniej jeden nie,
            None gdy wiek < 0 lub wzrost <= 0.
    """
    if wiek < 0 or wzrost <= 0:
        return None
    if wiek >= 18 and wzrost >= 160:
        return True
    else:
        return False


def zadanie_12_kategoria_bmi(waga: float, wzrost_cm: float) -> Optional[str]:
    """Oblicza BMI i zwraca kategorię wagową.

    BMI = waga / (wzrost_m ** 2), gdzie wzrost_m = wzrost_cm / 100.

    Args:
        waga: waga ciała w kilogramach.
        wzrost_cm: wzrost w centymetrach.

    Returns:
        Optional[str]: "niedowaga" gdy BMI < 18.5, "norma" gdy 18.5–24.9,
            "nadwaga" gdy 25.0–29.9, "otyłość" gdy >= 30.0,
            None gdy waga <= 0 lub wzrost_cm <= 0.
    """
    if waga <= 0 or wzrost_cm <= 0:
        return None
    wzrost_m = wzrost_cm / 100
    bmi = waga / (wzrost_m ** 2)
    if bmi < 18.5:
        return "niedowaga"
    elif bmi < 25:
        return "norma"
    elif bmi < 30:
        return "nadwaga"
    else:
        return "otyłość"
