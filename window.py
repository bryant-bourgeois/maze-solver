from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title = 'Maze Solver'
        self.canvas = Canvas(width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack()


class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self.has_left_wall:
            p1 = Point(self._x1, self._y1)
            p2 = Point(self._x1, self._y2)
            line = Line(p1, p2)
            self._win.draw_line(line, 'purple')
        if self.has_bottom_wall:
            p1 = Point(self._x1, self._y2)
            p2 = Point(self._x2, self._y2)
            line = Line(p1, p2)
            self._win.draw_line(line, 'purple')
        if self.has_right_wall:
            p1 = Point(self._x2, self._y1)
            p2 = Point(self._x2, self._y2)
            line = Line(p1, p2)
            self._win.draw_line(line, 'purple')
        if self.has_top_wall:
            p1 = Point(self._x1, self._y1)
            p2 = Point(self._x2, self._y1)
            line = Line(p1, p2)
            self._win.draw_line(line, 'purple')

    def draw_move(self, to_cell, undo=False):
        p1 = Point(self._x1 + (self._x2 - self._x1)/2, self._y1 + (self._y2 - self._y1)/2)
        p2 = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1)/2, to_cell._y1 + (to_cell._y2 - to_cell._y1)/2)
        line = Line(p1, p2)
        if not undo:
            color = 'red'
        else:
            color = 'gray'
        self._win.draw_line(line, color)


class maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win,
                 ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for col in self.num_cols:
            col = []
            for row in self.num_rows:
                row = Cell()
                col.append(row)
            self._cells.append(col)
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        p1 = Point(self.x1 * i, self.y1 * j)
        p2 = Point((self.x1 * i) + self.cell_size_x, (self.y1 * j) + self.cell_size_y)
        cell = Cell(p1.x, p1.y, p2.x, p2.y, self.win)
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

