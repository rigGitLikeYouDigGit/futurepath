from __future__ import annotations
from tree.lib.object import TypeNamespace
from futurepath.syntax.atom import Atom

class Field(TypeNamespace):
	"""individual attribute for object, action, goal etc
	field may have value of constant or exp"""

	class _Base(Atom.base()):
		terminal = True # this may not always be so
		pass

	class Location(_Base):
		"""physical location of object"""
		pass

	pass


