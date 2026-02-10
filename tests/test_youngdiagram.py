import pytest

from yungdiagram import Cell, YoungDiagram

def test_young_diagram_initialization():
    yd = YoungDiagram([4, 3, 1])
    assert yd.partition == [4, 3, 1]
    assert len(yd.cells) == 3
    assert len(yd.cells[0]) == 4
    assert len(yd.cells[1]) == 3
    assert len(yd.cells[2]) == 1

def test_invalid_partition():
    with pytest.raises(ValueError, match="Invalid partition"):
        YoungDiagram([1, 2])


def test_addable_cells():
    yd = YoungDiagram([3, 2])
    addable = yd.addable_cells()
    expected = [Cell(3, 0), Cell(2, 1), Cell(0, 2)]
    assert addable == expected

def test_removable_cells():
    yd = YoungDiagram([2, 2])
    removable = yd.removable_cells()

    assert removable == [Cell(1, 1)]

def test_transpose():
    yd = YoungDiagram([1])

    assert yd.transpose() == yd

    yd = YoungDiagram([5, 5, 2, 1])
    expected = YoungDiagram([4, 3, 2, 2, 2])

    assert yd.transpose() == expected

def test_stringification():
    yd = YoungDiagram([5, 5, 4])

    table = str(yd)
    assert isinstance(table, str)
    assert "■" in table