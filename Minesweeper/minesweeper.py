import numpy as np
import random

class board(object):
    """An object for the game minesweeper.

    Essential attributes are the `board` and the `sboard` (meant 
    to stand for show-board). The `board` stores the 
    true locations of the mines. The `sboard` stores
    the board meant to be printed to screen.

    """
    def __init__(self, size, N, seed = 1234):
        np.random.seed(seed)
        random.seed(seed)
        
        assert N < size*size, "Too many mines"

        #TODO replace with list comprehension
        #TODO2 replace with a list of mine positions
        #self.board = [[0]*size for _ in range(size)]
        self.board = np.zeros((size, size), dtype=int)
        self.size = size
        self.N = N
        n = N
        
        while n > 0:
            i = random.randint(0, size-1)
            j = random.randint(0, size-1)
            if self.board[i, j] == 0:
                self.board[i, j] = 1
                n -= 1

        self.sboard = np.chararray((size, size), unicode=True)
        self.sboard[:] = "_"

        self.N_free = size*size - N

    def __str__(self):
        return "\n".join(str(r) for r in self.sboard)

    def print_secret_board(self):
        s = "\n".join(str(r) for r in self.board)
        print(s)
        return

    def _get_adj(self, i, j):
        #TODO replace with nested loops
        
        out = []
        #up & down and diagonals
        if i > 0:
            out.append([i-1, j])
            if j > 0:
                out.append([i - 1, j - 1])
            if j < self.size - 1:
                out.append([i - 1, j + 1])

        if i < self.size - 1:
            out.append([i+1, j])
            if j > 0:
                out.append([i + 1, j - 1])
            if j < self.size - 1:
                out.append([i + 1, j + 1])

        #Left and right
        if j > 0:
            out.append([i, j-1])
        if j < self.size - 1:
            out.append([i, j+1])
        return out

    def _get_count(self, i, j):
        #Get the number for this square
        #or else replace with a C for 0
        #or * with a bomb
        if self.board[i, j]:
            return "*"
        t = 0
        adj = self._get_adj(i, j)

        for ii, jj in adj:
            t += self.board[ii, jj]
        if t == 0:
            return "C"
        return str(t)

    def click(self, i, j):
        #Simulate a person clicking square (i, j)
        
        self.sboard[i, j] = self._get_count(i, j)
        if self.board[i, j]:
            print(self)
            self.print_secret_board()
            print("you explode")
            return

        stack = self._get_adj(i, j)
        if self.sboard[i, j] != "C":
            print(self)
            if len(self.sboard[self.sboard == "_"]) - self.N == 0:
                print("confetti and music")
            return
        
        #breadth first search on
        #adjacent squares to fill in
        
        
        def clear(stack):
            for ind, (i, j) in enumerate(stack):
                if self.sboard[i, j] != "_" or self.board[i, j] == 1:
                    stack.pop(ind) #remove
            return stack
        
        stack = clear(stack)
        while stack:
            ii, jj = stack.pop()
            if self.sboard[ii, jj] != "_" or self.board[ii, jj]:
                continue
            
            c = self._get_count(ii, jj)
            self.sboard[ii, jj] = c
            
            if c == "C": #if the revealed square is a C, branch
                stack += self._get_adj(ii, jj)
                stack = clear(stack)
        print(self)

        if len(self.sboard[self.sboard == "_"]) - self.N == 0:
            print("confetti and music")
        return
