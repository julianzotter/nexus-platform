from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


SCHEMA = """
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;
CREATE TABLE metadata (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE sources (
  source_uid TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  account_scope TEXT NOT NULL,
  native_id TEXT,
  name TEXT NOT NULL,
  locator TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  content_status TEXT NOT NULL,
  authority_status TEXT NOT NULL,
  revision TEXT,
  sha256_original TEXT,
  covered_claim TEXT NOT NULL,
  evidence_class TEXT NOT NULL
);
CREATE TABLE roles (
  role_id TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  capability TEXT NOT NULL,
  write_scope TEXT NOT NULL,
  approval_scope TEXT NOT NULL,
  status TEXT NOT NULL
);
CREATE TABLE findings (
  finding_id TEXT PRIMARY KEY,
  topic TEXT NOT NULL,
  claim TEXT NOT NULL,
  evidence_class TEXT NOT NULL,
  source_uid TEXT NOT NULL REFERENCES sources(source_uid),
  locator TEXT NOT NULL,
  consequence TEXT NOT NULL,
  required_action TEXT NOT NULL,
  status TEXT NOT NULL,
  technical_release INTEGER NOT NULL DEFAULT 0 CHECK (technical_release IN (0,1))
);
CREATE TABLE signal_energy (
  signal_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  domain TEXT NOT NULL,
  evidence_class TEXT NOT NULL,
  consequence INTEGER NOT NULL CHECK (consequence BETWEEN 0 AND 4),
  urgency INTEGER NOT NULL CHECK (urgency BETWEEN 0 AND 4),
  dependencies INTEGER NOT NULL CHECK (dependencies BETWEEN 0 AND 4),
  uncertainty INTEGER NOT NULL CHECK (uncertainty BETWEEN 0 AND 4),
  energy INTEGER NOT NULL,
  priority TEXT NOT NULL CHECK (priority IN ('P0','P1','P2','P3')),
  release_gate TEXT NOT NULL,
  CHECK (energy = 4*consequence + 3*urgency + 2*dependencies + uncertainty)
);
CREATE TABLE experts (
  expert_id TEXT PRIMARY KEY,
  capability TEXT NOT NULL,
  primary_role_id TEXT REFERENCES roles(role_id),
  control_role_id TEXT REFERENCES roles(role_id),
  solver_required INTEGER NOT NULL CHECK (solver_required IN (0,1)),
  allowed_output TEXT NOT NULL
);
CREATE TABLE routes (
  route_id TEXT PRIMARY KEY,
  signal_id TEXT NOT NULL REFERENCES signal_energy(signal_id),
  sequence_no INTEGER NOT NULL,
  expert_id TEXT NOT NULL REFERENCES experts(expert_id),
  assigned_role_id TEXT REFERENCES roles(role_id),
  human_gate TEXT NOT NULL,
  status TEXT NOT NULL,
  UNIQUE(signal_id, sequence_no)
);
CREATE TABLE work_packages (
  package_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  objective TEXT NOT NULL,
  required_input TEXT NOT NULL,
  output_contract TEXT NOT NULL,
  gate TEXT NOT NULL,
  owner_role_id TEXT REFERENCES roles(role_id),
  status TEXT NOT NULL
);
CREATE TABLE runs (
  run_id TEXT PRIMARY KEY,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  goal TEXT NOT NULL,
  operation TEXT NOT NULL,
  status TEXT NOT NULL,
  coverage TEXT NOT NULL,
  open_items TEXT NOT NULL,
  tokens_input INTEGER,
  tokens_output INTEGER,
  telemetry_status TEXT NOT NULL
);
CREATE TABLE decisions (
  decision_id TEXT PRIMARY KEY,
  finding_id TEXT REFERENCES findings(finding_id),
  decision TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  approver_role_id TEXT REFERENCES roles(role_id),
  decided_at TEXT,
  status TEXT NOT NULL
);
CREATE TABLE blockers (
  blocker_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  affected_packages TEXT NOT NULL,
  owner_role_id TEXT REFERENCES roles(role_id),
  exit_criterion TEXT NOT NULL,
  status TEXT NOT NULL
);
CREATE VIEW v_priority_queue AS
SELECT s.signal_id, s.priority, s.energy, s.title, s.release_gate,
       group_concat(r.assigned_role_id || ':' || r.expert_id, ' -> ') AS route
FROM signal_energy s LEFT JOIN routes r ON r.signal_id = s.signal_id
GROUP BY s.signal_id ORDER BY s.energy DESC, s.signal_id;
CREATE VIEW v_release_blockers AS
SELECT blocker_id, title, owner_role_id, exit_criterion
FROM blockers WHERE status <> 'CLOSED';
"""


