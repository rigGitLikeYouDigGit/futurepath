

from __future__ import annotations

import networkx as nx
import pprint
from tree.lib.object import UidElement

from futurepath.syntax.atom import Atom, Condition, Symbol
from futurepath.syntax.field import Field
from futurepath.syntax.object import Object
from futurepath.syntax.actor import Actor
from futurepath.syntax.action import Action
from futurepath.syntax.operator import *
from futurepath.syntax.goal import Goal
from futurepath.syntax.eval import ExpressionVisitor

"""container for actors, objects and actions
"""

class WorldState:
	"""initialise state with template rules and objects

	internally we can regenerate new states at different times
	"""

	def __init__(self,
	             actors:list[Actor],
	             objects:list[Object],
	             actions:list[Action],
	             graph:nx.DiGraph=None):

		self._data = [actors, objects, actions]
		self.graph = graph


	@property
	def actors(self)->list[Actor]:
		return self._data[0]
	@actors.setter
	def actors(self, value:list[Actor]):
		self._data[0] = value

	@property
	def objects(self)->list[Object]:
		return self._data[1]
	@objects.setter
	def objects(self, value:list[Object]):
		self._data[1] = value

	@property
	def actions(self)->list[Action]:
		return self._data[2]
	@actions.setter
	def actions(self, value:list[Action]):
		self._data[2] = value

	def copy(self)->WorldState:
		"""create new worldState, with fully copied
		internal objects"""
		transformer = ExpressionVisitor({})
		newData = transformer.visitRecursive(self._data)
		return WorldState(*newData, graph=None)




