#!/usr/bin/env python3
"""
Generates G-code files for 6"x2" nametags from names.csv.
Uses TextPath.to_polygons() to flatten curves into line segments.
Requires: matplotlib, numpy
"""

import csv, math, os
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

# ----------- USER CONFIG -----------
INPUT_CSV = "names.csv"
OUTPUT_PREFIX = "nametags_run"
OUTPUT_DIR = "gcode_sheets"

WORK_W = 300.0
WORK_H = 300.0
TAG_W = 152.4
TAG_H = 50.8
SPACING = 10.0
TEXT_MARGIN = 4.0

# Your pen sequences (exact)
PEN_UP_SEQ = "G04 P0.5\n\rM03\n\rG04 P0.5"
PEN_DOWN_SEQ = "G04 P0.5\n\rM05\n\rG04 P0.5"

RAPID_FEED = 3000
LINEAR_FEED = 1000

FONT_PATH = None    # or "Arial.ttf"
FONT_POINTSIZE = 120.0
# -----------------------------------

font_prop = FontProperties(fname=FONT_PATH, size=FONT_POINTSIZE)

# compute cols/rows
cols = int(math.floor((WORK_W + SPACING) / (TAG_W + SPACING)))
rows = int(math.floor((WORK_H + SPACING) / (TAG_H + SPACING)))
if cols < 1 or rows < 1:
    raise SystemExit("TAG size + spacing doesn't fit the work area.")

TAGS_PER_RUN = cols * rows
print(f"Layout: {cols} columns × {rows} rows = {TAGS_PER_RUN} tags per run")

def append_pen_sequence(gcode_list, seq):
    for line in seq.splitlines():
        gcode_list.append(line.strip())

def polygon_to_gcode(poly, scale, dx, dy, gcode_list):
    """Draw one polygon (Nx2 ndarray) as G0 to first, then G1 through points."""
    if poly.shape[0] < 2:
        return
    # first point
    x0 = poly[0,0]*scale + dx
    y0 = poly[0,1]*scale + dy
    gcode_list.append(f"G0 X{x0:.3f} Y{y0:.3f} F{RAPID_FEED}")
    append_pen_sequence(gcode_list, PEN_DOWN_SEQ)
    for p in poly[1:]:
        x = p[0]*scale + dx
        y = p[1]*scale + dy
        gcode_list.append(f"G1 X{x:.3f} Y{y:.3f} F{LINEAR_FEED}")
    # close polygon back to first (helps ensure closed outline)
    gcode_list.append(f"G1 X{x0:.3f} Y{y0:.3f} F{LINEAR_FEED}")
    append_pen_sequence(gcode_list, PEN_UP_SEQ)

def make_rectangle_gcode(x0, y0, w, h, g):
    g.append(f"G0 X{x0:.3f} Y{y0:.3f} F{RAPID_FEED}")
    append_pen_sequence(g, PEN_DOWN_SEQ)
    g.append(f"G1 X{x0+w:.3f} Y{y0:.3f} F{LINEAR_FEED}")
    g.append(f"G1 X{x0+w:.3f} Y{y0+h:.3f} F{LINEAR_FEED}")
    g.append(f"G1 X{x0:.3f} Y{y0+h:.3f} F{LINEAR_FEED}")
    g.append(f"G1 X{x0:.3f} Y{y0:.3f} F{LINEAR_FEED}")
    append_pen_sequence(g, PEN_UP_SEQ)

def generate_run_gcode(names_for_run, run_index):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    g = []
    g.append("G21 ; units = mm")
    g.append("G90 ; absolute coords")
    append_pen_sequence(g, PEN_UP_SEQ)

    for idx, name in enumerate(names_for_run):
        col = idx % cols
        row = idx // cols
        x0 = col * (TAG_W + SPACING)
        y0 = row * (TAG_H + SPACING)

        # build TextPath and get bounds
        tp = TextPath((0,0), name, prop=font_prop)
        verts = np.asarray(tp.vertices)
        if verts.size == 0:
            g.append(f"(Skipping empty glyph for '{name}')")
        else:
            vmin = verts.min(axis=0)
            vmax = verts.max(axis=0)
            text_w_raw = vmax[0] - vmin[0]
            text_h_raw = vmax[1] - vmin[1]
            if text_w_raw > 0 and text_h_raw > 0:
                avail_w = TAG_W - 2*TEXT_MARGIN
                avail_h = TAG_H - 2*TEXT_MARGIN
                scale = min(avail_w / text_w_raw, avail_h / text_h_raw)
                text_draw_w = text_w_raw * scale
                text_draw_h = text_h_raw * scale
                dx = x0 + (TAG_W - text_draw_w)/2 - vmin[0]*scale
                dy = y0 + (TAG_H - text_draw_h)/2 - vmin[1]*scale

                # IMPORTANT: use to_polygons() to flatten curves
                polys = tp.to_polygons()
                for poly in polys:
                    poly = np.asarray(poly)
                    if poly.shape[0] >= 2:
                        polygon_to_gcode(poly, scale, dx, dy, g)

        # rectangle outline (after text)
        make_rectangle_gcode(x0, y0, TAG_W, TAG_H, g)

    append_pen_sequence(g, PEN_UP_SEQ)
    g.append(f"G0 X0 Y0 F{RAPID_FEED}")
    outname = os.path.join(OUTPUT_DIR, f"{OUTPUT_PREFIX}{run_index:02d}.gcode")
    with open(outname, "w", encoding="utf-8") as fh:
        fh.write("\n".join(g))
    print(f"Saved: {outname} (tags: {len(names_for_run)})")

def load_names_from_csv(path):
    names = []
    with open(path, newline="", encoding="utf-8") as csvf:
        rdr = csv.reader(csvf)
        first = next(rdr, None)
        if first is None:
            return []
        if len(first) > 0 and first[0].strip().lower() == "name":
            pass
        else:
            if first and first[0].strip():
                names.append(first[0].strip())
        for row in rdr:
            if row and row[0].strip():
                names.append(row[0].strip())
    return names

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: {INPUT_CSV} not found.")
        return
    all_names = load_names_from_csv(INPUT_CSV)
    if not all_names:
        print("No names found.")
        return
    total_runs = math.ceil(len(all_names) / TAGS_PER_RUN)
    for r in range(total_runs):
        start = r * TAGS_PER_RUN
        end = start + TAGS_PER_RUN
        subset = all_names[start:end]
        generate_run_gcode(subset, r + 1)

if __name__ == "__main__":
    main()
