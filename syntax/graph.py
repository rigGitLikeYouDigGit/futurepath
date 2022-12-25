
from __future__ import annotations

import networkx as nx
import pprint
from tree.lib.object import UidElement

from futurepath.syntax.atom import Atom, Condition, Symbol
from futurepath.syntax.field import Field
from futurepath.syntax.object import Object
from futurepath.syntax.actor import Actor
from futurepath.syntax.action import Action
from futurepath.syntax.operator import *
from futurepath.syntax.goal import Goal
from futurepath.syntax.eval import ExpressionVisitor

from futurepath.syntax.world import WorldState

"""evaluating graph might get properly crazy

some actions cause mutation of graph structure if graph is regenerated - 
eg picking up object

while PLANNING, at each node traversal, the HYPOTHETICAL graph has to be regenerated,
since at each action taken, the state of the HYPO graph might change

while EXECUTING, entire process should be run after each real action taken anyway


"""


def buildActionGraph(worldState:WorldState)->nx.DiGraph:
	actors = worldState.actors
	objects = worldState.objects
	allActions = worldState.actions

	graph = nx.DiGraph()
	# add actions and discrete (object, field, value) states
	# as nodes

	for actor in actors:
		# field values should all be resolved at this stage
		# test adding actor as node
		graph.add_node(actor)
		for field, value in actor.fieldMap.items():
			graph.add_node((actor, field, value))
			graph.add_edge(actor, (actor, field, value))

		# add goals
		for goal in actor.goals:
			graph.add_node(goal)
			for condition in goal.terms:
				if isinstance(condition, Condition.Equal):
					if isinstance(condition.terms[0], GetField):
						nodeTie = (condition.terms[0].owner,
						           condition.terms[0].field,
						           condition.terms[1])
						graph.add_node(nodeTie)
						graph.add_edge(nodeTie, goal)


	for action in allActions:
		graph.add_node(action)

		for result in action.result:
			if isinstance(result, SetField):
				nodeTie = (result.owner, result.field, result.value)
				graph.add_node(nodeTie)
				graph.add_edge(action, nodeTie)

		for reqCondition in action.reqs:
			# sweater spaghetti and cringe abound here
			# literally no idea how to represent conditions in graph
			if isinstance(reqCondition, Condition.Equal):
				if isinstance(reqCondition.terms[0], GetField):
					nodeTie = (reqCondition.terms[0].owner,
					           reqCondition.terms[0].field,
					           reqCondition.terms[1]
					           )
					graph.add_node(nodeTie)
					graph.add_edge(nodeTie, action)

	return graph
# print("")
# print("visit actor")

def combineGoalPlans(graph:nx.DiGraph, actor:Actor, goalPlans:list[list[Action]]):
	"""weigh goal plans against each other, see if there are any
	duplicate actions etc
	not sure about this yet
	"""
	return goalPlans[0]

def getPlans(world:WorldState)->dict[Actor, list[Action]]:
	"""only look for the immediate action to perform - at that point,
	re-evaluate and re-resolve entire system? with new actors

	actors, objects and actions should all be resolved by this point
	"""

	graph = buildActionGraph(world)

	actorActionMap = {}
	for actor in world.actors:
		plans = []
		for goal in actor.goals:
			plans.append(nx.shortest_path(
				graph, source=actor, target=goal))
		actorActionMap[actor] = combineGoalPlans(graph, actor, plans)

	return actorActionMap


