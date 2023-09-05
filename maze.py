import time
import random
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
            seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        if seed:
            random.seed(seed)

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
        time.sleep(0.01)

    def break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        loopin = True
        while loopin:
            # see if there is an adjacent cell to visit
            cells_can_visit = []
            # check left adjacent cell
            if i > 0:
                if not self._cells[i - 1][j].visited:
                    cells_can_visit.append([i - 1, j, 'left'])
            # check right adjacent cell
            if i < self.num_cols - 1:
                if not self._cells[i + 1][j].visited:
                    cells_can_visit.append([i + 1, j, 'right'])
            # check top adjacent cell
            if j > 0:
                if not self._cells[i][j - 1].visited:
                    cells_can_visit.append([i, j - 1, 'up'])
            # check bottom adjacent cell
            if j < self.num_rows - 1:
                if not self._cells[i][j + 1].visited:
                    cells_can_visit.append([i, j + 1, 'down'])

            if len(cells_can_visit) == 0:
                self._draw_cell(i, j)
                return
            else:
                rand_choice = random.randint(0, len(cells_can_visit) - 1)
                rand_cell = cells_can_visit[rand_choice]
                if rand_cell[2] == 'left':
                    self._cells[i][j].has_left_wall = False
                    self._cells[rand_cell[0]][rand_cell[1]].has_right_wall = False
                elif rand_cell[2] == 'right':
                    self._cells[i][j].has_right_wall = False
                    self._cells[rand_cell[0]][rand_cell[1]].has_left_wall = False
                elif rand_cell[2] == 'up':
                    self._cells[i][j].has_top_wall = False
                    self._cells[rand_cell[0]][rand_cell[1]].has_bottom_wall = False
                else:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[rand_cell[0]][rand_cell[1]].has_top_wall = False

                self._draw_cell(i, j)
                self.break_walls_r(rand_cell[0], rand_cell[1])

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

    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        directions = ['left', 'right', 'up', 'down']
        for direction in directions:
            if direction == 'left':
                if i > 0 and not self._cells[i - 1][j].has_right_wall and not self._cells[i - 1][j].visited:
                    self._cells[i][j].draw_move(self._cells[i - 1][j])
                    result = self._solve_r(i - 1, j)
                    if result:
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
            elif direction == 'right':
                if i < self.num_cols - 1 and not self._cells[i + 1][j].has_left_wall and not self._cells[i + 1][
                    j].visited:
                    self._cells[i][j].draw_move(self._cells[i + 1][j])
                    result = self._solve_r(i + 1, j)
                    if result:
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
            elif direction == 'up':
                if j > 0 and not self._cells[i][j - 1].has_bottom_wall and not self._cells[i][j - 1].visited:
                    self._cells[i][j].draw_move(self._cells[i][j - 1])
                    result = self._solve_r(i, j - 1)
                    if result:
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)
            else:
                if j < self.num_rows - 1 and not self._cells[i][j + 1].has_top_wall and not self._cells[i][
                    j + 1].visited:
                    self._cells[i][j].draw_move(self._cells[i][j + 1])
                    result = self._solve_r(i, j + 1)
                    if result:
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        return False
