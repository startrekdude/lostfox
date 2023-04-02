from ..chapter import Chapter
from ..game import game
from ..objects import GameObjects
from ..room import InWorldDescription
from ..textsfx import slowprint

MOOSE_DESC = InWorldDescription(GameObjects.MOOSE, "Charging at you fast is an enraged moose!")

class Forest(Chapter):
	MOOSE_THRESHOLD = 19
	
	def __init__(self):
		super().__init__("chapter1")
		self.turn_counter = 0
		self.moose_room = None
		self.moose_dead = False
	
	def jump_maybe_win(self):
		if self.moose_room == self.room:
			self.moose_dead = True
			self.room.remove_object(GameObjects.MOOSE)
			self.room.remove_object(GameObjects.ELECTRIC_FENCE)
			self.room.edges["forward"] = "forest_chapter_change"
			self.moose_room = None
			slowprint(game.messages["moose_death"])
			game.player.objectives[1] = "Defeat the rampaging bull moose."
	
	def enter_room(self, room):
		if room == "forest_chapter_change":
			print("This will end the current chapter, and you will not be able to return.")
			s = input("Are you sure you would like to continue [yes/no]? ").lower().strip()
			print()
			if s == "yes":
				game.player.objectives[2] = "Make your way through the dark forest."
				game.change_chapter(2)
			return
		
		self.turn_counter += 1
		if self.turn_counter >= Forest.MOOSE_THRESHOLD and not self.moose_dead:
			if not self.moose_room:
				self.release_moose()
			self.moose_pathfind(self.rooms[room])
		
		super().enter_room(room)
		
		if self.moose_room and self.moose_room != self.room:
			if self.moose_distance >= 5:
				print("You hear a rumbling noise in the distance.\n")
			elif 3 < self.moose_distance < 5:
				print("You hear a loud rumbling noise and it's getting closer...\n")
			else:
				print("The ground is shaking and you hear hoofbeats and twigs snapping!")
				print("It's almost upon you now...\n")
	
	# the moose must head toward the player
	def moose_pathfind(self, room):
		unvisited = set(self.rooms.values())
		distances = {k: 999 for k in self.rooms.values()}
		sources = {k: None for k in self.rooms.values()}
		
		distances[self.moose_room] = 0
		current = self.moose_room
		
		while room in unvisited:
			edges = current.edges.values()
			neighbours = set(room for room in self.rooms.values() if (room.name in edges or room in edges))
			for neighbour in neighbours:
				distance = distances[current] + 1
				if distance < distances[neighbour]:
					distances[neighbour] = distance
					sources[neighbour] = current
			unvisited.remove(current)
			
			if unvisited:
				current = min(((distances[room], room) for room in unvisited), key=lambda x: x[0])[1]
		
		next_room = room
		if next_room != self.moose_room:
			while sources[next_room] != self.moose_room:
				next_room = sources[next_room]
			
			self.moose_room.remove_object(GameObjects.MOOSE)
			self.moose_room = next_room
			self.moose_room.objects.append(MOOSE_DESC)
		self.moose_distance = distances[room]
	
	def release_moose(self):
		self.moose_room = self.rooms["forest_moose"]
		self.moose_room.remove_object(GameObjects.SLEEPING_MOOSE)
		self.moose_room.objects.append(MOOSE_DESC)
	
	def begin_chapter(self):
		super().begin_chapter()
		self.enter_room("forest_landing")
	
	def act(self, action):
		room_before = self.room
		super().act(action)
		
		# punish players if they don't run from the moose
		if self.room == room_before and self.moose_room == self.room:
			print("The moose lowers its antlers and charges at you!")
			print("You try to dodge, but suffer a glancing blow...")
			game.player.damage(4)
			print()