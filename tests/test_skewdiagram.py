import pytest

from yungdiagram import Cell, SkewDiagram, YoungDiagram


def test_skewdiagram_initialization():
    big = YoungDiagram([3, 2])
    small = YoungDiagram([1])
    skew = SkewDiagram(big, small)
    assert skew.big == big
    assert skew.small == small


def test_skewdiagram_invalid():
    with pytest.raises(ValueError):
        SkewDiagram(YoungDiagram([2, 1]), YoungDiagram([3]))


def test_repr():
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert repr(skew) == "SkewDiagram((3, 2), (1,))"


def test_eq():
    big, small = YoungDiagram([3, 2]), YoungDiagram([1])
    assert SkewDiagram(big, small) == SkewDiagram(big, small)
    other = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([2]))
    assert SkewDiagram(big, small) != other


def test_hash():
    big, small = YoungDiagram([3, 2]), YoungDiagram([1])
    assert isinstance(hash(SkewDiagram(big, small)), int)
    assert hash(SkewDiagram(big, small)) == hash(SkewDiagram(big, small))


def test_size():
    # • ■ ■
    # ■ ■
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert skew.size == 4


def test_cells():
    # • ■ ■
    # ■ ■
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert skew.cells == [Cell(1, 0), Cell(2, 0), Cell(0, 1), Cell(1, 1)]


def test_contains():
    # • ■ ■
    # ■ ■
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert (1, 0) in skew
    assert (0, 1) in skew
    assert (0, 0) not in skew
    assert (5, 5) not in skew


def test_conjugate():
    # • • ■      • ■
    # ■ ■    ->  • ■
    #            ■
    big = YoungDiagram([3, 2])
    small = YoungDiagram([2])
    skew = SkewDiagram(big, small)
    expected = SkewDiagram(big.conjugate(), small.conjugate())
    assert skew.conjugate() == expected


def test_is_horizontal_strip():
    # • • ■  — at most one cell per column: yes
    # ■ ■
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([2]))
    assert skew.is_horizontal_strip()

    # • ■
    # • ■  — column 1 has two cells: not a horizontal strip
    skew2 = SkewDiagram(YoungDiagram([2, 2]), YoungDiagram([1, 1]))
    assert not skew2.is_horizontal_strip()


def test_is_vertical_strip():
    # • ■
    # • ■  — at most one cell per row: yes
    skew = SkewDiagram(YoungDiagram([2, 2]), YoungDiagram([1, 1]))
    assert skew.is_vertical_strip()

    # • • ■  — row 1 has two cells: not a vertical strip
    # ■ ■
    skew2 = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([2]))
    assert not skew2.is_vertical_strip()


def test_str_english():
    # • ■ ■
    # ■ ■
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert str(skew) == "  ■ ■\n■ ■"


def test_str_french():
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    assert format(skew, "french") == "■ ■\n  ■ ■"


def test_str_unknown_convention():
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    with pytest.raises(ValueError, match="Unknown convention"):
        format(skew, "russian")


def test_repr_html():
    skew = SkewDiagram(YoungDiagram([3, 2]), YoungDiagram([1]))
    html = skew._repr_html_()
    assert "<table" in html
    assert "#d0d0d0" in html   # filled cells
    assert "30px" in html


def test_skew_connectedness():
    # • • ■ ■
    # • * ■ ■
    # ■ ■
    big = YoungDiagram([4, 4, 2])
    small_disconnected = YoungDiagram([2, 2])
    small_connected = YoungDiagram([2, 1])
    skew_disconnected = SkewDiagram(big, small_disconnected)
    skew_connected = SkewDiagram(big, small_connected)
    assert not skew_disconnected.is_connected()
    assert skew_connected.is_connected()
