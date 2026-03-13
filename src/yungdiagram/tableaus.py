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

    def __repr__(self) -> str:
        return f"YoungTableau({self.filling!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, YoungTableau):
            return False
        return self.filling == other.filling

    def __hash__(self) -> int:
        return hash(tuple(tuple(row) for row in self.filling))

    def __str__(self) -> str:
        return format(self)

    def __format__(self, convention: str) -> str:
        if convention not in ("", "english", "french"):
            raise ValueError(
                f"Unknown convention {convention!r}. Expected 'english' or 'french'."
            )
        if not self.filling:
            return ""
        width = max(len(str(x)) for row in self.filling for x in row)
        rows = [" ".join(str(x).rjust(width) for x in row) for row in self.filling]
        if convention == "french":
            rows = list(reversed(rows))
        return "\n".join(rows)

    def _repr_html_(self) -> str:
        td = 'style="width:30px;height:30px;border:1px solid black;text-align:center;"'
        rows = []
        for row in self.filling:
            cells = "".join(f"<td {td}>{x}</td>" for x in row)
            rows.append(f"<tr>{cells}</tr>")
        return f'<table style="border-collapse:collapse;">{"".join(rows)}</table>'

    def is_semistandard(self):
        """True if rows are weakly increasing and columns are strictly increasing."""
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
        """True if the filling uses {1, …, n} exactly once with strict rows and cols."""
        values = set(n for row in self.filling for n in row)
        if values != set(range(1, self.diagram.size + 1)):
            return False
        if not all(y > x for row in self.filling for x, y in zip(row, row[1:])):
            return False
        return all(
            self.filling[y + 1][x] > self.filling[y][x]
            for y in range(len(self.filling) - 1)
            for x in range(len(self.filling[y + 1]))
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
        """Transpose the filling; conjugate of a standard tableau is standard."""
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

    def __repr__(self) -> str:
        return f"SkewTableau({self.filling!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SkewTableau):
            return False
        return self.filling == other.filling

    def __hash__(self) -> int:
        return hash(tuple(tuple(row) for row in self.filling))

    def __str__(self) -> str:
        return format(self)

    def __format__(self, convention: str) -> str:
        if convention not in ("", "english", "french"):
            raise ValueError(
                f"Unknown convention {convention!r}. Expected 'english' or 'french'."
            )
        if not self.filling:
            return ""
        all_values = [x for row in self.filling for x in row if x is not None]
        width = max(len(str(x)) for x in all_values) if all_values else 1
        blank = " " * width
        rows = [
            " ".join(str(x).rjust(width) if x is not None else blank for x in row)
            for row in self.filling
        ]
        if convention == "french":
            rows = list(reversed(rows))
        return "\n".join(rows)

    def _repr_html_(self) -> str:
        td_filled = (
            'style="width:30px;height:30px;'
            'border:1px solid black;text-align:center;"'
        )
        td_empty = 'style="width:30px;height:30px;background-color:#e0e0e0;"'
        rows = []
        for row in self.filling:
            cells = "".join(
                f"<td {td_filled}>{x}</td>"
                if x is not None
                else f"<td {td_empty}></td>"
                for x in row
            )
            rows.append(f"<tr>{cells}</tr>")
        return f'<table style="border-collapse:collapse;">{"".join(rows)}</table>'

    def is_semistandard(self) -> bool:
        """True if non-None entries are weakly increasing in rows, strictly in cols."""
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
        """True if non-None entries are {1, …, n} exactly once, strictly increasing."""
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
        """Transpose the filling; conjugate of a standard skew tableau is standard."""
        max_cols = max(len(row) for row in self.filling) if self.filling else 0
        n_rows = len(self.filling)
        transposed = [
            [self.filling[r][col] for r in range(n_rows) if col < len(self.filling[r])]
            for col in range(max_cols)
        ]
        return SkewTableau(transposed)
