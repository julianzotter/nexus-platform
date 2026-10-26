from __future__ import annotations
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from xml.sax.saxutils import escape
import json, re, hashlib
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'/'pdf'; OUT.mkdir(parents=True,exist_ok=True)
S=json.loads((ROOT/'pdf_sources_current.json').read_text())
G=json.loads((ROOT/'pdf_sources_governance.json').read_text())
prior=OUT/'dossier_build.json'
NOW=datetime.fromisoformat(json.loads(prior.read_text())['timestamp']) if prior.exists() else datetime.now(ZoneInfo('Europe/Berlin'))
TS=NOW.isoformat(timespec='seconds')
PREFIX=NOW.strftime('%y_%m_%d_%H%M_')
STEM=PREFIX+'NEXUS-SYSTEMARCHITEKTUR-DOSSIER-v1.0.0_0086_ID03'
PDF=OUT/(STEM+'.pdf')
NAVY=colors.HexColor('#102C43'); TEAL=colors.HexColor('#007E87'); GOLD=colors.HexColor('#B7791F')
INK=colors.HexColor('#223747'); MUTED=colors.HexColor('#526878'); LIGHT=colors.HexColor('#EEF4F7'); LINE=colors.HexColor('#CFDDE4')
for n,f in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DI','DejaVuSans-Oblique.ttf'),('DM','DejaVuSansMono.ttf')]:
    fp=Path('/usr/share/fonts/truetype/dejavu')/f
    if not fp.exists():fp=fp.with_name('DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont(n,str(fp)))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='DI',boldItalic='DB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyN',fontName='D',fontSize=9.2,leading=13,textColor=INK,spaceAfter=6,splitLongWords=True))
styles.add(ParagraphStyle(name='H1N',fontName='DB',fontSize=19,leading=24,textColor=NAVY,spaceBefore=0,spaceAfter=14,keepWithNext=True))
styles.add(ParagraphStyle(name='H2N',fontName='DB',fontSize=11.5,leading=16,textColor=TEAL,spaceBefore=11,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='SmallN',fontName='D',fontSize=7.4,leading=10.4,textColor=MUTED,spaceAfter=6))
styles.add(ParagraphStyle(name='CellN',fontName='D',fontSize=8.0,leading=11.8,textColor=INK,spaceAfter=0))
styles.add(ParagraphStyle(name='CellHeadN',parent=styles['CellN'],fontName='DB',textColor=colors.white))
styles.add(ParagraphStyle(name='CodeN',fontName='DM',fontSize=7.5,leading=11,textColor=NAVY,backColor=LIGHT,borderPadding=8,spaceAfter=10))
styles.add(ParagraphStyle(name='TOCN',fontName='D',fontSize=8.5,leading=11.5,leftIndent=0,firstLineIndent=0,spaceBefore=2,textColor=INK))
styles.add(ParagraphStyle(name='SourceTitle',fontName='DB',fontSize=9.5,leading=12,textColor=TEAL,spaceBefore=6,spaceAfter=3,keepWithNext=True))

def normal(s: str) -> str:
    return s.replace('\u2011','-').replace('—','-').replace('–','-').replace('\u00a0',' ')
def inline(s: str) -> str:
    s=escape(normal(s))
    s=re.sub(r'`([^`]+)`',r'<font name="DM">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#007E87">\1</link>',s)
    return s
def P(s: str,style: str='BodyN') -> Paragraph:return Paragraph(inline(s),styles[style])

class Figure(Flowable):
    def __init__(self,kind: str): super().__init__();self.kind=kind;self.width=487;self.height={'layers':260,'pipeline':310,'states':250,'storage':240,'integrity':210,'intervals':220}.get(kind,260)
    def box(self,x,y,w,h,title,sub='',fill=LIGHT):
        c=self.canv;c.setFillColor(fill);c.setStrokeColor(LINE);c.roundRect(x,y,w,h,6,fill=1,stroke=1)
        c.setFillColor(NAVY);c.setFont('DB',9.0);c.drawString(x+10,y+h-17,title)
        if sub:
            p=Paragraph(escape(normal(sub)),ParagraphStyle(name='fig',fontName='D',fontSize=7.8,leading=10,textColor=INK))
            pw,ph=p.wrap(w-20,h-25);p.drawOn(c,x+10,y+h-24-ph)
    def arrow(self,x1,y1,x2,y2,color=TEAL):
        import math
        c=self.canv;c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(1.1);c.line(x1,y1,x2,y2)
        a=math.atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-6*math.cos(a-.45),y2-6*math.sin(a-.45));p.lineTo(x2-6*math.cos(a+.45),y2-6*math.sin(a+.45));p.close();c.drawPath(p,fill=1,stroke=0)
    def draw(self):
        if self.kind=='layers':
            rows=[('01  MENSCH / ID01','Priorität, Adoption, technische Freigabe'),('02  GOVERNANCE / KONTROLLE','AGBs, Manifest, Baseline, Tickets, AIM, Ledger'),('03  AUSFÜHRUNG / RUNTIME','LLM-Routing, Parser, Python, Scheduler, Transport'),('04  WISSEN / RETRIEVAL','Quellenobjekte, Chunks, Graph- und Vektorprojektionen'),('05  ENGINEERING / SOLVER','Geprüfte Eingaben, Einheiten, Referenzen, Fachrechnung'),('06  AUSTAUSCH / AUDIT','Drive-Original, GitHub-Snapshot, Readback, ACK')]
            for i,(a,b) in enumerate(rows):
                y=217-i*42;self.box(12,y,460,37,a,b)
                if i<5:self.arrow(242,y,242,y-5)
        elif self.kind=='pipeline':
            self.canv.translate(18,0);self.canv.scale(.92,.92)
            rows=[('1 Quelle + Rechte','Unveränderte Originalbytes'),('2 Identität + Registry','Version, Darstellung, SHA-256'),('3 Extraktion + OCR','Seiten-/Blockmodell'),('4 Chunk + Kandidat','Locator, Kontext, Schema'),('5 Verifikation','Hash, Inhalt, Review, Gate'),('6 Projektionen','Graph / optional Vektorindex'),('7 Retrieval + Reuse','Quelle / Locator oder Enthaltung')]
            for i,(a,b) in enumerate(rows):
                x=8 if i<4 else 263;y=275-(i if i<4 else i-4)*75
                self.box(x,y,215,57,a,b)
                if i<3 or 4<=i<6:self.arrow(x+107,y,x+107,y-18)
            self.arrow(223,78,242,78);self.arrow(242,78,242,303);self.arrow(242,303,263,303)
        elif self.kind=='states':
            for x,t,s in [(5,'OPEN','Auftrag erfasst'),(171,'CLAIMED','Zuständigkeit belegt'),(337,'RUNNING','Tatsächlicher Lauf')]:self.box(x,180,145,54,t,s)
            self.arrow(150,207,171,207);self.arrow(316,207,337,207)
            self.box(337,83,145,57,'PRÜFUNG','Ergebnis + Abnahmekriterien');self.arrow(410,180,410,140)
            self.box(171,83,145,57,'DONE','Akzeptanz erfüllt / Waiver');self.arrow(337,111,316,111)
            self.box(5,83,145,57,'BLOCKED / FAILED','Fehler ausdrücklich erhalten',colors.HexColor('#FFF3DB'))
            self.arrow(410,180,77,140,GOLD)
            self.box(171,0,311,54,'HUMAN GATE = SEPARATE ACHSE','Kein automatischer Freigabeschluss aus DONE oder PASS',colors.HexColor('#E2F1EF'))
        elif self.kind=='storage':
            self.box(140,175,220,55,'DRIVE / DOKUMENT-SSOT','Kanonische IDs, Versionen, Quellen')
            for x,t,s in [(4,'WORK','WO, Rücklauf, Runlog'),(170,'SSOT-ROOT','Handbuch, Governance, Ledger'),(336,'ARTEFAKTE / ARCHIV','Muster, Paket, Vorstände')]:
                self.box(x,77,145,62,t,s);self.arrow(250,175,x+72,139)
            self.box(75,0,335,48,'GITHUB = VERSIONIERTER AUSTAUSCH','Code, Tests und identifizierte Dokument-Snapshots')
            self.arrow(242,77,242,48)
        elif self.kind=='integrity':
            self.box(5,140,220,60,'KONZEPT / LOGISCHE IDENTITÄT','Eine AIM-ID bleibt über Revisionen erhalten')
            self.box(263,140,220,60,'KONKRETE REPRÄSENTATION','Datei-ID + Version + vollständiger Bytehash');self.arrow(225,170,263,170)
            self.box(5,40,220,62,'VORGÄNGER / SNAPSHOT','Erhaltene Bytes; supersedes + Locator');self.box(263,40,220,62,'NACHFOLGER / READBACK','Neue Bytes prüfen; Ledger additiv erweitern');self.arrow(225,71,263,71)
            self.arrow(373,140,373,102)
        elif self.kind=='intervals':
            for i,(t,s) in enumerate([('1 min','Spezial-WO, Scope, Ablauf, Stop'),('10 / 30 / 60 min','Je Aufgabe und Runtime evaluieren'),('00 / 06 / 12 / 18','Wandzeit Europe/Vienna'),('Wöchentlich','Eigener Wartungsauftrag')]):
                self.box(10,162-i*53,463,46,t,s)

