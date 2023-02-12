


from __future__ import annotations
from tree.lib.object import UidElement, NamedElement

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.condition import Condition
from futurepath.field import Field
from field import GetField, SetField


class Action(NamedElement, Atom.base()):

	terminal = False # actions may contain expressions, and need evaluation

	def __init__(self, #actor:Actor
	             #reqs:list[Atom]
	             name="action",
	             ):
		#self.actor = actor
		NamedElement.__init__(self, name)
		# action as atom defines 2 top-level lists, requirements and effects
		Atom.base().__init__(self, [], [])

		self.reqs:list[Condition] = []
		self.result:list[SetField] = [] # list of SetFields

	def __repr__(self):
		return NamedElement.__repr__(self)

	def __str__(self):
		return repr(self)

	@property
	def reqs(self)->list[Condition]:
		return self.terms[0]
	@reqs.setter
	def reqs(self, value:list[Condition]):
		self.terms[0] = value

	@property
	def result(self)->list[tuple[Atom]]:
		return self.terms[1]
	@result.setter
	def result(self, value:list[tuple[Atom]]):
		self.terms[1] = value

	def _visitTraverse(self, masterVisitRecursiveFn,
	                   visitArgsKwargs=((), {})):
		"""Action probably can't / shouldn't be conformed to
		simple Atom initialiser signature"""
		newAction = type(self)(self.name)
		newAction.terms = tuple(
			masterVisitRecursiveFn(
				self.terms,
				*visitArgsKwargs[0],
				**visitArgsKwargs[1]
			))
		return newAction


"""
how should we formulate complex effect of actions?

-actor wants to move through door
	-actor's knowledge shows door can open, and actor can pass

- actor takes action "openDoor"

- action FAILS because door is locked and needs a key

- actor gains knowledge that door is locked
	- gains knowledge of requirements of "openDoor" action?




"""

