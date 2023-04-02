from collections import defaultdict

# singleton game object that all other code can access things through
game = None

class Game:
	def init(self):
		# avoid circular imports
		# also, can't use __init__ or the other files with have game = None
		from .chapter0.main import Family
		from .chapter1.main import Forest
		from .chapter2.main import TwoLeg
		from .chapter3.main import Town
		from .formats import read_all_tdefs
		from .player import Player
		
		# load all data, make the game objects (player/chapter/flags), etc
		self.player = Player()
		self.messages = read_all_tdefs()
		self.chapters = ( Family(),  Forest(), TwoLeg(), Town() )
		self.flags = defaultdict(lambda: False)
		self.chapter = None
		self.game_complete = False
	
	def do_end_game(self):
		from .battle import battle, Enemies
		from .converse import run_conversation
		from .epilogue.main import Epilogue
		
		# finish off chapter 3
		self.chapter.end_chapter()
		self.chapter = None
		
		# we're now in a void state with no chapter active - time for the boss battle
		run_conversation("stub_endgame_intro")
		print()
		battle(Enemies.CROWLEY.copy())
		print()
		
		if self.game_complete:
			# well, the player lost
			# sucks for them
			return
		
		self.player.objectives[7] = "Defeat Crowley."
		self.player.objectives[8] = "Get back to your family."
		
		run_conversation("epilogue")
		print()
		
		self.chapter = Epilogue()
		self.chapter.begin_chapter()
	
	def change_chapter(self, idx):
		if self.chapter: self.chapter.end_chapter()
		self.chapter = self.chapters[idx]
		self.chapter.begin_chapter()
	
	def select_name(self):
		# disallow empty names
		while not (name := input("Name the lost fox: ").strip()):
			pass
		self.player.name = name
	
	def start(self):
		print(self.messages["intro"])
		
		self.select_name()
		print()
		
		self.change_chapter(0)
		
		self.run_loop()

	def run_loop(self):		
		while not self.game_complete:
			action = input("== What would you like to do? ")
			
			# actions are handled by the chapter, to implement chapter-specific logic
			# (like the chapter 1 moose and such)
			self.chapter.act(action)
			self.player.check_optional_objectives()

def start():
	global game
	game = Game()
	game.init()
	game.start()