
"""individual tile representing position in world
may hold actors, items etc

links to other tiles via actions - these actions are copied into state graph
"""
from palette import *
from networkx import DiGraph
from tree.lib.object import UidElement, NamedElement

from futurepath.core import Action
from futurepath.gameobject import GameObject

class WorldTile(NamedElement):

	def __init__(self, name:str):
		NamedElement.__init__(self, name)

		# objects that currently exist on this world tile
		self.objects : list[GameObject] = []




class WorldMap(DiGraph):

	def linkTiles(self, tileA:WorldTile, tileB:WorldTile, action=None):
		action = action or Action()
		# link forwards
		self.add_edge(tileA, action)
		self.add_edge(action, tileB)



# define different maps

# basic
# A - B - C
def makeBasicMap():
	basicMap = WorldMap()
	aTile = WorldTile("A")
	bTile = WorldTile("B")
	cTile = WorldTile("C")
	for i in [aTile, bTile, cTile]:
		basicMap.add_node(i)
	# link forwards
	basicMap.linkTiles(aTile, bTile)
	basicMap.linkTiles(bTile, cTile)
	# link backwards
	basicMap.linkTiles(cTile, bTile)
	basicMap.linkTiles(bTile, aTile)

	# basic pathing
	p = nx.algorithms.shortest_path(basicMap, aTile, cTile)
	print(p)


basicMap = makeBasicMap()

