import pytest

from yungdiagram import YoungDiagram, YoungTableau


def test_repr():
    yt = YoungTableau([[1, 2, 4], [3, 5]])
    assert repr(yt) == "YoungTableau([[1, 2, 4], [3, 5]])"


def test_eq_and_hash():
    a = YoungTableau([[1, 2], [3]])
    b = YoungTableau([[1, 2], [3]])
    c = YoungTableau([[1, 3], [2]])
    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)


def test_str_english():
    yt = YoungTableau([[1, 2, 4], [3, 5]])
    assert str(yt) == "1 2 4\n3 5"


def test_str_french():
    yt = YoungTableau([[1, 2, 4], [3, 5]])
    assert format(yt, "french") == "3 5\n1 2 4"


def test_str_multidigit():
    yt = YoungTableau([[1, 10], [3]])
    assert str(yt) == " 1 10\n 3"


def test_str_unknown_convention():
    yt = YoungTableau([[1, 2], [3]])
    with pytest.raises(ValueError, match="Unknown convention"):
        format(yt, "russian")


def test_repr_html():
    yt = YoungTableau([[1, 2], [3]])
    html = yt._repr_html_()
    assert "<table" in html
    assert ">1<" in html
    assert ">2<" in html
    assert ">3<" in html


def test_standard_row_decreasing_fails():
    yt = YoungTableau([[2, 1], [3]])
    assert not yt.is_standard()


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
