
"""main state graph defining all things that are and may be"""

from palette import *
from networkx import DiGraph
from tree.lib.object import UidElement, NamedElement

from futurepath.core import Action, State
from futurepath.gameobject import GameObject

from futurepath.worldtile import WorldTile, WorldMap

class WorldState(DiGraph):
	"""represents a certain point of view
	not immutable, as actions of other agents may have effect -
	picking up items, pressing buttons etc"""

	def makeStatesFromWorldMap(self, worldMap:WorldMap):
		"""given a world map, for each tile, generate an "At" state, showing that
		an object occupies that location
		this feels crude but it lets us do literal pathfinding through the world,
		as well as through any states that get in the way"""


	def linkStates(self, tileA:State, tileB:State, action=None):
		action = action or Action()
		# link forwards
		self.add_edge(tileA, action)
		self.add_edge(action, tileB)



