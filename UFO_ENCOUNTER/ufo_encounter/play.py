import sys
sys.path.append('/home/oldest/my_projects/TICTACTOE/tictactoe')
sys.path.append('/home/oldest/my_projects/CHECKERS/checkers')
from encounter_script import *
from play_checkers import *
from play_tictactoe import *
import random
import time



forestI = ('''
It is beautiful night.
The moon is on its full.
The stars are soo bright.
When you\'re looking at the stars 
you bring back memorys from childhood.
When as little boy looking first time at the stars,
strange feeling was coming to you that
you know this stars and they know you...
Time goes by year after year.
But when you\'re looking at the sky 
you feel that something
is not changed at all.
You\'re looking at the sky and
you feel it deep in the sky and deep in yourself.
''')

forestII = '''
You walking alone this wood path.
On the right side are trees and shrubs.
On the left side clearing.
You look again in the sky and you see something...
Something different...This..This..can not beee....
Bright light is coming from the sky.
You don\'t know what to do..
But you have to do something..
You\'re starting shaking..
Quickly there is no time..
'''

forestIII = '''
Strange warm is enclosing your body.
Unkonwn force is draging you up.
You can move your body but you can do nothig,
when you are pulled up in the air
closer and closer to the light.
Then you\'re loosing your consciousness.
'''

list_escape = ['''
You start running.
Beam of light is casting at your way.
You\'re running even faster,
but then you feel that something is slowing you down.
''', '''
You\'re climbing on the tree.
The branches crumble under your foots,
but your grip is firm and solid.
Fear overpower you and doesn\'t allow you to loose the grip.
Then all hope is lost.
The beam of light is poiting at you.
''', ''' 
You\'re lowering your head behind shrubs.
You\'re wandering what will happen.
Looking nervously at the strange light from the sky,
you\'re starting feel that your heart is going to stop,
when beam of light is pointing at your direction.
''']

dark_room = '''
Strange sound is weaking you up.
You\'re lying on the cold floor 
that appears to be some kind of metal.
In surrounding darknes you see three flashing lights.
You\'re getting up and you walk to these lights.
When you are close to it 
you see in front of you three flashing buttons.
'''

yellow_and_blue = ['''
You hear scraping sound...
Close to you in the wall appears opening.
From opening slids out a bright display.''', 
''' 
From above is caming strange noise.
On the ceiling appears strange patterns and
then from ceiling pulls out some kind of cocpit.
It is lowering to the point of your chest.
Then the display is turning on.''']

sleep_gas = '''
You hear piping noise.
Something is coming from the walls.
It\'s some kind of gas.
You start feeling sleepy.
Then you\'re falling to your knees 
and then slowly lowering on your hands to the floor 
as dream overpower you.
'''

encounter = '''
You pass through whole in the ceiling.
Everything is blue...
You are frozen when you hear footsteps
coming in your direction.
Then you catch a glimps of three silhouette.
Now you berly can breath as
three beeings appearing to your eyes.
They don\'t talk but somehow 
you can understand what they mean.
They sending you information through the mind.
They make surveys of human evolution level.
One creature is pointing it\'s finger
toward white long table.
Oh noo.... 
They want look into my body...
I have to do something...
'''

actions = ['''
You\'re looking around and you see black hole
on the other side of room.
There is only one problem to get to it.
You have to go through them...
You\'re looking into their eyes
And you know immediately
that they don\'t allow you for this.''', 
'''
You\'re looking at them and 
you\'re twisting your head with disagreement.
GET ON THIS TABLE
This was like switch in your mind.
This is their will.''', 
'''
You\'re walking toward white table,
You\'re getting on aline unit...
''']

scan = '''
You feel cold as creatures coming closer to the unit.
On of them click something on the near metal column.
From the ceiling pulls out strange object.
From your belly fear is rising up to your throat.
You\'re shaking when two needels insert in your chest.
You don\'t fell pain.
Instead your attention is going to the center of the room.
Holographic patterns appears there.
You don't know what it is.
Then time stops.
The light arround you fades.
You only hear piping noise in your head...
'''

