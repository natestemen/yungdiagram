import pytest

from yungdiagram import YoungDiagram, SkewDiagram, YoungTableau


def test_young_tableau_initialization():
    filling = [[5, 6, 4, 3], [8, 8, 1], [1]]
    yt = YoungTableau(filling)
    yd = YoungDiagram([4, 3, 1])

    assert yt.diagram == yd
    assert yt.filling == filling

def test_young_tableau_invalid_filling():
    # - - - -
    # 1 2 3 2
    # 2 2
    # 7
    filling = [[1, 2, 3, 2], [2, 2], [7]]
    with pytest.raises(ValueError, match="Invalid"):
        YoungTableau(filling)

    filling = [[1, 2, 2, 2], [2, 2], [7]]
    with pytest.raises(ValueError, match="Invalid"):
        YoungTableau(filling)

def test_tableau_standard():
    # - - - -
    # 1 3 4 6
    # 2 5
    # 7
    # 8
    filling = [[1, 3, 4, 6], [2, 5], [7], [8]]
    yt = YoungTableau(filling)
    assert yt.is_standard()

def test_tableau_nonstandard():
    # - - - - -
    # 1 3 4 6
    # 5 7
    # 8
    filling = [[1, 3, 4, 6], [5, 7], [8]]  # missing "2"
    yt = YoungTableau(filling)
    assert not yt.is_standard()
