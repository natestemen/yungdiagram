import math
import random
from itertools import accumulate, zip_longest
from typing import NamedTuple


class Cell(NamedTuple):
    x: int
    y: int

    @property
    def content(self) -> int:
        return self.x - self.y


class YoungDiagram:
    _P = None  # partition counts
    _max_precomputed = 0

    def __init__(self, partition: tuple[int, ...] | list[int]):
        self.partition = self._validate_partition(list(partition))
        self.cells = self._generate_cells(partition)

    def _validate_partition(self, partition: list[int]) -> tuple[int, ...]:
        while partition and partition[-1] == 0:
            partition.pop()

        if any(x <= 0 for x in partition):
            raise ValueError("Invalid partition.")
        for i, j in zip(partition, partition[1:]):
            if j > i:
                raise ValueError("Invalid partition.")
        return tuple(partition)

    def _generate_cells(self, partition: list[int]) -> list[Cell]:
        cells = []
        for y, row_length in enumerate(partition):
            row = []
            for x in range(row_length):
                row.append(Cell(x, y))
            cells.append(row)
        return cells

    def __getitem__(self, index: tuple[int, int]) -> Cell:
        x, y = index
        return self.cells[y][x]

    @property
    def size(self) -> int:
        return sum(self.partition)

    def content(self, index: tuple[int, int]) -> int:
        return self[index].content

    def __repr__(self) -> str:
        return f"YoungDiagram({self.partition})"

    def __str__(self) -> str:
        return format(self)

    def __format__(self, convention: str) -> str:
        """Format the diagram using a convention specifier.

        Supported conventions: ``"english"`` (default), ``"french"``, ``"russian"``.

        Examples::

            str(diagram)            # english (default)
            f"{diagram}"            # english (default)
            f"{diagram:french}"     # french
            format(diagram, "russian")
        """
        if not convention or convention == "english":
            return "\n".join("■ " * row for row in self.partition)
        if convention == "french":
            return "\n".join("■ " * row for row in reversed(self.partition))
        if convention == "russian":
            return self._to_string_russian()
        raise ValueError(
            f"Unknown convention {convention!r}. "
            "Expected 'english', 'french', or 'russian'."
        )

    def _to_string_russian(self) -> str:
        if not self.partition:
            return ""

        coords: list[tuple[int, int]] = []
        for y, row_len in enumerate(self.partition):
            for x in range(row_len):
                # Rotate the French diagram by 45 degrees to get Russian coordinates.
                u = x - y
                v = x + y
                coords.append((u, v))

        us = [u for u, _ in coords]
        vs = [v for _, v in coords]
        min_u, max_u = min(us), max(us)
        min_v, max_v = min(vs), max(vs)

        scale = 2  # spacing to keep the diagonals readable
        width = (max_u - min_u) * scale + 1

        by_v: dict[int, list[int]] = {}
        for u, v in coords:
            by_v.setdefault(v, []).append(u)

        rows: list[str] = []
        for v in range(max_v, min_v - 1, -1):
            row = [" "] * width
            for u in by_v.get(v, []):
                idx = (u - min_u) * scale
                row[idx] = "■"
            rows.append("".join(row).rstrip())
        return "\n".join(rows)

    def addable_cells(self) -> list[Cell]:
        """A list of individual cells that can be added to self to maintain a valid
        diagram"""
        addable = []
        for row_index, row in enumerate(self.cells):
            above_len = self.partition[row_index - 1] if row_index > 0 else float("inf")
            if above_len > len(row):
                addable.append(Cell(len(row), row_index))
        addable.append(Cell(0, len(self.partition)))
        return addable

    def reachable_young_diagrams_by_addition(self) -> list["YoungDiagram"]:
        """A list of reachable diagrams via a single cell addition. Often notated λ↗μ
        where μ is the collection of diagrams being returned."""
        return [self + cell for cell in self.addable_cells()]

    def removable_cells(self) -> list[Cell]:
        removable = []
        for row_index, row in enumerate(self.cells):
            below_len = (
                self.partition[row_index + 1]
                if row_index < len(self.partition) - 1
                else 0
            )
            if below_len < len(row):
                removable.append(Cell(len(row) - 1, row_index))
        return removable

    def reachable_young_diagrams_by_removal(self) -> list["YoungDiagram"]:
        """A list of reachable diagrams via a single cell removal. Often notated λ↘︎μ
        where μ is the collection of diagrams being returned. Alternatively this is
        written μ↗λ. That is the diagrams which give back lambda when adding a single
        cell."""
        return [self - cell for cell in self.removable_cells()]

    def _draw_with_marks(
        self, marks: dict[tuple[int, int], str], height: int, width: int
    ) -> str:
        diagram = [[" "] * width for _ in range(height)]
        for y, row_len in enumerate(self.partition):
            diagram[y][:row_len] = ["■"] * row_len
        for (x, y), ch in marks.items():
            diagram[y][x] = ch
        return "\n".join(" ".join(row) for row in diagram)

    def draw_addable(self) -> str:
        """Return the diagram as a string with addable cells marked by '+'."""
        marks = {(c.x, c.y): "+" for c in self.addable_cells()}
        return self._draw_with_marks(
            marks,
            height=len(self.partition) + 1,
            width=max(self.partition) + 1 if self.partition else 1,
        )

    def draw_removable(self) -> str:
        """Return the diagram as a string with removable cells marked by '□'."""
        marks = {(c.x, c.y): "□" for c in self.removable_cells()}
        return self._draw_with_marks(
            marks,
            height=len(self.partition),
            width=max(self.partition) if self.partition else 0,
        )

    def arm_length(self, cell: Cell | tuple[int, int]) -> int:
        if cell not in self:
            raise ValueError(f"cell {cell} is not contained in diagram.")
        x, y = cell
        return self.partition[y] - x - 1

    def leg_length(self, cell: Cell | tuple[int, int]) -> int:
        if cell not in self:
            raise ValueError(f"cell {cell} is not contained in diagram.")
        x, y = cell
        return sum(1 for row in self.partition[y + 1 :] if row > x)

    def hook_length(self, cell: Cell | tuple[int, int]) -> int:
        return self.arm_length(cell) + self.leg_length(cell) + 1

    def number_of_standard_tableaux(self) -> int:
        n = sum(self.partition)
        hook_lengths = []
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                hook_lengths.append(self.hook_length((x, y)))

        # Compute n! / prod(hook_lengths) without constructing n! directly.
        # Reduce factors incrementally to keep intermediate values smaller.
        denoms = hook_lengths
        result = 1
        for i in range(2, n + 1):
            num = i
            for idx, d in enumerate(denoms):
                if d == 1:
                    continue
                g = math.gcd(num, d)
                if g > 1:
                    num //= g
                    d //= g
                    denoms[idx] = d
                    if num == 1:
                        break
            if num > 1:
                result *= num
        return result

    def __add__(self, other: Cell) -> "YoungDiagram":
        if other not in self.addable_cells():
            raise ValueError("Cell is not addable.")

        new_partition = list(self.partition)
        if other.y == len(new_partition):
            new_partition.append(1)
        else:
            new_partition[other.y] += 1
        return YoungDiagram(new_partition)

    def __sub__(self, other: Cell) -> "YoungDiagram":
        if other not in self.removable_cells():
            raise ValueError("Cell is not removable.")

        new_partition = list(self.partition)
        new_partition[other.y] -= 1
        if new_partition[other.y] == 0:
            new_partition.pop()
        return YoungDiagram(new_partition)

    def __eq__(self, other: "YoungDiagram") -> bool:
        if not isinstance(other, YoungDiagram):
            return False
        return self.partition == other.partition

    def __hash__(self) -> int:
        return hash(self.partition)

    def __contains__(self, cell: Cell | tuple[int, int]) -> bool:
        if isinstance(cell, (Cell, tuple)):
            x, y = cell
            return y < len(self.partition) and x < self.partition[y]
        return NotImplemented

    def conjugate(self) -> "YoungDiagram":
        if not self.partition:
            return YoungDiagram([])
        new_partition = [
            sum(1 for x in self.partition if x >= j)
            for j in range(1, self.partition[0] + 1)
        ]
        return YoungDiagram(new_partition)

    def is_self_conjugate(self) -> bool:
        return self == self.conjugate()

    def is_strict(self) -> bool:
        return all(x > y for x, y in zip(self.partition, self.partition[1:]))

    def dominates(self, other: "YoungDiagram") -> bool:
        """self dominates (≽) other if the cumulative sum of self's parts is >= other's
        at every position."""
        self_cumulative = accumulate(self.partition)
        other_cumulative = accumulate(other.partition)
        return all(
            p >= q
            for p, q in zip_longest(self_cumulative, other_cumulative, fillvalue=0)
        )

    def contains(self, other: "YoungDiagram") -> bool:
        """self contains other if every cell in other belongs to self."""
        return all(
            p >= q for p, q in zip_longest(self.partition, other.partition, fillvalue=0)
        )

    def strictly_contains(self, other: "YoungDiagram") -> bool:
        return all(
            p > q for p, q in zip_longest(self.partition, other.partition, fillvalue=0)
        )

    def div(self, other: "YoungDiagram") -> "SkewDiagram":
        return SkewDiagram(self, other)

    @property
    def durfee_square_size(self) -> int:
        return sum(
            1 for k, row_len in enumerate(self.partition, start=1) if row_len >= k
        )

    def durfee_square(self) -> "YoungDiagram":
        size = self.durfee_square_size
        return YoungDiagram([size] * size)

    @classmethod
    def _ensure_partition_tables(cls, n: int):
        if cls._max_precomputed >= n:
            return

        P = [[0] * (n + 1) for _ in range(n + 1)]

        for k in range(n + 1):
            P[0][k] = 1  # one way to partition 0

        for total in range(1, n + 1):
            for k in range(1, n + 1):
                if k > total:
                    P[total][k] = P[total][total]
                else:
                    P[total][k] = P[total][k - 1] + P[total - k][k]

        cls._P = P
        cls._max_precomputed = n

    @classmethod
    def random(cls, num_cells: int) -> "YoungDiagram":
        cls._ensure_partition_tables(num_cells)

        partition = []
        cells_left = num_cells
        max_row = num_cells

        while cells_left > 0:
            max_row = min(max_row, cells_left)

            total = cls._P[cells_left][max_row]

            r = random.randint(1, total)

            cumulative = 0
            for k in range(1, max_row + 1):
                # exact count for largest part exactly k
                exact = cls._P[cells_left][k] - cls._P[cells_left][k - 1]
                cumulative += exact
                if cumulative >= r:
                    break

            partition.append(k)
            cells_left -= k
            max_row = k

        return cls(partition)

    def _repr_html_(self) -> str:
        rows = []
        for row_len in self.partition:
            cells = "".join(
                '<td style="width:30px;height:30px;border:1px solid black;"></td>'
                * row_len
            )
            rows.append(f"<tr>{cells}</tr>")
        return f'<table style="border-collapse:collapse;">{"".join(rows)}</table>'


