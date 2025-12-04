from itertools import chain, batched

class Board:
    @classmethod
    def from_filling(cls, filling:list[list[str|int]]|list[str|int]|str)->None:
        if isinstance(filling, str):
            filling = filling.strip()
            width = filling.index('\n')
            height = len(filling)//width
            if height*width != len(filling):
                raise ValueError("Filling not rectangular")
            flat_filling = filling.replace('\n', '')
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
        for addr, val in zip(new_board.cells, flat_filling):
            new_board.cells[addr] = Cell(val, *addr, new_board)
        return new_board
    
    def __init__(self, w: int, h: int)->None:
        self.height = h
        self.width = w
        self.cells:dict[tuple[int,int],None|int|str] = {(r, c): None for r in range(h) for c in range(w)}
        self.size = len(self.cells)

    def as_rows(self):
        return batched(self.cells.values(), self.width)

    def to_str(self, sep='', end='\n') -> str:
        rows = ((str(cell) for cell in row) for row in self.as_rows())
        return end.join(sep.join(row) for row in rows)

    def __str__(self) -> str:
        return self.to_str()


class Cell:
    def __init__(self, val, row, col, brd):
        self.value = val
        self.address = (row, col)
        self.board = brd

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f'Cell({self.value}, {self.address[0]}, {self.address[1]})'
    
    @property
    def neighbors(self):
        nbrs = self.board.neighbors(*self.address)
        return nbrs

if __name__ == '__main__':
    fill = [['a', 'b', 'c'], ['d', 'e', 'f']]
    x = Board.from_filling(fill)
    print(x)

    c = Cell(0, 1, 2, [1,2,3,4,5,6,7,8])
    print(*[c,c,c])
