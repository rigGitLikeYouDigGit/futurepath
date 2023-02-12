

from __future__ import annotations

from futurepath.syntax.atom import Symbol
from futurepath.field import Field
from futurepath.measure import Measure
from futurepath.object import Object
from futurepath.filter import Filter
from futurepath.goal import Goal
from futurepath.graph import *
from futurepath import component


"""world map:
A - B - C

actor starts at C
has goal to bring 3 letters to C, on ground
letters are at A
case is at B

actor has full knowledge of the world

ideal result:
actor moves to B,
 picks up case, 
 moves to A, 
 puts down case,
 picks up letter,
 puts in case,
 (repeat 3 times)
 
 picks up case,
 moves to C,
 puts down case,
 takes letter out of case,
 puts down letter,
 (repeat 3 times)


how do we teach an agent that a case is a container?
that it can carry any "hypothetical" object?

added spice: goal of bringing 3 letters to C - not 3 SPECIFIC letters

"""

Constant = Atom.Constant
locA = Constant("a") # start position
locB = Constant("b") # mid position
locC = Constant("c") # end position


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



#define actor
agent = Actor("agent")
# actor is at C
agent.fieldMap[Field.Location] = locC
agent.fieldMap[Field.Type] = Constant("human") # temp

# define letters
letters = []
# define master letter, then copy it
masterLetter = Object("letterMaster")
masterLetter.fieldMap[Field.Location] = locA
masterLetter.addComponents([
	component.Type(clearType="letter"),
	component.Shape((0.5, 0.5, 0.05))
	]
)
#TEMP TEMP TEMP
masterLetter.fieldMap[Field.Type] = Constant("letter")

for i in range(3):
	letter = masterLetter.copy()
	letter.name = "letter" + str(i)
	letters.append(letter)

print("letters")
print(letters)
# define goals


lettersAtCGoal = Goal(
	[Condition.Equal(
		Measure.Count(Filter(
			Condition.Equal(GetField(Symbol.Object, Field.Type), Constant("letter")),
			Condition.Equal(GetField(Symbol.Object, Field.Location), locC))),
	3)],

		)

"""
3 letters at c

condition(equal, quantity ( 
		fieldFilter( 
			condition(equal(type, letter)), 
			condition(equal(location, c))
			 ) ), 
	 3)  

trying to brute force this directly into pathfinding is a dead end, and for more complex goals, it's not even possible

any arbitrary condition may be affected by any arbitrary action - we need to see if that effect is beneficial

we could evaluate goal condition before and after each action? get its "gradient"?

condition is evaluated:
	- number of objects which are letters, and at C, is 0
	- 0 is not equal to 3
	- equality adds "impulse" to both sides, as either side might be changed
	- tries to raise 0 to 3, and lower 3 to 0
	- 3 is a constant - doesn't go anywhere
	
	- track back to how we arrived at that 0
		- quantity loses information, so we copy the impulse across all of it?
		- quantity converts field expressions to numeric
		- fieldFilter shows all objects that satisfy its conditions - we need more objects to satisfy them - how to gather though?
		- filter obviously returns no results here anyway - can we break down each filter term?
		- for all objects that are letters, try to make their location c
		- for all objects at c, try to make their type letters? (obviously nothing actually does this)
	
	
field filter matches objects against multiple conditions - track HOW WELL objects match, even if they're not returned - try splitting each field individually?

objects satisfying location=c - here is none, but some are nearer than others - 
	if the "error" or "delta" or whatever is 0, condition is met
	otherwise, a delta value may be returned for some things?
		so a letter at B will have error of 1, while at A will have error of 2
objects satisfying type=letter - obviously just letters.
	letters return error of 0
	non-letters return error of 1 (or infinity?)
	let's assume type can never change :)
	
	how do we reconcile those two kinds of checks - one continuous, one boolean?
	maybe "mask" fields in filter - if a certain field does not match, discard object immediately?
	
	filter is basically refining a set progressively after all - as each term is checked,
	mutate running total
	if you include a "discrete" field, we assume we can filter by it
	
	
	
	

"""



# goToCGoal = Goal(
#
# 		[Condition.Equal(GetField(Symbol.Actor, Field.Location), locC)],
# 		name="goToCGoal")
#
#
# allActions = [aGoToB, bGoToA, bGoToC, cGoToB]

