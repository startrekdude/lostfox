from ..battle import Enemies
from ..objects import GameObjects
from ..room import InWorldDescription, Npc, Room

DESC_CROWLEY = InWorldDescription(GameObjects.CROWLEY, "Crowley followed you here.")

home_cage = Room(npcs=[
	Npc(InWorldDescription(GameObjects.CROWLEY, "Across from you you see a snake in another cage."), "caged"),
])

home_basement = Room(edges={
	"stairs": "home_landing",
}, objects=[
	InWorldDescription(GameObjects.SAFE, "You see a large safe on the floor."),
], npcs=[
	Npc(DESC_CROWLEY, "stub_basement"),
])

home_landing = Room(edges={
	"backward": "home_basement",
	"down": "home_basement",
	"stairs": "home_basement",
	"left": "home_living",
	"right": "home_outside",
	"door": "home_outside",
	"outdoor": "home_outside",
	"exterior": "home_outside",
}, npcs=[
	Npc(DESC_CROWLEY, "stub_landing"),
], enemy=Enemies.DOG.copy())

home_living = Room(edges={
	"backward": "home_landing",
	"landing": "home_landing",
	"right": "home_landing",
}, objects=[
	InWorldDescription(GameObjects.WHETSTONE, "On the table, you see a whetstone."),
])

home_outside = Room(edges={
	"backward": "home_landing",
	"forward": "home_chapter_change",
}, npcs=[
	Npc(DESC_CROWLEY, "post_battle"),
	Npc(InWorldDescription(GameObjects.TIM, "Tim the owl is perched on the balustrade."), "tim"),
])

home_chapter_change = Room()