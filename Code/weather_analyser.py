"""
WeatherAnalyser – Wetterdaten-Auswertung
Auftraggeber: Bergbahnen Flumserberg AG
"""

import csv
import os


def header():
    """
    Gibt den Programmkopf im Terminal aus.

    Args:
        keine

    Returns:
        None
    """
    header_line = "=" * 50
    file_path = os.path.abspath(__file__)
    print(header_line)
    print("Programm: WeatherAnalyser | Bergbahnen Flumserberg AG, Flums")
    print("Datei/Pfad: " + file_path)
    print(header_line)


def csv_einlesen(dateipfad):
    """
    Liest eine CSV-Datei mit Wetterdaten ein.

    Args:
        dateipfad (str): Pfad zur CSV-Datei (Semikolon-getrennt).

    Returns:
        list[dict]: Liste von Dictionaries mit den Schlüsseln
                    'datum', 'temperatur', 'windgeschwindigkeit', 'schneehoehe'.

    Raises:
        FileNotFoundError: Wenn die Datei nicht gefunden wird.
    """
    messwerte = []

    with open(dateipfad, newline='', encoding='utf-8') as datei:
        reader = csv.DictReader(datei, delimiter=';')
        for zeile in reader:
            messwerte.append({
                'datum': zeile['datum'],
                'temperatur': float(zeile['temperatur']),
                'windgeschwindigkeit': float(zeile['windgeschwindigkeit']),
                'schneehoehe': float(zeile['schneehoehe'])
            })

    return messwerte


def _merge(links, rechts, schluessel):
    """
    Führt zwei sortierte Listen zu einer sortierten Liste zusammen.

    Args:
        links (list[dict]): Linke Teilliste.
        rechts (list[dict]): Rechte Teilliste.
        schluessel (str): Dictionary-Schlüssel nach dem sortiert wird.

    Returns:
        list[dict]: Zusammengeführte, sortierte Liste.
    """
    ergebnis = []
    i = 0
    j = 0

    while i < len(links) and j < len(rechts):
        if links[i][schluessel] <= rechts[j][schluessel]:
            ergebnis.append(links[i])
            i += 1
        else:
            ergebnis.append(rechts[j])
            j += 1

    while i < len(links):
        ergebnis.append(links[i])
        i += 1

    while j < len(rechts):
        ergebnis.append(rechts[j])
        j += 1

    return ergebnis


def merge_sort(liste, schluessel):
    """
    Sortiert eine Liste von Dictionaries aufsteigend nach einem Schlüssel.
    Verwendet das Teile-und-herrsche-Verfahren (rekursiv).

    Basisfall:  Liste hat 0 oder 1 Element → bereits sortiert, direkt zurückgeben.
    Rekursionsfall: Liste halbieren → beide Hälften sortieren → zusammenführen.

    Args:
        liste (list[dict]): Zu sortierende Liste.
        schluessel (str): Dictionary-Schlüssel nach dem sortiert wird.

    Returns:
        list[dict]: Neue, sortierte Liste (Original bleibt unverändert).
    """
    # Basisfall
    if len(liste) <= 1:
        return liste[:]

    # Teilen
    mitte = len(liste) // 2
    links = merge_sort(liste[:mitte], schluessel)
    rechts = merge_sort(liste[mitte:], schluessel)

    # Zusammenführen
    return _merge(links, rechts, schluessel)


def minimum(liste, schluessel):
    """
    Gibt den Datensatz mit dem kleinsten Wert zurück.

    Args:
        liste (list[dict]): Liste von Dictionaries.
        schluessel (str): Dictionary-Schlüssel für den Vergleich.

    Returns:
        dict: Datensatz mit dem kleinsten Wert.
    """
    min_eintrag = liste[0]
    for eintrag in liste[1:]:
        if eintrag[schluessel] < min_eintrag[schluessel]:
            min_eintrag = eintrag
    return min_eintrag


def maximum(liste, schluessel):
    """
    Gibt den Datensatz mit dem grössten Wert zurück.

    Args:
        liste (list[dict]): Liste von Dictionaries.
        schluessel (str): Dictionary-Schlüssel für den Vergleich.

    Returns:
        dict: Datensatz mit dem grössten Wert.
    """
    max_eintrag = liste[0]
    for eintrag in liste[1:]:
        if eintrag[schluessel] > max_eintrag[schluessel]:
            max_eintrag = eintrag
    return max_eintrag


def durchschnitt(liste, schluessel):
    """
    Berechnet den Mittelwert eines Schlüssels über alle Einträge.

    Args:
        liste (list[dict]): Liste von Dictionaries.
        schluessel (str): Dictionary-Schlüssel für die Berechnung.

    Returns:
        float | None: Mittelwert gerundet auf 2 Dezimalstellen,
                      oder None bei leerer Liste.
    """
    if len(liste) == 0:
        return None

    summe = 0
    for eintrag in liste:
        summe += eintrag[schluessel]

    return round(summe / len(liste), 2)


def auswertung(dateipfad):
    """
    Hauptfunktion: Liest CSV ein, sortiert und berechnet Statistiken.
    Gibt einen formatierten Bericht im Terminal aus.

    Args:
        dateipfad (str): Pfad zur CSV-Datei.
    """
    header()

    try:
        daten = csv_einlesen(dateipfad)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.")
        return

    if len(daten) == 0:
        print("Fehler: Die CSV-Datei enthält keine Messwerte.")
        return

    print("=" * 55)
    print("  WeatherAnalyser – Bergbahnen Flumserberg AG")
    print("=" * 55)

    for schluessel, einheit, bezeichnung in [
        ('temperatur', '°C', 'Temperatur'),
        ('windgeschwindigkeit', 'km/h', 'Windgeschwindigkeit'),
        ('schneehoehe', 'cm', 'Schneehöhe'),
    ]:
        sortiert = merge_sort(daten, schluessel)
        min_wert = minimum(daten, schluessel)
        max_wert = maximum(daten, schluessel)
        avg_wert = durchschnitt(daten, schluessel)

        print(f"\n{bezeichnung}:")
        print(f"  Min: {min_wert[schluessel]} {einheit} (am {min_wert['datum']})")
        print(f"  Max: {max_wert[schluessel]} {einheit} (am {max_wert['datum']})")
        print(f"  Ø  : {avg_wert} {einheit}")
        print(f"  Sortiert: {[e[schluessel] for e in sortiert]}")

    print("\n" + "=" * 55)
    

if __name__ == '__main__':
    auswertung('/home/igor/ipt2_1/Code/wetterdaten.csv')
