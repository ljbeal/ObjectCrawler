from typing import Union

from objectcrawler.get_assignment import get_assignment


class Entity:
    """
    Class to store a single entity of the queried class

    Args:
        obj:
            actual object
        assignment:
            explicitly set the assigned parameter for this object. Attempts to extract it using gc if not set
        source:
            class where this object is stored, not necessarily the parent
        parent:
            actual parent class where this entity was found
    """

    __slots__ = ["assignment", "source", "classname", "value", "parent"]

    def __init__(self, obj, assignment=None, source="self", parent: Union[None, "Entity"] = None):
        self.assignment = assignment or get_assignment(obj)
        self.source = source
        self.parent = parent

        self.classname = obj.__class__.__name__
        self.value = str(obj)

    def __repr__(self):
        return f"Entity {self.classname} @ {self.assignment}"

    def __hash__(self):
        return hash(self.assignment + self.value)
