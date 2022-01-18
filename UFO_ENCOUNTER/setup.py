from setuptools import setup

setup(
	name = 'ufo_encounter',
	version = '1.0',
	description = 'this package contains adwenture game',
	author = 'Pawel Kukuczka',
	author_email = 'Paulgreen777@protonmail.com'
	packages = ['ufo_encounter'],
	entry_points = {
		'console_scripts': ['play_ufo_encounter = ufo_encounter.ufo_encounter: play']
	}
)
