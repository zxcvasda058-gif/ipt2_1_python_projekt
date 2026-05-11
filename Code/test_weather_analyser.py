"""
Unit-Tests fuer WeatherAnalyser
Ziel: 100% Statement Coverage mit pytest-cov
Ausfuehren: pytest test_weather_analyser.py --cov=weather_analyser --cov-report=term-missing
"""
 
import pytest
import os
from weather_analyser import (
    csv_einlesen,
    merge_sort,
    minimum,
    maximum,
    durchschnitt,
    auswertung,
    _merge
)
 
# ---------------------------------------------------------------------------
# Hilfsdaten
# ---------------------------------------------------------------------------
 
TESTDATEN = [
    {'datum': '2024-01-15', 'temperatur': -8.2,  'windgeschwindigkeit': 34, 'schneehoehe': 120},
    {'datum': '2024-01-16', 'temperatur': -3.1,  'windgeschwindigkeit': 18, 'schneehoehe': 118},
    {'datum': '2024-01-17', 'temperatur': -12.5, 'windgeschwindigkeit': 52, 'schneehoehe': 125},
    {'datum': '2024-01-18', 'temperatur': -1.8,  'windgeschwindigkeit': 11, 'schneehoehe': 119},
    {'datum': '2024-01-19', 'temperatur': -6.4,  'windgeschwindigkeit': 29, 'schneehoehe': 122},
    {'datum': '2024-01-20', 'temperatur': -15.3, 'windgeschwindigkeit': 61, 'schneehoehe': 130},
    {'datum': '2024-01-21', 'temperatur': -4.7,  'windgeschwindigkeit': 22, 'schneehoehe': 128},
]
 
 
# ---------------------------------------------------------------------------
# T01-T03: csv_einlesen
# ---------------------------------------------------------------------------
 
def test_csv_einlesen_normalfall(tmp_path):
    """T01: Normalfall – 7 Zeilen werden korrekt eingelesen."""
    csv_datei = tmp_path / "wetterdaten.csv"
    csv_datei.write_text(
        "datum;temperatur;windgeschwindigkeit;schneehoehe\n"
        "2024-01-15;-8.2;34;120\n"
        "2024-01-16;-3.1;18;118\n"
        "2024-01-17;-12.5;52;125\n"
        "2024-01-18;-1.8;11;119\n"
        "2024-01-19;-6.4;29;122\n"
        "2024-01-20;-15.3;61;130\n"
        "2024-01-21;-4.7;22;128\n",
        encoding='utf-8'
    )
    result = csv_einlesen(str(csv_datei))
    assert len(result) == 7
    assert result[0]['datum'] == '2024-01-15'
    assert result[0]['temperatur'] == -8.2
    assert result[0]['windgeschwindigkeit'] == 34
    assert result[0]['schneehoehe'] == 120
 
 
def test_csv_einlesen_datei_fehlt():
    """T02: FileNotFoundError wenn Datei nicht existiert."""
    with pytest.raises(FileNotFoundError):
        csv_einlesen('existiert_nicht.csv')
 
 
def test_csv_einlesen_nur_kopfzeile(tmp_path):
    """T03: Nur Kopfzeile -> leere Liste."""
    csv_datei = tmp_path / "leer.csv"
    csv_datei.write_text(
        "datum;temperatur;windgeschwindigkeit;schneehoehe\n",
        encoding='utf-8'
    )
    result = csv_einlesen(str(csv_datei))
    assert result == []
 
 
# ---------------------------------------------------------------------------
# T04-T09: merge_sort
# ---------------------------------------------------------------------------
 
def test_merge_sort_gemischt():
    """T04: Gemischte Liste wird korrekt sortiert."""
    liste = [
        {'wert': 3}, {'wert': 1}, {'wert': 4}, {'wert': 1}, {'wert': 5}
    ]
    result = merge_sort(liste, 'wert')
    assert [e['wert'] for e in result] == [1, 1, 3, 4, 5]
 
 
def test_merge_sort_bereits_sortiert():
    """T05: Bereits sortierte Liste bleibt korrekt."""
    liste = [{'wert': 1}, {'wert': 2}, {'wert': 3}]
    result = merge_sort(liste, 'wert')
    assert [e['wert'] for e in result] == [1, 2, 3]
 
 
def test_merge_sort_umgekehrt():
    """T06: Umgekehrt sortierte Liste wird korrekt umsortiert."""
    liste = [{'wert': 5}, {'wert': 4}, {'wert': 3}, {'wert': 2}, {'wert': 1}]
    result = merge_sort(liste, 'wert')
    assert [e['wert'] for e in result] == [1, 2, 3, 4, 5]
 
 
def test_merge_sort_ein_element():
    """T07: 1-Element-Liste wird unveraendert zurueckgegeben."""
    liste = [{'wert': 42}]
    result = merge_sort(liste, 'wert')
    assert result == [{'wert': 42}]
 
 
def test_merge_sort_leere_liste():
    """T08: Leere Liste gibt leere Liste zurueck."""
    result = merge_sort([], 'wert')
    assert result == []
 
 
def test_merge_sort_dict_liste_nach_temperatur():
    """T09: Dict-Liste wird nach 'temperatur' korrekt sortiert."""
    result = merge_sort(TESTDATEN, 'temperatur')
    temps = [e['temperatur'] for e in result]
    assert temps == sorted(temps)
 
 
