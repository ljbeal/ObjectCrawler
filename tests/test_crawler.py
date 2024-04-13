from typing import Any

from objectcrawler import Crawler


class BasicClass:

    __slots__ = ["name", "value"]

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value


class BasicSubclass(BasicClass):
    pass


class BasicExtraClass(BasicClass):
    def __init__(self, name: str, value: Any, integer: int):
        super().__init__(name, value)

        self.integer = integer
        self.extra = "extra value"


class TestCrawler:
    basic = BasicClass("test", "foo")
    basicSub = BasicSubclass("test", "bar")
    basicExtra = BasicExtraClass("test", "baz", 42)

    def test_basic_data_length(self):
        crawl = Crawler(self.basic)

        assert len(crawl.data) == 3

    def test_basic_subclass_data_length(self):
        crawl = Crawler(self.basicSub)

        assert len(crawl.data) == 3

    def test_basic_extra_data_length(self):
        crawl = Crawler(self.basicExtra)

        assert len(crawl.data) == 5

    def test_parent_assignment(self):
        crawl = Crawler(self.basic)

        assert crawl.data[1].parent == crawl.data[0]
