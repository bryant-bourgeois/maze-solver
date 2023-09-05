from maze import Maze
from window import Window


def main():
    win = Window(600, 800)
    maze = Maze(
        50,
        50,
        20,
        20,
        50,
        50,
        win,
    )
    maze.break_walls_r(0, 0)
    maze.reset_cells_visited()
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