def md_blocks(text: str) -> list:
    lines=text.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            out.append(Paragraph('<br/>'.join(escape(normal(x)) for x in block),styles['CodeN']));i+=1;continue
        if line.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',c) for c in cells):table.append(cells)
                i+=1
            cols=len(table[0]);weights=[1]*cols
            if cols==3:weights=[.23,.37,.40]
            if cols==4:weights=[.22,.28,.25,.25]
            if cols==2:weights=[.32,.68]
            widths=[487*w/sum(weights) for w in weights]
            data=[[P(c,'CellHeadN' if r==0 else 'CellN') for c in row] for r,row in enumerate(table)]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.5,LINE),('LINEBELOW',(0,0),(-1,0),.5,TEAL),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));out.extend([t,Spacer(1,10)]);continue
        if line.startswith('### '):out.append(P(line[4:],'H2N'));i+=1;continue
        if line.startswith('- '):out.append(P('• '+line[2:]));i+=1;continue
        if re.match(r'^\d+[ .]',line):out.append(P(line));i+=1;continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('|','```','### ','- ')) and not re.match(r'^\d+[ .]',lines[i].strip()):
            para.append(lines[i].strip());i+=1
        out.append(P(' '.join(para)))
    return out

class DossierDoc(SimpleDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='H1N':
            text=f.getPlainText();key='h'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,0,False);self.notify('TOCEntry',(0,text,self.page,key))

