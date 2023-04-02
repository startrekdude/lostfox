from importlib import import_module

from .action import dispatch_action
from .battle import battle
from .game import game
from .room import Room
from .textsfx import slowprint

# the game is organized into multiple chapters
class Chapter:
	def __init__(self, name):
		self.name = name
		self.load_rooms()
	
	def load_rooms(self):
		self.rooms = {}
		
		# this probably deserves at least some explanation
		# basically, i'm abusing Python as a very powerful DSL
		module = import_module(".{}.rooms".format(self.name), package="logic").__dict__
		for key, val in module.items():
			if isinstance(val, Room):
				val.name = key
				self.rooms[key] = val
	
	def begin_chapter(self):
		slowprint(game.messages["{}.intro".format(self.name)])
	
	def end_chapter(self):
		slowprint(game.messages["{}.outro".format(self.name)])
	
	def enter_room(self, name):
		self.room = self.rooms[name]
		print(self.room.short_desc)
		
		# if there's an enemy, it attacks our player
		# (at least, the type of enemies represented by this battle system)
		if self.room.enemy:
			print(self.room.enemy.appear_message)
			print()
			battle(self.room.enemy)
			print()
			self.room.enemy = None
	
	def act(self, action):
		dispatch_action(action)