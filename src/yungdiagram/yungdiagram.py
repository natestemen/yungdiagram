import math

from yungdiagram.cell import Cell


class YoungDiagram:
    def __init__(self, partition: list[int]):
        self.partition = partition
        self.cells = self._generate_cells()

    def _generate_cells(self) -> list[Cell]:
        for i, j in zip(self.partition, self.partition[1:]):
            if j > i:
                raise ValueError("Invalid partition.")
        cells = []
        for y, row_length in enumerate(self.partition):
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
        cell = self[index]
        return cell.x - cell.y

    def __str__(self):
        for row in self.partition:
            print("■ " * row)

    def addable_cells(self) -> list[Cell]:
        addable = []
        for row_index, row in enumerate(self.cells):
            last_cell = row[-1]
            if row_index == 0:
                addable.append(Cell(last_cell.x + 1, last_cell.y))
            else:
                above_row = self.cells[row_index - 1]
                if len(above_row) > len(row):
                    addable.append(Cell(last_cell.x + 1, last_cell.y))
        addable.append(Cell(0, last_cell.y + 1))
        return addable

    def reachable_young_diagrams_by_addition(self) -> list["YoungDiagram"]:
        diagrams = []
        for cell in self.addable_cells():
            new_partition = self.partition.copy()
            if cell.y == len(new_partition):
                new_partition.append(1)
            else:
                new_partition[cell.y] += 1
            diagrams.append(YoungDiagram(new_partition))
        return diagrams

    def removable_cells(self) -> list[Cell]:
        removable = []
        for row_index, row in enumerate(self.cells):
            last_cell = row[-1]
            if row_index == len(self.cells) - 1:
                removable.append(last_cell)
            else:
                below_row = self.cells[row_index + 1]
                if len(below_row) < len(row):
                    removable.append(last_cell)
        return removable

    def reachable_young_diagrams_by_removal(self) -> list["YoungDiagram"]:
        diagrams = []
        for cell in self.removable_cells():
            new_partition = self.partition.copy()
            new_partition[cell.y] -= 1
            if new_partition[cell.y] == 0:
                new_partition.pop()
            diagrams.append(YoungDiagram(new_partition))
        return diagrams

    def _draw_with_marks(
        self, marks: dict[tuple[int, int], str], height: int, width: int
    ) -> None:
        diagram = [[" "] * width for _ in range(height)]
        for y, row_len in enumerate(self.partition):
            diagram[y][:row_len] = ["■"] * row_len
        for (x, y), ch in marks.items():
            diagram[y][x] = ch
        for row in diagram:
            print(" ".join(row))
    
    def draw_addable(self):
        """Draw the Young diagram with addable cells marked by '+'."""
        marks = {(c.x, c.y): '+' for c in self.addable_cells()}
        self._draw_with_marks(
            marks,
            height=len(self.partition) + 1,
            width=max(self.partition) + 1 if self.partition else 1
        )

    def draw_removable(self):
        """draws the young diagram with the removable cells marked with a red square.
        the function removable_cells is used.
        """
        marks = {(c.x, c.y): '□' for c in self.removable_cells()}
        self._draw_with_marks(
            marks,
            height=len(self.partition),
            width=max(self.partition) if self.partition else 0
        )

    def hook_length(self, index: tuple[int, int]) -> int:
        x, y = index
        right = len(self.cells[y][x + 1 :])
        below = []
        for row in self.cells[y + 1 :]:
            if x < len(row):
                below.append(row[x])

        below = len(below)
        return right + below + 1

    def number_of_standard_tableaux(self) -> int:
        n = sum(self.partition)
        hook_lengths = []
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                hook_lengths.append(self.hook_length((x, y)))
        product_of_hook_lengths = math.prod(hook_lengths)
        return int(math.factorial(n) / product_of_hook_lengths)

    def __add__(self, other: Cell) -> "YoungDiagram":
        if other not in self.addable_cells():
            raise ValueError("Cell is not addable.")

        new_partition = self.partition.copy()
        if other.y == len(new_partition):
            new_partition.append(1)
        else:
            new_partition[other.y] += 1
        return YoungDiagram(new_partition)

    def __sub__(self, other: Cell) -> "YoungDiagram":
        if other not in self.removable_cells():
            raise ValueError("Cell is not removable.")

        new_partition = self.partition.copy()
        new_partition[other.y] -= 1
        if new_partition[other.y] == 0:
            new_partition.pop()
        return YoungDiagram(new_partition)

    def __eq__(self, other: "YoungDiagram") -> bool:
        return self.partition == other.partition

    def transpose(self) -> "YoungDiagram":
        new_partition = [
            sum(1 for x in self.partition if x >= j)
            for j in range(1, self.partition[0] + 1)
        ]
        print(new_partition)
        return YoungDiagram(new_partition)