def rows_sources(observed_at: str) -> list[tuple[object, ...]]:
    drive = "PRIVATE_PROJECT"
    return [
        ("SRC-AGBS", "Google Drive", drive, "10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg", "_AGBS.md v007.1", "https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view", observed_at, "READ", "GOVERNANCE", "v007.1", None, "NEXUS process and persistence rules", "VERIFIED"),
        ("SRC-BASELINE", "Google Drive", drive, "1CdwNHr6i8lMG3k8A939kiznLMw8q7J69", "NEXUS baseline", "https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view", observed_at, "READ", "GOVERNANCE", None, None, "Approved operating baseline", "VERIFIED"),
        ("SRC-MANIFEST", "Google Drive", drive, "1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn", "NEXUS manifest", "https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view", observed_at, "READ", "GOVERNANCE", None, None, "Role and system manifest", "VERIFIED"),
        ("SRC-TICKETS", "Google Drive", drive, "1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE", "NEXUS ticket register", "https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit", observed_at, "READ", "GOVERNANCE", None, None, "Ticket identities and state", "VERIFIED"),
        ("SRC-REVE", "Google Drive", drive, "1oVj79Li7EiYxo2SnrvgtNGzbF3tmqbiQ", "FT-Träger Matrix RevE", "https://drive.google.com/file/d/1oVj79Li7EiYxo2SnrvgtNGzbF3tmqbiQ/view", observed_at, "BYTE_HASH_VERIFIED", "TECHNICAL_INPUT", "RevE", "af4d60389b7a89bb14995429eff3f3840948e7142133d575420d36af1240239e", "Stored workbook values and formulas", "VERIFIED"),
        ("SRC-REVF", "Google Drive", drive, "1BPpKIENzRPrCu0qhdn34YuErKzMZ8oyy", "FT-Träger Matrix RevF", "https://drive.google.com/file/d/1BPpKIENzRPrCu0qhdn34YuErKzMZ8oyy/view", observed_at, "HASH_FROM_REVIEW", "REPAIR_DRAFT", "RevF", "c47a1bc2308b19b16f69c07824fbf2f7508291fb252bfcc902389d8a486c33ee", "Changed formulas, choices and stale cached values", "VERIFIED"),
        ("SRC-PEER", "Google Drive", drive, "1N07Y1R8lIATvKs286mCZV_AEcetj6wdi", "P205 peer review v1.1", "https://drive.google.com/file/d/1N07Y1R8lIATvKs286mCZV_AEcetj6wdi/view", observed_at, "READ", "DERIVED_REVIEW", "v1.1", None, "Reproduced counts, cache conflicts and gaps", "VERIFIED"),
        ("SRC-SOLUTIONS", "Google Drive", drive, "1WrBCbEX12gid99s7TTn8MQ-c8L062hPW", "RevF cell comparison and solutions", "https://drive.google.com/file/d/1WrBCbEX12gid99s7TTn8MQ-c8L062hPW/view", observed_at, "READ", "DERIVED_REVIEW", None, None, "Cell-level change evidence", "VERIFIED"),
        ("SRC-PLANS", "Google Drive", drive, "1l6d5tZ33xJiasDYwbHU5-qrSHM3mjTDx", "BEKAMENT plan comparison", "https://drive.google.com/file/d/1l6d5tZ33xJiasDYwbHU5-qrSHM3mjTDx/view", observed_at, "READ", "TECHNICAL_INPUT", None, None, "EG-F and 2OG-3 geometry comparison", "VERIFIED"),
        ("SRC-HESS", "Google Drive", drive, "1PN45eUhlleDXvq66tNVavdQC7X_yWDS2", "HESS report P240508-260610-r00.00", "https://drive.google.com/file/d/1PN45eUhlleDXvq66tNVavdQC7X_yWDS2/view", observed_at, "READ", "EXTERNAL_REVIEW", "r00.00", None, "Historical review scope 4OG axes 01-04", "VERIFIED"),
        ("SRC-RFEM", "Google Drive", drive, "1iHsMEdz5hgiDy8ThK5mpe9oEAAxrmRlj", "RFEM result folder", "https://drive.google.com/drive/folders/1iHsMEdz5hgiDy8ThK5mpe9oEAAxrmRlj", observed_at, "PARTIAL_FOLDER_REVIEW", "TECHNICAL_INPUT", None, None, "Four 1OG/2OG My/Vz EK100 plots; mapping metadata missing", "VERIFIED"),
    ]


