

from __future__ import annotations

import typing as T
if T.TYPE_CHECKING:
	from futurepath.object import Object

from futurepath.syntax.atom import Atom
from futurepath.component.main import Component
from futurepath.component.shape import Shape

"""a component for an object with inventory?"""


class Container(Component):
	"""a container is an object that can hold other objects"""
	def __init__(self,
	             #parent:Object,
	             #name:str="container"
	             shape:Shape=Shape((1, 1, 1)) # shape describes internal volume of container
	             ):
		Component.__init__(self)
		self.shape = shape
		self.contents:list[Object] = [] # list of objects held by container


	def dimensions(self)->T.Tuple[int, int, int]:
		"""return the dimensions of the container
		semantically this is width, height, depth, but
		in contents checks this won't always be relevant"""
		return (1, 1, 1)



