class Board(object):
    def __init__(self):
        # create board for checkers game
        # board will be indexed by eight letters in horizontal length
        # and by by eight numbers in vertical length
        self.board = self.make_board()
        self.board_numbers = self.make_board_numbers()
     
    def make_board(self):
        # create the list in which each player's move is stored
        num = 7
        letters = list('$ABCDEFGH$')
        board = []
        for i in range(10):
            if i == 0:
                for letter in letters:
                    board.append(' ' + letter + ' ')
            elif i == 9:
                for letter in letters:
                    board.append(' ' + letter + ' ')
            else:
                board.append(' ' + (str(i + num)) + ' ')
                for empty in range(8):
                    board.append('   ')
                board.append(' ' + (str(i + num)) + ' ')
                num -= 2
        return board
        
               
    def print_board(self, board):
        # this function will display board in terminal  
        num = 0
        for row in [board[i * 10: (i + 1) * 10] for i in range(10)]:
            print('|' + '|'.join(row) + '|') 
            if num != 9:
                print('|' + ''.join(['---|' for i in range(10)]))
                num += 1
    
    def make_board_numbers(self):
        # this is showing the way in which
        # player will choose the square    
        num = 7
        letters = list('$ABCDEFGH$')
        board = []
        for i in range(10):
            if i == 0:
                for letter in letters:
                    board.append(' ' + letter + ' ')
            elif i == 9:
                for letter in letters:
                    board.append(' ' + letter + ' ')
            else:
                board.append(' ' + (str(i + num)) + ' ')
                for empty in range(8):
                    board.append(str(i + num) + letters[empty + 1])
                board.append(' ' + (str(i + num)) + ' ')
                num -= 2
        return board
        
   
class Player(object):
    def __init__(self, symbol, kind, name, types):
        # each player has a symbol that will be displayed on the board
        self.symbol = symbol
        # each player has attribute which is defined by True or False
        # if player is True the player is a human player
        self.kind = kind
        # this attribute define places in the start game position 
        self.position = self.make_checkers()
        self.name = name
        self.type = types 
        
    def make_checkers(self):
        if self.kind == False:
            position = [
                    12, 14, 16, 18,
                    21, 23, 25, 27,
                    32, 34, 36, 38
                    ]
        elif self.kind == True:
            position = [
                    61,63, 65, 67,
                    72, 74, 76, 78,
                    81, 83, 85, 87   
                    ]
        return position
             
    def set_player(self, board):
        # this function is setting player checkers in places defined
        # in self.position     
        for i in self.position:
            board.pop(i)
            board.insert(i, self.symbol)
                
            
        
    
                    






                
            
        
