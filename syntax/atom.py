

from __future__ import annotations

"""values, and expressions to resolve values.
got a bit wacky with inheritance here,
don't worry about it

probably could have used a subset of actual AST nodes instead
of reinventing here
"""

import typing as T
from tree.lib.object.namespace import TypeNamespace
from tree.lib.visit import Visitable
from copy import deepcopy


if T.TYPE_CHECKING:
	from field import Field


class AtomScope:
	"""base for objects that may override local
	variables, relevant for resolving signals

	eg Symbol.Actor -
		at outer scope means the originator of an action,
		at inner scope means the latest subject in that scope
	"""



class Atom(TypeNamespace):
	"""base for all components of a semantic relationship, as an expression
	these may tell the graph dynamically how to build and explore relationships

	take inspiration from ast here, each atom defines array of branches - we visit and transform these for every graph step

	"""

	class _Base(TypeNamespace.base(), Visitable):

		# can this atom be evaluated further?
		terminal = False

		#nTerms = 1

		def __init__(self, *terms):
			# create terms array
			self.terms: list[Atom.base()] = list(terms)

		def __iter__(self):
			return iter(self.terms)

		def __hash__(self):
			return hash(tuple(self.terms))

		def __eq__(self, other):
			"""I have absolutely no idea why this is necessary"""
			return hash(self) == hash(other)
			# print("eq", self, other, object.__eq__(self, other))
			# return object.__eq__(self, other)

		def isNumeric(self)->bool:
			"""does this atom represent a numeric value?"""
			return isinstance(self.value, (int, float))

		def isDiscrete(self)->bool:
			"""does this atom represent a discrete value, which cannot be interpolated?"""
			return isinstance(self.value, (str, bool, type))

		def copy(self)->Atom:
			return type(self)(*(i.copy() for i in self.terms))



		def _flattenDepthFirst(self)->list[Atom]:
			"""top down, depth first"""
			baseList = [self]
			for i in self.terms:
				baseList.extend(i._flattenDepthFirst())
			return baseList

		def flatten(self)->list[Atom]:
			return self._flattenDepthFirst()


		def dump(self):
			baseList = ""
			for i in self.terms:
				try:
					baseList += (i.dump())
				except (TypeError, AttributeError):
					baseList += str(i)
				baseList += " "
			#baseStr = [i.dump() for i in self.terms]
			return f"{self.__class__.__name__}( {baseList} )"

		# direct visitor to look up terms
		def _visitTraverse(self, masterVisitRecursiveFn,
	                   visitArgsKwargs=((), {})):

			if self.terminal: # just return a new atom of this type
				return type(self)(*self.terms)


			visitedTerms = list(masterVisitRecursiveFn(i,
				                       *visitArgsKwargs[0],
				                       **visitArgsKwargs[1])
					for i in self.terms)
			return type(self)( *visitedTerms )

		# def eval(self, symbolMap:dict)->Atom:
		# 	"""retrieve value of abstract expression in
		# 	current context"""
		# 	raise NotImplementedError

	class Constant(_Base):
		"""constant and literal values, like absolute locations
		an expression reduced to a constant
		cannot be evaluated further
		"""
		terminal = True
		def __init__(self, value):
			# creating constant around another constant copies it
			if isinstance(value, Atom.Constant):
				value = value.value
			Atom._Base.__init__(self, value)
			#self.value = value

		def __repr__(self):
			baseStr = repr(self.terms)
			return f"{self.__class__.__name__}( {baseStr} )"

		def __str__(self):
			return repr(self)

		@property
		def value(self):
			return self.terms[0]
		@value.setter
		def value(self, value):
			self.terms[0] = value


	# # common constants
	# success = Constant("success")
	# failure = Constant("failure")


# # common constants
success = Atom.Constant("success")
failure = Atom.Constant("failure")

class Symbol(TypeNamespace, Atom.base()):
	"""Specific atoms representing a relative value or object, to be resolved
	should these ever be instantiated?
	"""

	class _Base(Atom.base()):
		pass
		# def __init__(self, value):
		# 	self.value = value

		# def eval(self, symbolMap:dict) ->Atom:
		# 	return symbolMap[self.value]


	class Actor(_Base) : pass

	class Target(_Base):
		"""if an action may be aimed at an object,
		this will be replaced with it"""
		pass

	# semantic stuff
	class All(_Base):
		"""semantically shows 'all'
		possible this should be a Symbol instead"""

	class Any(_Base):pass

	class None_(_Base):pass

	class One(_Base):
		"""semantic for 'a single one', not literally the number 1"""

	class AllButOne(_Base):	pass





