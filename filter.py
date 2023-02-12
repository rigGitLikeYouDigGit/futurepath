
from __future__ import annotations

from futurepath.syntax.atom import Atom, Symbol
from futurepath.field import Field
from futurepath.condition import Condition
from futurepath.object import Object

class Filter(Atom.base()):
	"""refine a set of objects by checking matches against field conditions

	Filter( Condition, Condition, ...)
	Filter( Object pool (filter, reference to object field, etc), Condition, Condition, ...)

	we consider which objects match the conditions, but also
	sort failing objects by how close they are to matching -
	track error per condition, and total

	It seems nonsensical to also filter the matching objects - they just match?

	OR can we streamline by returning one list, and the objects with error 0 match exactly?

	"""

	def __init__(self, *terms):
		Atom.base().__init__(self, *terms)


	def baseSet(self)->(Filter, Atom):
		"""set of objects to filter - may be passed as first argument, otherwise all objects
		"""
		if isinstance(self.terms[0], Condition):
			return Symbol.All # filled in by world at eval
		return self.terms[0]










