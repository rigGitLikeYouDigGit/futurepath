
from __future__ import annotations
"""recursively evaluate expression at a certain state
"""
from dataclasses import dataclass

from tree.lib.object import UidElement
from tree.lib.visit import Visitor

from futurepath.syntax.atom import Atom, Symbol
from futurepath.field import Field
from futurepath.object import Object
from futurepath.actor import Actor
from futurepath.action import Action
from futurepath.condition import *
from futurepath.goal import Goal

"""expand and resolve expressions in preparation for generating graph"""

class ExpressionVisitor(Visitor):
	"""recurse through expression tree and replace symbols
	with current values"""

	@dataclass
	class VisitData(Visitor.VisitData):
		"""add symbol-value map specific to this frame of evaluation"""
		symbolValueMap : dict = None

	def __init__(self, symbolValueMap:dict):
		"""symbolValueMap is set at outset, but may be overridden
		by lower objects -
		maybe, not sure about this yet

		"""
		Visitor.__init__(self)
		self.initSymbolValueMap = symbolValueMap

	def getVisitData(self, newObj, parentObj, parentData:VisitData=None) ->VisitData:
		baseVisitData = super(ExpressionVisitor, self).getVisitData(newObj, parentObj, parentData)
		if baseVisitData.symbolValueMap is None:
			baseVisitData.symbolValueMap = dict(self.initSymbolValueMap)

		if parentData is None:
			return baseVisitData

		# override value map here later if needed
		newSymbolValueMap = baseVisitData.symbolValueMap

		newVisitData = self.VisitData(
			parentObject=parentData.parentObject,
			objectPath=parentData.objectPath,
			symbolValueMap=newSymbolValueMap
		)

		return newVisitData


	def visit(self, obj, visitData):
		#print("visit", obj)
		try: hash(obj)
		except (TypeError, AttributeError):
			#print("skipping unhashable", obj)
			return obj
		if obj in self.initSymbolValueMap:
			return self.initSymbolValueMap[obj]
		return obj

