

from __future__ import annotations
from tree.lib.object import TypeNamespace

import typing as T

from futurepath.constant import MAX_ERROR_VALUE
from futurepath.syntax.atom import Atom

if T.TYPE_CHECKING:
	from futurepath.world import WorldState
	from futurepath.graph import FPGraph

"""bits of expressions showing active modification
of the graph

not sure if this is necessary to have, or if it would be
better inferred - more explicit seems best at this early stage
"""


class CompareMode(TypeNamespace, Atom.base()):
	"""different ways of comparing values- numeric, graph state-space distance etc
	likely overkill making this itself an atom, but a bit of reflection never hurt anyone

	strings are still handled as graph distance for now, which is obviously crazy overkill,
	but it unifies the interface (we assume that any string represents some state in the graph,
	whether that is connected to other states or not)


	graph distance - is it possible to model different "axes" within the graph?
	eg. distance in time, distance in space, distance in number of actions etc?
	if terms differ in 2 regards, is that a 2d distance?

	keep it a flat value for now (shortest path through links between them)

	"""

	class _Base(Atom.base()): pass
	class Numeric(_Base): pass
	class GraphDistance(_Base): pass

class Condition(TypeNamespace, Atom.base()):
	"""Represent logical comparison between values
	NO IDEA how this might actually work
	"""



	class _Base(Atom.base()):
		"""base for all conditions"""
		# def __init__(self, *terms):
		# 	self.terms = terms

		def getError(self, world:WorldState, graph:FPGraph)->list[float]:
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
			return CompareMode.GraphDistance

		def _getErrorNumeric(self, world:WorldState)->list[float]:
			"""return error value for this condition"""
			try:
				average = sum(self.terms) / len(self.terms)
			except TypeError:
				return 1
			return [abs(i - average) for i in self.terms]

		def _getErrorGraphDistance(self, world:WorldState, graph:FPGraph)->list[float]:
			"""return error value for this condition
			for simplicity, if any constant terms are found, those are the 'base'

			difficulty here that some terms may not show what field they refer to -
			eg Equal( GetField(Object, Type), "human" )
			is perfectly readable, but current system can't understand it
			"""
			defaultField


		def getError(self, world:WorldState, graph:FPGraph)->list[float]:
			""" run after terms are evaluated in world

			return error value for each term, to return to average
			check that meaningful comparison can be made - if not, error

			specialcasing constants here

			returns float value for each term

			here we don't know what these values are, only their results
			but we DO need to know what fields they relate to - it's meaningless to
			compare 'locA' and 'human' without knowing one is a location and one is a type

			"""

			mode = self.checkTermsMode(world)
			if mode is CompareMode.Numeric:
				return self._getErrorNumeric(world)



			try:
				average = sum(self.terms) / len(self.terms)
			except TypeError:
				return 1
		pass

	# class Is(_Base):
	# 	"""maybe temp, version of Eq"""

	class NotEqual(_Base):
		pass





