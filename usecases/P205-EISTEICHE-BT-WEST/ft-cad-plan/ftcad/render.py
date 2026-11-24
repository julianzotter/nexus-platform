"""DXF-Layouts -> vektorielles PDF (mehrseitig) und PostScript (je Blatt). Renderer: ezdxf drawing + matplotlib."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.config import ColorPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

MM = 1 / 25.4
CFG = Configuration(color_policy=ColorPolicy.COLOR)


def _page(doc, layout_name: str) -> plt.Figure:
    """Ein Papierbereichs-Layout im Maßstab 1:1 auf A3 quer (420×297 mm)."""
    fig = plt.figure(figsize=(420 * MM, 297 * MM))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_facecolor("white")
    ctx = RenderContext(doc)
    ctx.set_current_layout(doc.layouts.get(layout_name))
    Frontend(ctx, MatplotlibBackend(ax), config=CFG).draw_layout(doc.layouts.get(layout_name), finalize=True)
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 297)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def render(dxf_path: Path, out_dir: Path, postscript: bool = True) -> list[Path]:
    """Schreibt <stem>.pdf (alle Blätter) und optional <stem>_BlattN.ps. Rückgabe: erzeugte Dateien."""
    doc = ezdxf.readfile(dxf_path)
    names = [n for n in doc.layouts.names_in_taborder() if n != "Model"]
    pdf = out_dir / f"{dxf_path.stem}.pdf"
    made = [pdf]
    with PdfPages(pdf, metadata={"Title": dxf_path.stem, "Creator": "ft-cad-plan / ezdxf"}) as pp:
        for k, n in enumerate(names, 1):
            fig = _page(doc, n)
            pp.savefig(fig)
            if postscript:
                ps = out_dir / f"{dxf_path.stem}_{n}.ps"
                fig.savefig(ps, format="ps", papertype="a3", orientation="landscape")
                made.append(ps)
            plt.close(fig)
    return made
