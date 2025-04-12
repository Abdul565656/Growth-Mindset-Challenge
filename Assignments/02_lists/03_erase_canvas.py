# Implement an 'eraser' on a canvas.

# The canvas consists of a grid of blue 'cells' which are drawn as rectangles on the screen. We then create an eraser rectangle which, when dragged around the canvas, sets all of the rectangles it is in contact with to white.

import tkinter as tk

# Constants
ROWS = 10
COLS = 10
CELL_SIZE = 40
ERASER_SIZE = 50

# Global variables
rectangles = []
eraser = None
canvas = None

def draw_grid():
    for row in range(ROWS):
        row_rects = []
        for col in range(COLS):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')
            row_rects.append(rect)
        rectangles.append(row_rects)

def move_eraser(event):
    x = event.x
    y = event.y
    canvas.coords(eraser, x, y, x + ERASER_SIZE, y + ERASER_SIZE)

    # Eraser coordinates
    x1, y1, x2, y2 = canvas.coords(eraser)

    # Check all cells for collision
    for row in rectangles:
        for rect in row:
            cx1, cy1, cx2, cy2 = canvas.coords(rect)
            if not (x2 < cx1 or x1 > cx2 or y2 < cy1 or y1 > cy2):
                canvas.itemconfig(rect, fill='white')

def main():
    global canvas, eraser

    root = tk.Tk()
    root.title("Eraser Canvas")

    canvas_width = COLS * CELL_SIZE
    canvas_height = ROWS * CELL_SIZE

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    draw_grid()

    # Create eraser
    eraser = canvas.create_rectangle(0, 0, ERASER_SIZE, ERASER_SIZE, fill='gray')

    # Bind dragging motion
    canvas.bind("<B1-Motion>", move_eraser)

    root.mainloop()

# Run the app
main()
