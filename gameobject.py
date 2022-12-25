
"""composable game object - collects individual components """

from tree.lib.object import Composite, ObjectComponent


class GameObject(Composite):
	pass

class GameComponent(ObjectComponent):
	parentType = GameObject



