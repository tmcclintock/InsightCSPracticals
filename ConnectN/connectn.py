class ConnectN(object):
    def __init__(self, N):
        assert N > 3
        self.N = N
        self.reset()
        
    def reset(self):
        self.board = [[0] * self.N for _ in range(self.N)]
        self.nmoves = 0
        self.iswon = False

    def _move_is_valid(self, c):
        if c < 0 or c > self.N-1:
            print("Invalid column.")
            return False
        
        if self.board[self.N-1][c] is not 0:
            print("Column is full.")
            return False

        if self.nmoves == self.N**2:
            print("Board is full.")
            print("No winner.")
            self.reset()
            return False

        #isfull = True
        #for i in range(self.N):
        #    if isfull:
        #        for j in range(self.N):
        #            if not self.board[i][j]:
        #                isfull = False
        #                break
        #if isfull:
        #    print("Board is full.")
        #    return False
        return True

    def __str__(self):
        out = ""
        for i in range(self.N):
            out += str(self.board[self.N-1-i])
            if i < self.N - 1:
                out += "\n"
        return out

    def _game_is_won(self, r, c):
        p = self.nmoves % 2 + 1 #current player

        #Check vertical
        if r > 2:
            won = True
            for i in range(r-3, r):
                if self.board[i][c] != p:
                    won = False
                    break
            if won:
                return True

        #Check horizontal
        #sweep L to R
        for i in range(max(0, c-3), min(self.N-3, c)):
            won = True
            for j in range(i, i+4):
                if self.board[r][j] != p:
                    won = False
                    break
            if won:
                return True
        
        #Check LR diagonal
        for i in range(0, 4): #starting point
            if r - i < 0 or c - i < 0 or r - i + 4 > self.N or c - i + 4 > self.N:
                continue
            won = True
            for j in range(0, 4):
                if self.board[r-i+j][c-i+j] != p:
                    won = False
                    break
            if won:
                return True

        #Check RL diagonal
        for i in range(0, 4): #starting point
            if r - i < 0 or c - i < 0 or r - i + 4 > self.N or c - i - 4 > self.N:
                continue
            won = True
            for j in range(0, 4):
                if self.board[r-i+j][c+i-j] != p:
                    won = False
                    break
            if won:
                return True
        
        #print("Shouldn't have gotten here")
        return False
            
    def drop_piece(self, column):
        if self.iswon:
            print("The game ended.")
            return
        
        if not self._move_is_valid(column):
            return #do nothing

        cur = self.nmoves % 2 + 1
        print(f"Player {cur} plays in column {column}")

        for i in range(self.N):
            if not self.board[i][column]:
                self.board[i][column] = cur
                if self._game_is_won(i, column):
                    self.iswon = True
                    print(f"Player {cur} wins in {self.nmoves + 1} moves!")
                    print("Call reset() to play again.")
                break
        
        self.nmoves += 1
        return
