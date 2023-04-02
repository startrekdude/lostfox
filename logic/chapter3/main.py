from random import choice, randrange, shuffle

from ..chapter import Chapter
from ..converse import run_conversation
from ..game import game
from ..objects import GameObjects
from ..room import InWorldDescription

def randomly_ordered(it):
	"""
	Returns the elements in an iterable in a random order
	Consumes the iterable
	"""
	a = list(it)
	shuffle(a)
	yield from a

class Town(Chapter):
	def __init__(self):
		self.rocco_room = "town_road4"
		self.hammer_visited = False
		self.shed_conversation_had = False
		super().__init__("chapter3")

	def enter_room(self, room):
		if room == "town_chapter_change":
			print("This will end the current chapter, and you will not be able to return.")
			s = input("Are you sure you would like to continue [yes/no]? ").lower().strip()
			print()
			if s == "yes":
				game.player.objectives[6] = "Make your way through the two-leg town."
				game.do_end_game()
			return
		
		if room == "town_park":
			game.player.objectives[5] = "Get past the jackhammer."
		
		if room == "town_hammer":
			self.hammer_visited = True

		if self.hammer_visited and room == "town_shed" and not self.shed_conversation_had:
			run_conversation("shed")
			self.shed_conversation_had = True
			self.kill_jackhammer()

		if room != self.rocco_room: self.move_rocco()
		super().enter_room(room)

		if not randrange(5):
			print("You thought you saw something moving in the shadows behind you.")
			print("Probably just a trick of the light...")
			print()

		self.move_roaming()

	def kill_jackhammer(self):
		room = self.rooms["town_hammer"]
		room.remove_object(GameObjects.JACKHAMMER)
		room.objects.append(InWorldDescription(GameObjects.DEAD_JACKHAMMER, "You see an inactive jackhammer."))
		room.edges["east"] = room.edges["left"] = "town_park"

	def move_rocco(self):
		for room in self.rooms.values():
			desc = next((desc for desc in room.objects if desc.obj is GameObjects.ROCCO), None)
			if desc:
				conv = next(conv for conv in room.conversations if conv.obj is GameObjects.ROCCO)

				room.objects.remove(desc)
				room.conversations.remove(conv)

				new_room = choice([key for key in room.edges.values() if key in self.rooms])
				self.rooms[new_room].objects.append(desc)
				self.rooms[new_room].conversations.append(conv)

				self.rocco_room = new_room
				break

	def move_roaming(self):
		moved_enemies = []

		# move the two raccoons, assuming any are alive
		for room in self.rooms.values():
			if room.enemy and room.enemy not in moved_enemies:
				for key in randomly_ordered(room.edges.values()):
					if key in self.rooms and not self.rooms[key].enemy:
						moved_enemies.append(room.enemy)
						self.rooms[key].enemy = room.enemy
						room.enemy = None
						break

	def begin_chapter(self):
		super().begin_chapter()
		self.enter_room("town_road3")