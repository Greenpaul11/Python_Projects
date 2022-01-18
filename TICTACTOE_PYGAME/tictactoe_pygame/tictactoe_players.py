import random

class Player(object):
    def __init__(self, symbol, kind):
        self.symbol = symbol
        self.kind = kind
        self.score = 0
        
    # computer chooses square   
    def artificial_move(self, board, engine):
        if self.kind == 'easy':
            board_numbers = [i for i in range(0, 9)]
            select = random.choice(board_numbers)
            while board[select] != ' ':
                select = random.choice(board_numbers)
            return select
        elif self.kind == 'normal':
            tree = Tree(1, -1, board, 1, None, 0, 'normal')
            value, position = engine.minmax(tree, 1, False)
            return position
        
        elif self.kind == 'hard':
            tree = Tree(1, -1, board, 1, None, 0, 'hard')
            value, position = engine.minmax(tree, 1, False)
            return position

# this class is used by algorithm that select the best move
class Tree():
    def __init__(self, depth, player_N, board, num, position, value, level):
        self.depth = depth
        self.player_N = player_N
        self.value = value
        self.board = board
        self.children = []
        self.position = position
        self.num = num
        self.level = level
        self.make_children()
        
    def make_children(self):
        letter = 'X'
        opposite_l = 'O'
        if self.player_N == 1:
            symbol = letter
        else:
            symbol = opposite_l

        en_board = [count for count, value in enumerate(self.board) if value == ' ']
        if self.depth >= 0:
            for i in en_board:
                check_board = [i for i in self.board]
                check_board.pop(i)
                check_board.insert(i, symbol)
                if self.num == 1:
                    self.position = i
                if self.depth == 0:
                    self.value = self.value + self.true_value(i, check_board, letter, opposite_l)
                else:
                    self.value = self.true_value(i, check_board, letter, opposite_l)
                
                self.children.append(
                        Tree(self.depth - 1, 
                        -self.player_N, 
                        check_board,
                        0,
                        self.position,
                        self.value,
                        self.level
                        ))
            
    def true_value(self, answer, board, letter, op_letter):
        val_X = 0
        val_O = 0
        rowI = [i for i in board[0:3]]
        rowII = [i for i in board[3:6]]
        rowIII = [i for i in board[6:]]
        columnI = [i for i in board[0:9:3]]
        columnII = [i for i in board[1:9:3]]
        columnIII = [i for i in board[2:9:3]]
        diagonalI = [i for i in board[0:9:4]]
        diagonalII = [i for i in board[2:7:2]]
        squares = [rowI, rowII, rowIII, columnI, columnII, columnIII, diagonalI, diagonalII]
        if self.level == 'normal':
            pointI = 600
            pointII = 400
            pointIII = 100
        elif self.level == 'hard':
            pointI = 800
            pointII = 400
            pointIII = 100

        for each in squares:
            if all([item == letter for item in each]):
                val_X += pointI
            if each.count(letter) == 2 and each.count(' ') == 1:
                val_X += pointII
            if each.count(letter) == 1 and each.count(' ') == 2:
                val_X += pointIII
                
            if all([item == op_letter for item in each]):
                val_O -= pointI
            if each.count(op_letter) == 2 and each.count(' ') == 1:
                val_O -= pointII
            if each.count(op_letter) == 1 and each.count(' ') == 2:
                val_O -= pointIII
      
        return val_X + val_O        
        
