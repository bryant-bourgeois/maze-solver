from maze import Maze
from window import Window


def main():
    win = Window(600, 800)
    maze = Maze(
        50,
        50,
        20,
        20,
        20,
        20,
        win,
    )
    win.wait_for_close()


if __name__ == "__main__":
    main()
