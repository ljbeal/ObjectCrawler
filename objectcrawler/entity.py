"""
Module holding base Entity class
"""

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
            explicitly set the assigned parameter for this object.
            Attempts to extract it using gc if not set
        source:
            class where this object is stored, not necessarily the parent
        parent:
            actual parent class where this entity was found
    """

    # pylint: disable=too-many-instance-attributes
    # we're using slots, so need to specify _everything_

    __slots__ = [
        "assignment",
        "source",
        "classname",
        "value",
        "value_is_explicit",
        "parent",
        "nchildren",
        "diff",
        "iterable",
    ]

    def __init__(
        self,
        obj,
        assignment: Union[None, str] = None,
        source: str = "self",
        parent: Union[None, "Entity"] = None,
    ):

        logger.debug(
            "Creating Entity for object %s with assignment: %s, source: %s, parent: %s",
            obj,
            assignment,
            source,
            parent,
        )
        self.assignment = str(assignment) or get_assignment(obj)
        self.source = str(source)

        self.classname = obj.__class__.__name__

        self.value = str(obj)
        # "value" is explicit of the str() representation is not just the memory
        # this implies that the string method has intrinsic value
        self.value_is_explicit = hex(id(obj)) not in self.value

        self.nchildren = 0
        self.parent = parent

        self.diff = False

        if not isinstance(obj, str):
            logger.debug("\tobj is not a string, checking for iter")
            if hasattr(obj, "__iter__"):
                self.iterable = len(obj)
                logger.debug("\t\thas __iter__, True, len %s", self.iterable)
            else:
                self.iterable = False
                logger.debug("\t\tno __iter__, False")
        else:
            self.iterable = False

    def __repr__(self) -> str:
        uid = str(hash(self))[-8:]
        return f"Entity #{uid}"

    def __hash__(self) -> int:
        if self.value_is_explicit:
            return hash(self.assignment + self.value)
        return hash(self.assignment + self.classname)

    def __eq__(self, other) -> bool:
        if hash(self) == hash(other):
            return True
        return False
