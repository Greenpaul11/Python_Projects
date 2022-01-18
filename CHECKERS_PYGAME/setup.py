from setuptools import setup

setup(
	name = 'checkers_pygame',
	version = '1.0',
	description = 'this package contains checkers game',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com',
	packages = ['checkers'],
	entry_points = {
		'console_scripts': ['play_checkers = checkers.checkers_game: play_checkers']
	}
	
	
