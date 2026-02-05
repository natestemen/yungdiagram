from yungdiagram import Cell, YoungDiagram

def test_young_diagram_initialization():
    yd = YoungDiagram([4, 3, 1])
    assert yd.partition == [4, 3, 1]
    assert len(yd.cells) == 3
    assert len(yd.cells[0]) == 4
    assert len(yd.cells[1]) == 3
    assert len(yd.cells[2]) == 1

def test_addable_cells():
    yd = YoungDiagram([3, 2])
    addable = yd.addable_cells()
    expected = [Cell(3, 0), Cell(2, 1), Cell(0, 2)]
    assert addable == expected

def test_removable_cells():
    yd = YoungDiagram([2, 2])
    removable = yd.removable_cells()

    assert removable == [Cell(1, 1)]