def frame(c,doc):
    w,h=A4;c.saveState()
    if doc.page>1:
        c.setStrokeColor(LINE);c.setLineWidth(.6);c.line(54,h-42,w-54,h-42)
        c.setFont('DB',7.4);c.setFillColor(NAVY);c.drawString(54,h-30,'NEXUS AI-OS  /  TECHNISCHES DOSSIER')
        c.setFont('D',7.2);c.setFillColor(MUTED);c.drawRightString(w-54,h-30,'v1.0.0  ·  REVIEW')
    c.setStrokeColor(LINE);c.line(54,43,w-54,43);c.setFont('D',7.2);c.setFillColor(MUTED)
    c.drawString(54,29,'Quellengebundene Architektur | Stand '+NOW.strftime('%d.%m.%Y'))
    c.drawRightString(w-54,29,f'{doc.page:02d}')
    c.restoreState()

story=[]
story+=[Spacer(1,30),P('NEXUS AI-OS','H2N'),Spacer(1,12)]
cover=ParagraphStyle(name='cover',fontName='DB',fontSize=32,leading=38,textColor=NAVY,spaceAfter=14)
story.append(Paragraph('Systemarchitektur,<br/>Hierarchie &amp;<br/>Funktionslogik',cover))
story.append(P('AEC Engineering Knowledge System','H2N'))
story.append(P('TECHNISCHES DOSSIER · USER MANUAL · IMPLEMENTATION GUIDE'))
story.append(Spacer(1,16));story.append(Figure('layers'))
story.append(P('Dokumentstatus REVIEW · Version 1.0.0 · '+TS,'SmallN'))
story.append(P('Für Julian Zotter / NEXUS ID01. Vektorbasiertes A4-Dokument mit eingebetteten Schriften und durchsuchbarem Text. Kein Nachweis einer Produktions- oder Engineering-Freigabe.','SmallN'))
story.append(PageBreak());story.append(P('Leseführung und Systembefund','H1N'))
story.extend(md_blocks('''Ziel dieses Dossiers ist ein nachvollziehbares Gesamtmodell: Wer entscheidet, wo Daten liegen, welche Softwarebausteine existieren, wie Quellen zu Wissen werden und welche Nachweise einen Auftrag abschließen. Das vorhandene Handbuch v0.2.0 wird vollständig als betriebliche Basis übernommen und durch Architekturtafeln sowie konkrete Implementierungs- und Abnahmeschritte ergänzt. [S01]

### Problemstellung
Die Komponenten sind über Dokumente, Code, Accounts und Speicherorte verteilt. Risiken entstehen an Übergängen: Ablage wird mit Kenntnisnahme verwechselt, Test-PASS mit Freigabe, Modellrolle mit erreichbarer Runtime und ein geplanter Mechanismus mit laufendem Betrieb. Das Design muss diese Übergänge explizit machen. [S01, S03, S06]

### Methode und Prüfumfang
Aktuelle Drive-Inhalte des Handbuchs, AIM, Reparatur-WO, AGBs, Manifest, Baseline und Technikachsen-Entscheids wurden gelesen. Zusätzlich wurden PR41 und PR4 frisch abgefragt. Bestehende Testzahlen sind Angaben der jeweiligen Prüfnachweise; in diesem Dossierlauf wurden weder Parserbenchmarks noch fremde Accounts oder Scheduler ausgeführt. [S01-S10]

### Drei getrennte Wahrheiten
**Normativ:** Welche Quellen und datierten Entscheidungen gelten? **Technisch:** Welcher konkrete Code und welche Schnittstelle sind vorhanden? **Operativ:** Welcher Lauf ist tatsächlich mit Ergebnis, Readback und Abnahme nachgewiesen? Kein Bereich ersetzt den anderen.

### Status der Lieferung
Das Architekturhandbuch v0.2.0 ist gespeichert. PR41 ist offen und Draft; sein Dokumentationsstand ist kein gemergter Produktionsstand. Parser PR4 steht auf rc3 und ist offen/unmerged. Eine unabhängige Handbuch- und Betriebsabnahme bleibt offen. [S01, S09, S10]
'''))
story.append(PageBreak());story.append(P('Inhaltsverzeichnis','H1N'));toc=TableOfContents();toc.levelStyles=[styles['TOCN']];story.append(toc);story.append(PageBreak())

