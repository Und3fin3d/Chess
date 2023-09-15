import re
from copy import deepcopy

squares = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
squares2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


class board:
    def __init__(self,FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.grid = [['•' for y in range(8)] for x in range(8)]
        self.wmove, self.wcast, self.bcast, self.movenum = self.fenconvert(FEN)
        self.dmove = False
        self.lastdoubp = ''
        self.ep = []
    def fenconvert(self, FEN):
        FEN = re.split('[//// ]', FEN)
        gamestate = FEN[8:]
        FEN = FEN[:8]
        FEN.reverse()
        count = 0
        count2 = 0
        for element in FEN:
            for char in element:
                if count2 > 7:
                    count += 1
                    count2 = count2 - 7
                if char.isdigit() == True:
                    count2 += int(char)
                else:
                    self.grid[count][count2] = char
                    count2 += 1
            count2 = 0
            count += 1
        return gamestate[0], gamestate[1][:2], gamestate[1][2:], gamestate[-1]
    def displayboard(self):
        for y in range(7, -1, -1):
            for x in range(0, 8):
                print('|' + self.grid[y][x] + '|', sep=' ', end='')
            print()
        print()
    def cleaner(self, pot):
        count = 0
        pot = pot.split(',')
        pot.pop()
        count = 0
        for sq in pot:
            pot[count] = sq[2:]
            count += 1
        return pot
    def kingfinder(self, king):
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == king:
                    x1 = x
                    y1 = y
        return x1, y1
    def check(self, x1=None, y1=None):
        kingfinder = self.kingfinder
        if x1 == y1 == None:
            x1, y1 = kingfinder('K')
        cleaner = self.cleaner
        potsquares = self.bishop(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'b' or self.grid[y][squares[x]] == 'q':
                    return True
        potsquares = self.rook(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'r' or self.grid[y][squares[x]] == 'q':
                    return True
        potsquares = self.knight(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'n':
                    return True
        if (x1 - 1 >= 0 and 1 + y <= 7 and self.grid[y1+1][x1-1] == 'p') or (x1 + 1 <= 7 and 1 + y <= 7 and self.grid[y1+1][x1+1] == 'p'):
            return True
        return False
    def bcheck(self, x1=None, y1=None):
        kingfinder = self.kingfinder
        if x1 == y1 == None:
            x1, y1 = kingfinder('k')
        cleaner = self.cleaner
        potsquares = self.bishop(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'B' or self.grid[y][squares[x]] == 'Q':
                    return True
        potsquares = self.rook(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'R' or self.grid[y][squares[x]] == 'Q':
                    return True
        potsquares = self.knight(x1, y1)
        if potsquares != '':
            potsquares = cleaner(potsquares)
            for element in potsquares:
                x = element[0]
                y = int(element[1]) - 1
                if self.grid[y][squares[x]] == 'n':
                    return True
        if (x1 - 1 >= 0 and y -1 >= 0 and self.grid[y1-1][x1-1] == 'P') or (x1 + 1 <= 7 and y -1 >= 0 and self.grid[y1-1][x1+1] == 'P'):
            return True
        return False
    def incheck(self):
        if self.check()==True:
            x,y = self.kingfinder('K')
            return squares2[x]+str(y+1)
        elif self.bcheck()==True:
            x,y = self.kingfinder('k')
            return squares2[x]+str(y+1)
        else:
            return ''
    def wpawn(self, x, y):
        legalmoves = ''
        if self.dmove == True and (squares[self.lastdoubp[0]] == x + 1 or squares[self.lastdoubp[0]]== x - 1) and int(self.lastdoubp[1]) - 1 == y and self.grid[int(self.lastdoubp[1]) - 1][squares[self.lastdoubp[0]]] != self.grid[y][x] and self.grid[int(self.lastdoubp[1]) -1][squares[self.lastdoubp[0]]] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + self.lastdoubp[0] + str(y + 1 +1) + ','
            self.ep.append(str(squares2[x]) + str(y + 1) + self.lastdoubp[0] +str(y + 1 + 1))
        if y == 1:
            if self.grid[y + 1][x] == '•' and self.grid[y + 2][x] == '•':
                legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 + 2) + ','
        if 1 + y <= 7 and self.grid[y + 1][x] == '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 + 1) + ','
        if x + 1 <= 7 and 1 + y <= 7 and self.grid[y + 1][x + 1].islower() != self.grid[y][x].islower() and self.grid[y + 1][x + 1] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y + 1 + 1) + ','
        if x - 1 >= 0 and 1 + y <= 7 and self.grid[y + 1][x - 1].islower() != self.grid[y][x].islower() and self.grid[y + 1][x - 1] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y + 1 + 1) + ','
        legalmovesnew = ''
        for element in legalmoves:
            if element == '8':
                legalmovesnew += '8P'
            else:
                legalmovesnew += element
        return legalmovesnew
    def bpawn(self, x, y):
        legalmoves = ''
        if self.dmove == True and (squares[self.lastdoubp[0]] == x + 1 or squares[self.lastdoubp[0]]== x - 1) and int(self.lastdoubp[1]) - 1 == y and self.grid[int(self.lastdoubp[1]) - 1][squares[self.lastdoubp[0]]] != self.grid[y][x] and self.grid[int(self.lastdoubp[1]) -1][squares[self.lastdoubp[0]]] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + self.lastdoubp[0] + str(y + 1 - 1) + ','
            self.ep.append(str(squares2[x]) + str(y + 1) + self.lastdoubp[0] +str(y + 1 - 1))
        if y == 6:
            if self.grid[y - 1][x] == '•' and self.grid[y - 2][x] == '•':
                legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 - 2) + ','
        if y - 1 >= 0 and self.grid[y - 1][x] == '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 - 1) + ','
        if x + 1 <= 7 and y - 1 >= 0 and self.grid[y - 1][x + 1].islower() != self.grid[y][x].islower() and self.grid[y - 1][x + 1] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y - 1 + 1) + ','
        if x - 1 >= 0 and y - 1 >= 0 and self.grid[y - 1][x - 1].islower() != self.grid[y][x].islower() and self.grid[y - 1][x - 1] != '•':
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y - 1 + 1) + ','
        legalmovesnew = ''
        for element in legalmoves:
            if element == '1':
                legalmovesnew += '1P'
            else:
                legalmovesnew += element
        return legalmovesnew
    def bishop(self, x, y):
        count = 1
        legalmoves = ''
        while count + x <= 7 and count + y <= 7:
            if self.grid[y][x].islower() == self.grid[count + y][count +x].islower() and self.grid[count + y][count + x] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + count]) + str(y + count + 1) + ','
            if self.grid[y][x].islower() != self.grid[count + y][count + x].islower() and self.grid[count + y][count +x] != '•':
                break
            count += 1
        count = 1
        while x - count >= 0 and y - count >= 0:
            if self.grid[y][x].islower() == self.grid[y - count][x -count].islower() and self.grid[y - count][x -count] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - count]) + str(y + 1 - count) + ','
            if self.grid[y][x].islower() != self.grid[y - count][x - count].islower() and self.grid[y - count][x - count] != '•':
                break
            count += 1
        count = 1
        while x - count >= 0 and count + y <= 7:
            if self.grid[y][x].islower() == self.grid[count + y][x - count].islower() and self.grid[count +y][x - count] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - count]) + str(y + 1 + count) + ','
            if self.grid[y][x].islower() != self.grid[count + y][x - count].islower() and self.grid[y + count][x - count] != '•':
                break
            count += 1
        count = 1
        while count + x <= 7 and y - count >= 0:
            if self.grid[y][x].islower() == self.grid[y - count][count +x].islower() and self.grid[y - count][count + x] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(
                squares2[x + count]) + str(y + 1 - count) + ','
            if self.grid[y][x].islower() != self.grid[y - count][count + x].islower() and self.grid[y - count][count +x] != '•':
                break
            count += 1
        return legalmoves
    def knight(self, x, y):
        legalmoves = ''
        if x + 2 <= 7 and y - 1 >= 0 and (self.grid[y - 1][x + 2].islower() != self.grid[y][x].islower() and self.grid[y - 1][x + 2] != '•' or self.grid[y - 1][x + 2] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 2]) + str(y - 1 + 1) + ','
        if x - 2 >= 0 and y - 1 >= 0 and (self.grid[y - 1][x - 2].islower() != self.grid[y][x].islower() and self.grid[y - 1][x - 2] != '•' or self.grid[y - 1][x - 2] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(
                squares2[x - 2]) + str(y - 1 + 1) + ','
        if x + 2 <= 7 and y + 1 <= 7 and (self.grid[y + 1][x + 2].islower() != self.grid[y][x].islower() and self.grid[y + 1][x + 2] != '•' or self.grid[y + 1][x + 2] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 2]) + str(y + 1 + 1) + ','
        if x - 2 >= 0 and y + 1 <= 7 and (self.grid[y + 1][x - 2].islower() != self.grid[y][x].islower() and self.grid[y + 1][x - 2] != '•' or self.grid[y + 1][x - 2] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 2]) + str(y + 1 + 1) + ','
        if x + 1 <= 7 and y - 2 >= 0 and (self.grid[y - 2][x + 1].islower() != self.grid[y][x].islower() and self.grid[y - 2][x + 1] != '•' or self.grid[y - 2][x + 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y - 2 + 1) + ','
        if x - 1 >= 0 and y - 2 >= 0 and (self.grid[y - 2][x - 1].islower() != self.grid[y][x].islower() and self.grid[y - 2][x - 1] != '•' or self.grid[y - 2][x - 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y - 2 + 1) + ','
        if x + 1 <= 7 and y + 2 <= 7 and (self.grid[y + 2][x + 1].islower() != self.grid[y][x].islower() and self.grid[y + 2][x + 1] != '•'or self.grid[y + 2][x + 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y + 2 + 1) + ','
        if x - 1 >= 0 and y + 2 <= 7 and (self.grid[y + 2][x - 1].islower() != self.grid[y][x].islower() and self.grid[y + 2][x - 1] != '•'
                or self.grid[y + 2][x - 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(
                squares2[x - 1]) + str(y + 2 + 1) + ','
        return legalmoves
    def rook(self, x, y):
        count = 1
        legalmoves = ''
        while count + x <= 7:
            if self.grid[y][x].islower() == self.grid[y][count + x].islower() and self.grid[y][count + x] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + count]) + str(y + 1) + ','
            if self.grid[y][x].islower() != self.grid[y][count + x].islower() and self.grid[y][count + x] != '•':
                break
            count += 1
        count = 1
        while x - count >= 0:
            if self.grid[y][x].islower() == self.grid[y][x - count].islower() and self.grid[y][x - count] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - count]) + str(y + 1) + ','
            if self.grid[y][x].islower() != self.grid[y][x - count].islower() and self.grid[y][x - count] != '•':
                break
            count += 1
        count = 1
        while count + y <= 7:
            if self.grid[y][x].islower() == self.grid[count + y][x].islower() and self.grid[y + count][x] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 + count) + ','
            if self.grid[y][x].islower() != self.grid[count + y][x].islower() and self.grid[y + count][x] != '•':
                break
            count += 1
        count = 1
        while y - count >= 0:
            if self.grid[y][x].islower() == self.grid[y - count][x].islower() and self.grid[y - count][x] != '•':
                break
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 - count) + ','
            if self.grid[y][x].islower() != self.grid[y - count][x].islower() and self.grid[y - count][x] != '•':
                break
            count += 1
        return legalmoves
    def queen(self, x, y):
        legalmoves = ''
        legalmoves += self.bishop(x, y)
        legalmoves += self.rook(x, y)
        return legalmoves
    def king(self, x, y):
        legalmoves = ''
        if y - 1 >= 0 and (self.grid[y - 1][x].islower() != self.grid[y][x].islower() or self.grid[y - 1][x] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 - 1) + ','
        if x + 1 <= 7 and y - 1 >= 0 and (self.grid[y - 1][x + 1].islower() != self.grid[y][x].islower() or self.grid[y - 1][x + 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y - 1 + 1) + ','
        if x - 1 >= 0 and y - 1 >= 0 and (self.grid[y - 1][x - 1].islower() != self.grid[y][x].islower() or self.grid[y - 1][x - 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y - 1 + 1) + ','
        if 1 + y <= 7 and (self.grid[y + 1][x].islower() != self.grid[y][x].islower() or self.grid[y - 1][x] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x]) + str(y + 1 + 1) + ','
        if x + 1 <= 7 and 1 + y <= 7 and (self.grid[y + 1][x + 1].islower() != self.grid[y][x].islower() or self.grid[y + 1][x + 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y + 1 + 1) + ','
        if x - 1 >= 0 and y + 1 <= 7 and (self.grid[y + 1][x - 1].islower() != self.grid[y][x].islower() or self.grid[y + 1][x - 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y + 1 + 1) + ','
        if x - 1 >= 0 and (self.grid[y][x - 1].islower() != self.grid[y][x].islower() or self.grid[y][x - 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x - 1]) + str(y + 1) + ','
        if x + 1 <= 7 and (self.grid[y][x + 1].islower() != self.grid[y][x].islower() or self.grid[y][x + 1] == '•'):
            legalmoves += str(squares2[x]) + str(y + 1) + str(squares2[x + 1]) + str(y + 1) + ','
        count = 1
        beforegrid = deepcopy(self.grid)
        if self.grid[y][x] == 'K':
            while count + x <= 7 and self.grid[0][7] == 'R' and self.wcast[0] == 'K':
                self.playraw(str(squares2[x]) + str(y + 1) + str(squares2[x + count]) +str(y + 1) + ',')
                if self.check() == True:
                    break
                self.grid = deepcopy(beforegrid)
                if self.grid[y][count + x] == 'R' and (count + x) == 7:
                    legalmoves += 'O-O,'
                    break
                if self.grid[y][count + x] != '•':
                    break
                count += 1
            count = 1
            while x - count >= 0 and self.grid[0][0] == 'R' and self.wcast[1] == 'Q':
                self.playraw(str(squares2[x]) + str(y + 1) + str(squares2[x - count]) +str(y + 1) + ',')
                if self.check() == True:
                    break
                self.grid = deepcopy(beforegrid)
                if self.grid[y][x - count] == 'R' and (x - count) == 0:
                    legalmoves += 'O-O-O,'
                    break
                if self.grid[y][x - count] != '•':
                    break
                count += 1
            count = 1
        else:
            while count + x <= 7 and self.grid[7][7] == 'r' and self.bcast[0] == 'k':
                self.playraw(str(squares2[x]) + str(y + 1) + str(squares2[x + count]) +str(y + 1) + ',')
                if self.bcheck() == True:
                    break
                self.grid = deepcopy(beforegrid)
                if self.grid[y][count + x] == 'r' and (count + x) == 7:
                    legalmoves += 'O-O,'
                    break
                if self.grid[y][count + x] != '•':
                    break
                count += 1
            count = 1
            while x - count >= 0 and self.grid[7][0] == 'r' and self.bcast[1] == 'q':
                self.playraw(str(squares2[x]) + str(y + 1) + str(squares2[x - count]) +str(y + 1) + ',')
                if self.bcheck() == True:
                    break
                self.grid = deepcopy(beforegrid)
                if self.grid[y][x - count] == 'r' and (x - count) == 0:
                    legalmoves += 'O-O-O,'
                    break
                if self.grid[y][x - count] != '•':
                    break
                count += 1
        self.grid = deepcopy(beforegrid)
        return legalmoves
    def playalg(self, move):
        sq1 = move[:2]
        sq2 = move[2:]
        piece = self.grid[int(sq1[1]) - 1][squares[sq1[0]]]
        self.grid[int(sq1[1]) - 1][squares[sq1[0]]] = '•'
        self.grid[int(sq2[1]) - 1][squares[sq2[0]]] = piece
        if move in self.ep:
            self.grid[int(sq1[1]) - 1][squares[sq2[0]]] = '•'
    def playraw(self, move):
        playalg = self.playalg
        if self.wmove == 'w':
            if move == 'O-O':
                move = 'e1g1'
                playalg(move)
                move = 'h1f1'
                playalg(move)
            elif move == 'O-O-O':
                move = 'e1c1'
                playalg(move)
                move = 'a1d1'
                playalg(move)
            else:
                playalg(move)
        else:
            if move == 'O-O':
                move = 'e8g8'
                playalg(move)
                move = 'h8f8'
                playalg(move)
            elif move == 'O-O-O':
                move = 'e8c8'
                playalg(move)
                move = 'a8d8'
                playalg(move)
            else:
                playalg(move)
    def play(self, move):
        sq1 = move[:2]
        sq2 = move[2:]
        legal_moves = self.legal_moves
        playraw = self.playraw
        legalmoves = legal_moves()
        if move in legalmoves and move[-1]!='P':
            if 'O' not in move and self.grid[int(sq1[1]) - 1][squares[sq1[0]]].lower() == 'p' and abs(int(sq1[1]) -int(sq2[1])) == 2:
                self.dmove = True
                self.lastdoubp = sq2
            else:
                self.dmove = False
                self.lastdoubp = ''
            playraw(move)
            if 'O' in move and self.wmove == 'w':
                self.wcast = '--'
            elif 'O' in move and self.wmove == 'b':
                self.bcast = '--'
            elif self.grid[int(sq1[1]) - 1][squares[sq1[0]]] == 'K':  
                self.wcast = '--'
            elif self.grid[int(sq1[1]) - 1][squares[sq1[0]]] == 'k':
                self.bcast = '--'
            if self.wmove == 'w':
                self.wmove = 'b'
            else:
                self.wmove = 'w'
        elif move[-1].isupper():
            for m in legalmoves:
                if m[-1] == 'P' and move[:-1] == m[:-1] and self.wmove == 'w' and move[-1]!='P':
                    self.grid[int(move[-2]) - 1][squares[move[-3]]] = move[-1]
                    self.grid[int(sq1[1]) - 1][squares[sq1[0]]] = '•'
                    self.wmove = 'b'
                elif m[-1] == 'P' and move[:-1] == m[:-1] and self.wmove == 'b' and move[-1]!='P':
                    self.grid[int(move[-2]) -1][squares[move[-3]]] = move[-1].lower()#here here
                    self.grid[int(sq1[1]) - 1][squares[sq1[0]]] = '•'
                    self.wmove = 'w'
    def legal_moves(self):
        legalmoves = ''
        if self.wmove == 'w':
            for y in range(0, 8):
                for x in range(0, 8):
                    if self.grid[y][x].isupper():
                        tempmoves = ''
                        if self.grid[y][x] == 'P':
                            tempmoves = self.wpawn(x, y)
                        elif self.grid[y][x] == 'B':
                            tempmoves = self.bishop(x, y)
                        elif self.grid[y][x] == 'N':
                            tempmoves = self.knight(x, y)
                        elif self.grid[y][x] == 'R':
                            tempmoves = self.rook(x, y)
                        elif self.grid[y][x] == 'Q':
                            tempmoves = self.queen(x, y)
                        elif self.grid[y][x] == 'K':
                            tempmoves = self.king(x, y)
                        legalmoves += tempmoves
        else:
            for y in range(0, 8):
                for x in range(0, 8):
                    if self.grid[y][x].islower():
                        tempmoves = ''
                        if self.grid[y][x] == 'p':
                            tempmoves = self.bpawn(x, y)
                        elif self.grid[y][x] == 'b':
                            tempmoves = self.bishop(x, y)
                        elif self.grid[y][x] == 'n':
                            tempmoves = self.knight(x, y)
                        elif self.grid[y][x] == 'r':
                            tempmoves = self.rook(x, y)
                        elif self.grid[y][x] == 'q':
                            tempmoves = self.queen(x, y)
                        elif self.grid[y][x] == 'k':
                            tempmoves = self.king(x, y)
                        legalmoves += tempmoves

        legalmoves = legalmoves.split(',')
        legalmoves.pop()
        newlegalmoves = []
        beforegrid = deepcopy(self.grid)
        if self.wmove == 'w':
            for element in legalmoves:
                self.playraw(element)
                if self.check() != True:
                    newlegalmoves.append(element)
                self.grid = deepcopy(beforegrid)
        else:
            for element in legalmoves:
                self.playraw(element)
                if self.bcheck() != True:
                    newlegalmoves.append(element)
                self.grid = deepcopy(beforegrid)
        if newlegalmoves == []:
            if self.check() == True:
                newlegalmoves.append('Checkmate White wins')
            if self.bcheck() == True:
                newlegalmoves.append('Checkmate Black wins')
            else:
                newlegalmoves.append('Stalemate')
        self.grid = deepcopy(beforegrid)
        return newlegalmoves
