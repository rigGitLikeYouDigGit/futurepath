
"""object representing a transition between states (or world tiles)"""
from futurepath.palette import *
from tree.lib.object import UidElement, NamedElement

if T.TYPE_CHECKING:
	from futurepath.gameobject import GameObject

class State(NamedElement):
	"""base node in state graph"""

	def __init__(self, name:str):
		NamedElement.__init__(self, name)

		# list of objects for whom this state is true
		self.objects:list[GameObject] = []


class Action(UidElement):
	"""link between state nodes -
	a more complex action may have nontrivial effects on
	graph - how can we tell the graph what the action will do
	before it does it? how can we tell it the reverse?"""

	def __init__(self):
		UidElement.__init__(self)

		self.cost = None

	pass




