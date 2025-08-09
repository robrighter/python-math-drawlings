import csv
import math

# ======= CONFIG =======
work_area_x = 300.0  # mm
work_area_y = 300.0  # mm

tag_width_in = 6.0
tag_height_in = 2.0

tag_width = tag_width_in * 25.4   # mm
tag_height = tag_height_in * 25.4 # mm

penup_cmd = "G04 P0.5\nM03\nG04 P0.5"
pendown_cmd = "G04 P0.5\nM05\nG04 P0.5"

feedrate = 2000  # mm/min
font_scale = 0.5 # relative size for text drawing

input_csv = "names.csv"

# ======= FUNCTIONS =======

def load_names(filename):
    names = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)  # skip header if exists
        for row in reader:
            if row and row[0].strip():
                names.append(row[0].strip())
    return names

def draw_rectangle(x, y, w, h):
    return [
        f"G0 X{x:.2f} Y{y:.2f}",
        pendown_cmd,
        f"G1 X{x+w:.2f} Y{y:.2f} F{feedrate}",
        f"G1 X{x+w:.2f} Y{y+h:.2f} F{feedrate}",
        f"G1 X{x:.2f} Y{y+h:.2f} F{feedrate}",
        f"G1 X{x:.2f} Y{y:.2f} F{feedrate}",
        penup_cmd
    ]

def draw_text(x, y, text):
    # Simple placeholder text drawing using single line per name
    # You can replace with proper Hershey font plotting later
    return [
        f"G0 X{x+5:.2f} Y{y+tag_height/2:.2f}",
        pendown_cmd,
        f"( {text} )",  # just as a comment; your CAM can replace with actual stroke font code
        penup_cmd
    ]

def make_gcode_for_run(names, run_num):
    gcode = ["G21", "G90", penup_cmd]  # mm, absolute positioning
    cols = int(work_area_x // tag_width)
    rows = int(work_area_y // tag_height)
    max_per_run = cols * rows

    start_x = 0
    start_y = 0

    for idx, name in enumerate(names):
        col = idx % cols
        row = (idx // cols) % rows
        x = start_x + col * tag_width
        y = start_y + row * tag_height

        gcode.extend(draw_rectangle(x, y, tag_width, tag_height))
        gcode.extend(draw_text(x, y, name))

    gcode.append("M2")  # program end
    with open(f"nametags_run{run_num}.gcode", "w") as f:
        f.write("\n".join(gcode))

def main():
    names = load_names(input_csv)
    cols = int(work_area_x // tag_width)
    rows = int(work_area_y // tag_height)
    max_per_run = cols * rows
    total_runs = math.ceil(len(names) / max_per_run)

    for run in range(total_runs):
        start_index = run * max_per_run
        end_index = start_index + max_per_run
        run_names = names[start_index:end_index]
        make_gcode_for_run(run_names, run + 1)
        print(f"Generated nametags_run{run+1}.gcode with {len(run_names)} names")

if __name__ == "__main__":
    main()
