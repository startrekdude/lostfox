from copy import copy
from enum import Enum
from random import choice

from .game import game

# the battle system
# based on Wild Wild West (the hand game)
# some twists, though

# Properties:
# Strategy matters
# Luck also matters
# Must "reload" before attacking

class BattleAction(Enum):
	ATTACK = 0
	DEFEND = 1 # generic term, modelled as "dodge" for the MC
	RELOAD = 2 # also generic term

class Enemy:
	def __init__(self, id, name, health, attack_power):
		self.id = id
		self.name = name
		self.health = health
		self.attack_power = attack_power
		self.able_to_attack = False
	
	# text, as usual, comes from the .tdefs
	@property
	def appear_message(self):
		return game.messages["enemy.{}.appear".format(self.id)]
	
	@property
	def attack_message(self):
		return game.messages["enemy.{}.attack".format(self.id)]
	
	@property
	def defend_message(self):
		return game.messages["enemy.{}.defend".format(self.id)]
	
	@property
	def reload_message(self):
		return game.messages["enemy.{}.reload".format(self.id)]
	
	def damage(self, amount):
		print("Dealt {} damage.".format(amount))
		self.health -= amount
		if self.health <= 0:
			print("The enemy {} dies.".format(self.name))
	
	# only insert copies of enemies into rooms
	def copy(self):
		return copy(self)

class Enemies:
	RAT = Enemy("rat", "rat", 4, 1)
	DOG = Enemy("dog", "two-leg's dog", 7, 2)
	PIGEON = Enemy("pigeon", "pigeon", 5, 2)
	CROWLEY = Enemy("crowley", "betrayer Crowley", 12, 3)

# largely random
def pick_enemy_action(enemy):
	if not enemy.able_to_attack and not game.player.able_to_attack:
		return BattleAction.RELOAD # be at least a little bit intelligent
	
	elif enemy.able_to_attack:
		if not game.player.able_to_attack:
			# probably a good idea to attack now :) but maybe not!
			return choice([BattleAction.ATTACK, BattleAction.ATTACK, BattleAction.ATTACK, BattleAction.DEFEND])
		else:
			return choice([BattleAction.ATTACK, BattleAction.DEFEND])
	else:
		return choice([BattleAction.RELOAD, BattleAction.DEFEND])

def pick_player_action():
	while True:
		print("What would you like to do? ")
		print("  1. Dodge")
		if game.player.able_to_attack:
			print("  2. Attack")
		else:
			print("  2. Prepare to attack")
		s = input("? ")
		if not s.isdigit(): continue
		choice = int(s)
		if choice < 1 or choice > 2: continue
		if choice == 1: return BattleAction.DEFEND
		if game.player.able_to_attack: return BattleAction.ATTACK
		return BattleAction.RELOAD

def battle(enemy):
	game.player.able_to_attack = False
	vulnerable = False
	
	while True:
		print("You have {} health remaining.".format(game.player.health))
		print("The {} has {} health remaining.".format(enemy.name, enemy.health))
		
		# What actions do our guys take?
		enemy_action = pick_enemy_action(enemy)
		player_action = pick_player_action()
		print()
		
		# Handle attacks (enemy goes first)
		if enemy_action == BattleAction.ATTACK:
			print(enemy.attack_message)
			enemy.able_to_attack = False
			
			# The vulnerability check here breaks a dominant strategy
			if vulnerable or player_action != BattleAction.DEFEND:
				if vulnerable and player_action == BattleAction.DEFEND:
					print("You try to dodge to the side, but the attack hits you anyway!")
				game.player.damage(enemy.attack_power)
		if player_action == BattleAction.ATTACK:
			print(game.player.attack_message)
			game.player.able_to_attack = False
			if enemy_action != BattleAction.DEFEND:
				enemy.damage(game.player.attack_power)
		
		# If dead, we're done here
		if enemy.health <= 0 or game.player.health <= 0:
			break
		
		# Handle reloads
		if enemy_action == BattleAction.RELOAD:
			print(enemy.reload_message)
			enemy.able_to_attack = True
		if player_action == BattleAction.RELOAD:
			print("You prepare to attack!")
			game.player.able_to_attack = True
		
		# Handle defend (actual behaviour handled in attack, but we still print a message)
		if enemy_action == BattleAction.DEFEND:
			print(enemy.defend_message)
		if player_action == BattleAction.DEFEND and not vulnerable:
			print("Moving with lightning speed, you dodge to the side!")
		print()
		
		# Vulnerability check
		if player_action == BattleAction.ATTACK and enemy_action == BattleAction.RELOAD:
			vulnerable = True
		else:
			vulnerable = False