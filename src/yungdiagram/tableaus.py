from yungdiagram.diagrams import SkewDiagram, YoungDiagram


def construct_tableau_from_filling(
    filling: list[list[int | None]],
) -> YoungDiagram | SkewDiagram:
    flattened = set(n for row in filling for n in row)

    if None not in flattened:
        partition = (len(row) for row in filling)
        return YoungDiagram(partition)

    big_partition = (len(row) for row in filling)
    small_partition = (row.count(None) for row in filling)
    big, small = YoungDiagram(big_partition), YoungDiagram(small_partition)
    return SkewDiagram(big, small)


class YoungTableau:
    def __init__(self, filling: list[list[int]]):
        if not self._valid_filling(filling):
            raise ValueError(
                "Invalid tableau filling. Filling must be weakly row increasing and strongly column increasing."
            )
        self.diagram = construct_tableau_from_filling(filling)
        self.filling = filling

    def _valid_filling(self, filling: list[list[int]]) -> bool:
        is_weakly_row_increasing = all(
            y >= x for row in filling for x, y in zip(row, row[1:])
        )
        is_column_strictly_increasing = all(
            filling[y + 1][x] > filling[y][x]
            for y in range(len(filling) - 1)
            for x in range(len(filling[y + 1]))
        )
        return is_weakly_row_increasing and is_column_strictly_increasing

    def is_standard(self):
        return set(n for row in self.filling for n in row) == set(
            range(1, self.diagram.size + 1)
        )


class SkewTableau:
    def __init__(self, filling: list[list[int | None]]):
        self.diagram = construct_tableau_from_filling(filling)
        self.filling = filling
