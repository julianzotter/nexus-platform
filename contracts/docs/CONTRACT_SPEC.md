# Vertragssemantik v0.1

Diese Spezifikation beschreibt den tatsächlich enthaltenen Referenzcode.
Status: Spezifikationskandidat, keine kanonische NEXUS-Registry-Promotion.

## 1. Gemeinsame Regeln

- `schema_version` ist exakt zu prüfen. Unbekannte Versionen benötigen explizite
  Migration; es gibt keine implizite Rückwärtskompatibilität.
- IDs sind innerhalb ihrer Objektkategorie eindeutig. Verweise müssen existieren.
- Der SI-Kanon ist `SI-m-N-Pa-kg-s-K-rad/1`. Externe kN/mm/MPa/Celsius-Werte
  werden von zukünftigen Adaptern explizit umgerechnet und rückgelesen.
- Dezimalwerte sind endliche `Decimal`; JSON transportiert Dezimalstrings ohne
  Exponent, Tausendertrennzeichen oder Dezimalkomma. Numerische JSON-Integer
  werden ausschließlich für Integer-Felder benutzt.
- Array-Reihenfolge bleibt erhalten. Es gibt keine implizite Sortierung nach IDs.
- Die Strukturprüfung ersetzt weder die Referenzprüfung noch einen Fachnachweis.
- Unbekannte Zusatzfelder sind auch in verschachtelten Objekten unzulässig.

## 2. AnalysisModel

Enthält Modell-ID/Revision, SI-Profil, externen Ursprung/Orientierung,
Knoten, Stäbe, Materialien, Querschnitte, starre Lager, Lasten, Lastfälle,
Analysezustände und die Ergebnisanforderung.

Knotenkoordinaten und als `global` bezeichnete Vektoren beziehen sich auf das
globale Modellkoordinatensystem. `origin_m` und `global_frame` beschreiben dessen
Bezug zu einem übergeordneten äußeren Koordinatensystem. Stab-/Lagerframes werden
in Komponenten dieses Modellkoordinatensystems angegeben. Frames sind orthonormal
und rechtshändig; Stab-x zeigt vom Start- zum Endknoten.

Materialumfang: linear-elastisch isotrop, mit E, nu, Massendichte und
thermischem Ausdehnungskoeffizienten. Kein aus E/G/nu erfundenes nichtlineares
Materialgesetz. Ein späterer Adapter dokumentiert G = E / (2(1+nu)) und seine
Elementformulierung. Querschnittskonstanten sind A, Iy, Iz und Torsionskonstante;
bei `beam` sind alle positiv, bei axialen Stäben dürfen Biege-/Torsionskonstanten
null sein. `beam` ist im v0.1-Umfang als räumlicher Euler-Bernoulli-Stab ohne
Schubverformung/Wölbkrafttorsion vorgesehen. Jeder reale Adapter muss diese
Annahme nachweisen oder ablehnen. Kein Stabilitäts-/Querschnittsnachweis folgt
aus einem gültigen Querschnittsobjekt.

`tension_only` und `compression_only` bezeichnen axiales Aktivierungsverhalten,
keine Vorspannung. `cable` erfordert einen expliziten Referenzzustand. Dieser ist
entweder unbelastete Länge, Anfangsnormalkraft oder ausdrücklich unbelastete
Referenzgeometrie bei angegebener Temperatur. Diese Darstellung ist keine
Bestätigung einer bestimmten Seilinterpolation oder Formfindungsmethode.
Ein realer Seiladapter muss die Referenzinterpretation, Interpolation,
Diskretisierung und Zustandsübernahme vor seiner Capability-Freigabe konkretisieren.

Formfindungsziele liegen separat im zugehörigen Analysezustand. Ein Kraftziel
trägt eine numerische positive Zugkraft. Ein Durchhangziel trägt einen
vorzeichenbehafteten Abstand in Richtung eines globalen Einheitsvektors,
eine Station im offenen Intervall (0,1) und den Bezug auf die Verbindung der
Endknoten. Die Anweisung ist damit kein frei interpretierbares Wort „sag“.

Alle Stäbe des Modells sind in jedem Zustand aktiv. Bauzustandsaktivierung,
Gelenke, Federn, Exzentrizitäten, veränderliche Querschnitte, Flächen/Volumen,
Kontakte, plastische Gesetze und Dynamik sind in dieser Version nicht darstellbar.
Entsprechende Zusatzfelder müssen beim Import abgewiesen werden. Die Definition
einer zukünftigen Schemaerweiterung ist von einer Adapterfähigkeit zu trennen.

## 3. Analysezustände und Lastkombinationen

`LoadCase` gruppiert Lasten. `AnalysisState` legt Theorie, explizite LF-Faktoren,
Gravitation, Numerik, optionalen Initialzustand und Formfindungsziele fest.
Ein LF-Ergebnis wird als Zustand mit einem LF-Faktor 1 angefordert. Eine
Lastkombination wird als eigener Zustand mit expliziten Faktoren dargestellt.
Es gibt keine getrennte, unvollständig definierte `combination`-Abkürzung.

LF-Faktoren und Gravitation beschreiben die TOTALEN Zielbelastungen des Zustands.
`initial_state_id` bezeichnet einen vorher berechneten Geometrie-/Spannungszustand;
es bedeutet keine automatische Addition seiner Lastfaktoren. Adapter, die diese
Semantik nicht verlustfrei übertragen können, müssen ablehnen. Der Graph ist
azyklisch; sämtliche Zustände müssen von der Capability-Prüfung abgedeckt sein.

