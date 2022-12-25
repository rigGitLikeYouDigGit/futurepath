
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


Constant = Atom.Constant
locA = Constant("a") # start position
#assert locA == locA
locB = Constant("b") # mid position
locC = Constant("c") # end position


class WorldState:
	"""everything
	test tracking all relationships as simple dicts and strings
	maybe it's possible for actions and expressions to be immutable,
	and respond to changes just through evaluation?
	"""

	def __init__(self):
		self.data = {
			"actor" : {},
			"action" : {}
		}


# world map:
#   A  -  B  -  C
# first test: make actor move from a to c via b

# define actions, directed moves between locations
aGoToB = Action("aGoToB")
aGoToB.reqs = [Condition.Equal(GetField(Symbol.Actor, Field.Location), locA)]
aGoToB.result = [SetField(Symbol.Actor, Field.Location, locB)]

bGoToA = Action("bGoToA")
bGoToA.reqs = [Condition.Equal(GetField(Symbol.Actor, Field.Location), locB)]
bGoToA.result = [SetField(Symbol.Actor, Field.Location, locA)]

bGoToC = Action("bGoToC")
bGoToC.reqs = [Condition.Equal(GetField(Symbol.Actor, Field.Location), locB)]
bGoToC.result = [SetField(Symbol.Actor, Field.Location, locC)]

cGoToB = Action("cGoToB")
cGoToB.reqs = [Condition.Equal(GetField(Symbol.Actor, Field.Location), locC)]
cGoToB.result = [SetField(Symbol.Actor, Field.Location, locB)]

allActions = [aGoToB, bGoToA, bGoToC, cGoToB]


#define actor
agent = Actor("agent")
# actor is at A
agent.fieldMap[Field.Location] = locA

# define goals
agent.goals.append(
	Goal(
		[Condition.Equal(GetField(Symbol.Actor, Field.Location), locC)],
		name="goToCGoal"
	)
)

exp = ExpressionVisitor(symbolValueMap={Symbol.Actor : agent})
#result = exp.visitRecursive(agent.goals[0])
# print("")
# print(agent.goals[0].dump())
# print(result.dump())
# #print(result.terms)

# to fully evaluate any expression, need a full state of the world
# later though

def evalEverything(objects:list[Object],
                   actions:list[Action],
				   goals:list[Goal]) -> list[Action]:
	"""evaluate all possible plans and return the best one"""


def availableActions(actor:Actor, allActions:list[Action]) -> list[Action]:
	"""get a list of actions that the agent can currently perform"""
	# # eval at higher scope, not here
	# exp = ExpressionVisitor(symbolValueMap={Symbol.Actor: actor})
	# allActions =

	actions = []
	for i in allActions:
		if all(n.eval() for n in i.reqs):
			actions.append(i)
	return actions

def actionsGivingFieldState(obj, field:Field, value:Atom,
                            allActions:list[Action]) -> list[Action]:
	"""get a list of actions that will change the value of a field"""
	allActions =[exp.visitRecursive(i) for i in allActions]
	actions = []
	for i in allActions:
		for result in i.result:
			if not isinstance(result, SetField):
				continue

			if result.owner == obj and result.field == field and result.value == value:
				actions.append(i)
				break
	return actions

#print(actionsGivingFieldState(agent, Field.Location, locC, allActions))

"""I don't know how best to convert these separate actions to a graph,
but it'll be easier if we can

FIELD VALUES ARE NODES easy
CONDITIONS hard


consider "toGraph()" method on atoms?

all actual states must be added beforehand - 
Equal.toGraph() looks up nodes for operands, adds edge from
each to parent

what does an And gate look like?

And( A, B ) - A and B are both object/field/value state nodes in graph?



"""

def buildActionGraph(actors:list[Actor], objects:list[Object], allActions:list[Action]):
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

def getPlans(actors, objects, allActions)->dict[Actor, list[Action]]:
	"""only look for the immediate action to perform - at that point,
	re-evaluate and re-resolve entire system? with new actors"""
	resolvedActors = exp.visitRecursive(actors)
	resolvedObjects = exp.visitRecursive(objects)
	resolvedActions = exp.visitRecursive(allActions)
	graph = buildActionGraph(
		resolvedActors,
		resolvedObjects,
		resolvedActions
	)

	actorActionMap = {}
	for actor in resolvedActors:
		plans = []
		for goal in actor.goals:
			plans.append(nx.shortest_path(
				graph, source=actor, target=goal))
		actorActionMap[actor] = combineGoalPlans(graph, actor, plans)

	return actorActionMap



# resolvedActor = exp.visitRecursive(agent)
# # print("\n visit actions\n")
# resolvedActions = exp.visitRecursive(allActions)


# graph = buildActionGraph([resolvedActor], resolvedActions)
# print(graph)
# print(tuple(graph.nodes))
# for i in graph.nodes:
# 	print(i)
# 	pass

# goalPath = nx.shortest_path(graph, source=resolvedActor, target=resolvedActor.goals[0])
# print("path")
# #print(goalPath)
# print([i for i in goalPath if isinstance(i, Action)])
#
# print(f"goal {agent.goals[0]} fulfilled")
# # print(tuple(graph.nodes)[0], hash(tuple(graph.nodes)[0]))
# # print(tuple(graph.nodes)[5], hash(tuple(graph.nodes)[5]))
#
#
# #pprint.pp(list(graph.nodes))

def getConcreteGoalPlan(actor:Actor, goal:Goal, allActions:list[Action]) -> list[Action]:
	"""check if there is an explicit action path readily available
	among actions"""

def goalPlan(actor:Actor, goal:Goal, allActions:list[Action]) -> list[Action]:
	"""build a plan for the agent to achieve a specific goal
	first check if there is a valid plan among the actions present -
	if a concrete chain exists, return it

	if not, then we need to get a bit creative



	"""

	# try working outwards from Actor, and backwards from goal





def buildActionPlan(actor:Actor, allActions:list[Action]) -> list[Action]:
	"""build a plan for the agent to achieve its goals"""
	plans = [goalPlan(actor, i, allActions) for i in actor.goals]
	return plans

#print(buildActionPlan(agent, allActions))



if __name__ == '__main__':
	pass



