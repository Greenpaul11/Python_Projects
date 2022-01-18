from setuptools import setup

setup(
	name = 'checkers_ai',
	version = '1.0',
	description = 'this package contains checkers game with smart AI player',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['checkers_ai'],
	entry_points = {
		'console_scripts': ['play_checkers_ai = checkers_ai.checkers_gameAI: play_checkers_ai']
	}
)
