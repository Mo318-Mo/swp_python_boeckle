#!/usr/bin/env python3
"""Pokerspielsimulator: zieht zufällig fünf Karten, erkennt die Kombination
und vergleicht die Häufigkeiten von vielen Spielen mit den exakten Werten.
"""
import math    # für math.comb: Anzahl aller möglichen 5-Karten-Hände
import random  # für random.randint: zufällige Position im Deck

# Eine Karte ist ein Tupel (wert, farbe):
#   wert  0..12 -> Index in SYMBOLE (0 = "2", 8 = "10", 12 = Ass)
#   farbe 0..3  -> Index in FARBEN
Karte = tuple[int, int]                    # Typ-Alias für die Type Hints

FARBEN = ("Herz", "Karo", "Pik", "Kreuz")  # die 4 Farben
SYMBOLE = ("2", "3", "4", "5", "6", "7", "8", "9", "10",
           "B", "D", "K", "A")             # die 13 Werte, aufsteigend
ANZAHL_SPIELE = 100_000                    # so viele Spiele simulieren


# ---------------------------------------------------------------------------
# Deck und Karten
# ---------------------------------------------------------------------------

def erzeuge_deck() -> list[Karte]:
    """Liefert alle 52 Karten (4 Farben x 13 Symbole)."""
    deck: list[Karte] = []                 # leere Liste für die Karten
    for farbe in range(len(FARBEN)):       # farbe läuft von 0 bis 3
        for wert in range(len(SYMBOLE)):   # wert läuft von 0 bis 12
            deck.append((wert, farbe))     # Karte als Tupel anhängen
    return deck                            # 4 * 13 = 52 Karten


def karten_geben(deck: list[Karte], anzahl: int = 5) -> list[Karte]:
    """Zieht `anzahl` verschiedene Karten, wie bei der Lottoziehung.

    Die gezogene Karte wird ans Ende des noch gültigen Bereichs getauscht,
    dadurch braucht jede Karte genau einen Aufruf von random.randint.
    Achtung: das Deck wird dabei nur umsortiert (Liste ist mutable),
    es bleibt aber vollständig und kann direkt wieder verwendet werden.
    """
    grenze = len(deck) - 1                 # letzte noch gültige Position
    hand: list[Karte] = []                 # leere Liste für die Hand
    for _ in range(anzahl):                # anzahl-mal ziehen
        pos = random.randint(0, grenze)    # Position 0..grenze (inklusive!)
        hand.append(deck[pos])             # Karte in die Hand übernehmen
        # Tausch: gezogene Karte ans Ende, letzte gültige Karte rückt nach
        deck[pos], deck[grenze] = deck[grenze], deck[pos]
        grenze -= 1                        # gezogene Karte ist jetzt gesperrt
    return hand                            # 5 verschiedene Karten


def karte_als_text(karte: Karte) -> str:
    """Wandelt eine Karte in Text um, z. B. (12, 0) -> "Herz-A"."""
    wert, farbe = karte                    # Tupel in zwei Variablen zerlegen
    farbname = FARBEN[farbe]               # z. B. 0 -> "Herz"
    symbol = SYMBOLE[wert]                 # z. B. 12 -> "A"
    return farbname + "-" + symbol         # z. B. "Herz-A"


def hand_als_text(hand: list[Karte]) -> str:
    """Alle Karten der Hand als Text, durch Komma getrennt."""
    texte: list[str] = []                  # leere Liste für die Texte
    for karte in hand:                     # jede Karte einzeln umwandeln
        texte.append(karte_als_text(karte))
    return ", ".join(texte)                # z. B. "Herz-A, Pik-2, ..."


# ---------------------------------------------------------------------------
# Hilfsfunktionen für die Auswertung
# ---------------------------------------------------------------------------

def werte_der_hand(hand: list[Karte]) -> list[int]:
    """Liefert nur die Werte der Karten, aufsteigend sortiert."""
    werte: list[int] = []                  # leere Liste für die Werte
    for wert, _ in hand:                   # Farbe wird nicht gebraucht
        werte.append(wert)                 # nur den Wert merken
    werte.sort()                           # aufsteigend sortieren
    return werte                           # z. B. [0, 3, 3, 9, 12]