ROLES: list[tuple[object, ...]] = [
    ("ID01", "Human engineering authority", "approval and technical decisions", "APPROVAL_ONLY", "TECHNICAL_RELEASE", "ACTIVE"),
    ("ID02", "Chief orchestrator", "routing, merge, governance", "WORK_AND_REGISTRY", "NONE", "ACTIVE"),
    ("ID03", "Independent peer reviewer", "independent QA", "REVIEW_OUTPUT", "REVIEW_ONLY", "ACTIVE"),
    ("ID04", "Evidence and source reviewer", "source identity, plans, locators", "EVIDENCE_OUTPUT", "NONE", "ACTIVE"),
    ("ID05", "External research", "public primary sources", "RESEARCH_OUTPUT", "NONE", "ACTIVE"),
    ("ID06", "Coding and Excel automation", "scripts and E2E execution", "RUN_OUTBOX", "NONE", "ACTIVE"),
    ("ID07", "Red-team auditor", "hash, cache and contradiction audit", "AUDIT_OUTBOX", "NONE", "ACTIVE"),
    ("ID08", "Local context worker", "local search and indexing", "LOCAL_OUTBOX", "NONE", "ACTIVE"),
    ("UNASSIGNED", "Unregistered model", "no authorized task", "NONE", "NONE", "BLOCKED"),
]


def rows_findings() -> list[tuple[object, ...]]:
    return [
        ("F01", "utilization_gt_105", "RevE stored cells >105%: M- 19, M+ 15, V 1, joint 115, consoles 52, openings 56.", "VERIFIED", "SRC-PEER", "section 1", "At least one stored exceedance exists in every listed proof group.", "Recalculate natively and independently verify every affected location.", "OPEN", 0),
        ("F02", "revf_cache", "RevF stored counts conflict with the separate LibreOffice report and include stale values.", "VERIFIED", "SRC-PEER", "section 1", "Current RevF utilization status is indeterminate.", "Run Excel Desktop full rebuild, save, close and OOXML/readback audit.", "BLOCKED", 0),
        ("F03", "stale_result", "2OG-I AH68 selects F3 while AH70 stores the former F1 MRd value.", "VERIFIED", "SRC-PEER", "2OG-I!AH68:AH72", "Affected stored utilization is unusable.", "Rebuild and compare selected catalogue type, Rd and utilization.", "BLOCKED", 0),
        ("F04", "missing_design_forces", "1OG-J and 2OG-J each contain 16 missing design-force values.", "VERIFIED", "SRC-PEER", "AH22:AK25", "Member design inputs are incomplete.", "Add model revision, member ID, local x, combination, axes, units and sign convention.", "BLOCKED", 0),
        ("F05", "missing_resistances", "RevF has 279 review locations with nonzero stored Ed; 251 have blank stored Rd.", "VERIFIED", "SRC-PEER", "result rows 32/33, 64/65, 70/71", "Stored results cannot establish proof completeness.", "Check applicability, formula and cache for each location.", "OPEN", 0),
        ("F06", "geometry_eg_f", "Plan EG-2004 indicates BT10a-III 40/65 cm near axis 4; EG-F!Z contains 40/80/15 cm.", "VERIFIED", "SRC-PLANS", "EG-F, axes 3-4", "A global geometry replacement is not justified.", "Confirm position list and assign geometry/detail/Rd section by section.", "BLOCKED", 0),
        ("F07", "geometry_2og_3_bc", "Plan O2-2006 supports WDB 30/8 cm and 57 cm residual depth; BC formulas still contain cross-column dependencies.", "DERIVED", "SRC-PLANS", "2OG-3!BC/BD", "Geometry itself need not be changed yet; formula ownership remains unresolved.", "Repair BC self-reference chain and recheck reinforcement, alpha and force chains.", "OPEN", 0),
        ("F08", "workbook_errors", "RevF stores 284 error cells; a hidden #REF! alternative branch and overview errors remain.", "VERIFIED", "SRC-PEER", "2OG-BC!Z114; Übersicht!N9/S9/T9", "Workbook error-free status is not achieved.", "Resolve every applicable error and document intentional non-applicable branches.", "BLOCKED", 0),
        ("F09", "layout_choices", "281 L/S/F selection cells changed; L1-L4 require manual engineering decision.", "VERIFIED", "SRC-PEER", "choice rows 30/62/68", "Automated rollout cannot approve layouts.", "Record plan reference, decision and reviewer for each affected section.", "BLOCKED", 0),
        ("F10", "prior_approval_scope", "HESS reviewed 26_02_11 and a sample of 4OG axes 01-04 only.", "VERIFIED", "SRC-HESS", "pages 6-8", "Historical review cannot be transferred to RevF or all floors.", "Obtain independent review of the current native recalculation.", "OPEN", 0),
        ("F11", "plan_release", "The available August plans are marked tender status; the technically latest execution basis is not evidenced.", "UNVERIFIED", "SRC-PLANS", "plan status fields", "Drawing and matrix revision may not be aligned.", "ID01 must name the binding drawing revision and position list.", "BLOCKED", 0),
        ("F12", "plot_coverage", "The standard print ranges omit 1OG-7!BJ156 and 2OG-7!BJ156.", "VERIFIED", "SRC-PEER", "plot audit", "The A2 proof package may omit relevant result cells.", "Extend or separately document plot coverage and readback.", "OPEN", 0),
    ]


