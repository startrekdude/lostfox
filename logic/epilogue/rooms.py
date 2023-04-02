from ..objects import GameObjects
from ..room import InWorldDescription, Npc, Room

epilogue_clearing = Room(npcs=[
	Npc(InWorldDescription(GameObjects.ARI, "You see your friend Ari, a juvenile bobcat."), "ari"),
	Npc(InWorldDescription(GameObjects.ODIN, "You see your friend Odin, a juvenile raven."), "odin"),
	Npc(InWorldDescription(GameObjects.CHLOE, "You see your friend Cody's younger sister Chloe, a baby coyote."), "chloe"),
], objects=[
	#InWorldDescription(GameObjects.REWARD1, "Debugging marble."),
	#InWorldDescription(GameObjects.REWARD2, "Debugging elephant."),
	#InWorldDescription(GameObjects.REWARD3, "Debugging truck."),
])