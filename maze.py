import time
from window import Window, Point, Line
from cell import Cell


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
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
        for i in range(self.num_cols):
            self._cells.append([])
            for j in range(self.num_rows):
                self._cells[i].append(Cell(self.win))
        self._break_entrance_and_exit()
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        p1 = Point(i * self.cell_size_x, j * self.cell_size_y)
        p2 = Point(p1.x + self.cell_size_x, p1.y + self.cell_size_y)
        self._cells[i][j].draw(p1.x, p1.y, p2.x, p2.y)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self.num_cols - 1][self.num_rows - 1]

        entrance_cell.has_left_wall = False
        entrance_cell.has_right_wall = False
        entrance_cell.has_top_wall = False
        entrance_cell.has_bottom_wall = False

        exit_cell.has_left_wall = False
        exit_cell.has_right_wall = False
        exit_cell.has_top_wall = False
        exit_cell.has_bottom_wall = False

        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)