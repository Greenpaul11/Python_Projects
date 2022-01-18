from nose.tools import *
import sys
sys.path.append('/home/oldest/my_projects/UFO_ENCOUNTER/ufo_encounter')
from ufo_encounter_game import *

def start():
	print('start')
	
def stop():
	print('stop')
	
@with_setup(start, stop)
def test_engine():
	engine = Engine()
	
