from .game import game
from .objects import EDIBLES, GameObjects, WEAPONS

# our brave player
class Player:
	def __init__(self):
		self.name = "Untitled" # changed later
		self.health = 20
		self.able_to_attack = False
		self.inventory = set()
		self.weapon = None
		
		self.objectives = ["???"] * 9
		self.optional_objectives = ["???"] * 6
	
	def check_optional_objectives(self):
		if GameObjects.REWARD1 in self.inventory:
			self.optional_objectives[0] = "Guess the woodpecker’s name and get the sea-green marble."
		if GameObjects.BRASS_KNUCKLES in self.inventory:
			self.optional_objectives[1] = "Get the brass knuckles."
		if GameObjects.REWARD2 in self.inventory:
			self.optional_objectives[2] = "Open the two-leg hunter’s safe and get the elephant figurine."
		if GameObjects.WHETSTONE in self.inventory:
			self.optional_objectives[3] = "Get the whetstone."
		if GameObjects.REWARD3 in self.inventory:
			self.optional_objectives[4] = "Get the Tonka Truck from the two-leg town."
		if GameObjects.POISON in self.inventory:
			self.optional_objectives[5] = "Solve Alex’s trivia game and get the vial of poison."
	
	def print_objectives(self):
		print("Objectives:")
		for i, s in enumerate(self.objectives):
			print("{}. {}".format(i + 1, s))
		print()
		
		print("Optional Objectives:")
		for i, s in enumerate(self.optional_objectives):
			print("{}. {}".format(i + 1, s))
	
	def status(self):
		print("You are a juvenile fox named {}.".format(self.name))
		print("Health: {}".format(self.health))
		print("Attack Power: {}".format(self.attack_power))
		
		print("Objectives: {}/{}".format(
			len(self.objectives) - self.objectives.count("???"), len(self.objectives)))
		print("Optional Objectives: {}/{}".format(
			len(self.optional_objectives) - self.optional_objectives.count("???"), len(self.optional_objectives)))
		
		print()
	
	# attack data comes from the weapon, if one is equipped
	# used by .battle
	@property
	def attack_power(self):
		if not self.weapon: return 1
		return WEAPONS[self.weapon].power
	
	@property
	def attack_message(self):
		if not self.weapon: return "You attack!"
		return WEAPONS[self.weapon].message
	
	# try to lookup a held item
	def get_item_by_name(self, name):
		for obj in self.inventory:
			if name in obj.examine_names:
				return obj
		return None
	
	def give(self, item):
		self.inventory.add(item)
		print("You got '{}'.".format(item.short_desc))
	
	def eat(self, item):
		assert item in EDIBLES
		amount = EDIBLES[item]
		self.inventory.remove(item)
		restored = min(20 - self.health, amount)
		self.health = min(self.health + amount, 20)
		
		print("You eat '{}'.".format(item.short_desc))
		print("You restore {} health.".format(restored))
		if not restored:
			print("You were already at full health...")
	
	def damage(self, amount):
		print("Took {} damage.".format(amount))
		self.health -= amount
		if self.health <= 0:
			print("You die...")
			game.game_complete = True
	
	def print_inventory(self):
		if len(self.inventory) == 0:
			print("You have nothing.\n")
			return
	
		print("You have:")
		for idx, obj in enumerate(self.inventory):
			# make sure to indicate which item is equipped
			print("  {}. {}{}".format(idx + 1, obj.short_desc, " (equipped)" if obj is self.weapon else ""))
		print()