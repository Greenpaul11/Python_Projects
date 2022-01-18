from nose.tools import setup

setup(
	name = 'tictactoe_pygame',
	version = '1.0',
	description = 'this package contains tictactoe game',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['tictactoe_pygame'],
	entry_points = {
		'console scripts': ['play_tictactoe_pygame = tictactoe_pygame.tictactoe_pygame: play_tictactoe_pygame']
	}
	)
	