manual=S['manual']['content'];manual=manual.split('---\n',2)[2];manual=manual.split('## Quellenverzeichnis')[0]
sections=re.split(r'(?=^## \d+\.)',manual,flags=re.M)
figures={4:('layers','Abb. 1 - Funktionale Verantwortungs- und Nachweisschichten. Schematische Sicht; keine zusätzliche globale Layer-Taxonomie.'),5:('storage','Abb. 2 - Kanonische Dokumentablage und versionierter Austausch; GitHub-Dokumente sind Spiegel.'),7:('integrity','Abb. 3 - Logische Identität, Repräsentation und additive Versionsnachweise.'),9:('states','Abb. 4 - Minimaler Auftragszustand und getrennte menschliche Freigabe.'),12:('intervals','Abb. 5 - Auftragsbezogene Evaluierungsprofile; kein Nachweis aktivierter Überwachung.'),14:('pipeline','Abb. 6 - Quellengebundene Wissenspipeline; Verifikation vor bestätigter Projektion.')}
for sec in sections:
    if not sec.startswith('## '):continue
    heading,body=sec.split('\n',1);num=int(re.match(r'## (\d+)',heading)[1]);title=heading[3:]
    if num in (4,5,6,9,10,12,14,15,18):story.append(PageBreak())
    story.append(P(title,'H1N'))
    story.append(P('QUELLENBASIS: S01; ergänzend S02-S08. Implementierungsdetails sind quellenbezogen, keine neue Live-Betriebsabnahme.','SmallN'))
    if num in figures:
        kind,caption=figures[num];story.append(Figure(kind));story.append(P(caption,'SmallN'));story.append(Spacer(1,8))
    story.extend(md_blocks(body))
    if num==4:story.append(P('Einordnung: Die Schichten dieses Dossiers sind eine Darstellungsstruktur. Sie ersetzen weder Pace-Layer-Entwürfe noch die technische Domänenachse.','SmallN'))
    if num==20:story.append(PageBreak())

