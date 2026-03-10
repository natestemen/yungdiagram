from yungdiagram import YoungDiagram, YoungTableau, SkewDiagram


def test_skew_tableau_initialization():
    #   - - - -
    # | • • 4 3
    # | • 8 1
    # | 1
    filling = [[None, None, 4, 3], [None, 8, 1], [1]]
    yt = YoungTableau(filling)
    big_yd = YoungDiagram([4, 3, 1])
    small_yd = YoungDiagram([2, 1])
    skew = SkewDiagram(big_yd, small_yd)

    assert yt.diagram == skew
    assert yt.filling == filling