search_for = '''
You open your eyes.
You feel strange warm in your body.
You\'re looking around.
There is nobody in the room.
You get up from the unit.
You see the column with unknown patterns on it.
These patterns appears to be some kind of switches.
'''  

symbols = ['''
From the recess in the wall comes scraping noise.
Metal cover is sliding to the side.
You see black hole there.''', 
'''
Nothing happen.''', 
'''
Nothing happen.''']

hole = ['''
You wait here but nothing happens.''', 
'''
You\'ve got to the hole.
The metal shutter slide back from the wall.
It\'s dark.
You wait some time.
Then you start feeling that 
floor beneath your feet start dissolve.
You drift in the air.
Then unknown force is dragging you down.
You fly down...
''', '''
You\'re shouting, but there is no reaction to it.''']

dream = '''
You open your eyes.
What you see now is a white ceiling of your bedroom.
What happend to me?
You asking yourself.
Was it dream or true event?
...
'''



game = Engine()
game.print_chapter('I')
time.sleep(2)
game.present_moment(forestI)
time.sleep(1)
input('Press ENTER to go further')
game.present_moment(forestII)
time.sleep(1)
input('Press ENTER to go further')
game.choose_posibility('run away along clearing path', 
						 'climb on the nearest tree', 
						 'hide behind shrubs', 
						 list_escape)
time.sleep(1)
input('Press ENTER to go further')
game.present_moment(forestIII)
time.sleep(1)
input('Press ENTER to go further')

game.print_chapter('II')
time.sleep(2)
game.present_moment(dark_room)
time.sleep(1)
input('Press ENTER to go further')
pressed_buttons = [sleep_gas, random.choice(yellow_and_blue), 
				   random.choice(yellow_and_blue)]
answers = game.choose_posibility('press yellow button', 
									'press blue button', 
									'press green button', 
									pressed_buttons) 
time.sleep(2)   
while 'w' in answers:
    print('''You open your eyes and you know this place.
Something happen here...
Hmmm....it was something about these buttons...''')
    time.sleep(2)
    answers = game.choose_posibility('press yellow button', 
    									'press blue button', 
    									'press green button', 
    									pressed_buttons) 
    time.sleep(2)
print('''
Something appearing on the screen.

---WIN THIS GAME TO GET TO THE UPPER LEVEL---
''')
time.sleep(2)
if 'q' in answers:
    print('It can\'t.... be... it\'s looking like board for tictactoe...')
    play_tictactoe()
if 'e' in answers:
	play_checkers()
print('\n---YOU WON---\n---YOU HAVE ACCESS TO UPPER LEVEL---\n') 
time.sleep(2)
print('The screen returned to it\'s blackness.')
time.sleep(2)
print('''
The rumble sound is coming from above.
From ceiling the metal staircase are unfolding to the center of the hall.
''')
time.sleep(2)
input('Press ENTER to go up the stairs')

game.print_chapter('III')
time.sleep(2)
game.present_moment(encounter)
time.sleep(1)
input('Press ENTER to go further')
answer = game.choose_posibility('find passage from room', 
									'make disagreement gesture',
									'walk to the table',
									actions)  
while answer != 'e':
	time.sleep(1)
	answer = game.choose_posibility('find passage from room', 
									'make disagreement gesture',
									'walk to the table',
									actions)  
time.sleep(1)
input('Press ENTER to go further')
game.present_moment(scan)
time.sleep(1)
input('Press ENTER to go further')

game.print_chapter('IV')
time.sleep(2)
game.present_moment(search_for)
time.sleep(1)
input('Press ENTER to go further')
answer = game.choose_posibility('press symbol &',
								   'press symbol *',
								   'press symbol #',
								   symbols)
while answer != 'w':
	time.sleep(1)
	answer = game.choose_posibility('press symbol &',
								   'press symbol *',
								   'press symbol #',
								   symbols)
answer = game.choose_posibility('wait here',
								   'go into hole',
								   'shout',
								   hole)	
while answer != 'q':
	time.sleep(1)
	answer = game.choose_posibility('wait here',
								   'go into hole',
								   'shout',
								   hole)	
input('Press ENTER to go further')

game.print_chapter('V')
time.sleep(2)
game.present_moment(dream)							   





    

