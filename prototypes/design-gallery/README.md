# NEXUS Design-Galerie

Lokales, animiertes Dashboard zum Durchblättern aller Designs im Repository. Prototyp, keine Freigabe.

## Starten

`index.html` direkt im Browser öffnen (file://, kein Server, keine API-Keys). Nach Änderungen an Designs:

```sh
python prototypes/design-gallery/build_manifest.py
python -m unittest tests.test_design_gallery
```

## Inhalt

- **HTML-Prototypen**: alle getrackten `*.html` außerhalb der Galerie, als Live-Vorschau in `sandbox="allow-scripts"` ohne Same-Origin (kein Zugriff auf localStorage/Cookies der Galerie).
- **Rechenmodule**: `ec5_solver.js` und `osr9_mmr.js` unverändert eingebunden, mit interaktiven Reglern und Plots.
- **Konzepte**: aus `docs/concepts/2026-10-13/catalog.json`.
- **Architekturen**: `curated.json`, animierte Flussdiagramme. Quelle ist ein Chat-Entwurf vom 2026-10-21; Status `concept_unverified`, Modell- und Produktangaben ungeprüft.

Bedienung: `/` Suche, Klick oder Enter öffnet Details, `←`/`→` blättern, `Esc` schließt, „Tour“ blättert automatisch (7 s). Direktlinks über `index.html#<ID>`.
