import random                      # Modul für Zufallszahlen laden (z. B. random.randint)

def lottoziehung():                # Funktion definieren, keine Parameter; liefert 6 gezogene Zahlen
    zahlen = {}                    # leeres Dictionary anlegen (Schlüssel → Wert)
    for i in range(45):            # Schleife: i läuft von 0 bis 44 (45 Durchläufe, 45 selbst ist exklusiv)
        zahlen[i] = i + 1          # Position i bekommt die Lottozahl i+1 → {0:1, 1:2, ..., 44:45}
    grenze = 44                    # letzte noch „gültige“ Position; alles dahinter ist schon gezogen
    gezogen = []                   # leere Liste für die Ergebnisse
    for _ in range(6):             # 6-mal wiederholen; "_" = Laufvariable wird nicht gebraucht
        pos = random.randint(0, grenze)   # zufällige Position zwischen 0 und grenze (beide INKLUSIVE!)
        gezogen.append(zahlen[pos])       # Zahl an dieser Position ans Listenende anhängen
        zahlen[pos], zahlen[grenze] = zahlen[grenze], zahlen[pos]
                                   # Tausch: gezogene Zahl ans Ende verschieben, letzte gültige Zahl
                                   # rückt an ihre Stelle (Tuple-Unpacking, kein Hilfsvariable nötig)
        grenze -= 1                # Bereich um 1 verkleinern → gezogene Zahl kann nicht nochmal kommen
    return gezogen                 # Liste mit 6 verschiedenen Zahlen zurückgeben

def statistik(ziehung, zaehler):   # Funktion mit 2 Parametern: eine Ziehung (Liste) und ein Zähler-Dict
    for zahl in ziehung:           # über jede der 6 gezogenen Zahlen iterieren
        zaehler[zahl] += 1         # Zähler dieser Zahl um 1 erhöhen
                                   # kein return nötig: das Dict wird direkt verändert (Referenz!)

print(lottoziehung())              # eine einzelne Ziehung ausgeben, z. B. [12, 3, 45, 27, 8, 31]

for anzahl in [1000, 10000, 100000]:   # äußere Schleife über eine Liste: 3 Durchläufe mit versch. Mengen
    zaehler = {}                   # für jeden Durchlauf ein neues, leeres Zähler-Dict
    for i in range(1, 46):         # i läuft von 1 bis 45
        zaehler[i] = 0             # jede Lottozahl startet mit Zählerstand 0
    for _ in range(anzahl):        # so oft ziehen, wie "anzahl" vorgibt
        statistik(lottoziehung(), zaehler)   # Ziehung erzeugen und direkt in den Zähler eintragen
    print(anzahl, "Ziehungen:", zaehler)     # Ergebnis ausgeben: wie oft kam jede Zahl