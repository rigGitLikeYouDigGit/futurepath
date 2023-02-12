


from __future__ import annotations

import typing as T
if T.TYPE_CHECKING:
	from futurepath.object import Object

from futurepath.syntax.atom import Atom
from futurepath.component.main import Component
"""semantically, just what the hell IS this object?

no way am I trying to represent this with python inheritance, 
this is totally decoupled

time to make my boy diogenes proud
"""


class Type(Component):
	"""provide any kind of classification, taxonomy etc that we might need
	to stratify objects in the world"""

	def __init__(self,
	             clearType
	             ):
		"""
		:param clearType: if you look at this thing, what do you call it?
			eg: if you look at a tree, you call it a tree
		"""
		Component.__init__(self)
		self.clearType = clearType


