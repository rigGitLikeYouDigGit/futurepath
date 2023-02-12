
from __future__ import annotations

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.field import Field
if T.TYPE_CHECKING:
	from futurepath.object import Object


class Component:
	"""one component of each type per object,
	testing no reference to parent object"""

	def __init__(self,# owner:Object
	             ):
		self.fieldMap: dict[T.Type[Field], Atom] = {}
	pass


class GetComponent(Atom.base()):
	"""retrieve component from object"""

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

