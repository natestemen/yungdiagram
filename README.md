# yungdiagram

A Python package for working with Young diagrams, Young tableaux, and skew shapes — the combinatorial objects at the heart of symmetric function theory, representation theory of the symmetric group, and algebraic combinatorics.

## Installation

```bash
pip install -e .   # from source (PyPI release coming soon)
```

## Quick start

```python
from yungdiagram import YoungDiagram, SkewDiagram, YoungTableau, SkewTableau
```

**Young diagrams** are created from integer partitions (weakly decreasing sequences of positive integers):

```python
d = YoungDiagram([4, 3, 1])
print(d)
# ■ ■ ■ ■
# ■ ■ ■
# ■

print(d.size)            # 8
print(d.conjugate())     # YoungDiagram((3, 2, 2, 1))
print(d.number_of_standard_tableaux())  # 70
```

**Display conventions** — English (default), French, and Russian are all supported:

```python
print(f"{d:french}")    # rows bottom-to-top
print(f"{d:russian}")   # 45-degree rotation
```

**Hook lengths** — arm, leg, and hook length of any cell:

```python
from yungdiagram import Cell
d.arm_length(Cell(1, 0))   # 2
d.hook_length(Cell(0, 0))  # 6
```

**Young tableaux** — fillings of a diagram that are weakly increasing along rows:

```python
t = YoungTableau([[1, 1, 2, 3], [2, 3, 4], [5]])
print(t.is_semistandard())  # True
print(t.weight)             # (1, 2, 2, 1, 1)
print(t)
# 1 1 2 3
# 2 3 4
# 5

syt = YoungTableau([[1, 2, 5, 6], [3, 4], [7]])
print(syt.is_standard())    # True
```

**Skew shapes and tableaux:**

```python
big   = YoungDiagram([4, 3, 1])
small = YoungDiagram([2, 1])
skew  = SkewDiagram(big, small)
print(skew)
# ■ ■ ■ ■   (outer shape minus inner shape)
#   ■ ■
# ■
print(skew.is_horizontal_strip())  # False

st = SkewTableau([[None, None, 1, 2], [None, 3, 4], [5]])
print(st.is_semistandard())  # True
```

**Random diagrams** — uniformly random partition of n:

```python
YoungDiagram.random(50)
```

## API overview

| Class | Represents |
|-------|-----------|
| `YoungDiagram` | Integer partition / Young diagram (λ) |
| `SkewDiagram` | Skew shape λ/μ where μ ⊆ λ |
| `YoungTableau` | Filling of a Young diagram |
| `SkewTableau` | Filling of a skew shape (None = inner cells) |
| `Cell` | A single box (x, y) in a diagram |

## Further reading

- Stanley, *Enumerative Combinatorics*, Vol. 2, Chapter 7
- Sagan, *The Symmetric Group*, Chapter 4
- Fulton, *Young Tableaux*
- Pak & Yang, "The product formula for the number of standard Young tableaux"
