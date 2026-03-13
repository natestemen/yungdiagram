from yungdiagram import SkewDiagram, SkewTableau, YoungDiagram


def test_skew_tableau_initialization():
    #   - - - -
    # | • • 4 3
    # | • 8 1
    # | 1
    filling = [[None, None, 4, 3], [None, 8, 1], [1]]
    st = SkewTableau(filling)
    big_yd = YoungDiagram([4, 3, 1])
    small_yd = YoungDiagram([2, 1])
    skew = SkewDiagram(big_yd, small_yd)

    assert st.diagram == skew
    assert st.filling == filling


def test_is_semistandard():
    # • 1 2
    # • 2 3
    st = SkewTableau([[None, 1, 2], [None, 2, 3]])
    assert st.is_semistandard()

    # • 2 1  — row not weakly increasing
    # • 2 3
    st2 = SkewTableau([[None, 2, 1], [None, 2, 3]])
    assert not st2.is_semistandard()

    # • 1 2
    # • 1 3  — column 1: 1 not < 1
    st3 = SkewTableau([[None, 1, 2], [None, 1, 3]])
    assert not st3.is_semistandard()


def test_is_standard():
    # • 1 2
    # • 3 4
    st = SkewTableau([[None, 1, 2], [None, 3, 4]])
    assert st.is_standard()

    # • 1 3
    # • 2 4
    st2 = SkewTableau([[None, 1, 3], [None, 2, 4]])
    assert st2.is_standard()

    # • 1 2  — missing 4, has repeated 3
    # • 3 3
    st3 = SkewTableau([[None, 1, 2], [None, 3, 3]])
    assert not st3.is_standard()

    # • 2 1  — row not strictly increasing
    # • 3 4
    st4 = SkewTableau([[None, 2, 1], [None, 3, 4]])
    assert not st4.is_standard()


def test_weight():
    # • 1 1
    # • 2 3
    st = SkewTableau([[None, 1, 1], [None, 2, 3]])
    assert st.weight == (2, 1, 1)

    # • 2 2
    # • 2 3
    st2 = SkewTableau([[None, 2, 2], [None, 2, 3]])
    assert st2.weight == (0, 3, 1)


def test_conjugate():
    # • 1 2      • •
    # • 3 4  ->  1 3
    #            2 4
    st = SkewTableau([[None, 1, 2], [None, 3, 4]])
    conj = st.conjugate()
    assert conj.filling == [[None, None], [1, 3], [2, 4]]
    assert conj.diagram == st.diagram.conjugate()

    # conjugate of a skew SYT is a skew SYT
    assert st.is_standard()
    assert conj.is_standard()