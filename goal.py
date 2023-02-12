


from __future__ import annotations
from tree.lib.object import UidElement, NamedElement

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.condition import Condition
from futurepath.field import Field

class Goal(NamedElement, Atom.base()):
	"""goals define a desired state of the world, as a map of
	{ object : set of conditions to satisfy }

	intenally, it's most consistent to store raw list of conditions

	"""
	def __init__(self,
	             conditions:list[Condition._Base],
	             # conditions:dict[(Atom, Object), list[Condition.base()]],
	             name="goal"
	             ):
		NamedElement.__init__(self, name)
		Atom.base().__init__(self, *conditions)

	def __repr__(self):
		return NamedElement.__repr__(self)


	def __str__(self):
		return repr(self)


	def _visitTraverse(self, masterVisitRecursiveFn,
                   visitArgsKwargs=((), {})):
		"""bit of messiness here, could conform Goal to use the same
		initialiser signature as other atoms"""

		visitedTerms = tuple(masterVisitRecursiveFn(i,
			                       *visitArgsKwargs[0],
			                       **visitArgsKwargs[1])
				for i in self.terms)

		return type(self)( visitedTerms, self.name )