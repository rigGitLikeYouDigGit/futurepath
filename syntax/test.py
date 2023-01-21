
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
from futurepath.syntax.graph import *

Constant = Atom.Constant
locA = Constant("a") # start position
#assert locA == locA
locB = Constant("b") # mid position
locC = Constant("c") # end position


# world map:
#   A  -  B  -  C
# first test: make actor move from a to c via b



#define actor
agent = Actor("agent")
# actor is at A
agent.fieldMap[Field.Location] = locA

# define letter
letter = Object("letter")
# letter is at C
letter.fieldMap[Field.Location] = locC

# define goals
goToCGoal = Goal(
		[Condition.Equal(GetField(Symbol.Actor, Field.Location), locC)],
		name="goToCGoal")

# goal to bring letter back to A
letterAtAGoal = Goal([Condition.Equal(GetField(letter, Field.Location), locA)])

agent.goals.append(letterAtAGoal)

# actions regarding letter
pickUpAction = Action("pickUp")
pickUpAction.reqs = [Condition.Equal(GetField(Symbol.Actor, Field.Location),
                                     GetField(Symbol.Target, Field.Location))]
pickUpAction.result = [SetField(Symbol.Actor, Field.Holding, Symbol.Target)]
# how do we define that a held object takes the location of its holder?

putDownAction = Action("putDown")
putDownAction.reqs = [Condition.NotEqual(GetField(Symbol.Actor, Field.Holding), None)]
putDownAction.result = [SetField(Symbol.Actor, Field.Holding, None),
                        SetField(Symbol.Target, Field.Location, GetField(Symbol.Actor, Field.Location))]

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


exp = ExpressionVisitor(symbolValueMap={Symbol.Actor : agent})

resolvedActors = exp.visitRecursive(actors)
resolvedObjects = exp.visitRecursive(objects)
resolvedActions = exp.visitRecursive(allActions)

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



if __name__ == '__main__':
	pass



