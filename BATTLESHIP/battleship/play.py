import random
import time
import math
# create a class Board that have some common attributes like board
# or board_numbers
class Board():
    def __init__(self):
        # this list allows user to choose position on the board
        # using index position of each choosen place we can
        # make correct changes for board(list items) 
        self.board_numbers = self.make_board_numbers() 
        # create board(list) 
        self.board = self.make_board()
    
    def make_board(self):
        num = 1
        letters = [i for i in '$ABCDEFGHIJ']
        for j in range(10):
            letters.append(' ' + str(num))
            for i in range(10):
                letters.append('   ')
            num = num + 1
        return letters
        
    def make_board_numbers(self):
        num = 1
        letters =[i for i in '$ABCDEFGHIJ']
        for j in range(10):
            letters.append(' ' + str(num))
            for i in 'ABCDEFGHIJ':
                q = str(num) + i
                if len(q) == 4:
                    q = str(num) + i
                letters.append(q)
            num = num + 1
        return letters

    # this function displays player board   
    def print_board(self):  
        for row in [self.board[i*11:(i+1)*11] for i in range(1)]:
            print('|  ' + '|  '.join(row) + '|')
        for row in [self.board[i*11:(i+1)*11] for i in range(1,10)]:
            print('|' + ''.join(['---|' for i in range(11)]))
            print('| ' + '|'.join(row) + '|')
        for row in [self.board[i*11:(i+1)*11] for i in range(10,11)]:
            print('|' + ''.join(['---|' for i in range(11)]))
            print('|' + '|'.join(row) + '|')

    # this function displays board that has places with their identifiers
    def print_board_numbers(self):
        for row in [self.board_numbers[i*11:(i+1)*11] for i in range(1)]:
            print('|  ' + '|  '.join(row) + '|')
        for row in [self.board_numbers[i*11:(i+1)*11] for i in range(1,10)]:
            print('|' + ''.join(['---|' for i in range(11)]))
            print('| ' + '| '.join(row) + '|')
        for row in [self.board_numbers[i*11:(i+1)*11] for i in range(10,11)]:
            print('|' + ''.join(['---|' for i in range(11)]))
            print('|' + '|'.join(row) + '|')

# create fleet for human player
class Player(Board):
    def __init__(self, player):
        super().__init__()
        # this attribute allows to identify kind of player
        self.player = player
        self.battleship = self.make_ship(5, 'BATTLESHIP', '#')
        self.cruiser = self.make_ship(4, 'CRUISER','&')
        self.destroyerI = self.make_ship(3, 'DESTROYER', '*')
        self.sub = self.make_ship(2, 'SUB', '^')

    # this function allows to place diffrent kind of ships on the board
    # quantity argument define how many places is needed for kind of ship
    # each kind of ship has it's own identifier on board that is specified symbol
    # each ship has to be joined by places that create vertical or horizontal line  
    def make_ship(
            self, quantity, kind_of_ship, symbol, 
            horizontal_pattern = False, 
            vertical_pattern = False):
        # keep track of each loop
        num = 0
        # store the choosen place
        choice = []
        for i in range(quantity):
            num += 1
            # set add_ship to False, when the ship has all needed places the variable
            # is set to True value
            add_ship = False 
            while add_ship == False:

                if self.player == False:
                    answer = random.choice(self.board_numbers)

                elif self.player == True:
                    print(f'Choose the position index for your {kind_of_ship}')
                    print(kind_of_ship, f'{i + 1}/', quantity)
                    self.print_board()
                    answer = input('> ').upper()
                
                if answer in self.board_numbers:    
                    index_p = self.board_numbers.index(answer)
                    
                    if self.board[index_p] == '   ':
                        
                        if (index_p > 10 and 
                                index_p not in [i * 11 for i in range(11)]):
                            add_ship = True
                            # now we can use loop checker(num)
                            # to implement the principles
                            # for correct placing our ship
                            if num == 2:
                                if (index_p == choice[0] + 1 
                                        or index_p == choice[0] - 1):
                                    horizontal_pattern = True
                                    add_ship = True
                                elif (index_p == choice[0] + 11 
                                        or index_p == choice[0] - 11):
                                    vertical_pattern = True
                                    add_ship = True
                                else:
                                    add_ship = False
                            
                            elif horizontal_pattern == True: 
                                if (index_p in [i + 1 for i in choice] 
                                        or index_p in [i - 1 for i in choice]):
                                    add_ship = True
                                else:
                                    add_ship = False
                            
                            elif vertical_pattern == True: 
                                if (index_p in[i + 11 for i in choice] 
                                        or index_p in [i - 11 for i in choice]):
                                    add_ship = True
                                else:
                                    add_ship = False
                
                elif self.player == True and answer not in self.board_numbers:
                    print('Type correct index place!')
                
            choice.append(index_p)              
            self.board.pop(index_p)
            self.board.insert(index_p, f' {symbol} ')