SIGNALS: list[tuple[object, ...]] = [
    ("S01", "RevF stale/mixed result cache", "EXCEL", "VERIFIED", 4, 4, 4, 4, 40, "P0", "STOP"),
    ("S02", "RFEM mapping metadata missing", "RFEM", "VERIFIED", 4, 4, 4, 4, 40, "P0", "STOP"),
    ("S03", "Stored >105% inventory not resolved", "EC2_REVIEW", "VERIFIED", 4, 4, 4, 2, 38, "P0", "STOP"),
    ("S04", "EG-F and 2OG-3 geometry only partly resolved", "GEOMETRY", "VERIFIED", 4, 3, 3, 4, 35, "P0", "STOP"),
    ("S05", "Historical HESS scope not transferable", "GOVERNANCE", "VERIFIED", 4, 3, 4, 3, 36, "P0", "STOP"),
    ("S06", "Excel COM script invoked incompletely", "EXCEL", "VERIFIED", 3, 4, 3, 3, 33, "P0", "E2E_OPEN"),
    ("S07", "Expected workbook hash must match run target", "SOURCE_IDENTITY", "VERIFIED", 4, 4, 4, 4, 40, "P0", "STOP"),
    ("S08", "Tender and drawings depend on unresolved proof state", "DELIVERABLES", "DERIVED", 3, 3, 3, 3, 30, "P0", "BLOCKED"),
]


EXPERTS: list[tuple[object, ...]] = [
    ("SOURCE_IDENTITY", "File, version, hash and model revision", "ID04", "ID03", 0, "evidence record"),
    ("EXCEL_ENGINE", "Excel COM E2E and persisted-cache audit", "ID06", "ID07", 1, "run outbox"),
    ("RFEM_RESULTS", "Member, combination and local x mapping", "ID04", "ID03", 1, "evidence mapping"),
    ("GEOMETRY_PLAN", "Plan-to-matrix geometry mapping", "ID04", "ID03", 0, "geometry evidence"),
    ("EC2_REVIEW", "Input and result review using deterministic solver output", None, "ID03", 1, "review record"),
    ("RED_TEAM_AUDIT", "Contradiction, hash and cache audit", "ID07", "ID03", 0, "audit record"),
    ("RELEASE_GOVERNANCE", "AGBS, ledger, registry and rollout", "ID02", "ID03", 0, "governance record"),
]


