"""
Module holding main crawler for __slots__ based objects
"""
from objectcrawler.get_assignment import get_assignment


class SlotsCrawler:
    """
    Takes an object `obj`, and attempts to recursively crawl the __slots__
    """

    __slots__ = ["obj", "indent", "continuation", "data"]

    def __init__(self, obj):
        self.obj = obj
        self.indent = 0
        self.continuation = {0: True}
        self.data = {}

    def __str__(self):
        self._crawl(self.obj, initialise=True)

        header = []
        spacer = []
        ljust_sizes = []
        for key, vals in self.data.items():
            maxlen = max(max([len(i) for i in vals]), len(key)) + 2
            ljust_sizes.append(maxlen)

            header.append(key.ljust(maxlen))
            spacer.append("─" * maxlen)

        uspacer = "─┬─".join(spacer)
        spacer = "─┼─".join(spacer)
        header = " │ ".join(header)

        zipped = []
        for idx in range(len(self.data[key])):
            tmp = []
            for key, vals in self.data.items():
                tmp.append(vals[idx])

            zipped.append(tmp)

        output = [uspacer, header, spacer]
        for line in zipped:
            tmp = []
            for idx, item in enumerate(line):
                tmp.append(str(item).ljust(ljust_sizes[idx]))

            output.append(" │ ".join(tmp))

        return "\n".join(output)

    def _initialise_crawl(self, obj):
        self.indent = 0
        self.continuation = {0: True}

        assignment = get_assignment(obj)

        try:
            value = str(obj)
        except Exception as E:
            value = f"{type(E)}: {str(E)}"

        self.data = {
            "item": [assignment],
            "value": [value],
            "class": [obj.__class__.__name__],
            "source": [obj.__class__.__name__],
        }

    def _crawl(self, obj, indent=0, initialise=True):
        if initialise:
            self._initialise_crawl(obj)

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
                        indentstr.append("│  ")
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
                    self._crawl(val, indent + 1, initialise=False)

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
