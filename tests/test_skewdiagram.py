from yungdiagram import SkewDiagram, YoungDiagram


def test_skewdiagram_initialization():
    ...

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
