from objectcrawler.entity import Entity


class Simple:

    __slots__ = ["name"]

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Simple({self.name})"


class NonString:
    pass


class TestEntity:

    objects = {"simple": Simple("test"), "nonstring": NonString()}

    entities = {k: Entity(v, assignment=k, source="test") for k, v in objects.items()}

    def test_assignment(self):
        for k, e in self.entities.items():
            assert e.assignment == k

    def test_source(self):
        for k, e in self.entities.items():
            assert e.source == "test"

    def test_classname(self):
        assert self.entities["simple"].classname == "Simple"

    def test_explicit_value(self):
        assert self.entities["simple"].value_is_explicit

    def test_non_explicit_value(self):
        assert not self.entities["nonstring"].value_is_explicit

    def test_is_not_eq(self):
        assert self.entities["simple"] != self.entities["nonstring"]

    def test_is_eq(self):
        new = Entity(Simple("test"), assignment="simple", source="test")
        assert new == self.entities["simple"]
