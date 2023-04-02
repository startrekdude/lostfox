from ..objects import GameObjects
from ..room import InWorldDescription, Npc, Room

den_main = Room(edges={
	"sister's": "You aren't allowed in your sister's bedroom.",
	"parent's": "You aren't allowed in your parents' bedroom.",
	"bedroom": "den_bedroom",
	"right": "den_bedroom",
	"left": "den_dining",
	"dining": "den_dining",
})

den_bedroom = Room(edges={
	"backward": "den_main",
	"main": "den_main",
	"tunnel": "den_main",
	"left": "den_main",
}, objects=[
	InWorldDescription(GameObjects.MOSS_BED, "You see your bed in the corner."),
	InWorldDescription(GameObjects.FLUFFY, "On your bed, you see your stuffed animal."),
])

den_dining = Room(edges={
	"backward": "den_main",
	"main": "den_main",
	"tunnel": "den_main",
	"right": "den_main",
})

den_sitting = Room(npcs=[
	Npc(InWorldDescription(GameObjects.FAMILY, "Sitting around the table is your family."), "family"),
])