from yungdiagram import Cell

def test_cell_initialization():
    cell = Cell(2, 3)
    assert cell.x == 2
    assert cell.y == 3

def test_cell_content():
    cell = Cell(5, 2)
    assert cell.content == 3

    cell = Cell(4, 4)
    assert cell.content == 0

    cell = Cell(1, 5)
    assert cell.content == -4