def wert_anzahlen(hand: list[Karte]) -> list[int]:
    """Zählt, wie oft jeder Wert vorkommt, absteigend sortiert.

    Beispiel Full House (3x König, 2x Sieben) -> [3, 2]
    """
    zaehler: dict[int, int] = {}           # Wert -> wie oft er vorkommt
    for wert, _ in hand:                   # Farbe wird nicht gebraucht
        if wert in zaehler:                # Wert schon einmal gesehen?
            zaehler[wert] += 1             # ja: Zähler um 1 erhöhen
        else:
            zaehler[wert] = 1              # nein: erstes Vorkommen
    anzahlen = list(zaehler.values())      # nur die Anzahlen, z. B. [2, 3]
    anzahlen.sort(reverse=True)            # absteigend sortieren -> [3, 2]
    return anzahlen


# ---------------------------------------------------------------------------
# Prüffunktionen: jede prüft genau eine Kombination
# ---------------------------------------------------------------------------

def ist_paar(hand: list[Karte]) -> bool:
    """Genau zwei Karten mit gleichem Wert, z. B. 7, 7, 2, 9, K."""
    return wert_anzahlen(hand) == [2, 1, 1, 1]


def ist_zwei_paare(hand: list[Karte]) -> bool:
    """Zwei verschiedene Paare, z. B. 7, 7, 9, 9, K."""
    return wert_anzahlen(hand) == [2, 2, 1]


def ist_drilling(hand: list[Karte]) -> bool:
    """Drei Karten mit gleichem Wert, z. B. 7, 7, 7, 9, K."""
    return wert_anzahlen(hand) == [3, 1, 1]


def ist_full_house(hand: list[Karte]) -> bool:
    """Drilling und Paar zusammen, z. B. 7, 7, 7, 9, 9."""
    return wert_anzahlen(hand) == [3, 2]


def ist_poker(hand: list[Karte]) -> bool:
    """Poker = Vierling, vier Karten mit gleichem Wert."""
    return wert_anzahlen(hand) == [4, 1]


def ist_flush(hand: list[Karte]) -> bool:
    """Alle fünf Karten haben dieselbe Farbe."""
    erste_farbe = hand[0][1]               # Farbe der ersten Karte
    for _, farbe in hand:                  # jede Karte vergleichen
        if farbe != erste_farbe:           # andere Farbe gefunden?
            return False                   # dann kein Flush
    return True                            # alle Farben gleich


def ist_strasse(hand: list[Karte]) -> bool:
    """Fünf aufeinanderfolgende Werte; das Ass darf auch als 1 zählen."""
    if wert_anzahlen(hand) != [1, 1, 1, 1, 1]:  # ein Wert doppelt?
        return False                            # dann keine Straße
    werte = werte_der_hand(hand)           # z. B. [3, 4, 5, 6, 7]
    if werte == [0, 1, 2, 3, 12]:          # Sonderfall A-2-3-4-5
        return True                        # Ass zählt hier als 1
    abstand = werte[4] - werte[0]          # höchster minus niedrigster Wert
    return abstand == 4                    # 5 verschiedene Werte, Abstand 4


def ist_straight_flush(hand: list[Karte]) -> bool:
    """Straße, bei der alle Karten dieselbe Farbe haben."""
    if not ist_flush(hand):                # nicht alle gleiche Farbe?
        return False                       # dann kein Straight Flush
    return ist_strasse(hand)               # sonst entscheidet die Straße


def ist_royal_flush(hand: list[Karte]) -> bool:
    """Straight Flush von 10 bis Ass."""
    if not ist_straight_flush(hand):       # kein Straight Flush?
        return False                       # dann auch kein Royal Flush
    niedrigster_wert = werte_der_hand(hand)[0]  # Liste ist sortiert
    return SYMBOLE[niedrigster_wert] == "10"    # beginnt die Straße bei 10?


def ist_hoechste_karte(hand: list[Karte]) -> bool:
    """Keine andere Kombination; trifft als letzte Prüfung immer zu."""
    return True


