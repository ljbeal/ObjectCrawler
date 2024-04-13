from objectcrawler.Entity import Entity


class Simple:

    __slots__ = ["name"]

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Simple({self.name})"


class TestEntity:

    simple = Simple("test")
    entity = Entity(obj=simple, assignment="entity", source="test")

    def test_assignment(self):
        assert self.entity.assignment == "entity"

    def test_source(self):
        assert self.entity.source == "test"

    def test_explicit_value(self):
        assert self.entity.value_is_explicit
