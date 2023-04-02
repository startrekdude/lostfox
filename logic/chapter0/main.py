from ..chapter import Chapter
from ..game import game

class Family(Chapter):
	def __init__(self):
		super().__init__("chapter0")
	
	def begin_chapter(self):
		super().begin_chapter()
		self.enter_room("den_main")
	
	def act(self, action):
		super().act(action)
		if game.flags["conv.family.complete"]: # chapter end condition
			game.player.objectives[0] = "Talk to your family."
			game.change_chapter(1)