ROUTES: list[tuple[object, ...]] = [
    ("RT-S01-1", "S01", 1, "EXCEL_ENGINE", "ID06", "ID01", "PENDING_ACK"),
    ("RT-S01-2", "S01", 2, "RED_TEAM_AUDIT", "ID07", "ID01", "PENDING_ACK"),
    ("RT-S02-1", "S02", 1, "RFEM_RESULTS", "ID04", "ID01", "PENDING_ACK"),
    ("RT-S02-2", "S02", 2, "GEOMETRY_PLAN", "ID04", "ID01", "PENDING_ACK"),
    ("RT-S03-1", "S03", 1, "EC2_REVIEW", None, "ID01", "SOLVER_REQUIRED"),
    ("RT-S03-2", "S03", 2, "RED_TEAM_AUDIT", "ID07", "ID01", "PENDING_ACK"),
    ("RT-S04-1", "S04", 1, "GEOMETRY_PLAN", "ID04", "ID01", "PENDING_ACK"),
    ("RT-S04-2", "S04", 2, "SOURCE_IDENTITY", "ID04", "ID01", "PENDING_ACK"),
    ("RT-S05-1", "S05", 1, "RELEASE_GOVERNANCE", "ID02", "ID01", "IN_PROGRESS"),
    ("RT-S06-1", "S06", 1, "EXCEL_ENGINE", "ID06", "ID01", "LOCAL_E2E_REQUIRED"),
    ("RT-S07-1", "S07", 1, "SOURCE_IDENTITY", "ID04", "ID01", "PENDING_ACK"),
    ("RT-S08-1", "S08", 1, "RELEASE_GOVERNANCE", "ID02", "ID01", "BLOCKED"),
    ("RT-S08-2", "S08", 2, "GEOMETRY_PLAN", "ID04", "ID01", "BLOCKED"),
]


def work_packages() -> list[tuple[object, ...]]:
    titles = [
        ("R00", "Governance bootstrap", "Read current AGBS, baseline, manifest, tickets and roles", "governance IDs", "bootstrap record", "G0", "ID02"),
        ("R01", "Source identity", "Inventory versions, hashes and duplicates", "source bytes and metadata", "source records", "G1", "ID04"),
        ("R02", "Excel native rebuild", "Validate formulas, cache, links and persisted results", "hash-bound workbook", "calculation and readback records", "G2", "ID06"),
        ("R03", "Geometry mapping", "Map sections, openings and component identities", "binding plans", "geometry evidence", "G1", "ID04"),
        ("R04", "Design-force mapping", "Map RFEM member, x, combination, axes and units", "RFEM model/results", "force evidence", "G2", "ID04"),
        ("R05", "Resistance logic", "Audit norms, parameters and Rd selection", "native rebuild plus norm profile", "solver/review record", "G2", "ID03"),
        ("R06", "Exceedance review", "Resolve every utilization above 105 percent", "R02-R05 passed", "location decisions", "G3", "ID03"),
        ("R07", "Tender and drawings", "Complete drawing and tender residual work", "released proof revision", "deliverable checklist", "G3", "ID02"),
        ("R08", "MoE synthesis", "Reconcile independent outputs without averaging conflicts", "review outboxes", "conflict report", "G3", "ID02"),
        ("R09", "Independent reproduction", "Repeat critical checks independently", "frozen evidence pack", "audit report", "G3", "ID07"),
        ("R10", "Human approval", "Make explicit technical decision", "all gates passed", "ID01 approval record", "G4", "ID01"),
        ("R11", "Registry and publication", "Persist, hash and read back all artifacts", "approved package", "receipt manifest", "G5", "ID02"),
    ]
    return [(*row, "PENDING") for row in titles]


