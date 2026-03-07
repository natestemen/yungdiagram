import pytest

from yungdiagram import Cell, YoungDiagram


def test_young_diagram_initialization():
    yd = YoungDiagram([4, 3, 1])
    assert yd.partition == (4, 3, 1)
    assert len(yd.cells) == 3
    assert len(yd.cells[0]) == 4
    assert len(yd.cells[1]) == 3
    assert len(yd.cells[2]) == 1


def test_invalid_partition():
    with pytest.raises(ValueError, match="Invalid partition"):
        YoungDiagram([1, 2])


def test_addable_cells():
    yd = YoungDiagram([3, 2])
    #   0 1 2 3
    # 0 ■ ■ ■ *
    # 1 ■ ■ *
    # 2 *
    addable = yd.addable_cells()
    expected = [Cell(3, 0), Cell(2, 1), Cell(0, 2)]
    assert addable == expected


def test_addable_removable_with_empty_partition():
    yd = YoungDiagram([])
    assert yd.addable_cells() == [Cell(0, 0)]

    assert yd.removable_cells() == []


def test_diagram_hashing():
    yd = YoungDiagram.random(4)
    assert isinstance(hash(yd), int)


def test_removable_cells():
    yd = YoungDiagram([2, 2])
    removable = yd.removable_cells()

    assert removable == [Cell(1, 1)]


def test_conjugate():
    yd = YoungDiagram([1])

    assert yd.conjugate() == yd

    yd = YoungDiagram([5, 5, 2, 1])
    expected = YoungDiagram([4, 3, 2, 2, 2])

    assert yd.conjugate() == expected

def test_conjugate_empty():
    yd = YoungDiagram(())
    assert yd.conjugate() == yd


def test_stringification():
    yd = YoungDiagram([5, 5, 4])

    table = str(yd)
    assert table == "■ ■ ■ ■ ■ \n■ ■ ■ ■ ■ \n■ ■ ■ ■ "


def test_reachable_diagrams_by_single_addition():
    yd = YoungDiagram((2, 1))
    reachable = yd.reachable_young_diagrams_by_addition()
    assert len(reachable) == 3


def test_reachable_diagrams_by_single_removal():
    yd = YoungDiagram((2, 1))
    reachable = yd.reachable_young_diagrams_by_removal()
    assert len(reachable) == 2


def test_adding_cell():
    yd = YoungDiagram((5, 5, 5))
    nyd = yd + Cell(5, 0)
    assert nyd.size == 16


def test_adding_invalid_cell():
    yd = YoungDiagram((5, 5, 5))
    with pytest.raises(ValueError, match="not addable"):
        yd + Cell(5, 1)

    with pytest.raises(ValueError, match="not addable"):
        yd + Cell(0, 1)


def test_remove_cell():
    yd = YoungDiagram((5, 5))
    nyd = yd - Cell(4, 1)
    assert nyd.size == 9


def test_removing_invalid_cell():
    yd = YoungDiagram((5, 5))
    with pytest.raises(ValueError, match="not removable"):
        yd - Cell(5, 1)

    with pytest.raises(ValueError, match="not removable"):
        yd - Cell(0, 1)


@pytest.mark.parametrize("diagram_size", range(500, 1, -10))
def test_random_diagram(diagram_size):
    yd = YoungDiagram.random(num_cells=diagram_size)
    assert yd.size == diagram_size