class SkewDiagram:
    def __init__(self, big: YoungDiagram, small: YoungDiagram):
        # TODO: if small is None, return YoungDiagram? (rather than skew)
        if not big.contains(small):
            raise ValueError("The first argument does not contain the second.")
        self.big = big
        self.small = small

    def __repr__(self) -> str:
        return f"SkewDiagram({self.big.partition}, {self.small.partition})"

    def __str__(self) -> str:
        return format(self)

    def __format__(self, convention: str) -> str:
        if convention not in ("", "english", "french"):
            raise ValueError(
                f"Unknown convention {convention!r}. "
                "Expected 'english' or 'french'."
            )
        rows = []
        for y, big_len in enumerate(self.big.partition):
            small_len = (
                self.small.partition[y] if y < len(self.small.partition) else 0
            )
            row = "  " * small_len + "■ " * (big_len - small_len)
            rows.append(row.rstrip())
        if convention == "french":
            rows = list(reversed(rows))
        return "\n".join(rows)

    def _repr_html_(self) -> str:
        td_filled = (
            "width:30px;height:30px;"
            "border:1px solid black;background-color:#d0d0d0;"
        )
        td_empty = "width:30px;height:30px;"
        rows = []
        for y, big_len in enumerate(self.big.partition):
            small_len = (
                self.small.partition[y] if y < len(self.small.partition) else 0
            )
            cells = (
                "".join(f'<td style="{td_empty}"></td>' for _ in range(small_len))
                + "".join(
                    f'<td style="{td_filled}"></td>'
                    for _ in range(big_len - small_len)
                )
            )
            rows.append(f"<tr>{cells}</tr>")
        return f'<table style="border-collapse:collapse;">{"".join(rows)}</table>'

    def __eq__(self, other: "SkewDiagram") -> bool:
        if not isinstance(other, SkewDiagram):
            return False
        return self.big == other.big and self.small == other.small

    def __hash__(self) -> int:
        return hash((self.big.partition, self.small.partition))

    def __contains__(self, cell: Cell | tuple[int, int]) -> bool:
        return cell in self.big and cell not in self.small

    @property
    def size(self) -> int:
        return self.big.size - self.small.size

    @property
    def cells(self) -> list[Cell]:
        return [
            Cell(x, y)
            for y, row_len in enumerate(self.big.partition)
            for x in range(
                self.small.partition[y] if y < len(self.small.partition) else 0,
                row_len,
            )
        ]

    def conjugate(self) -> "SkewDiagram":
        return SkewDiagram(self.big.conjugate(), self.small.conjugate())

    def is_horizontal_strip(self) -> bool:
        """A skew shape is a horizontal strip if it has at most one cell per column,
        equivalently if small_i >= big_{i+1} for all i."""
        return all(
            small_i >= big_i1
            for small_i, big_i1 in zip_longest(
                self.small.partition, self.big.partition[1:], fillvalue=0
            )
        )

    def is_vertical_strip(self) -> bool:
        """A skew shape is a vertical strip if it has at most one cell per row,
        equivalently if big_i - small_i <= 1 for all i."""
        return all(
            big_i - small_i <= 1
            for big_i, small_i in zip_longest(
                self.big.partition, self.small.partition, fillvalue=0
            )
        )

    def is_connected(self) -> bool:
        cells = set()
        for y, row_len in enumerate(self.big.partition):
            small_len = self.small.partition[y] if y < len(self.small.partition) else 0
            for x in range(small_len, row_len):
                cells.add((x, y))

        if not cells:
            return True

        visited = set()
        queue = [next(iter(cells))]
        while queue:
            x, y = queue.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) in cells and (nx, ny) not in visited:
                    queue.append((nx, ny))

        return len(visited) == len(cells)
