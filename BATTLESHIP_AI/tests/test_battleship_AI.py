from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/BATTLESHIP_AI/battleship_ai')
from battleshipAI_game import *

def start():
	print('start')
	
def stop():
	print('stop')
	
@with_setup(start, stop)
def test_board():
	alien = Player(False)
	assert_equal(5, alien.board.count(' # '))
	assert_equal(2, alien.board.count(' ^ '))
	assert '$' == alien.board[0]
	
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