# define the rules for ech player
# define the step that can take ech player
class Game():
    def __init__(self):
        # while winner is None the game will run
        self.winner = None
        
    def computer_move(self, artificial, human, display):
        print('Your opponent is striking at your fleet')
        # your fleet
        ships = ['BATTLESHIP', 'CRUISER', 'DESTROYER', 'SUBMARINE']
        for name in ships:
            if name == 'BATTLESHIP':
                # symbol allows to identify the kind of ship and the amount
                # of symbol tells about the remaining parts of the ship
                symbol = ' # '
                # missile define how many time the kind of ship can strike 
                missile = 3
                
            elif name == 'CRUISER':
                symbol = ' & '
                missile = 2
                
            elif name == 'DESTROYER':
                symbol = ' * '
                missile = 2

            elif name == 'SUBMARINE':
                symbol = ' ^ '
                missile = 1
            # to make a strike computer needs to choose places
            strikes = self.fleet(name, symbol, missile,
                                    display, artificial, human, 
                                    player = False)

            self.make_move(strikes, human, display, player = False)

    def human_move(self,human, artificial, display):
        print('Aim at your opponent')
        # your fleet
        ships = ['BATTLESHIP', 'CRUISER', 'DESTROYER', 'SUBMARINE']
        for ship in ships:
            if ship == 'BATTLESHIP':
                # symbol allows to identify the kind of ship and the amount
                # of symbol tells about the remaining parts of the ship
                symbol = ' # '
                # missile define how many time the kind of ship can strike 
                missile = 3
                
            elif ship == 'CRUISER':
                symbol = ' & '
                missile = 2
                
            elif ship == 'DESTROYER':
                symbol = ' * '
                missile = 2

            elif ship == 'SUBMARINE':
                symbol = ' ^ '
                missile = 1

            strikes = self.fleet(ship, symbol, missile,
                                    display, human, artificial, 
                                    player = True)

            self.make_move(strikes, artificial, display, player = True)
       
    def make_move(self, strikes, enemy, display, player):
        # get index position from the items and check them in the enemy board
        # assign ' X ' to field in enemy board that index positions are equeal 
        # to those in strikes
        if player == False:
            state = 'Your'
            face = ':('
            stateI = 'Enemy'
        
        elif player == True:
            state = 'Enemy'
            face = ':)'
            stateI = 'Your'
        
        for i in strikes:
            time.sleep(1)
            x = enemy.board_numbers.index(i)
            q = enemy.board[x]
           
            if ' # ' in q:
                print(f'{state} BATTLESHIP has been hit {face}')
                if player == True:
                    display.board.pop(x)
                    display.board.insert(x, ' B ')

            elif ' ^ ' in q:
                print(f'{state} SUBMARINE has been hit {face}')
                if player == True:
                    display.board.pop(x)
                    display.board.insert(x, ' S ')

            elif ' & ' in q:
                print(f'{state} CRUISER has been hit {face}')
                if player == True:
                    display.board.pop(x)
                    display.board.insert(x, ' C ')

            elif ' * ' in q:
                print(f'{state} DESTROYER has been hit {face}')
                if player == True:
                    display.board.pop(x)
                    display.board.insert(x, ' D ')

            else:
                print(f'{stateI} missile missed its target')
                if player == True:
                    display.board.pop(x)
                    display.board.insert(x, ' X ') 
            
            enemy.board.pop(x)
            enemy.board.insert(x, ' X ')
        # if in enemy board there is no more symbol of ships
        # set variable winner to true, this should stop
        # the game and print messeage with winning player 
        if (' # ' not in enemy.board
                and ' ^ ' not in enemy.board 
                and ' & ' not in enemy.board
                and ' * ' not in enemy.board):

            if player == False:
                print('ARTIFICIAL PLAYER IS A WINNER')

            elif player == True:
                print('HUMAN PLAYER IS A WINNER')

            self.winner = True
          
        
    # choose places in which player want to strike
    def fleet(
            self, ship, symbol, missile,
            display, board, 
            enemy, player):
        strikes = []

        if player == True:

            if board.board.count(symbol) > 2:
                print(f'{ship} ready to strike')
                for i in range(missile):
                    display.print_board()
                    aim = input('> ').upper()
                    while (aim not in board.board_numbers 
                            or board.board_numbers.index(aim) < 10 
                            or board.board_numbers.index(aim) in [i * 11 for i in range(11)] 
                            or enemy.board[board.board_numbers.index(aim)] == ' X ' 
                            or aim in strikes):
                        print('You\'ve not locate your target')
                        aim = input('> ').upper()
                    strikes.append(aim)
                    display.board.pop(board.board_numbers.index(aim))
                    display.board.insert(board.board_numbers.index(aim), ' X ')   

            # if ship lost some parts it gives less strikes
            elif board.board.count(symbol) <= 2 and board.board.count(symbol) > 0:
                display.print_board()

                if ship != 'SUBMARINE':
                    print(f'Your {ship} is damaged')
                    aim = input('> ').upper()

                elif ship == 'SUBMARINE' and board.board.count(symbol) == 2:
                    print(f'{ship} is ready to strike')
                    aim = input('> ').upper()

                elif ship == 'SUBMARINE' and board.board.count(symbol) == 1:
                    print(f'Your {ship} is damaged')
                    aim = input('> ').upper()

                while (aim not in board.board_numbers or board.board_numbers.index(aim) < 10 
                        or board.board_numbers.index(aim) in [i * 11 for i in range(11)] 
                        or enemy.board[board.board_numbers.index(aim)] == ' X ' 
                        or aim in strikes):
                    print('You\'ve not locate your target')
                    aim = input('> ').upper()
                strikes.append(aim)
                display.board.pop(board.board_numbers.index(aim))
                display.board.insert(board.board_numbers.index(aim), ' X ')
                      
        # if player has False value the player is a computer        
        elif player == False:
            if board.board.count(symbol) > 2:
                for i in range(missile):
                    aim = random.choice(board.board_numbers)
                    while (board.board_numbers.index(aim) < 10 
                            or board.board_numbers.index(aim) in [i * 11 for i in range(11)] 
                            or enemy.board[board.board_numbers.index(aim)] == ' X ' 
                            or aim in strikes):
                        aim = random.choice(board.board_numbers)
                    strikes.append(aim)
                        
            elif board.board.count(symbol) < 2 and board.board.count(symbol) > 0:
                aim = random.choice(board.board_numbers)
                while (board.board_numbers.index(aim) < 10 
                        or board.board_numbers.index(aim) in [i * 11 for i in range(11)] 
                        or enemy.board[board.board_numbers.index(aim)] == ' X ' 
                        or aim in strikes):
                    aim = random.choice(board.board_numbers)
                strikes.append(aim)
        # returns the list with choosen fields
        return strikes
        
def make_game(human, artificial, game, display_board):
    print('Your opponent is ready')
    while game.winner == None:
        if game.winner == None: 
            game.computer_move(artificial, human, display_board)
            time.sleep(4)
        human.print_board()
        if game.winner == None:
            time.sleep(4)
            game.human_move(human, artificial, display_board)

def play_battleship():    
	board = Board()
	human = Player(True)
	alien = Player(False)
	game = Game()
	make_game(human, alien, game, board)

play_battleship()




