from collections import Counter

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
        if any(x < 1 for row in filling for x in row):
            raise ValueError("Only fillings with positive integers are supported.")
        self.diagram: YoungDiagram = construct_tableau_from_filling(filling)
        self.filling = filling

    def is_semistandard(self):
        is_weakly_row_increasing = all(
            y >= x for row in self.filling for x, y in zip(row, row[1:])
        )
        is_column_strictly_increasing = all(
            self.filling[y + 1][x] > self.filling[y][x]
            for y in range(len(self.filling) - 1)
            for x in range(len(self.filling[y + 1]))
        )
        return is_weakly_row_increasing and is_column_strictly_increasing

    def is_standard(self):
        return set(n for row in self.filling for n in row) == set(
            range(1, self.diagram.size + 1)
        )
    
    @property
    def weight(self) -> tuple[int, ...]:
        """Compute the weight of the tableau.

        Returns a tuple (a1, a2, ..., ak) where ai is the count of i.
        """
        counts = Counter(x for row in self.filling for x in row)
        if not counts:
            return ()

        max_label = max(counts)
        return tuple(counts.get(i, 0) for i in range(1, max_label + 1))

    def conjugate(self) -> "YoungTableau":
        max_cols = max(len(row) for row in self.filling) if self.filling else 0
        n_rows = len(self.filling)
        transposed = [
            [self.filling[r][col] for r in range(n_rows) if col < len(self.filling[r])]
            for col in range(max_cols)
        ]
        return YoungTableau(transposed)


class SkewTableau:
    def __init__(self, filling: list[list[int | None]]):
        self.diagram: SkewDiagram = construct_tableau_from_filling(filling)
        self.filling = filling

    def is_semistandard(self) -> bool:
        for row in self.filling:
            non_none = [x for x in row if x is not None]
            if any(b < a for a, b in zip(non_none, non_none[1:])):
                return False
        for y in range(len(self.filling) - 1):
            for x in range(min(len(self.filling[y]), len(self.filling[y + 1]))):
                above, below = self.filling[y][x], self.filling[y + 1][x]
                if above is not None and below is not None and below <= above:
                    return False
        return True

    def is_standard(self) -> bool:
        values = [x for row in self.filling for x in row if x is not None]
        if set(values) != set(range(1, self.diagram.size + 1)):
            return False
        for row in self.filling:
            non_none = [x for x in row if x is not None]
            if any(b <= a for a, b in zip(non_none, non_none[1:])):
                return False
        for y in range(len(self.filling) - 1):
            for x in range(min(len(self.filling[y]), len(self.filling[y + 1]))):
                above, below = self.filling[y][x], self.filling[y + 1][x]
                if above is not None and below is not None and below <= above:
                    return False
        return True

    @property
    def weight(self) -> tuple[int, ...]:
        counts = Counter(x for row in self.filling for x in row if x is not None)
        if not counts:
            return ()
        max_label = max(counts)
        return tuple(counts.get(i, 0) for i in range(1, max_label + 1))

    def conjugate(self) -> "SkewTableau":
        max_cols = max(len(row) for row in self.filling) if self.filling else 0
        n_rows = len(self.filling)
        transposed = [
            [self.filling[r][col] for r in range(n_rows) if col < len(self.filling[r])]
            for col in range(max_cols)
        ]
        return SkewTableau(transposed)