def blockers() -> list[tuple[object, ...]]:
    return [
        ("B01", "Windows Excel Desktop E2E not executed", "R02,R05,R06", "ID06", "Successful native rebuild, save/close/reopen and independent OOXML readback", "OPEN"),
        ("B02", "RFEM source mapping incomplete", "R04,R05,R06", "ID04", "Model revision, member ID, local x, combination, axes, units and signs recorded", "OPEN"),
        ("B03", "Binding drawing revision not designated", "R03,R07", "ID01", "Explicit plan revision and position list decision", "OPEN"),
        ("B04", "Stored exceedances not independently resolved", "R06,R07,R10", "ID03", "Every >105 percent location has current calculated record and review decision", "OPEN"),
        ("B05", "Unregistered LLM roles", "R08,R11", "ID02", "Role register and ticket authorize model, scope and write path", "OPEN"),
    ]


def insert_many(db: sqlite3.Connection, sql: str, rows: Iterable[Sequence[object]]) -> None:
    db.executemany(sql, list(rows))


def seed(db: sqlite3.Connection, stamp: str, observed_at: str) -> None:
    insert_many(db, "INSERT INTO metadata VALUES (?,?)", [("project", "P205_Campus_Eisteiche_BIG / FT-Träger"), ("schema_version", "1.0"), ("created_at", observed_at), ("created_by", "ID02"), ("engineering_release", "BLOCKED"), ("score_formula", "E=4*C+3*U+2*D+X; routing only")])
    insert_many(db, "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows_sources(observed_at))
    insert_many(db, "INSERT INTO roles VALUES (?,?,?,?,?,?)", ROLES)
    insert_many(db, "INSERT INTO findings VALUES (?,?,?,?,?,?,?,?,?,?)", rows_findings())
    insert_many(db, "INSERT INTO signal_energy VALUES (?,?,?,?,?,?,?,?,?,?,?)", SIGNALS)
    insert_many(db, "INSERT INTO experts VALUES (?,?,?,?,?,?)", EXPERTS)
    insert_many(db, "INSERT INTO routes VALUES (?,?,?,?,?,?,?)", ROUTES)
    insert_many(db, "INSERT INTO work_packages VALUES (?,?,?,?,?,?,?,?)", work_packages())
    insert_many(db, "INSERT INTO blockers VALUES (?,?,?,?,?,?)", blockers())
    db.execute("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?)", (f"P205-FT-PR-{stamp}", observed_at, observed_at, "Critical peer review, MoE routing and workflow generation", "Read-only evidence synthesis plus artifact generation", "REVIEWED_BLOCKED", "Governance sources and named P205 artifacts; no Excel/RFEM recalculation", "Windows Excel E2E, RFEM mapping, plan revision and ID01 decision", None, None, "NOT_EXPOSED"))
    db.execute("INSERT INTO decisions VALUES (?,?,?,?,?,?,?)", ("D01", "F02", "Do not use RevF stored caches for technical release", "SRC-PEER section 1", "ID01", None, "PROPOSED_PENDING_ID01"))


def export_matrix(db: sqlite3.Connection, path: Path) -> None:
    rows = db.execute("SELECT * FROM v_priority_queue").fetchall()
    headers = [item[0] for item in db.execute("SELECT * FROM v_priority_queue").description]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def verify(db: sqlite3.Connection) -> None:
    if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise RuntimeError("SQLite integrity_check failed")
    if db.execute("PRAGMA foreign_key_check").fetchall():
        raise RuntimeError("SQLite foreign_key_check failed")
    if db.execute("SELECT count(*) FROM signal_energy").fetchone()[0] != 8:
        raise RuntimeError("Unexpected signal count")
    if db.execute("SELECT count(*) FROM findings").fetchone()[0] != 12:
        raise RuntimeError("Unexpected finding count")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--created-at", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    db_path = args.output_dir / f"{args.stamp}_ID02_P205_FT-AUDIT.sqlite"
    csv_path = args.output_dir / f"{args.stamp}_ID02_P205_FT-SIGNAL-ENERGY-MATRIX.csv"
    if db_path.exists() or csv_path.exists():
        raise FileExistsError("STOP: output already exists; use a new timestamp")
    with sqlite3.connect(db_path) as db:
        db.executescript(SCHEMA)
        seed(db, args.stamp, args.created_at)
        verify(db)
        export_matrix(db, csv_path)
        db.commit()
    print(db_path)
    print(csv_path)


if __name__ == "__main__":
    main()
