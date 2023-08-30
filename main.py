from window import Window, Line, Point, Cell


def main():
    win = Window(800, 600)
    p1 = Point(125, 125)
    p2 = Point(375, 375)
    c1 = Cell(p1.x, p1.y, p2.x, p2.y, win)
    p3 = Point(250, 250)
    p4 = Point(500, 500)
    c2 = Cell(p3.x, p3.y, p4.x, p4.y, win)
    c1.draw()
    c2.draw()
    win.wait_for_close()


if __name__ == "__main__":
    main()
