import os.path

from glob import iglob

from .converse import Choice, Command, CommandType, Sequence
from .game import game
from .objects import GameObjects

# read a text definition file
# format is simple, i'll provide an example
# =key1
# this is a long
# multiline string
# =key2
# this one is shorter
# ==
def read_tdef(name):
	result = {}
	
	current_message_key = ""
	current_message_val = ""
	
	with open(name, encoding="utf8") as f:
		for line in f:
			if line.startswith("=="): # EOF
				result[current_message_key] = current_message_val.strip() # take off newlines
				break
			elif line.startswith("="): # new key
				if current_message_key: result[current_message_key] = current_message_val.strip()
				current_message_key = line[1:].strip()
				current_message_val = ""
			else:
				current_message_val += line
	
	return result

# yeah, it's basic, but i didn't need anything more soooo
def format_message(msg):
	return game.messages[msg].replace("$(name)", game.player.name)

# load a conversatin .seq(uence) file to be processed
# by .converse. It's a sequence of labelled commands
def load_conversation(name):
	name += ".seq"
	name = os.path.join("assets", name)
	
	# order is by lines in file, commands is by labels
	order = []
	commands = {}
	
	with open(name, encoding="utf8") as f:
		lines = f.read().splitlines() # this takes out \ns
	
	for line in lines:
		id, type, *tokens = line.split(" ")
		order.append(id)
		
		if type == "P": # print
			commands[id] = Command(CommandType.PRINT, msg=format_message(tokens[0]))
		elif type == "J": # jump
			commands[id] = Command(CommandType.JUMP, target=tokens[0])
		elif type == "F": # flag
			commands[id] = Command(CommandType.FLAG, flag=tokens[0])
		elif type == "B": # branch
			commands[id] = Command(CommandType.BRANCH, flag=tokens[0], target=tokens[1])
		elif type == "E": # freeform Entry
			commands[id] = Command(CommandType.FREEFORM_ENTRY, expected=tokens[0], target=tokens[1])
		elif type == "G": # give
			commands[id] = Command(CommandType.GIVE, item=getattr(GameObjects, tokens[0]))
		elif type == "T": # take
			commands[id] = Command(CommandType.TAKE, item=getattr(GameObjects, tokens[0]))
		elif type == "H": # has
			commands[id] = Command(CommandType.HAS, item=getattr(GameObjects, tokens[0]), target=tokens[1])
		elif type == "R": # room
			commands[id] = Command(CommandType.ROOM, room=tokens[0])
		elif type == "N": # nop
			commands[id] = Command(CommandType.NOP)
		elif type == "C": # choices
			choices = []
			for i in range(0, len(tokens), 2):
				choices.append(Choice(format_message(tokens[i]), tokens[i+1]))
			commands[id] = Command(CommandType.CHOICE, choices=choices)
	
	return Sequence(commands, order)

def read_all_tdefs():
	result = {}
	for name in iglob("assets/*.tdef"):
		result.update(read_tdef(name))
	return result