# Von der besten zur schlechtesten Kombination: (Name, Prüffunktion,
# Anzahl der Hände unter allen 2.598.960 möglichen 5-Karten-Händen).
# Quelle der exakten Anzahlen: https://en.wikipedia.org/wiki/Poker_probability
KOMBINATIONEN = (
    ("Royal Flush", ist_royal_flush, 4),
    ("Straight Flush", ist_straight_flush, 36),
    ("Poker (Vierling)", ist_poker, 624),
    ("Full House", ist_full_house, 3_744),
    ("Flush", ist_flush, 5_108),
    ("Straße", ist_strasse, 10_200),
    ("Drilling", ist_drilling, 54_912),
    ("Zwei Paare", ist_zwei_paare, 123_552),
    ("Ein Paar", ist_paar, 1_098_240),
    ("Höchste Karte", ist_hoechste_karte, 1_302_540),
)


def bewerte_hand(hand: list[Karte]) -> str:
    """Liefert den Namen der besten Kombination der Hand.

    Die Reihenfolge in KOMBINATIONEN ist wichtig: ein Straight Flush ist
    auch ein Flush, wird aber vorher geprüft und deshalb zuerst gefunden.
    """
    for name, pruefen, _ in KOMBINATIONEN:  # von der besten zur schlechtesten
        if pruefen(hand):                   # passt diese Kombination?
            return name                     # ja: das ist die beste
    # wird nie erreicht, weil ist_hoechste_karte immer True liefert;
    # steht nur da, damit die Funktion in jedem Fall einen str zurückgibt
    return "Höchste Karte"


# ---------------------------------------------------------------------------
# Simulation und Ausgabe
# ---------------------------------------------------------------------------

def simuliere(spiele: int) -> dict[str, int]:
    """Spielt `spiele` Runden und zählt, wie oft jede Kombination kommt."""
    zaehler: dict[str, int] = {}           # Name der Kombination -> Anzahl
    for name, _, _ in KOMBINATIONEN:       # jede Kombination ...
        zaehler[name] = 0                  # ... startet mit 0
    deck = erzeuge_deck()                  # ein Deck reicht für alle Spiele
    for _ in range(spiele):                # so oft spielen wie gewünscht
        hand = karten_geben(deck)          # 5 Karten ziehen
        name = bewerte_hand(hand)          # beste Kombination bestimmen
        zaehler[name] += 1                 # Treffer zählen
    return zaehler


def prozent(anteil: int, gesamt: int) -> float:
    """Rechnet einen Anteil in Prozent um, z. B. 1 von 4 -> 25.0."""
    return anteil / gesamt * 100


def ausgabe(zaehler: dict[str, int], spiele: int) -> None:
    """Tabelle: simulierter Anteil im Vergleich zum exakten Anteil."""
    alle_haende = math.comb(52, 5)         # 2.598.960 mögliche Hände
    # Formatangaben: <17 = linksbündig auf 17 Zeichen, >8 = rechtsbündig
    # auf 8 Zeichen, .4f = 4 Nachkommastellen, + = Vorzeichen immer zeigen
    print(f"{'Kombination':<17}{'Anzahl':>8}{'Simuliert':>12}"
          f"{'Exakt':>12}{'Differenz':>12}")
    print("-" * 61)                        # Trennlinie, so breit wie Tabelle
    for name, _, exakte_anzahl in KOMBINATIONEN:
        anzahl = zaehler[name]             # Treffer in der Simulation
        simuliert = prozent(anzahl, spiele)           # simulierter Anteil
        exakt = prozent(exakte_anzahl, alle_haende)   # exakter Anteil
        differenz = simuliert - exakt                 # Abweichung
        print(f"{name:<17}{anzahl:>8}{simuliert:>10.4f} %"
              f"{exakt:>10.4f} %{differenz:>+12.4f}")


if __name__ == "__main__":
    beispiel = karten_geben(erzeuge_deck())    # eine einzelne Hand ziehen
    print("Beispielhand:", hand_als_text(beispiel))
    print("Kombination: ", bewerte_hand(beispiel))
    print()                                    # Leerzeile
    print(f"{ANZAHL_SPIELE} Spiele:")
    ergebnis = simuliere(ANZAHL_SPIELE)        # viele Spiele simulieren
    ausgabe(ergebnis, ANZAHL_SPIELE)           # Ergebnis als Tabelle
