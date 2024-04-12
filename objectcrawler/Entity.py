import logging
from typing import Union

from objectcrawler.get_assignment import get_assignment

logger = logging.getLogger(__name__)


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

    __slots__ = ["assignment", "source", "classname", "value", "value_is_explicit", "parent", "nchildren"]

    def __init__(self, obj, assignment=None, source="self", parent: Union[None, "Entity"] = None):
        logger.debug(f"Creating Entity for object {obj} "
                     f"with assignment: {assignment}, source: {source}, parent: {parent}")
        self.assignment = assignment or get_assignment(obj)
        self.source = source

        self.classname = obj.__class__.__name__

        self.value = str(obj)
        # "value" is explicit of the str() representation is not just the memory
        # this implies that the string method has intrinsic value
        self.value_is_explicit = hex(id(obj)) not in self.value

        self.nchildren = 0
        self.parent = parent

    def __repr__(self) -> str:
        uid = str(hash(self))[-8:]
        return f"Entity #{uid}"

    def __hash__(self) -> int:
        if self.value_is_explicit:
            return hash(self.assignment + self.value)
        return hash(self.assignment + self.classname)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
