"""
Classic Minesweeper in Python (Tkinter)

Save as minesweeper.py and run with: python minesweeper.py

Controls:
 - Left click: reveal cell
 - Right click: toggle flag
 - Double-click (or middle-click): chord (reveal neighbors if flags equal number)

Features:
 - Adjustable rows, cols, mines via constants or command-line args
 - Recursive reveal of empty cells
 - Win / Lose dialogs and restart
"""

import sys
import random
import tkinter as tk
from tkinter import messagebox

CELL_SIZE = 28
PADDING = 4

class Cell:
    def __init__(self):
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent = 0

class Minesweeper(tk.Frame):
    def __init__(self, master, rows=9, cols=9, mines=10):
        super().__init__(master)
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.first_click = True
        self.game_over = False
        self.flags_left = mines

        self.grid_cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

        self.create_widgets()
        self.draw_board()
        self.update_title()

    def create_widgets(self):
        # top control frame
        ctrl = tk.Frame(self.master)
        ctrl.pack(padx=6, pady=6, anchor="n")

        self.flag_label = tk.Label(ctrl, text=f"Flags: {self.flags_left}")
        self.flag_label.pack(side=tk.LEFT, padx=(0,10))

        self.reset_btn = tk.Button(ctrl, text="Restart", command=self.restart)
        self.reset_btn.pack(side=tk.LEFT)

        # canvas for board
        width = self.cols * CELL_SIZE + PADDING*2
        height = self.rows * CELL_SIZE + PADDING*2
        self.canvas = tk.Canvas(self.master, width=width, height=height, bg='#c0c0c0')
        self.canvas.pack(padx=6, pady=6)

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        # double click for chord
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        # allow middle click too
        self.canvas.bind("<Button-2>", self.on_double_click)

    def draw_board(self):
        self.canvas.delete('all')
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = PADDING + c*CELL_SIZE
                y1 = PADDING + r*CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                cell = self.grid_cells[r][c]
                if cell.revealed:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#e0e0e0', outline='#808080')
                    if cell.is_mine:
                        self.canvas.create_oval(x1+6, y1+6, x2-6, y2-6, fill='black')
                    elif cell.adjacent > 0:
                        self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(cell.adjacent), font=('Helvetica', 12, 'bold'))
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#bdbdbd', outline='#7a7a7a')
                    if cell.flagged:
                        # small flag triangle
                        cx, cy = (x1+x2)//2, (y1+y2)//2
                        self.canvas.create_text(cx, cy, text='⚑', font=('Helvetica', 12, 'bold'))

    def coords_from_event(self, event):
        x = event.x - PADDING
        y = event.y - PADDING
        if x < 0 or y < 0:
            return None
        c = x // CELL_SIZE
        r = y // CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return r, c
        return None

    def place_mines(self, safe_r, safe_c):
        # place mines randomly, avoiding the first clicked cell and its neighbors
        forbidden = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr = safe_r + dr
                cc = safe_c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    forbidden.add((rr, cc))

        positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in forbidden]
        mines = random.sample(positions, self.mines)
        for (r, c) in mines:
            self.grid_cells[r][c].is_mine = True

        # update adjacent counts
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid_cells[r][c].is_mine:
                    continue
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = r+dr, c+dc
                        if 0 <= rr < self.rows and 0 <= cc < self.cols and self.grid_cells[rr][cc].is_mine:
                            cnt += 1
                self.grid_cells[r][c].adjacent = cnt

    def on_left_click(self, event):
        if self.game_over:
            return
        pos = self.coords_from_event(event)
        if not pos:
            return
        r, c = pos
        cell = self.grid_cells[r][c]
        if self.first_click:
            # ensure first click is never a mine
            self.place_mines(r, c)
            self.first_click = False
        if cell.flagged or cell.revealed:
            return
        if cell.is_mine:
            cell.revealed = True
            self.game_lost()
            return
        self.reveal_cell(r, c)
        self.draw_board()
        if self.check_win():
            self.game_won()

    def on_right_click(self, event):
        if self.game_over:
            return
        pos = self.coords_from_event(event)
        if not pos:
            return
        r, c = pos
        cell = self.grid_cells[r][c]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.flags_left += -1 if cell.flagged else 1
        self.flag_label.config(text=f"Flags: {self.flags_left}")
        self.draw_board()

    def on_double_click(self, event):
        if self.game_over:
            return
        pos = self.coords_from_event(event)
        if not pos:
            return
        r, c = pos
        cell = self.grid_cells[r][c]
        if not cell.revealed or cell.adjacent == 0:
            return
        # count flagged neighbors
        flagged = 0
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r+dr, c+dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    neighbors.append((rr, cc))
                    if self.grid_cells[rr][cc].flagged:
                        flagged += 1
        if flagged == cell.adjacent:
            for rr, cc in neighbors:
                neigh = self.grid_cells[rr][cc]
                if not neigh.flagged and not neigh.revealed:
                    if neigh.is_mine:
                        neigh.revealed = True
                        self.game_lost()
                        return
                    self.reveal_cell(rr, cc)
            self.draw_board()
            if self.check_win():
                self.game_won()

    def reveal_cell(self, r, c):
        cell = self.grid_cells[r][c]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        if cell.adjacent == 0 and not cell.is_mine:
            # flood fill neighbors
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr, cc = r+dr, c+dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols:
                        if not self.grid_cells[rr][cc].revealed:
                            self.reveal_cell(rr, cc)

    def game_lost(self):
        self.game_over = True
        # reveal all mines
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid_cells[r][c].is_mine:
                    self.grid_cells[r][c].revealed = True
        self.draw_board()
        messagebox.showinfo("Game Over", "You hit a mine! Game over.")

    def check_win(self):
        # win if all non-mine cells are revealed
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid_cells[r][c]
                if not cell.is_mine and not cell.revealed:
                    return False
        return True

    def game_won(self):
        self.game_over = True
        messagebox.showinfo("You Win!", "Congratulations — you cleared the minefield!")

    def restart(self):
        self.first_click = True
        self.game_over = False
        self.flags_left = self.mines
        self.flag_label.config(text=f"Flags: {self.flags_left}")
        self.grid_cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_board()
        self.update_title()

    def update_title(self):
        self.master.title(f"Minesweeper — {self.rows}x{self.cols} Mines: {self.mines}")


def parse_args():
    rows, cols, mines = 9, 9, 10
    if len(sys.argv) >= 2:
        try:
            rows = int(sys.argv[1])
        except:
            pass
    if len(sys.argv) >= 3:
        try:
            cols = int(sys.argv[2])
        except:
            pass
    if len(sys.argv) >= 4:
        try:
            mines = int(sys.argv[3])
        except:
            pass
    # clamp values
    rows = max(5, min(30, rows))
    cols = max(5, min(30, cols))
    mines = max(1, min(rows*cols-1, mines))
    return rows, cols, mines


if __name__ == '__main__':
    r, c, m = parse_args()
    root = tk.Tk()
    app = Minesweeper(root, rows=r, cols=c, mines=m)
    app.pack()
    root.mainloop()
