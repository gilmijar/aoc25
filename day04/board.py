from itertools import chain, batched


def tuple_add(t1: tuple[int, int], t2:tuple[int, int]) -> tuple[int, int]:
    t3 = (
        t1[0] + t2[0],
        t1[1] + t2[1]
    )
    return t3


class Cell:
    def __init__(self, val:int|str, row:int, col:int, brd:object):
        self.value = val
        self.address = (row, col)
        self.board = brd

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f'Cell({self.value}, {self.address[0]}, {self.address[1]})'
    
    @property
    def neighbors(self) -> list[object]:
        nbrs = self.board.neighbors(self.address) # type: ignore
        return nbrs # type: ignore

    @property
    def neighbor_values(self) -> list[str]|list[int]:
        return [nbr.value for nbr in self.neighbors if nbr is not None]


class Board:
    @classmethod
    def from_filling(cls, filling: list[list[str]] | list[list[int]] | list[str] | list[int] | str)->object:
        if isinstance(filling, str):
            filling = filling.strip()
            width = filling.index('\n')
            filling = filling.replace('\n', '')
            height = len(filling)//width
            if height*width != len(filling):
                raise ValueError("Filling not rectangular")
            flat_filling = filling
        elif isinstance(filling, list): # type: ignore
            width = len(filling[0])
            height = len(filling)
            if isinstance(filling[0], list):
                flat_filling = chain(*filling)
            elif isinstance(filling[0], (str, int)):
                flat_filling = filling
            else:
                raise ValueError("Unexpected inner type of board filling")
        else:
            raise ValueError("Unexpected type of board filling")
        
        new_board = cls(width, height)
        for addr, val in zip(new_board._cells, flat_filling):
            new_board._cells[addr] = Cell(val, *addr, new_board)
        return new_board
    
    def __init__(self, w: int, h: int)->None:
        self.height = h
        self.width = w
        self._cells:dict[tuple[int,int],None|Cell] = {(r, c): None for r in range(h) for c in range(w)}
        self.size = len(self._cells)
        self.neighbor_coords = (
            (-1, -1), (-1, 0), (-1,  1),
            ( 0, -1),          ( 0,  1),
            ( 1, -1), ( 1, 0), ( 1,  1)
        )

    def as_rows(self):
        return batched(self.cells, self.width)

    def to_str(self, sep='', end='\n') -> str:
        rows = ((str(cell) for cell in row) for row in self.as_rows())
        return end.join(sep.join(row) for row in rows)

    def __str__(self) -> str:
        return self.to_str()

    def neighbors(self, addr: tuple[int, int]) -> list[Cell]:
        resp = [self._cells.get(tuple_add(addr, shift), None) for shift in self.neighbor_coords]
        return resp

    def each_apply(self, func, by_rows = False):
        """ 
            apply func to each cell and return a list of results.
            function must accept a Cell as its first argument
        """
        if by_rows:
            return [[func(cell) for cell in row] for row in self.as_rows()]
        return [func(cell) for cell in self.cells]

    @property
    def cells(self) -> list[Cell]:
        return list(self._cells.values())
    
    def count(self, what):
        vals = [c.value for c in self.cells]
        return vals.count(what)


if __name__ == '__main__':
    fill = [['a', 'b', 'c'], ['d', 'e', 'f']]
    x = Board.from_filling(fill)
    print(x)

    print(
        x._cells[(0,0)].neighbors
    )
