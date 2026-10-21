---
name: access-point-navigator
description: Find and rank the fastest verified API, MCP, plugin, skill, or open-source library access point for NEXUS AEC, CAD, BIM, RFEM, cloud storage, documents and knowledge workflows. Use when asked for Schnittstellen, Access Points, MCP Server, API links, software integration, or fastest route to a tool.
---

# NEXUS Access Point Navigator

1. Read `access-points/registry.json` in `julianzotter/nexus-platform` first; treat it as a catalog, not proof of connectivity.
2. Filter by user task, domain and priority. Prefer existing authenticated connectors, then native APIs, then tested MCP wrappers, then local libraries.
3. For each candidate report: name, category, canonical documentation URL, installed/authenticated/tested status (only if verified), capabilities, next action.
4. Never conflate documentation URL, live API endpoint, MCP server transport URL and credentials.
5. When current availability matters, validate against official documentation and available connector tools. Mark unverified facts explicitly.
6. For CAD/BIM/structural workflows favor Dlubal API, IfcOpenShell, buildingSMART, FreeCAD, ezdxf; for file discovery favor Google Drive metadata and existing indexes before full-content reads.
7. Never disclose or store secrets. No writes to production without authorization. Record verification evidence and timestamp.
8. Output max three recommended routes and direct links. Include a concrete next step.
