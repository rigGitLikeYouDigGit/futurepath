from __future__ import annotations
from tree.lib.object import UidElement, NamedElement
from copy import deepcopy

import typing as T
if T.TYPE_CHECKING:
	from futurepath.component.main import Component

from futurepath.syntax.atom import Atom
from futurepath.field import Field

"""all entities relevant to the graph are objects,
and interact with graph through their fields"""




class Object(UidElement, Atom.base()):
	"""entity in the world owning a set of fields"""
	terminal = True
	def __init__(self, name="object", _uid=""):
		UidElement.__init__(self, _uid) # will name always be unique?
		Atom.base().__init__(self)
		self.name = name
		self.fieldMap: dict[T.Type[Field], Atom] = {}

		self.componentMap: dict[T.Type[Component], Component] = {}

	# def __repr__(self):
	# 	return f"{self.__class__.__name__}( {self.name} )"
	def __repr__(self):
		return NamedElement.__repr__(self)

	def __str__(self):
		return repr(self)

	def copy(self)->Object:
		"""create a copy of this object, used to 'posit' during planning"""

		new = type(self)(self.name)
		new.fieldMap = deepcopy(self.fieldMap)
		new.componentMap = deepcopy(self.componentMap)

		return new

	def resolve(self)->Object:
		return self

	def addComponents(self, components:list[Component]):
		for component in components:
			self.componentMap[type(component)] = component

	def getComponent(self, componentType:T.Type[Component])->Component:
		return self.componentMap[componentType]

	def hasComponent(self, componentType:T.Type[Component])->bool:
		return componentType in self.componentMap
