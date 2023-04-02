from ..chapter import Chapter

class Epilogue(Chapter):
	def __init__(self):
		super().__init__("epilogue")
	
	def begin_chapter(self):
		self.enter_room("epilogue_clearing")