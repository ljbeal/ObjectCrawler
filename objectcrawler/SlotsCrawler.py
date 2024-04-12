"""
Module holding main crawler for __slots__ based objects
"""
import logging

from objectcrawler.Entity import Entity


logger = logging.getLogger(__name__)


class SlotsCrawler:
    """
    Takes an object `obj`, and attempts to recursively crawl the __slots__
    """

    __slots__ = ["obj", "indent", "continuation", "data"]

    def __init__(self, obj):
        self.obj = obj
        self.data = []

    def __str__(self):
        return self.tree()

    def tree(self, debug=False):
        logger.info("generating tree")
        self._crawl(self.obj, initialise=True)

        # calculate column widths, pre-fill with title lengths
        widths = {"assignment": 10,
                  "value": 5,
                  "classname": 9,
                  "source": 6}
        if debug:
            widths.update({"entity": 6, "parent": 6, "nchildren": 8})

        extra = 2  # extra whitespace
        # cache a list of lines, for later treating dependent on col widths
        cache = []
        indents = {}
        indents_used = {}
        for item in self.data:
            logger.debug(f"treating item {item}")
            logger.debug(f"\tparent is {item.parent}")
            if item.parent not in indents:
                indent = 0
                logger.debug(f"\t\tparent {item.parent} not in indents, setting to 0")
            else:
                indent = indents[item.parent] + 1
                logger.debug(f"\t\tfound parent {item.parent} at indent {indent - 1}")

            indents[item] = indent
            logging.debug(f"\tindent level set to {indent}")

            if indent == 0:
                indentstr = ""
            else:
                indentstr =  "│ " * (indent - 1)
                try:
                    indents_used[item.parent] += 1
                except KeyError:
                    indents_used[item.parent] = 1
                logger.debug(f"\titem {item} has used {indents_used[item.parent]} indents "
                             f"of max {item.parent.nchildren}")
                if indents_used[item.parent] >= item.parent.nchildren:
                    indentstr += "└ "
                else:
                    indentstr += "├ "

            line = []
            for k in widths:
                if k == "entity":
                    val = str(item)
                else:
                    val = str(getattr(item, k))

                if k == "assignment":
                    val = indentstr + val

                line.append(val)
                # update the lengths if necessary
                if len(val) > widths[k]:
                    widths[k] = len(val)
            # add this line
            cache.append(line)

        # generate the true output
        # start with the header
        header = []
        spacer = []
        for col, width in widths.items():
            header.append(col.ljust(width + extra))
            spacer.append("─" * (width + extra))
        uspacer = "┬─".join(spacer)
        spacer = "┼─".join(spacer)
        header = "│ ".join(header)

        # now generate table
        output = [uspacer, header, spacer]
        for line in cache:
            tmp = []
            for idx, item in enumerate(line):
                width = list(widths.values())[idx]

                tmp.append(item.ljust(width + extra))

            output.append("│ ".join(tmp))

        return "\n".join(output)

    def _crawl(self, obj, assignment=None, initialise=True):
        logger.debug(f"crawling object {obj}")
        objEntity = Entity(obj, assignment=assignment)
        if initialise:
            self.data = [objEntity]

        for o in obj.__class__.__mro__:
            if not hasattr(o, "__slots__"):
                continue

            source = o.__name__
            slots = o.__slots__

            objEntity.nchildren += len(slots)

            for idx, item in enumerate(slots):
                try:
                    tmp = getattr(obj, item)
                except Exception as E:
                    tmp = str(E)
                self.data.append(Entity(tmp, assignment=item, source=source, parent=objEntity))

                if hasattr(tmp, "__slots__"):
                    self._crawl(tmp, assignment=item, initialise=False)

    @property
    def str(self) -> str:
        """
        Return result as a string.

        This will initiate a crawl

        :return:
            (str) result
        """
        return str(self)

    def print(self, debug=False) -> None:
        """
        Print self

        This will initiate a crawl

        :return:
            None
        """
        print(self.tree(debug))
