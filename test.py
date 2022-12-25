
from tree.lib.object import TypeNamespace

class Symbol:
	"""Replaceable symbol to make graph operations abstract -
	can be substituted for real objects as needed in order to
	generate bespoke graph regions"""
	pass

S = Symbol # shorter namespace






class FPNode:
	"""node in futurepath network"""

class State(FPNode):
	"""shared global state object,
	describing fragment of overall network
	should probably be static
	but might be defined as function of multiple other states
	"""

class Condition:
	"""probably should not be a node
	defines some lemma about the graph that must be met
	(for goals, actions etc)

	might also define how far off current state is, for deltas and gradients,
	but not now
	"""

class Action(FPNode):
	"""link between states -
	defines requisites,
	and separate results based on success,
	or for any failure cases """


class Goal(FPNode):
	"""defines desired state or combination of states
	for agent to achieve"""

class Network:
	pass
