# PowerShell-Handoff · Excel Desktop E2E

## Ursache des aktuellen Fehlers

Der Skriptinhalt wurde blockweise in die interaktive PowerShell eingefügt. Damit fehlen Initialisierung, Hilfsfunktionen und gebundene Parameter. `$source` ist der erste sichtbare Fehler; ein manuelles Setzen nur dieser Variable reicht nicht.

## Sicherer Aufruf

1. Aktuellen unvollständigen Lauf mit `Ctrl+C` abbrechen.
2. Das vollständige v1.2-Skript als `P205_FT_Excel_Native_Recalc_v1_2.ps1` speichern.
3. Im folgenden Wrapper den beabsichtigten Hash setzen und als zusammenhängenden Block ausführen:

```powershell
$root = 'G:\Meine Ablage\ZT-Gesellschaft\10_PROJEKTE\P205_Campus_Eisteiche_BIG\05_STATIK\EXCEL\JULIAN'
$expected = 'a921f515c3d56b281a47343ff5ee39c65e8cc2093fe371ef048006c4a55810f9'
$matches = @(Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.xlsx' |
  Where-Object {
    (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -eq $expected
  })
if ($matches.Count -ne 1) {
  throw "STOP: expected exactly one source with SHA256 $expected; found $($matches.Count)"
}
$out = Join-Path $PWD ((Get-Date -Format 'yy_MM_dd_HHmmss') + '_ID06_EXCEL-NATIVE-RECALC')
New-Item -ItemType Directory -Path $out -ErrorAction Stop | Out-Null
& (Join-Path $PWD 'P205_FT_Excel_Native_Recalc_v1_2.ps1') `
  -InputXlsx $matches[0].FullName `
  -OutputDirectory $out `
  -ExpectedSha256 $expected
```

Hashvarianten nicht vermischen:

- Vers-D-Baseline: `a921f515c3d56b281a47343ff5ee39c65e8cc2093fe371ef048006c4a55810f9`
- RevF-Reparaturentwurf: `c47a1bc2308b19b16f69c07824fbf2f7508291fb252bfcc902389d8a486c33ee`

## Abnahme

- Quelle bleibt unverändert; Zielpfad existiert vorher nicht.
- 106 Blätter und 239.689 Formelzellen sind nur Strukturinvarianten, keine EC2-Freigabe.
- Excel-Rebuild, SaveCopyAs, Schließen, manuelles Wiederöffnen und unabhängiger OOXML-Formel-/Cache-Readback sind erfolgreich.
- Externe Links, UDFs, Queries, volatile Funktionen, Add-ins, Locale und Excel-Build sind protokolliert.
- Formel-/Cachefehler, RFEM-/Geometrielücken und >105-%-Stellen bleiben bis zur unabhängigen Prüfung offen.
