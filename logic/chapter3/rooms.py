from ..battle import Enemies
from ..game import game
from ..objects import GameObjects
from ..room import InWorldDescription, Npc, Room

NO = "You can't go in this direction."

town_road3 = Room(edges={
	"north": "town_road1",
	"east": "town_intersection",
	"south": NO,
	"west": NO,
})

town_road1 = Room(edges={
	"north": NO,
	"east": "town_road2",
	"south": "town_road3",
	"west": NO,
}, npcs=[
	Npc(InWorldDescription(GameObjects.PABLO, "You see a squirrel."), "pablo"),
])

town_road2 = Room(edges={
	"north": NO,
	"east": "You aren't in the mood for a swim.",
	"south": "town_intersection",
	"west": "town_road1",
}, enemy=Enemies.PIGEON.copy())

town_intersection = Room(edges={
	"north": "town_road2",
	"east": "town_shed",
	"south": "town_road4",
	"west": "town_road3",
})

town_road4 = Room(edges={
	"north": "town_intersection",
	"east": "town_road5",
	"south": "town_dead_end",
	"west": NO
}, npcs=[
	Npc(InWorldDescription(GameObjects.ROCCO, "You see a raccoon."), "raccoon"),
])

town_dead_end = Room(edges={
	"north": "town_road4",
	"backward": "town_road4",
	"east": NO,
	"south": NO,
	"west": NO,
}, objects=[
	InWorldDescription(GameObjects.ROTTING_MEAT, "You see a piece of rotting meat."),
])

town_shed = Room(edges={
	"north": NO,
	"east": NO,
	"south": "town_road5",
	"west": "town_intersection",
}, objects=[
	InWorldDescription(GameObjects.SHED, game.messages["chapter3.shed_inworld"]),
])

town_road5 = Room(edges={
	"north": "town_shed",
	"east": NO,
	"south": "town_hammer",
	"west": "town_road4",
}, npcs=[
	Npc(InWorldDescription(GameObjects.JAYNE, "You see a blue jay."), "jayne"),
])

JACKHAMMER_NO = "The jackhammer is blocking the path."

town_hammer = Room(edges={
	"north": "town_road5",
	"backward": "town_road5",
	"east": JACKHAMMER_NO,
	"left": JACKHAMMER_NO,
	"`____secret_debug_bypass": "town_park",
	"south": NO,
	"west": NO,
}, objects=[
	InWorldDescription(GameObjects.JACKHAMMER, game.messages["chapter3.jackhammer_inworld"]),
], enemy=Enemies.PIGEON.copy())

town_park = Room(edges={
	"north": NO,
	"east": "town_chapter_change",
	"south": "town_trivia",
	"west": "town_hammer",
})

town_trivia = Room(edges={
	"north": "town_park",
	"east": NO,
	"south": NO,
	"west": NO,
}, npcs=[
	Npc(InWorldDescription(GameObjects.ALEX, "You see a cat."), "trivia"),
])

town_chapter_change = Room()