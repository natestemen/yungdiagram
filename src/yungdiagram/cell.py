class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other: 'Cell') -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    @property
    def content(self) -> int:
        return self.x - self.y
    
    def __repr__(self) -> str:
        return f"Cell(x={self.x}, y={self.y})"