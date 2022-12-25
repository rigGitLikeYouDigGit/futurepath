

from __future__ import annotations
from tree.lib.object import UidElement

import typing as T

from futurepath.syntax.atom import Atom, Condition
from futurepath.syntax.field import Field

"""bits of expressions showing active modification
of the graph

not sure if this is necessary to have, or if it would be
better inferred - more explicit seems best at this early stage
"""

class GetField(Atom.base()):
	"""retrieve field value from object"""

	def __init__(self, owner:(Atom, T.Type[Atom]), field:Field.T()):
		Atom.base().__init__(self, owner, field)

	@property
	def owner(self)->Atom:
		return self.terms[0]
	@owner.setter
	def owner(self, value:Atom):
		self.terms[0] = value

	@property
	def field(self)->Field.T():
		return self.terms[1]
	@field.setter
	def field(self, value:Field.T()):
		self.terms[1] = value


class SetField(Atom.base()):
	"""signify field modification in expression, as
	action result"""

	def __init__(self, owner:(Atom, T.Type[Atom]), field:Field.T(),  value:Atom):
		Atom.base().__init__(self, owner, field, value)

	@property
	def owner(self)->Atom:
		return self.terms[0]
	@owner.setter
	def owner(self, value:Atom):
		self.terms[0] = value

	@property
	def field(self)->Field.T():
		return self.terms[1]
	@field.setter
	def field(self, value:Field.T()):
		self.terms[1] = value

	@property
	def value(self)->Atom:
		return self.terms[2]
	@value.setter
	def value(self, value:Atom):
		self.terms[2] = value





