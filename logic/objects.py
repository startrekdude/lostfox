from collections import namedtuple

from .game import game

# models something that can be, at minimum examined
# some can also be taken
# or talked to
class GameObject:
	def __init__(self, name, examine_names, is_item):
		self.name = name
		self.examine_names = examine_names
		self.is_item = is_item
	
	# make sure these can go in sets and be used as dict keys
	def __hash__(self):
		return hash(self.name)
	
	def __eq__(self, other):
		return self.name == other.name
	
	# read text data from .tdefs
	@property
	def short_desc(self):
		return game.messages["obj.{}.short".format(self.name)]
	
	@property
	def long_desc(self):
		return game.messages["obj.{}.long".format(self.name)]
	
class GameObjects:
	# Objects
	MOSS_BED = GameObject("moss_bed", ("bed",), False)
	SLEEPING_MOOSE = GameObject("sleeping_moose", ("moose", "sleeping"), False)
	MOOSE = GameObject("moose", ("moose", "antler", "bull"), False)
	ELECTRIC_FENCE = GameObject("electric_fence", ("fence", "electric", "barrier"), False)
	SAFE = GameObject("safe", ("safe",), False)
	JACKHAMMER = GameObject("jackhammer", ("jackhammer", "hammer", "jack"), False)
	DEAD_JACKHAMMER = GameObject("dead_jackhammer", ("jackhammer", "hammer", "jack"), False)
	SHED = GameObject("shed", ("shed",), False)
	
	# Characters are a special type of object (just with a conversation associated)
	FAMILY = GameObject("family", ("family",), False)
	TIM = GameObject("tim", ("owl", "tim", "sandaele", "mentor"), False)
	KARL = GameObject("karl", ("woodpecker", "wood", "pecker", "karl"), False)
	CROWLEY = GameObject("crowley", ("snake", "crowley", "ally", "betrayer"), False)
	ROCCO = GameObject("rocco", ("raccoon", "rocco"), False)
	ALEX = GameObject("alex", ("cat", "alex", "trebek", "trivia"), False)
	PABLO = GameObject("pablo", ("squirrel", "pablo", "hyper"), False)
	JAYNE = GameObject("jayne", ("jay", "blue", "jayne"), False)
	ARI = GameObject("ari", ("ari", "bobcat"), False)
	ODIN = GameObject("odin", ("odin", "raven"), False)
	CHLOE = GameObject("chloe", ("chloe", "coyote"), False)
	
	# Items
	FLUFFY = GameObject("fluffy", ("fluffy", "stuffed", "stuffy", "stuffie"), True)
	BRASS_KNUCKLES = GameObject("brass_knuckles", ("brass", "knuckles", "knuckle", "metal"), True)
	CHEKHOVS_GUN = GameObject("gun", ("gun", "shot", "shotgun", "pewpew", "chekhov"), True)
	WHETSTONE = GameObject("whetstone", ("whetstone", "whet", "stone", "sharp", "sharpen"), True)
	POISON = GameObject("poison", ("poison", "vial",), True)
	ORANGE = GameObject("orange", ("orange",), True)
	GRAPEFRUIT = GameObject("grapefruit", ("grapefruit",), True)
	APPLE = GameObject("apple", ("apple",), True)
	ROTTING_MEAT = GameObject("meat", ("rotting", "meat"), True)
	DEED_OF_NEST = GameObject("deed", ("nest", "deed"), True)
	REWARD1 = GameObject("reward1", ("marble", "sea", "green", "blue"), True)
	REWARD2 = GameObject("reward2", ("carved", "elephant", "phant", "carve", "toy"), True)
	REWARD3 = GameObject("reward3", ("tonka", "truck"), True)

# some objects can be used as weapons
WeaponSpec = namedtuple("WeaponSpec", ("power", "message"))

WEAPONS = {
	GameObjects.BRASS_KNUCKLES: WeaponSpec(2, "You attack with brass knuckles!"),
	GameObjects.WHETSTONE: WeaponSpec(3, "You attack with freshly sharpened claws!"),
	GameObjects.POISON: WeaponSpec(4, "You attack with poisoned claws!"),
}

# some items heal the player
EDIBLES = {
	GameObjects.ORANGE: 5,
	GameObjects.GRAPEFRUIT: 10,
	GameObjects.APPLE: 10,
}