

from __future__ import annotations
from tree.lib.object import UidElement, TypeNamespace

import typing as T

from futurepath.syntax.atom import Atom, Condition
from futurepath.syntax.field import Field

"""
define persistent relationships between objects

think of how a physics sim is defined - all the objects live at
lowest level, and constraints are built atop them

can the same work here?

in this case the only way is to decentralise graph construction,
allow each relation constraint to alter the graph as it sees fit
"""

class Relation(TypeNamespace, Atom.base()):
	"""Specific atoms representing a relative value or object, to be resolved
	should these ever be instantiated?
	"""

	class _Base(Atom.base()):
		pass

	class Holding(_Base):
		"""object holds by another object
		first object is driver,
		second object is driven"""
		pass