story.append(P('21. Implementation Guide - kontrollierte Ausbauschritte','H1N'))
story.extend(md_blocks('''Der Ausbau erfolgt entlang nachgewiesener Übergänge. Ein Arbeitspaket erhält erst dann einen Abschlussstatus, wenn sein konkreter Umfang überprüft wurde. Die Reihenfolge ist ein Implementierungsvorschlag auf Basis der offenen Nachweise, keine Aktivierung neuer Aufgaben. [S03, S06]

| Schritt | Konkretes Ergebnis | Abnahmekriterium |
|---|---|---|
| I1 Governance-Vertrag | Vorrang, Namen, Statusachsen und Quell-IDs konsolidiert | Datierter ID01-Entscheid; widersprüchliche Spiegel markiert |
| I2 Dokumenttransport | Autorisierter Eingang und gespeicherter Rücklauf | Byte-Readback, Hash, Ledger, Empfänger-ACK getrennt |
| I3 Auftragsbetrieb | Ein vorhandenes Ticket durchgängig abgearbeitet | Claim, Bearbeitung, Prüfung, Ergebnis, Wiederanlauf |
| I4 Quellenpilot | Eingefrorene Quelle bis Kandidatenobjekt | Stabile IDs, Seiten-/Block-Locator, Replay ohne Dubletten |
| I5 Retrievalpilot | Quellengebundene Abfragen auf freigegebenem Teilbestand | Richtige Quelle/Stelle oder Enthaltung; negative Testfragen |
| I6 Engineering-Reuse | Fachsolver nutzt ausdrücklich geprüfte Wissensobjekte | Einheiten, Normausgabe/NAD, Referenz und unabhängige Prüfung |
| I7 Betrieb | Wiederkehrende Ausführung mit begrenzten Profilen | Echte Laufquittungen, Ausfallprobe, Wiederherstellung, Human Gate |

### Fehlerszenarien vor Skalierung
Doppelte Zustellung darf keinen zweiten Auftrag erzeugen. Fehlende Credentials müssen als Blocker erkennbar sein. Ein abgelaufener Minutenmodus muss stoppen. Quellenmanipulation muss die Verifikation verhindern. Ein Schreibkonflikt darf keine fremde Fassung still ersetzen. Ein fehlender Locator verhindert die Beförderung zum bestätigten Wissensobjekt.
'''));story.append(PageBreak())
story.append(P('22. Schnittstellen und Nachweisverträge','H1N'))
story.extend(md_blocks('''| Übergang | Mindestdaten | Unzulässige Gleichsetzung |
|---|---|---|
| Idee zu WO | AIM-ID, ticket_id, Scope, Owner, Acceptance | Idee erfasst = Auftrag ausgeführt |
| WO zu Runtime | Claim, Instanz, Rechte, Inputversion | Rollenname = laufender Agent |
| Quelle zu Chunk | source_id, Darstellung, Hash, Locator | ähnlicher Text = identische Quelle |
| Kandidat zu Graph | Schema, Relationsbeleg, Evidenzstatus | Vektornähe = bewiesene Relation |
| Ergebnis zu Register | Datei-ID, Version, Bytehash, Quelle | Upload = registriert |
| Publikation zu Empfänger | Ausgabereferenz und tatsächliche Antwort | gespeichert = zugestellt = ACK |
| Test zu Freigabe | Commit, Testumfang, Reviewer, ID01-Entscheid | PASS = produktionsreif |

### Kontrollierte Mindestlogik
Schema-first bedeutet: Felder, Zustände und Übergangsbedingungen vor ihrer Automatisierung definieren. FAIL-CLOSED bedeutet: Bei fehlender kritischer Evidenz den betroffenen Schritt blockieren. Es bedeutet nicht, unabhängige autorisierte Dokumentationsarbeit einzustellen. Registry-first bedeutet: Identität vor semantischer Anreicherung; die Suche erzeugt keine nachträgliche Quellenidentität. [S02, S03]

### Systemgrenzen
Dieses Dossier installiert keine Software, ändert keine Rechte und aktiviert keine Daueraufgabe. Kein Fremdmodell wird als beteiligt behauptet, nur weil sein Name in einem Rollenregister oder Routingvorschlag steht. Externe Normen und rechtliche Geltung werden hier nicht neu bewertet.
'''));story.append(PageBreak())
story.append(P('23. Ausblick und geordnete Ideen','H1N'))
story.extend(md_blocks('''### Vorrangige Entwicklung
Zuerst die Übergänge des bestehenden Systems schließen. Danach vorhandene Parserfamilie und Quellenmodelle konsolidieren, Retrieval gegen Referenzfragen prüfen und nur nachgewiesene Spezialisten anbinden. Mehr Frameworks oder zusätzliche Register sind kein Ersatz für diese Abnahme.

### Ideen mit bestehender AIM-Zuordnung
| AIM | Gegenstand | Fortführung |
|---|---|---|
| AIM-0003 | CPLM / CICKS / Kommunikationsprofile | Betrieb über tatsächliche Laufnachweise konkretisieren |
| AIM-0004 | Folder-Zustand / DELTA | Zustandsänderungen und Vorgänger referenzieren |
| AIM-0005 | Capability-/Rechtematrix | Konto, Runtime und getestete Operation getrennt erfassen |
| AIM-0006 | Kompetenzrouting | Auswahlregel und erreichbare Instanz gemeinsam prüfen |
| AIM-0007 | Pace Layers | Änderungsgrenzen als Vorschlag präzisieren |
| AIM-0008 | Gemini-Schreibbrücke | Einen autorisierten, idempotenten Roundtrip nachweisen |
| AIM-0009 | Markdown-Historiemuster | Vorhandenes Muster prüfen; Validator und Rollout separat |

Keine neue Ideenliste und keine automatische Statuspromotion durch diese Publikation. Umgesetzte, zurückgestellte und verworfene Ideen bleiben im bestehenden Register nachvollziehbar. [S05]

### Konsequenz für das Zielbild
NEXUS soll eine kontrollierte Verbindung aus Quellen, Software und menschlicher Entscheidung bilden. Skalierung ist nachgewiesen, wenn mehr Aufträge bei unveränderten Identitäts-, Evidenz- und Freigaberegeln zuverlässig verarbeitet werden - nicht, wenn nur mehr Modelle oder Dateien vorhanden sind.
'''));story.append(PageBreak())

