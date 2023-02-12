

from __future__ import annotations
from tree.lib.object import UidElement, TypeNamespace

import typing as T

from futurepath.syntax.atom import Atom
from futurepath.field import Field

"""operations measuring quantities and attributes of objects
these operations lose information from their inputs, so need to propagate
any error corrections to all of them
"""


class Measure(TypeNamespace, Atom.base()):

	class _Base(Atom.base()):
		"""base for all measures"""

	class Count(_Base):
		"""count number of objects in set"""
		pass
