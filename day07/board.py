from itertools import chain, batched
from typing import Self, Iterable, TypeVar, Callable, Any

T = TypeVar("T")
type Addr = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def addr_add(t1: Addr, t2: Addr) -> Addr:
    t3 = (t1[0] + t2[0], t1[1] + t2[1])
    return t3


class Board:
    @classmethod
    def from_filling(
        cls, filling: list[list[str]] | list[list[int]] | list[str] | list[int] | str
    ) -> Self:
        flat_filling: Iterable[int | str]
        if isinstance(filling, str):
            filling = filling.strip()
            width = filling.index("\n")
            filling = filling.replace("\n", "")
            height = len(filling) // width
            if height * width != len(filling):
                raise ValueError("Filling not rectangular")
            flat_filling = filling
        elif isinstance(filling, list):  # type: ignore
            width = len(filling[0])  # type: ignore
            height = len(filling)
            if isinstance(filling[0], list):
                flat_filling = chain(*filling)  # type: ignore
            elif isinstance(filling[0], (str, int)):  # type: ignore
                flat_filling = filling  # type: ignore
            else:
                raise ValueError("Unexpected inner type of board filling")
        else:
            raise ValueError("Unexpected type of board filling")

        new_board = cls(width, height)
        for addr, val in zip(new_board._cells, flat_filling):
            new_board[addr] = val
        return new_board

    def __init__(self, w: int, h: int, start_value=".") -> None:
        self.height = h
        self.width = w
        self._cells: dict[Addr, Cell] = {
            (r, c): Cell(start_value, r, c, self) for r in range(h) for c in range(w)
        }
        self.size = len(self._cells)
        self.neighbor_coords = (
            (-1, -1),
            UP,
            (-1, 1),
            LEFT,
            RIGHT,
            (1, -1),
            DOWN,
            (1, 1),
        )

    def __str__(self) -> str:
        return self.to_str()

    def __getitem__(self, addr: Addr) -> "Cell":
        return self._cells[addr]

    def get(self, addr, default: None | T = None) -> "Cell" | T:
        return self._cells.get(addr, default)

    def __setitem__(self, addr: Addr, val: int | str) -> bool:
        if addr not in self._cells:
            return False
        self._cells[addr].value = val
        return True

    def as_rows(self):
        return batched(self.cells, self.width)

    def to_str(self, sep: str = "", end: str = "\n") -> str:
        rows = ((str(cell) for cell in row) for row in self.as_rows())
        return end.join(sep.join(row) for row in rows)

    def neighbors(self, addr: Addr) -> list["Cell"]:
        resp = [
            self._cells.get(addr_add(addr, shift), None)
            for shift in self.neighbor_coords
        ]
        return [cell for cell in resp if cell is not None]

    def each_apply(
        self, func: Callable[..., T], by_rows: bool = False
    ) -> list[list[T] | T]:
        """
        apply func to each cell and return a list of results.
        function must accept a Cell as its first argument
        """
        if by_rows:
            return [[func(cell) for cell in row] for row in self.as_rows()]
        return [func(cell) for cell in self.cells]

    def find(self, needle: int | str) -> Iterable["Cell"]:
        x = filter(lambda c: c == needle, self.cells)
        return list(x)

    @property
    def cells(self) -> list["Cell"]:
        return list(self._cells.values())

    def count(self, what: str | int):
        vals = [1 for c in self.cells if c == what]
        return len(vals)


class Cell:
    def __init__(self, val: int | str, row: int, col: int, brd: "Board"):
        self.value = val
        self.address = (row, col)
        self.board = brd
        self.extra:Any = None

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Cell({self.value}, {self.address[0]}, {self.address[1]})"

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            return self.value == other

    @property
    def neighbors(self) -> list[Self | None]:
        nbrs = self.board.neighbors(self.address)  # type: ignore
        return nbrs  # type: ignore

    @property
    def neighbor_values(self) -> list[str | int]:
        return [nbr.value for nbr in self.neighbors if nbr is not None]

    def neighbor(self, direction: Addr) -> Self:
        return self.board.get(addr_add(self.address, direction))


if __name__ == "__main__":
    fill = [["a", "b", "c"], ["d", "e", "f"]]
    x: Board = Board.from_filling(fill)
    print(x)

    print(x[(0, 0)].neighbors)
