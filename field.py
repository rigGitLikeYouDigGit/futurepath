from __future__ import annotations

import typing as T

from syntax import Atom
from tree.lib.object import TypeNamespace
from futurepath.syntax.atom import Atom
if T.TYPE_CHECKING:
	from futurepath.object import Object
	from futurepath.component import Component

class Field(TypeNamespace):
	"""individual attribute for object, action, goal etc
	field may have value of constant or exp"""

	class _Base(Atom.base()):
		terminal = True # this may not always be so
		numeric = False
		immutable = False # used for optimising filters - Type can never be changed, for example
		pass

	class Location(_Base):
		"""physical world location of object - maybe best handled by component?"""
		pass

	class Holding(_Base):
		"""object holds by another object"""
		pass
	class HeldBy(_Base):
		"""object held by another object
		can we define some kind of 'relationship' here,
		instead of loads of different fields?"""
		pass

	class Type(_Base):
		"""TEMP TEMP TEMP until we can integrate components into
		objects and fields"""
		immutable = True


class GetField(Atom.base()):
	"""retrieve field value from object
	optionally get component field too"""

	def __init__(self, owner:(Atom, T.Type[Atom]), field:Field.T(), component:T.Type[Component]=None):
		Atom.base().__init__(self, owner, field)
		self.component = component

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