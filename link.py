
from __future__ import annotations

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.field import Field
from futurepath.object import Object

class Link(Atom.base()):
	"""represent live relation between fields"""

	terminal = True

	def __init__(self,
	             targetOwner:Object,
	             targetField:Field):
		Atom.base().__init__(self)
		self.targetOwner = targetOwner
		self.targetField = targetField

	def __repr__(self):
		return f"{self.__class__.__name__}( {self.targetOwner} . {self.targetOwner} )"

	def __str__(self):
		return repr(self)

	def copy(self)->Link:
		"""create a copy of this object, used to 'posit' during planning"""

		new = type(self)(self.source, self.target)
		return new

