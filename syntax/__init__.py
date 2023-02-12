

"""package for defining expressions and complex relationships
between parts of network"""

import typing as T


from .atom import Atom, Symbol, Condition
# add atoms to global ns
globals().update(Atom.members())
#
# for k, v in Atom.members().items():
# 	locals()[k] = v
if T.TYPE_CHECKING:
	Constant = Atom.Constant