sources=[('S01','Betriebshandbuch v0.2.0','https://drive.google.com/file/d/1Xo4gL6N_OWcnnde70baStp0ATNVwu5Wo/view','Volltextbasis; bestehende Architektur, Ablage, Betrieb und offene Nachweise.'),('S02','CURRENT Manifest 28.09.2026','https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit','§2 spätere Adoptionen; §4 Rollen; §§6-10 Betrieb und Änderung.'),('S03','CURRENT Baseline 28.09.2026','https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit','MUST-20-34, 40-55, 90-96, 130-159.'),('S04','_AGBS.md v002','https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view','Freigabevermerk 23.10.; Vorrang und Benennung; Abgleich mit älteren Quellen offen.'),('S05','AIM v0.3.2','https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view','Neun Ideen; Fortschrittscodes und Dispositionen; Historie.'),('S06','Reparaturcheckliste v1.0.2','https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view','Abgegrenzte Dokumentationslieferung und verbleibende Betriebsnachweise.'),('S07','Technikachsen-Entscheidung v1.0.0','https://drive.google.com/file/d/1prAgbIXHIOac8uJOoPClMFbke9I_DaM-/view','Technik primär, Recht ergänzend, Deutsch primär; Ledger0059.'),('S08','WORK Folder-Policy 0.4.0-pilot','https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view','Dokument-SSOT, Spiegelrolle und bestehende Betriebsblocker; ältere Rechtetests nicht als heutiger Live-Test.'),('S09','nexus-platform PR41','https://github.com/julianzotter/nexus-platform/pull/41','Frisch abgefragt: offen, Draft, unmerged; Head '+S['pr41']['head_sha']+'.'),('S10','Parser PR4 / rc3','https://github.com/julianzotter/AI-ENGINEERING-SYSTEM/pull/4','Frisch abgefragt: offen, unmerged; Head '+S['pr4']['head_sha']+'. Testzahlen sind PR-Bericht, kein neuer Testlauf.'),('S11','ID-Ledger','https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view','Aktueller Identitätsnachweis; keine ID-Vergabe aus Dateinamen.'),('S12','Dokumentations-Abschlussbeleg','https://drive.google.com/file/d/1Y2C6bW_9TtQNcuRGSTQCAa_N5JlN2eZM/view','Vorangegangene Ablage-, Hash-, Register- und GitHub-Nachweise.')]
story.append(P('24. Quellen, Versionen und Prüfgrenzen','H1N'))
story.append(P('Abrufstand dieses Dossierlaufs: '+TS+'. Interne Quellen und Repositorystände; keine neue normative Bemessung. Links sind klickbar.','SmallN'))
for code,title,url,scope in sources:
    story.append(P(code+'  '+title,'SourceTitle'));story.append(P(scope,'SmallN'));story.append(Paragraph('<link href="'+url+'" color="#007E87">'+escape(url)+'</link>',styles['SmallN']))
