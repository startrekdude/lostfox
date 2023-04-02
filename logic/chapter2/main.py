from random import choice

from ..chapter import Chapter
from ..converse import run_conversation
from ..game import game
from ..objects import GameObjects
from ..room import InWorldDescription
from ..textsfx import slowprint

class TwoLeg(Chapter):
	def __init__(self):
		super().__init__("chapter2")
		self.lights = [choice((True, False)) for _ in range(7)]
		self.lights_complete = False
	
	def format_bool_as_on_off(self, b):
		return "on" if b else "off"
	
	def flick(self, idx):
		print("You flick switch #{}.".format(idx))
		
		if self.lights_complete:
			print("Nothing happens.\n")
			return
		
		i = idx - 1
		self.lights[i] ^= True
		if i > 0:
			self.lights[i - 1] ^= True
		if i < 6:
			self.lights[i + 1] ^= True
		
		print(self.lights_description)
		if all(self.lights):
			print("The safe opens.")
			print("Inside is a small white elephant, carved from alabaster.")
			self.room.remove_object(GameObjects.SAFE)
			self.room.objects.append(InWorldDescription(GameObjects.REWARD2, "Inside the safe is a small white elephant."))
		
		print()
	
	@property
	def lights_description(self):
		first_part = ", ".join(self.format_bool_as_on_off(b) for b in self.lights[:-1])
		return "From left to right, the lights are {}, and {}.".format(first_part, self.format_bool_as_on_off(self.lights[-1]))
	
	def enter_room(self, room):
		if room == "home_chapter_change":
			print("This will end the current chapter, and you will not be able to return.")
			s = input("Are you sure you would like to continue [yes/no]? ").lower().strip()
			print()
			if s == "yes":
				game.change_chapter(3)
				game.player.objectives[4] = "Escape the two-leg hunter."
			return
		
		if room == "home_basement":
			game.player.objectives[3] = "Escape the cage."
		
		if room == "home_outside":
			slowprint(game.messages["two_leg_fight"])
			run_conversation("post_battle")
			print()
		
		super().enter_room(room)
	
	def begin_chapter(self):
		super().begin_chapter()
		self.enter_room("home_cage")