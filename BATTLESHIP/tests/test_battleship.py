from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/BATTLESHIP/battleship')
from battleship_game import *

def start():
    print('start')
    
def stop():
    print('stop')
    
@with_setup(start, stop)
def test_board():
    board = Board()
    assert_equal('$', board.board[0])
    assert_equal(121, len(board.board))
    nums = [' ' + str(i) for i in range(1,11)]
    for i in nums:
        assert i in nums
        
def test_player():
    playerI = Player(False)
    assert_equal(5, playerI.board.count(' # '))
    assert_equal(2, playerI.board.count(' ^ '))
    
def test_strikes():
    display = Board()
    playerI = Player(False)
    playerII = Player(False)
    game = Game()
    strikes = game.fleet('ship', ' # ', 20, 
                         display, playerI, 
                         playerII, False)
    game.make_move(strikes, playerII, 
                   display, False)
    assert 20 == playerII.board.count(' X ')
    
    strikes = game.fleet('ship', ' & ', 20,
                         display, playerI,
                         playerII, False)
    game.make_move(strikes, playerII,
                   display, False)
    assert 40 == playerII.board.count(' X ')
     
def test_game():
    display = Board()
    playerI = Player(False)
    playerII = Player(False)
    game = Game()
    while game.winner == None:
        game.computer_move(playerI, playerII, display)
        if game.winner == None:
            game.computer_move(playerII, playerI, display)
    assert ((' # ' not in playerI.board 
             and ' & ' not in playerI.board
             and ' ^ ' not in playerI.board
             and ' * ' not in playerI.board)
             or
             (' # ' not in playerII.board 
             and ' & ' not in playerII.board
             and ' ^ ' not in playerII.board
             and ' * ' not in playerII.board))





