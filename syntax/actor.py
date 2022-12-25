


from __future__ import annotations
from tree.lib.object import UidElement

import typing as T

from futurepath.syntax.atom import Atom, Condition
from futurepath.syntax.field import Field
from futurepath.syntax.object import Object
from futurepath.syntax.goal import Goal

class Actor(Object):
	"""an actor is an object that can perform actions,
	and form plans based on goals"""

	def __init__(self,
	             name="actor"):
		Object.__init__(self, name=name)
		self.goals:list[Goal] = []

	def copy(self)->Actor:
		new = super(Actor, self).copy()
		new.goals = self.goals.copy()
		return new

	# direct visitor to look up terms
	def _visitTraverse(self, masterVisitRecursiveFn,
	                   visitArgsKwargs=((), {})):

		visitedGoals = [masterVisitRecursiveFn(
			i,
			*visitArgsKwargs[0],
			**visitArgsKwargs[1])
	            for i in self.goals]
		newActor = self.copy()
		newActor.goals = visitedGoals
		return newActor

