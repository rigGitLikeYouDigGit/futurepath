
"""holds object defining goals, weighting, completion requirements etc
completion best modelled as combination of states
"""

from futurepath.core import State
from futurepath.gameobject import GameObject
from futurepath.worldtile import WorldTile, WorldMap


class Goal:
	"""goals themselves are ignorant of goal owner?
	they may be tested as if an arbitrary object owns them,
	and if requiredStates are true for that object,
	goal is complete"""

	def __init__(self,
	             requiredStates:tuple[State]=(),
	             requiredNotStates:tuple[State]=(),
	             ):
		self.requiredStates = requiredStates
		self.requiredNotStates = requiredNotStates


class GoHereGoal(Goal):
	"""might not need separate classes -
	this directs an agent to a specific world tile"""

	def __init__(self,tile:WorldTile):
		super(GoHereGoal, self).__init__()
		self.tile = tile







