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


def test_diagram_containment():
    yd1 = YoungDiagram([8, 4, 4, 1])
    yd2 = YoungDiagram([8, 2, 1])

    assert yd1.contains(yd2)
    assert not yd2.contains(yd1)


def test_diagram_domination():
    yd1 = YoungDiagram([3, 1])
    yd2 = YoungDiagram([2, 2])

    assert yd1.dominates(yd2)
    assert not yd2.dominates(yd1)
    assert not yd1.contains(yd2)


def test_durfee_square():
    yd = YoungDiagram((8, 4, 4, 3, 1))
    # ■ ■ ■ □ □ □ □ □
    # ■ ■ ■ □
    # ■ ■ ■ □
    # □ □ □
    # □

    assert yd.durfee_square_size == 3
    assert yd.durfee_square() == YoungDiagram((3, 3, 3))


def test_durfee_square_empty():
    yd = YoungDiagram(())
    assert yd.durfee_square_size == 0
    assert yd.durfee_square() == yd


def test_cell_containment():
    yd = YoungDiagram((5, 1))
    # ■ ■ ■ ■ ■
    # ■
    assert (1, 0) in yd
    assert Cell(0, 1) in yd
    assert Cell(2, 2) not in yd


def test_arm_length():
    yd = YoungDiagram((5, 2))
    # ■ ■ ■ ■ ■
    # ■ ■
    for i in range(5):
        assert yd.arm_length((i, 0)) == 5 - i - 1
    assert yd.arm_length((0, 1)) == 1


def test_leg_length():
    yd = YoungDiagram((3, 3, 2, 2, 1))
    # ■ ■ ■
    # ■ ■ ■
    # ■ ■
    # ■ ■
    # ■
    for i in range(5):
        assert yd.leg_length((0, i)) == 5 - i -1
    
    assert yd.leg_length((1, 1)) == 2
    assert yd.leg_length((2, 1)) == 0

def test_hook_length():
    yd = YoungDiagram((3, 3, 2))
    # ■ ■ ■
    # ■ ■ ■
    # ■ ■
    assert yd.hook_length((0, 0)) == 5
    assert yd.hook_length((0, 1)) == 4
    assert yd.hook_length((1, 1)) == 3


def test_repr():
    assert repr(YoungDiagram([4, 2, 1])) == "YoungDiagram((4, 2, 1))"
    assert repr(YoungDiagram([])) == "YoungDiagram(())"


def test_format_french():
    yd = YoungDiagram([3, 2, 1])
    assert format(yd, "french") == "■ \n■ ■ \n■ ■ ■ "


def test_format_russian():
    # too lazy to define the diagram
    yd = YoungDiagram([3, 2, 1])
    result = format(yd, "russian")
    assert isinstance(result, str)
    assert result.count("■") == yd.size


def test_format_invalid_convention():
    yd = YoungDiagram([2, 1])
    with pytest.raises(ValueError, match="Unknown convention"):
        format(yd, "diagonal")


def test_size():
    assert YoungDiagram([4, 3, 1]).size == 8
    assert YoungDiagram([]).size == 0


def test_eq():
    assert YoungDiagram([3, 2]) == YoungDiagram([3, 2])
    assert YoungDiagram([3, 2]) != YoungDiagram([3, 1])
    assert YoungDiagram([3, 2]) != "not a diagram"


def test_cell_content():
    # content = x - y
    assert Cell(3, 1).content == 2
    assert Cell(0, 0).content == 0

    yd = YoungDiagram([3, 2, 1])
    assert yd.content((2, 0)) == 2
    assert yd.content((0, 2)) == -2


def test_number_of_standard_tableaux():
    # Single cell: only one SYT
    assert YoungDiagram([1]).number_of_standard_tableaux() == 1
    # Hook formula for (2,1): 3! / (3*1*1) = 2
    assert YoungDiagram([2, 1]).number_of_standard_tableaux() == 2
    # Staircase (3,2,1): 6! / (5*3*1*3*1*1) = 16
    assert YoungDiagram([3, 2, 1]).number_of_standard_tableaux() == 16
    # Rectangle (2,2): 4! / (3*1*2*1) = 2
    assert YoungDiagram([2, 2]).number_of_standard_tableaux() == 2


def test_is_self_conjugate():
    assert YoungDiagram([3, 2, 1]).is_self_conjugate()
    assert YoungDiagram([1]).is_self_conjugate()
    assert not YoungDiagram([3, 1]).is_self_conjugate()


def test_trailing_zeros_stripped():
    yd = YoungDiagram([3, 2, 0])
    assert yd.partition == (3, 2)


def test_draw_addable_returns_string():
    yd = YoungDiagram([2, 1])
    result = yd.draw_addable()
    assert isinstance(result, str)
    assert "+" in result


def test_draw_removable_returns_string():
    yd = YoungDiagram([2, 1])
    result = yd.draw_removable()
    assert isinstance(result, str)
    assert "□" in result

