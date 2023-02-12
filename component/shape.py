

from __future__ import annotations

import typing as T
if T.TYPE_CHECKING:
	from futurepath.object import Object

from futurepath.syntax.atom import Atom
from futurepath.component.main import Component
"""represents physical shape of an object
may not need to be a component
"""


class Shape(Component):

	def __init__(self,
	             dimensions:T.Tuple[float, float, float]=(1, 1, 1) # in cm, constants for now
	             ):
		Component.__init__(self)
		self.dimensions = tuple(map(Atom.Constant, map(float, dimensions)))

	def total(self)->float:
		"""return the total volume of the shape, temp for now"""
		return self.dimensions[0] + self.dimensions[1] + self.dimensions[2]




