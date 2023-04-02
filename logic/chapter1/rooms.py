from random import shuffle

from ..battle import Enemies
from ..objects import GameObjects
from ..room import InWorldDescription, Npc, Room

NO_MOVE_UNDERBRUSH = "Harsh, thick underbrush impedes any progress in this direction."

# the fixed rooms for this chapter

forest_landing = Room(edges={
	"right": "forest_puzzle",
	"left": NO_MOVE_UNDERBRUSH,
	"backward": "forest_moose",
})

forest_puzzle = Room(edges={
	"backward": "forest_landing",
	"right": NO_MOVE_UNDERBRUSH,
	"forward": NO_MOVE_UNDERBRUSH,
	"left": NO_MOVE_UNDERBRUSH,
}, npcs=[
	Npc(InWorldDescription(GameObjects.KARL, "You see a woodpecker."), "karl"),
])

forest_moose = Room(edges={
	"forward": "forest_landing",
	"backward": NO_MOVE_UNDERBRUSH,
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
}, objects=[
	InWorldDescription(GameObjects.SLEEPING_MOOSE, "You see a sleeping moose."),
])

forest_rat_den = Room(edges={
	"forward": NO_MOVE_UNDERBRUSH,
	"backward": "forest_path2",
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
}, objects=[
	InWorldDescription(GameObjects.BRASS_KNUCKLES, "You see a pair of brass knuckles."),
], enemy=Enemies.RAT.copy())

forest_eegg = Room(edges={
	"forward": NO_MOVE_UNDERBRUSH,
	"backward": "forest_path4",
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
}, objects=[
	InWorldDescription(GameObjects.CHEKHOVS_GUN, "You see a discarded gun."),
])

# these ones are connected in a random order
forest_path1 = Room(edges={
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
}, npcs=[
	Npc(InWorldDescription(GameObjects.TIM, "You see an owl perched on a low branch."), "owl"),
])
forest_path2 = Room(edges={
	"left": "forest_rat_den",
	"right": NO_MOVE_UNDERBRUSH,
})
forest_path3 = Room(edges={
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
}, enemy=Enemies.RAT.copy())
forest_path4 = Room(edges={
	"left": NO_MOVE_UNDERBRUSH,
	"right": "forest_eegg",
})
forest_path5 = Room(edges={
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
})

# make the connections

forest_end = Room(edges={
	"left": NO_MOVE_UNDERBRUSH,
	"right": NO_MOVE_UNDERBRUSH,
	"forward": "The path is blocked by the electric fence.",
}, objects=[
	InWorldDescription(GameObjects.ELECTRIC_FENCE, "You see an electric fence blocking the path forward."),
])

forest_chapter_change = Room()

path_rooms = [forest_path1, forest_path2, forest_path3, forest_path4, forest_path5]
shuffle(path_rooms)

path_rooms[0].edges["backward"] = "forest_landing"
forest_landing.edges["forward"] = path_rooms[0]

path_rooms[-1].edges["forward"] = "forest_end"
forest_end.edges["backward"] = path_rooms[-1]

for i in range(0, 4):
	path_rooms[i].edges["forward"] = path_rooms[i + 1]
	path_rooms[i + 1].edges["backward"] = path_rooms[i]