def test_merge_sort_original_unveraendert():
    """Zusatz: Original-Liste wird durch merge_sort nicht veraendert."""
    original = [{'wert': 3}, {'wert': 1}, {'wert': 2}]
    kopie = [e.copy() for e in original]
    merge_sort(original, 'wert')
    assert original == kopie
 
 
# ---------------------------------------------------------------------------
# T10-T13: minimum / maximum
# ---------------------------------------------------------------------------
 
def test_minimum_normalfall():
    """T10: Kleinster Temperaturwert wird korrekt gefunden."""
    result = minimum(TESTDATEN, 'temperatur')
    assert result['temperatur'] == -15.3
    assert result['datum'] == '2024-01-20'
 
 
def test_minimum_ein_element():
    """T11: 1-Element-Liste gibt dieses Element zurueck."""
    liste = [{'wert': 99}]
    assert minimum(liste, 'wert') == {'wert': 99}
 
 
def test_maximum_normalfall():
    """T12: Groesster Temperaturwert wird korrekt gefunden."""
    result = maximum(TESTDATEN, 'temperatur')
    assert result['temperatur'] == -1.8
    assert result['datum'] == '2024-01-18'
 
 
def test_maximum_alle_gleich():
    """T13: Alle gleichen Werte -> erstes Element wird zurueckgegeben."""
    liste = [{'wert': 5}, {'wert': 5}, {'wert': 5}]
    result = maximum(liste, 'wert')
    assert result['wert'] == 5
 
 
# ---------------------------------------------------------------------------
# T14-T16: durchschnitt
# ---------------------------------------------------------------------------
 
def test_durchschnitt_normalfall():
    """T14: Durchschnitt von [10, 20, 30] = 20.0."""
    liste = [{'wert': 10}, {'wert': 20}, {'wert': 30}]
    assert durchschnitt(liste, 'wert') == 20.0
 
 
def test_durchschnitt_leere_liste():
    """T15: Leere Liste gibt None zurueck."""
    assert durchschnitt([], 'wert') is None
 
 
def test_durchschnitt_rundung():
    """T16: Ergebnis wird auf 2 Dezimalstellen gerundet."""
    liste = [{'wert': 3.333}, {'wert': 6.667}]
    assert durchschnitt(liste, 'wert') == 5.0
 
 
# ---------------------------------------------------------------------------
# T17-T18: Eigene Tests
# ---------------------------------------------------------------------------
 
def test_merge_sort_schneehoehe():
    """T17: Sortierung nach 'schneehoehe' korrekt."""
    result = merge_sort(TESTDATEN, 'schneehoehe')
    hoehen = [e['schneehoehe'] for e in result]
    assert hoehen == sorted(hoehen)
 
 
def test_minimum_wind():
    """T18: Kleinster Windwert korrekt gefunden."""
    result = minimum(TESTDATEN, 'windgeschwindigkeit')
    assert result['windgeschwindigkeit'] == 11
 
 
# ---------------------------------------------------------------------------
# auswertung() – Integrationstests (capsys fuer Terminal-Ausgabe)
# ---------------------------------------------------------------------------
 
def test_auswertung_normalfall(tmp_path, capsys):
    """auswertung() gibt korrekten Bericht aus."""
    csv_datei = tmp_path / "wetterdaten.csv"
    csv_datei.write_text(
        "datum;temperatur;windgeschwindigkeit;schneehoehe\n"
        "2024-01-15;-8.2;34;120\n"
        "2024-01-20;-15.3;61;130\n",
        encoding='utf-8'
    )
    auswertung(str(csv_datei))
    ausgabe = capsys.readouterr().out
    assert "WeatherAnalyser" in ausgabe
    assert "-15.3" in ausgabe
    assert "WeatherAnalyser" in ausgabe
 
 
def test_auswertung_datei_fehlt(capsys):
    """auswertung() gibt Fehlermeldung aus wenn Datei fehlt."""
    auswertung('existiert_nicht.csv')
    ausgabe = capsys.readouterr().out
    assert "Fehler" in ausgabe
 
 
def test_auswertung_leere_csv(tmp_path, capsys):
    """auswertung() gibt Fehlermeldung aus bei leerer CSV."""
    csv_datei = tmp_path / "leer.csv"
    csv_datei.write_text(
        "datum;temperatur;windgeschwindigkeit;schneehoehe\n",
        encoding='utf-8'
    )
    auswertung(str(csv_datei))
    ausgabe = capsys.readouterr().out
    assert "Fehler" in ausgabe
 
 
def test_main_block(tmp_path, monkeypatch, capsys):
    """Deckt den if __name__ == '__main__' Block ab."""
    import runpy
    csv_datei = tmp_path / "wetterdaten.csv"
    csv_datei.write_text(
        "datum;temperatur;windgeschwindigkeit;schneehoehe\n"
        "2024-01-15;-8.2;34;120\n",
        encoding='utf-8'
    )
    monkeypatch.chdir(tmp_path)
    runpy.run_module('weather_analyser', run_name='__main__')
    ausgabe = capsys.readouterr().out
    assert "WeatherAnalyser" in ausgabe