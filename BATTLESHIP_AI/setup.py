from setuptools import setup

setup(
	name = 'battleship_ai',
	version = '1.0',
	description = 'this package contains simple game battleship with smart AI player',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['battleship_ai'],
	entry_points = {
		'console_scripts': ['play_battleship_ai = battleship_ai.battleship_ai: play_battleship_ai']
	}
)
