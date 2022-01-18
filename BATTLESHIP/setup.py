from setuptools import setup

setup(
	name = 'battleship',
	version = '1.0',
	description = 'this package contains simple game battleship',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['battleship_game'],
	entry_points = {
		'console_scripts': ['play_battleship = battleship.battleship_game: play_battleship']
	}
)
