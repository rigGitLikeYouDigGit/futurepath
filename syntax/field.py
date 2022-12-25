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

	class Holding(_Base):
		"""object holds by another object"""
		pass
	class HeldBy(_Base):
		"""object held by another object
		can we define some kind of 'relationship' here,
		instead of loads of different fields?"""
		pass

	class Contains(_Base):
		"""object contained by another object"""
		pass

	pass


