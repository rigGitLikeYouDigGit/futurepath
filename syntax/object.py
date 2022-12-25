from __future__ import annotations
from tree.lib.object import UidElement, NamedElement

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.syntax.field import Field

"""all entities relevant to the graph are objects,
and interact with graph through their fields"""




class Object(NamedElement, Atom.base()):
	"""entity in the world owning a set of fields"""
	terminal = True
	def __init__(self, name="object"):
		NamedElement.__init__(self, name)
		Atom.base().__init__(self)
		#self.name = name
		self.fieldMap: dict[T.Type[Field], Atom] = {}

	# def __repr__(self):
	# 	return f"{self.__class__.__name__}( {self.name} )"
	def __repr__(self):
		return NamedElement.__repr__(self)

	def __str__(self):
		return repr(self)

	def copy(self)->Object:
		"""create a copy of this object, used to 'posit' during planning"""

		new = type(self)(self.name)
		new.fieldMap = self.fieldMap.copy()
		return new

	def resolve(self)->Object:
		return self