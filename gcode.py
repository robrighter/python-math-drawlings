# gcodegen.py
#
# Description:
#   A command-line tool to generate G-Code from a Python turtle graphics script.
#   This tool imports a user-provided Python script, executes a designated drawing function,
#   and outputs the G-Code to standard out, formatted with a custom template.
#
# Usage:
#   python gcodegen.py <filename.py>
#
# Dependencies:
#   - turtle-gcode (pip install turtle-gcode)

import argparse
import importlib.util
import sys
import io
import turtle_gcode as t

def main():
    """
    Main function to parse arguments, run the turtle graphics script,
    and generate the G-Code.
    """
    parser = argparse.ArgumentParser(
        description='Generate G-Code from a Python turtle graphics script.'
    )
    parser.add_argument(
        'filename',
        help='The Python script with the turtle drawing function.'
    )
    parser.add_argument(
        '--draw-function',
        default='draw',
        help='The name of the drawing function in the script (default: draw).'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=410,
        help='The width of the printable area.'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=300,
        help='The height of the printable area.'
    )

    args = parser.parse_args()

    try:
        # Dynamically import the user-provided Python script
        spec = importlib.util.spec_from_file_location("user_module", args.filename)
        if spec is None:
            print(f"Error: Cannot find module specification for '{args.filename}'.", file=sys.stderr)
            sys.exit(1)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Get the drawing function from the imported module
        if hasattr(user_module, args.draw_function) and callable(getattr(user_module, args.draw_function)):
            draw_func = getattr(user_module, args.draw_function)
        else:
            print(f"Error: The file '{args.filename}' does not have a function named '{args.draw_function}'.", file=sys.stderr)
            sys.exit(1)

        # Create a turtle instance from the turtle-gcode library
        t.setup(800,800,0,0)
        t.speed(0)
        t.tracer(0,0)


        # Execute the user's drawing function
        draw_func(t)
        t.update()

        # Generate the G-Code
        gcode_output = t.write_gcode(args.width, args.height, penup_command = "M03", pendown_command = "M05")

        # Split the generated G-Code
        gcode_lines = gcode_output.strip().split('\n')

        first_line = ""
        rest_of_lines = []

        if gcode_lines:
            first_line = gcode_lines[0]
            rest_of_lines = gcode_lines[1:]

        # Format the G-Code using the user-provided template
        template = f""";### Header ###

G21
G90
F2000
M03
G0 X0 Y0
G04 P1

;### First line of the gcode ###
{first_line}

;### Stuff to be inserted after the first G0 ###
M05
G04 P1

;### Rest of the gcode ###
"""
        template += "\n".join(rest_of_lines)
        template += """
;### Footer ###

M03
G04 P1
G0 X0 Y0
"""
        # Print the final formatted G-Code
        print(template)

    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
