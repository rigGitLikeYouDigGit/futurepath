
"""base class for ai agent - in reality would probably be better composed"""

from futurepath.gameobject import GameComponent, GameObject
from futurepath.goal import Goal, GoHereGoal

class GoalComponent(GameComponent):

	def __init__(self, parent:GameObject):
		super(GoalComponent, self).__init__(parent)

		# dict of goal : priority
		self.goalMap : dict[Goal, float] = {}



class Agent(GameObject):

	def createDefaultComponents(self):
		pass

	pass


