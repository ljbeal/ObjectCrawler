from objectcrawler.get_assignment import get_assignment


class Entity:

    __slots__ = ["assignment", "parent", "classname", "value"]

    def __init__(self, obj, assignment = None, parent = ""):
        self.assignment = assignment or get_assignment(obj)
        self.parent = parent

        self.classname = obj.__class__.__name__
        self.value = str(obj)

    def table_line(self, indent=0, widths = None):
        if widths is None:
            widths = [0, 0, 0, 0]

        return (" " * indent + self.assignment.ljust(widths[0]) +
                " | " + self.value.ljust(widths[1]) +
                " | " + self.classname.ljust(widths[2]) +
                " | " + self.parent.ljust(widths[3]))
