from collections import namedtuple
from enum import Enum

from .game import game
from .textsfx import slowprint

def run_conversation(name):
	from .formats import load_conversation
	load_conversation(name).execute()

# a conversation is a sequence of commands
# go find a .seq file as an example

class CommandType(Enum):
	PRINT = 0
	JUMP = 1
	CHOICE = 2
	FLAG = 3
	BRANCH = 4
	NOP = 5
	FREEFORM_ENTRY = 6
	GIVE = 7
	ROOM = 8
	HAS = 9
	TAKE = 10

Choice = namedtuple("Choice", ("msg", "target"))

# could have subclassed, but ¯\_(ツ)_/¯
# when each piece of logic is so simple i prefer one method with a switch
# statement to polymorphism
class Command:
	def __init__(self, type, msg=None, target=None, choices=None, flag=None, expected=None, item=None, room=None):
		self.type = type
		self.msg = msg
		self.target = target
		self.choices = choices
		self.flag = flag
		self.expected = expected
		self.item = item
		self.room = room

class Sequence:
	def __init__(self, commands, order):
		self.commands = commands
		self.order = order
		self.iptr = order[0]
	
	def print_choice_menu(self, choices):
		print("What would you like to do? ")
		for i, (msg, _) in enumerate(choices):
			print("  {}. {}".format(i + 1, msg))
	
	def select_choice(self, choices):
		while True:
			self.print_choice_menu(choices)
			s = input("? ")
			if not s.isdigit(): continue
			idx = int(s) - 1
			if idx < 0 or idx >= len(choices): continue
			return choices[idx].target
	
	def execute(self):
		while True:
			command = self.commands[self.iptr]
			if command.type == CommandType.JUMP:
				self.iptr = command.target
				continue # jump
			elif command.type == CommandType.BRANCH:
				if game.flags[command.flag]:
					self.iptr = command.target
					continue # jump
			elif command.type == CommandType.PRINT:
				slowprint(command.msg, end="")
			elif command.type == CommandType.FLAG:
				game.flags[command.flag] = True
			elif command.type == CommandType.GIVE:
				game.player.give(command.item)
			elif command.type == CommandType.HAS:
				if command.item in game.player.inventory:
					self.iptr = command.target
					continue # jump
			elif command.type == CommandType.TAKE:
				game.player.inventory.remove(command.item)
			elif command.type == CommandType.ROOM:
				game.chapter.enter_room(command.room)
			elif command.type == CommandType.FREEFORM_ENTRY:
				s = input("What would you like to say? ").lower().strip()
				if s == command.expected:
					self.iptr = command.target
					continue # jump
			elif command.type == CommandType.CHOICE:
				print()
				self.iptr = self.select_choice(command.choices)
				continue # jump
			
			# move to the next item if no jump happened
			idx = self.order.index(self.iptr)
			if idx + 1 >= len(self.order): break
			self.iptr = self.order[idx + 1]