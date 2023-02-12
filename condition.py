

from __future__ import annotations
from tree.lib.object import TypeNamespace

import typing as T

from futurepath.constant import MAX_ERROR_VALUE
from futurepath.syntax.atom import Atom

if T.TYPE_CHECKING:
	from futurepath.world import WorldState

"""bits of expressions showing active modification
of the graph

not sure if this is necessary to have, or if it would be
better inferred - more explicit seems best at this early stage
"""


class CompareMode(TypeNamespace, Atom.base()):
	"""different ways of comparing values- numeric, absolute (like strings), graph state-space distance etc
	likely overkill making this itself an atom, but a bit of reflection never hurt anyone


	graph distance - is it possible to model different "axes" within the graph?
	eg. distance in time, distance in space, distance in number of actions etc?
	if terms differ in 2 regards, is that a 2d distance?

	keep it a flat value for now (shortest path through links between them)

	"""

	class _Base(Atom.base()): pass
	class Numeric(_Base): pass
	class Absolute(_Base): pass
	class GraphDistance(_Base): pass

class Condition(TypeNamespace, Atom.base()):
	"""Represent logical comparison between values
	NO IDEA how this might actually work
	"""



	class _Base(Atom.base()):
		"""base for all conditions"""
		# def __init__(self, *terms):
		# 	self.terms = terms

		def getError(self, world:WorldState):
			"""return error value for this condition"""
			raise NotImplementedError



	class Equal(_Base):

		def checkTermsMode(self, world:WorldState)->CompareMode.T():
			"""chekc mode of this comparison, as determined by term types -
			if any term is an absolute, then any error is infinite -
			if they exist in world or graph, can a distance be calculated?
			else if they are all numeric, do a basic float operation"""
			if all(i.isNumeric() for i in self.terms):
				return CompareMode.Numeric
			return all(isinstance(i, Atom.Constant) for i in self.terms)

		def getError(self, world:WorldState)->list[float]:
			""" run after terms are evaluated in world

			return error value for each term, to return to average
			check that meaningful comparison can be made - if not, error

			specialcasing constants here

			returns float value for each term

			here we don't know what these values are, only their results
			"""

			for i in self.terms:
				if isinstance(i, Atom.Constant):
					target = i.value




			try:
				average = sum(self.terms) / len(self.terms)
			except TypeError:
				return 1
		pass

	# class Is(_Base):
	# 	"""maybe temp, version of Eq"""

	class NotEqual(_Base):
		pass





