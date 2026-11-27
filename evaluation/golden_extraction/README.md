# NEXUS Golden Dataset v0.1 · Extraktion und Klassifikation

Review-Kandidat für drei Arbeitsstränge. Der Versionsstand umfasst 58 quellgebundene Fälle mit 296 Sollfeldern. Das private Drive-Prüfpaket enthält den getrennten Eingabesatz, Referenzannotation, Quellenrevisionen, Fundstellen, Baseline, Portfolio und vollständige Ergebnisse. Der öffentliche Commit enthält die Prüfsummen je Datensatz und Fall sowie den ausführbaren Offline-Prüfer. Fall-IDs verbinden beide Teile. Produktions- und Fachfreigabe sind offen.

## Wiederholen

Python 3.9 oder neuer, ohne Zusatzpakete. Die Befehle im entpackten Drive-Prüfpaket ausführen.

```sh
python baseline.py inputs.jsonl > candidate.jsonl
python verify_bundle.py
python -m unittest -v test_score
```

Zum Test eines anderen Extraktors nur inputs.jsonl übergeben, seine Ausgaben als candidate.jsonl ablegen und anschließend `python verify_bundle.py candidate.jsonl` ausführen. Für den zweiten Versuch nur questions.jsonl übergeben. Mit `python verify_bundle.py --routing routing-predictions.jsonl` wird gegen den separaten Routing-Schlüssel geprüft. Bei Verwendung eines anderen Kandidaten den jeweiligen Dateinamen angeben. Die Datei manifest.json aus diesem Commit vor dem ersten Lauf mit der Paketkopie vergleichen.

Jede Vorhersage ist eine JSONL-Zeile mit case_id, label und fields. Felder, Datentypen, Einheiten, Nullwerte und Klassenzuordnung werden exakt verglichen. Reihenfolge von Objektschlüsseln ist frei, die Reihenfolge von Arrays ist Teil des Vertrags. Die Bewertung liefert Fall- und Feldtreffer, Makro-F1, Fehler-IDs und Exit 0 oder 2. Doppelte Schlüssel, zusätzliche oder fehlende Fälle und abweichende Referenzprüfsummen sperren die Abnahme.

## Befund

Der strukturierte Referenzlauf reproduzierte 58/58 Klassen und 296/296 Felder. Beim getrennten Lauf allein auf 20 Fragewortlauten erreichte eine einfache Regelbasis 15/20 korrekte Routen. Die fünf Fehlfälle bleiben im Prüfpaket dokumentiert. Es handelt sich um eine rückblickende, gebundene Stichprobe. Für die Modellabnahme ist ein neuer, unabhängig beschrifteter und vorab zurückgehaltener Quellensatz erforderlich.