Eigengewicht ist nur bei explizit von null verschiedener Gravitation aktiv;
es stammt aus Massendichte und Gravitation. Es gibt keinen stillen Faktor 1.
Für nichtlineare Zustände ist jede Kombination tatsächlich zu rechnen, nicht
durch lineare Ergebnisaddition zu ersetzen. Numerische Einstellungen sind
ausdrücklich angegeben. Ihre Übertragung und die konkrete Residualnorm müssen
im realen Adapter-/Solverprotokoll nachvollziehbar sein; das DTO erzwingt keinen
solverübergreifend identischen Iterationsalgorithmus.

## 4. Ergebnisanforderung und AnalysisResults

`ResultRequest` benennt explizite Zustände sowie Kombinationen aus Ergebnistyp,
Objektart, Objekt-IDs und gegebenenfalls Stationen. Stabstationen sind relative
Koordinaten von Start=0 bis Ende=1. Doppelte oder überlappende Anforderungen sind
ungültig. Reaktionsmomente dürfen unabhängig von Reaktionskräften angefordert werden.

| Größen | Einheit | Achsen / Interpretation |
| --- | --- | --- |
| N, V_y, V_z | N | Stablokal; N positiv bei Zug |
| M_y, M_z, T | Nm | Stablokal; T um lokale x-Achse |
| u_x, u_y, u_z | m | Globale Knotenverschiebungen |
| phi_x, phi_y, phi_z | rad | Globale Knotenrotationen, Rechte-Hand-Regel |
| R_x, R_y, R_z | N | Vom Lager auf das Tragwerk wirkende globale Kräfte |
| M_R_x, M_R_y, M_R_z | Nm | Vom Lager auf das Tragwerk wirkende globale Momente |

`nexus-results/0.1`: Schnittgrößen sind auf der Schnittfläche mit positiver
lokaler x-Normalen definiert; positive Kraft-/Momentvektoren folgen den positiven
lokalen Achsen/Rechte-Hand-Regel. Herstellerkonventionen benötigen einen
expliziten Vorzeichen-/Achsenabgleich. Graphische Diagrammseiten ersetzen diese
Definition nicht.

Jeder Skalar enthält Zustand, Objekt, Typ, Wert, Einheit, Frame,
Vorzeichenprofil und gegebenenfalls Station. Der Ergebniscontainer bindet alle
Werte an Modell-ID, Revision, Hash sowie Solver-/Adapterversion und Ausführungsart.
Die Zuordnung erfolgt über explizite Schlüssel, niemals über parallele Tupelpositionen.

`solved` verlangt vollständige angeforderte Skalare. Bei nichtlinearen Zuständen
ist `converged` erforderlich; ein unbekannter Status wird nicht umgedeutet.
`partial` und `failed` können zur Diagnose gespeichert werden, blockieren aber
die Weitergabe an Bemessung. Lineare direkte Lösungen dürfen `not_required`
mit dokumentiertem Grund melden. Daraus folgt kein Beweis für Modellstabilität.

Hüllkurven sind bewusst nicht Bestandteil dieses Rohdatenvertrags. Eine spätere
Hüllkurve muss je Extremum den verursachenden Zustand und gegebenenfalls
zugehörige gleichzeitig wirkende Komponenten erhalten. Sie darf nicht als
ein einzelner gleichzeitig wirkender Lastzustand ausgegeben werden.

## 5. CheckResult und MappingReport

`CheckResult` trennt Methode/Version, Norm-ID/Ausgabe, Änderungen und
NA-ID/NA-Ausgabe. Jede Feststellung verweist auf konkrete Evidenz-IDs;
alle Evidenzen benennen URI, Version und Fundstelle. `pass/fail/not_evaluated`
ist eine Befundzusammenfassung und kein technischer Freigabevermerk.

Kein normatives Bemessungsmodul ist enthalten. QTO, Kosten und LCA können später
separate Fachverträge ergänzen. EPD-UUID/Version, Bezugsmenge, Materialzuordnung,
Lebenszyklusmodule sowie Kostenstand sind dabei ausdrücklich zu definieren;
sie werden nicht in analytische Kräftefelder hineingemischt.

`MappingReport` enthält Warnungen, Fehler und Verluste mit Quellbezug.
`lossless` ist eine aus den Issues abgeleitete Aussage für den deklarierten
Mappingumfang, kein Nachweis universeller Gleichwertigkeit verschiedener Formate.

## 6. Hashing und Versionierung

Profil: `nexus-c14n/0.1`, lokal definiert, kein RFC-8785-/JCS-Anspruch.

1. Alle Dataclass-Felder rekursiv übernehmen; abgeleitete Properties nicht.
2. Tupel als Arrays in bestehender Reihenfolge erhalten.
3. Endliche Decimal-Werte als Festkommastrings ohne überflüssige Nachkommennullen;
   -0 wird 0. Unicode bleibt unverändert, keine NFC/NFD-Äquivalenzbehauptung.
4. JSON-Objektschlüssel sortieren; UTF-8, keine Leerzeichen, keine NaN-/Float-Tokens.
5. SHA-256 über `ASCII(profile) + NUL + UTF8(JSON)`.

Der Modellhash umfasst ID, Revision, Reihenfolge und Ergebnisanforderung.
Er ist ein vollständiger Inhaltssnapshot, kein semantischer Tragwerksfingerprint.
Eine andere Reihenfolge kann einen anderen Hash ergeben, obwohl ein Ingenieur
die Modelle als gleichwertig betrachtet. Paket-/Quelldateiprüfsummen sind davon getrennt.
Änderungen an Profil, Einheiten oder Bedeutung benötigen eine neue Vertrags-/Profilversion.

Eine Hashübereinstimmung beweist weder physikalische Richtigkeit noch erfolgreichen
Solverlauf, Unveränderlichkeit eines Betriebssystems oder technische Freigabe.
