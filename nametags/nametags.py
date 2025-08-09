#!/usr/bin/env python3
"""
Generates G-code files for 6"x2" nametags from names.csv.
Each run fits within a 300x300 mm bed. Uses matplotlib text paths to
convert text to vector strokes and outputs pen-up/pen-down commands.

Requires: matplotlib, numpy
"""

import csv
import math
import os
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

# ----------- USER CONFIG -----------
INPUT_CSV = "names.csv"         # csv file, first column used for names
OUTPUT_PREFIX = "nametags_run"  # output files: nametags_run01.gcode, ...
OUTPUT_DIR = "gcode_sheets"

# Work area and tag sizes (mm)
WORK_W = 300.0
WORK_H = 300.0
TAG_W = 152.4   # 6 in
TAG_H = 50.8    # 2 in
SPACING = 10.0  # mm between tags (adjust if you want)

# Pen control sequences (exact multi-line strings you gave)
PEN_UP_SEQ = "G04 P0.5\n\rM03\n\rG04 P0.5"
PEN_DOWN_SEQ = "G04 P0.5\n\rM05\n\rG04 P0.5"

# Motion/feed
RAPID_FEED = 3000   # used with G0
LINEAR_FEED = 1000  # used with G1

# Font - point-size used is arbitrary; we'll scale to fit TAG box
FONT_PATH = None  # e.g. "Arial.ttf" or leave None to use default
FONT_POINTSIZE = 120.0

# margin inside tag for text (mm)
TEXT_MARGIN = 4.0

# -----------------------------------

font_prop = FontProperties(fname=FONT_PATH, size=FONT_POINTSIZE)

# compute how many columns/rows will fit considering spacing between tags
cols = int(math.floor((WORK_W + SPACING) / (TAG_W + SPACING)))
rows = int(math.floor((WORK_H + SPACING) / (TAG_H + SPACING)))
if cols < 1 or rows < 1:
    raise SystemExit("TAG size + spacing doesn't fit your work area; reduce tag size or spacing.")

TAGS_PER_RUN = cols * rows

print(f"Layout: {cols} columns × {rows} rows = {TAGS_PER_RUN} tags per run")

# helper to append pen sequences into gcode list as separate lines
def append_pen_sequence(gcode_list, seq):
    for line in seq.splitlines():
        # preserve empty lines if any
        gcode_list.append(line.strip())

def textpath_to_gcode(tp_vertices, tp_codes, scale, dx, dy, gcode_list):
    """
    Convert a Matplotlib TextPath to G-code moves.
    - tp_vertices: vertices array of TextPath
    - tp_codes: path codes (MOVETO, LINETO, CLOSEPOLY)
    - scale: scalar applied to raw vertices
    - dx, dy: offsets in mm to add after scaling (world coords)
    """
    pen_is_down = False
    for (vx, vy), code in zip(tp_vertices, tp_codes):
        x = vx * scale + dx
        y = vy * scale + dy
        if code == 1:  # MOVETO
            if pen_is_down:
                append_pen_sequence(gcode_list, PEN_UP_SEQ)
                pen_is_down = False
            gcode_list.append(f"G0 X{x:.3f} Y{y:.3f} F{RAPID_FEED}")
        elif code == 2:  # LINETO
            if not pen_is_down:
                append_pen_sequence(gcode_list, PEN_DOWN_SEQ)
                pen_is_down = True
            gcode_list.append(f"G1 X{x:.3f} Y{y:.3f} F{LINEAR_FEED}")
        elif code == 79:  # CLOSEPOLY
            # treat like pen up after closing
            if pen_is_down:
                append_pen_sequence(gcode_list, PEN_UP_SEQ)
                pen_is_down = False
    if pen_is_down:
        append_pen_sequence(gcode_list, PEN_UP_SEQ)

