"""
Module holding main crawler for __slots__ based objects
"""
import gc


def get_assignment(obj) -> str:
    """
    Attempts to extract the assignment location of object `obj` from gc

    :param obj:
        Object to query
    :return:
        assignment location
    """
    locations = []
    for item in gc.get_referrers(obj):
        if isinstance(item, dict):
            for k, v in item.items():
                if v is obj:
                    locations.append(k)
    return locations[-1]


class SlotsCrawler:
    """
    Takes an object `obj`, and attempts to recursively crawl the __slots__
    """

    def __init__(self, obj):
        self.obj = obj
        self.indent = 0
        self.continuation = {0: True}

        self.data = {
            "item": [get_assignment(obj)],
            "value": [str(obj)],
            "class": [obj.__class__.__name__],
            "source": [obj.__class__.__name__],
        }

    def __str__(self):
        self._crawl(self.obj)

        header = []
        spacer = []
        ljust_sizes = []
        for key, vals in self.data.items():
            maxlen = max(max([len(i) for i in vals]), len(key)) + 2
            ljust_sizes.append(maxlen)

            header.append(key.ljust(maxlen))
            spacer.append("-" * maxlen)

        spacer = "-+-".join(spacer)
        header = " | ".join(header)

        zipped = []
        for idx in range(len(self.data[key])):
            tmp = []
            for key, vals in self.data.items():
                tmp.append(vals[idx])

            zipped.append(tmp)

        output = [spacer, header, spacer]
        for line in zipped:
            tmp = []
            for idx, item in enumerate(line):
                tmp.append(str(item).ljust(ljust_sizes[idx]))

            output.append(" | ".join(tmp))

        return "\n".join(output)

    def _crawl(self, obj, indent=0):
        self.continuation[indent] = True
        for o in obj.__class__.__mro__:
            if not hasattr(o, "__slots__"):
                continue

            source = o.__name__
            slots = o.__slots__

            for idx, item in enumerate(slots):
                last = (idx == len(slots) - 1)

                sub_indent = "├─ "
                if last:
                    sub_indent = "└─ "
                    self.continuation[indent] = False

                indentstr = []
                for i in range(indent):
                    if self.continuation[i]:
                        indentstr.append("|  ")
                    else:
                        indentstr.append("   ")
                indentstr = "".join(indentstr)

                try:
                    val = getattr(obj, item)
                except AttributeError:
                    val = "AttributeError"

                classname = val.__class__.__name__
                self.data["source"].append(" " * indent + source)
                self.data["class"].append(classname)
                self.data["item"].append(indentstr + sub_indent + item)
                self.data["value"].append(str(val))

                if hasattr(val, "__slots__"):
                    self._crawl(val, indent + 1)

    @property
    def str(self) -> str:
        """
        Return result as a string.

        This will initiate a crawl

        :return:
            (str) result
        """
        return str(self)

    def print(self) -> None:
        """
        Print self

        This will initiate a crawl

        :return:
            None
        """
        print(self.str)