story.append(P('Die Quellenbasis enthält bekannte Konflikte; diese werden sichtbar gehalten. Layout-/Hashprüfungen dieses PDF sind von unabhängiger Inhaltsprüfung und technischer Freigabe getrennt.','SmallN'))

doc=DossierDoc(str(PDF),pagesize=A4,rightMargin=54,leftMargin=54,topMargin=60,bottomMargin=57,title='NEXUS AI-OS - Systemarchitektur, Hierarchie und Funktionslogik',author='OpenAI Codex / NEXUS ID03, im Auftrag ID01',subject='Technisches Dossier / User Manual / Implementation Guide',pageCompression=1)
doc.multiBuild(story,onFirstPage=frame,onLaterPages=frame)
reader=PdfReader(PDF);text='\n'.join(p.extract_text() or '' for p in reader.pages)
assert len(reader.pages)>=16 and all(len(p.extract_text() or '')>150 for p in reader.pages)
assert all(t in text for t in ['Implementation Guide','MUST-30','AIM-0009','336f68e','Quellen'])
md=OUT/(PREFIX+'NEXUS-SYSTEMARCHITEKTUR-DOSSIER-v1.0.0_0087_ID03.md')
md.write_text('---\nname: NEXUS-SYSTEMARCHITEKTUR-DOSSIER\nversion: 1.0.0\nstatus: REVIEW\ntimestamp: '+TS+'\nagent_id: ID03\nexecutor_instance: /root\ngate: PENDING (Human Gate ID01)\nsource_manual: '+S['manual']['url']+'\n---\n# NEXUS AI-OS - Systemarchitektur, Hierarchie und Funktionslogik\n\nPDF-Quelltextbasis: das vollständige aktuelle Handbuch v0.2.0, Architekturtafeln und die im Generator dokumentierten Dossierkapitel. Der Generator ist die vollständige reproduzierbare Layoutquelle.\n\n'+manual+'\n## Dossier-Ergänzungen\nLeseführung/Problemstellung/Methode, sechs Vektorarchitekturtafeln, Implementation Guide mit I1-I7, Schnittstellenverträge, Ausblick und Quellenverzeichnis werden vollständig im mitgelieferten Generator geführt.\n',encoding='utf-8')
manifest={'title':'NEXUS AI-OS Systemarchitektur-Dossier','version':'1.0.0','status':'REVIEW','timestamp':TS,'pages':len(reader.pages),'pdf_path':str(PDF),'source_path':str(md),'generator_path':str(ROOT/'create_architecture_dossier.py'),'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(md.read_bytes()).hexdigest(),'format':'A4 / vector text and diagrams / embedded fonts','sources':[{'id':x[0],'title':x[1],'url':x[2],'scope':x[3]} for x in sources],'parser_commit':S['pr4']['head_sha'],'documentation_commit':S['pr41']['head_sha'],'checks':{'pdf_readable':'PASS','text_extraction':'PASS','visual_qa':'PENDING'},'filename_prefix':PREFIX}
(OUT/'dossier_build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(manifest,ensure_ascii=False))