def make_rectangle_gcode(x0, y0, w, h, gcode_list):
    """Draw rectangle starting at bottom-left (x0,y0) clockwise."""
    gcode_list.append(f"G0 X{x0:.3f} Y{y0:.3f} F{RAPID_FEED}")
    append_pen_sequence(gcode_list, PEN_DOWN_SEQ)
    gcode_list.append(f"G1 X{x0+w:.3f} Y{y0:.3f} F{LINEAR_FEED}")
    gcode_list.append(f"G1 X{x0+w:.3f} Y{y0+h:.3f} F{LINEAR_FEED}")
    gcode_list.append(f"G1 X{x0:.3f} Y{y0+h:.3f} F{LINEAR_FEED}")
    gcode_list.append(f"G1 X{x0:.3f} Y{y0:.3f} F{LINEAR_FEED}")
    append_pen_sequence(gcode_list, PEN_UP_SEQ)

def generate_run_gcode(names_for_run, run_index):
    """Create the G-code for one run (batch of tags)."""
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

        # draw rectangle outline (after text to avoid smudging, but drawing outlines
        # afterwards is okay too; we draw text first then outline)
        # STEP 1: convert text to path and append gcode
        tp = TextPath((0, 0), name, prop=font_prop)
        verts = np.asarray(tp.vertices)
        codes = tp.codes

        # raw bounds
        vmin = verts.min(axis=0)
        vmax = verts.max(axis=0)
        text_w_raw = vmax[0] - vmin[0]
        text_h_raw = vmax[1] - vmin[1]
        if text_w_raw <= 0 or text_h_raw <= 0:
            # degenerate; skip text
            print(f"Warning: '{name}' has empty text path; skipping text drawing.")
        else:
            # available box for text (leaving margin)
            avail_w = TAG_W - 2 * TEXT_MARGIN
            avail_h = TAG_H - 2 * TEXT_MARGIN

            # scale factor to fit available area
            scale = min(avail_w / text_w_raw, avail_h / text_h_raw)

            # after scaling, we'll place the text so it's centered in the tag
            text_draw_w = text_w_raw * scale
            text_draw_h = text_h_raw * scale

            # dx/dy to move the raw coords so that min becomes 0, then center inside tag:
            dx = x0 + (TAG_W - text_draw_w) / 2 - vmin[0] * scale
            dy = y0 + (TAG_H - text_draw_h) / 2 - vmin[1] * scale

            # convert the path into G-code
            textpath_to_gcode(verts, codes, scale, dx, dy, g)

        # STEP 2: draw border rectangle (after text so text doesn't smudge)
        make_rectangle_gcode(x0, y0, TAG_W, TAG_H, g)

    # finish up
    append_pen_sequence(g, PEN_UP_SEQ)
    g.append("G0 X0 Y0 F{:.0f} ; return to origin".format(RAPID_FEED))
    outname = os.path.join(OUTPUT_DIR, f"{OUTPUT_PREFIX}{run_index:02d}.gcode")
    with open(outname, "w", encoding="utf-8") as fh:
        fh.write("\n".join(g))
    print(f"Saved: {outname} (tags: {len(names_for_run)})")

def load_names_from_csv(path):
    names = []
    with open(path, newline="", encoding="utf-8") as csvf:
        rdr = csv.reader(csvf)
        # try to detect header: if first cell equals "Name" or "name", skip it
        first = next(rdr, None)
        if first is None:
            return []
        if len(first) > 0 and first[0].strip().lower() == "name":
            # skip header, read remainder
            pass
        else:
            # first row is actual data
            if first and first[0].strip():
                names.append(first[0].strip())
        for row in rdr:
            if row and row[0].strip():
                names.append(row[0].strip())
    return names

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: {INPUT_CSV} not found. Put your CSV in the same folder.")
        return

    all_names = load_names_from_csv(INPUT_CSV)
    if not all_names:
        print("No names found in CSV.")
        return

    total_runs = math.ceil(len(all_names) / TAGS_PER_RUN)
    for r in range(total_runs):
        start = r * TAGS_PER_RUN
        end = start + TAGS_PER_RUN
        subset = all_names[start:end]
        generate_run_gcode(subset, r + 1)

if __name__ == "__main__":
    main()
