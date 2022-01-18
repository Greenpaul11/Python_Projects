from setuptools import setup

setup(
	name = 'tictactoe',
	version = '1.0',
	description = 'this package contains simple tictactoe game',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['tictactoe'],
	entry_points = {
		'console_scripts': ['play_tictactoe = tictactoe.tictactoe_game: play_tictactoe']
	}
)
