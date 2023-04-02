from collections import namedtuple

from .game import game

# Npc is specified in the room definition files, but is desugared into IWD and convo
Npc = namedtuple("Npc", ("desc", "conversation_key"))

InWorldDescription = namedtuple("InWorldDescription", ("obj", "desc"))
Conversation = namedtuple("Conversation", ("obj", "key"))

class Room:
	def __init__(self, edges=None, objects=None, npcs=None, enemy=None):
		# we can't use edges={}, etc in the constructor itself because then
		# every Room will share the *same* {}, which is a problem if you need
		# to change it
		edges = {} if not edges else edges
		objects = [] if not objects else objects
		npcs = [] if not npcs else npcs
		
		self.edges = edges
		self.objects = objects
		self.enemy = enemy
		self.name = None # set later
		self.conversations = []
		for npc in npcs:
			self.objects.append(npc.desc)
			self.conversations.append(Conversation(npc.desc.obj, npc.conversation_key))
	
	def remove_object(self, obj):
		for i in range(len(self.objects) - 1, -1, -1):
			if self.objects[i].obj == obj:
				del self.objects[i]
	
	@property
	def short_desc(self):
		result = game.messages["{}.short".format(self.name)] + "\n"
		
		# include any objects in the room in the short description
		if len(self.objects) > 0:
			for obj, desc in self.objects:
				result += "\n" + desc
			result += "\n"
		
		return result
	
	@property
	def long_desc(self):
		return self.short_desc + "\n" + game.messages["{}.long".format(self.name)]