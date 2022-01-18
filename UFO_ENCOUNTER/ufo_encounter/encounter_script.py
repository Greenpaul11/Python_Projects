import random

		
class Engine():
	
	def print_chapter(self, chapter):
		print(f'\n\n\t\t\tCHAPTER {chapter}')
		
	def present_moment(self,present_scene):
		print(present_scene)
	
	def choose_posibility(self, posibilityI, posibilityII, posibilityIII, decisions):
		print('')
		print('Choose what to do: ')
		print(f'Press \'W\' to {posibilityI}')
		print(f'Press \'Q\' to {posibilityII}')
		print(f'Press \'E\' to {posibilityIII}')
		
		answer = input('> ').lower()
		posibility = False
		while posibility == False:
			if 'w' in answer:
				print(decisions[0])
				posibility = True
			elif 'q' in answer:
				print(decisions[1])
				posibility = True
			elif 'e' in answer:
				print(decisions[2])
				posibility = True
			else:
				print('Type the right symbol')
				print('')
				answer = input('> ').lower()
		
		return answer
	
	
		
		
		
		

class Scene():
	def __init__(self, chapter):
		self.chapter = chapter
		pass
		
	def print_chapter(self):
		print(f'\n\t\t\tCHAPTER {self.chapter}\n')
	
	def present_moment(self,present_scene):
		print(present_scene)
	
		
		
class Forest(Scene):
	def __init__(self, chapter, present_scene):
		self.present_scene = present_scene
		super().__init__(chapter)
		pass
		
					



		

		
		
		
		
		


		




	
		

		
		
		
		



	


