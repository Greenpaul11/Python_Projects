from setuptools import setup

setup(
	name = 'tictactoe_ai',
	version = '1.0',
	description = 'this package contains simple tictactoe game with smart AI player',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com'
	packages = ['tictactoe_ai'],
	entry_points = {
		'console_scripts': ['play_tictactoe_ai = tictactoe_ai.tictactoe_ai: play_tictactoe_ai']
	}
)
