import pytest

from yungdiagram import YoungDiagram, YoungTableau


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
    filling = [[-1, 2, 3, 2], [2, 2], [7]]
    with pytest.raises(ValueError, match="positive"):
        YoungTableau(filling)

    filling = [[0, 2, 2, 2], [2, 2], [7]]
    with pytest.raises(ValueError, match="positive"):
        YoungTableau(filling)


def test_tableau_semistandard():
    # - - - -
    # 1 1 2
    # 2 5
    # 7
    # 8
    filling = [[1, 1, 2], [2, 5], [7], [8]]
    yt = YoungTableau(filling)
    assert yt.is_semistandard()


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


def test_tableau_weight():
    # - - - - -
    # 2 2 4 5
    # 5 7
    # 5
    filling = [[2, 2, 4, 5], [5, 7], [5]]
    yt = YoungTableau(filling)
    assert yt.weight == (0, 2, 0, 1, 3, 0, 1)


def test_conjugate():
    # 1 2 4      1 3
    # 3 5    ->  2 5
    #            4
    yt = YoungTableau([[1, 2, 4], [3, 5]])
    conj = yt.conjugate()
    assert conj.filling == [[1, 3], [2, 5], [4]]
    assert conj.diagram == yt.diagram.conjugate()

    # conjugate of a SYT is a SYT
    syt = YoungTableau([[1, 2, 5], [3, 4]])
    assert syt.is_standard()
    assert syt.conjugate().is_standard()
