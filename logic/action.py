from time import sleep

from .converse import run_conversation
from .game import game
from .objects import EDIBLES, GameObjects, WEAPONS
from .room import InWorldDescription, Room

# all of these are ignored
CONNECTION_WORDS = (
	"to",
	"the",
	"towards",
	"into",
	"my",
	"at",
	"with",
	"up",
	"your",
)

SYNONYMS = {
	"gaze": "look",
	"end": "exit",
	"done": "exit",
	"bye": "exit",
	"move": "go",
	"run": "go",
	"details": "examine",
	"pickup": "take",
	"pick": "take",
	"get": "take",
	"grab": "take",
	"stuff": "inventory",
	"leap": "jump",
	"me": "status",
	"health": "status",
	"consume": "eat",
	"park": "sit",
	"converse": "talk",
	"ask": "talk",
	"gab": "talk",
	"chat": "talk",
	"nom": "eat",
	"nibble": "eat",
	"vore": "eat",
	"arm": "equip",
	"discard": "drop",
	"put": "drop",
	"place": "drop",
	"flip": "flick",
	"invert": "flick",
	"switch": "flick",
}

def look(args):
	print(game.chapter.room.long_desc + "\n")

def exit(args):
	print("Goodbye.\n")
	game.game_complete = True

# basically the help menu, show what actions can be taken
# NOTE: actions are not context sensitive in terms of availability
def actions(args):
	print("Here are the actions you can take:")
	for i, action in enumerate(sorted(ACTIONS)):
		synonyms = [k for k, v in SYNONYMS.items() if v == action]
		
		if synonyms:
			print("  {}. {} ({})".format(i + 1, action, ", ".join(synonyms)))
		else:
			print("  {}. {}".format(i + 1, action))
	print()

def go(args):
	if len(args) == 0:
		print("Don't know where to go.\n")
		return
		
	target = args[0]
	for direction, result in game.chapter.room.edges.items():
		if direction.startswith(target):
			# we can go to a room either by key or by reference
			if result in game.chapter.rooms:
				game.chapter.enter_room(result)
			elif isinstance(result, Room):
				game.chapter.enter_room(result.name)
			else:
				print(result + "\n")
			return
	
	print("I don't understand that direction.\n")

def find_object(name): # utility
	for obj, _ in game.chapter.room.objects:
		if name in obj.examine_names:
			return obj
	return None

def examine(args):
	if len(args) == 0:
		print("Don't know what to examine.\n")
		return
	
	target = args[0]
	obj = find_object(target)
	obj = game.player.get_item_by_name(target) if not obj else obj
	
	if not obj:
		print("I don't know what that is.\n")
		return
	
	print(obj.long_desc)
	
	if obj is GameObjects.SAFE:
		print(game.chapter.lights_description)
	
	print()

def equip(args):
	if len(args) == 0:
		print("Don't know what to equip.\n")
		return
	
	target = args[0]
	obj = game.player.get_item_by_name(target)
	
	if not obj:
		print("You don't have that.\n")
		return
	
	if obj not in WEAPONS:
		print("You can't equip that.\n")
		return
	
	game.player.weapon = obj
	print("Equipped.\n")

def drop(args):
	if len(args) == 0:
		print("Don't know what to drop.\n")
		return
	
	target = args[0]
	obj = game.player.get_item_by_name(target)
	
	if not obj:
		print("You don't have that.\n")
		return
	
	if obj is game.player.weapon:
		game.player.weapon = None
	
	desc = "You see a discarded item that can only be described as '{}'.".format(obj.short_desc)
	iwd = InWorldDescription(obj, desc)
	game.chapter.room.objects.append(iwd)
	game.player.inventory.remove(obj)
	
	print("Dropped '{}'.\n".format(obj.short_desc))

def eat(args):
	if len(args) > 0:
		target = args[0]
		obj = game.player.get_item_by_name(target)
		
		if not obj:
			print("You don't have that.\n")
			return
		
		if obj not in EDIBLES:
			print("You can't eat that.\n")
			return
		
		game.player.eat(obj)
		print()
	# because the verb admittedly isn't obvious here
	elif game.chapter.room.name == "den_dining":
		print("You need to sit down first.\n")
	elif game.chapter.room.name == "den_sitting":
		run_conversation("family")
		print()
	else:
		print("Don't know what to eat.\n")

def talk(args):
	if len(args) == 0:
		print("Don't know who to talk to.\n")
		return
	
	target = args[0]
	obj = find_object(target)
	
	if not obj:
		print("I don't know what that is.\n")
		return
	
	# try to find a conversation associated with the object
	conversation = next((k for o, k in game.chapter.room.conversations if o is obj), None)
	if not conversation:
		print("You can't talk to that.\n")
		return
	
	run_conversation(conversation)
	print()

def take(args):
	if len(args) == 0:
		print("Don't know what to take.\n")
		return
	
	target = args[0]
	obj = find_object(target)
	
	if not obj:
		print("I don't know what that is.\n")
		return
	
	# items can be taken, objects cannot
	if not obj.is_item:
		print("You can't take that.\n")
		return
	
	game.player.inventory.add(obj)
	game.chapter.room.remove_object(obj)
	print("Added '{}' to inventory.\n".format(obj.short_desc))

def inventory(args):
	game.player.print_inventory()

def jump(args):
	# the dev me thinks of everything
	if game.chapter.room.name.startswith("den_"):
		print("You hit your head, ouch!")
		game.player.damage(1)
		print()
	elif game.chapter.room.name == "forest_end":
		print("You jump eighteen times your body height!")
		print("You grab the low-hanging branch.")
		print("Nothing on the ground can get you now...\n")
		game.chapter.jump_maybe_win()
		sleep(4)
		print("The branch is slipping away from you!")
		print("You fall back to the ground.\n")
	else:
		print("You jump eighteen times your body height!\n")

def status(args):
	game.player.status()

def sit(args):
	if game.chapter.room.name == "den_dining":
		game.chapter.enter_room("den_sitting")
	else:
		print("You sit. It doesn't seem to accomplish much.\n")

def flick(args):
	if game.chapter.room.name != "home_basement":
		print("I don't understand.\n")
		return
	
	if len(args) == 0 or not args[0].isdigit():
		print("Don't know what to flick.")
		print("HINT: Specify which switch to flick as a number between 1 and 7, inclusive.\n")
		return
	
	idx = int(args[0])
	
	if not (1 <= idx <= 7):
		print("There are only 7 switches.\n")
		return
	
	game.chapter.flick(idx)

def objectives(args):
	game.player.print_objectives()
	print()

ACTIONS = {
	"look": look,
	"exit": exit,
	"actions": actions,
	"objectives": objectives,
	"go": go,
	"examine": examine,
	"take": take,
	"inventory": inventory,
	"jump": jump,
	"status": status,
	"sit": sit,
	"talk": talk,
	"eat": eat,
	"equip": equip,
	"drop": drop,
	"flick": flick,
}

def dispatch_action(action):
	print()
	
	# force lowercase, remove connecting words
	action = action.lower().strip()
	words = action.split(" ")
	words = [w for w in words if w not in CONNECTION_WORDS]
	
	# de-synonymize
	verb, *args = words
	if verb in SYNONYMS: verb = SYNONYMS[verb]
	
	# some things don't make sense
	if verb not in ACTIONS:
		print("I don't understand.\n")
		return
	
	# let's do it
	ACTIONS[verb](args)