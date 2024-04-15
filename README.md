# objectcrawler

Basic and lightweight python tool for inspecting python objects.

Originally built for objects defining `__slots__`, however it also handles the `__dict__` attribute just fine.

## Installation

1) Create a fork of this repo
2) Clone the forked repo to your machine
3) Install with `pip install ObjectCrawler`

For development you can install using the pip `-e` editable flag.

Feel free to file a pull request if you make any changes!

## Usage

Inspecting an object is simple, import the `Crawler` class and feed it the object in question:

```python
from objectcrawler import Crawler
print(Crawler(...))
```

### Demo

Lets demonstrate this with a simple class:

```python
class Food:
    __slots__ = ["name"]
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Food({self.name})"
```

After creating an instance of this class, we can inspect it:

```python
from objectcrawler import Crawler
a = Food("Apple")
print(Crawler(a))
```

This will output the following table:

```
────────────┬──────────────┬────────────┬─────────
assignment  │ value        │ classname  │ source
────────────┼──────────────┼────────────┼─────────
~           │ Food(Apple)  │ Food       │ self
└─ name     │ Apple        │ str        │ Food
```

### Inheritance

The purpose of the `source` column is to display information about inheritance.

If we create a subclass, we can see this behaviour:

```python
class PreparedFood(Food):
    __slots__ = ["prep_time"]
    def __init__(self, name: str, prep_time: int):
        super().__init__(name)

        self.prep_time = prep_time

    def __repr__(self):
        return f"PreparedFood({self.name}, {self.prep_time})"

b = PreparedFood("Pasta", 10)
print(Crawler(b))
```

Giving the following table. Note the `source` column:

```
──────────────┬──────────────────────────┬───────────────┬───────────────
assignment    │ value                    │ classname     │ source
──────────────┼──────────────────────────┼───────────────┼───────────────
~             │ PreparedFood(Pasta, 10)  │ PreparedFood  │ None
├─ prep_time  │ 10                       │ int           │ PreparedFood
└─ name       │ Pasta                    │ str           │ Food
```

### Iterators

Iterators are a special case, since they are implicit storage containers, an attempt is made to "unpack" them into the data tree.

lists, tuples, etc. wil have their `assignment` set to the index

dicts, OrderedDicts, etc. will have their `assignment` set to the key (the object must provide a `iter()` method for this functionality)

```python
class Meal:
    __slots__ = ["name", "ingredients"]
    def __init__(self, name: str, ingredients: list):
        self.name = name
        self.ingredients = ingredients

ingredients = [
    Food("Cheese"),
    PreparedFood("Beans", 10),
    PreparedFood("Toast", 5)
]

c = Meal("Cheesy Beans on Toast", ingredients)
print(Crawler(c))
```

```
────────────────────┬───────────────────────────────────────────┬───────────────┬───────────────
assignment          │ value                                     │ classname     │ source
────────────────────┼───────────────────────────────────────────┼───────────────┼───────────────
~                   │ <__main__.Meal object at 0x762f4d65de10>  │ Meal          │ None
├─ name             │ Cheesy Beans on Toast                     │ str           │ Meal
└─ ingredients      │ iterable: list                            │ list          │ Meal
│  ├─ 0             │ Food(Cheese)                              │ Food          │ Meal
│  │  └─ name       │ Cheese                                    │ str           │ Food
│  ├─ 1             │ PreparedFood(Beans, 10)                   │ PreparedFood  │ Meal
│  │  ├─ prep_time  │ 10                                        │ int           │ PreparedFood
│  │  └─ name       │ Beans                                     │ str           │ Food
│  └─ 2             │ PreparedFood(Toast, 5)                    │ PreparedFood  │ Meal
│  │  ├─ prep_time  │ 5                                         │ int           │ PreparedFood
│  │  └─ name       │ Toast                                     │ str           │ Food
```

## Differences

If you're trying to debug a class and have one working example of it, you can quickly find the issues by differencing it with a broken version. To do this, you should create two Crawler instances (one working, and one not). You can then "subtract" these objects to reveal the differences.

```python
a = Object(...)
b = Object(...)

crawl_a = Crawler(a)
crawl_b = Crawler(b)

print(crawl_a - crawl_b)
```

This will print out two joined tables with the differences highlighted in red.

## Debug

If you don't trust the output there exists a debug mode for the print which can help you figure out what's going on.

To activate this we should create the actual `Crawler` object and store it in a variable:

```python
crawl = Crawler(c)
```
We can then print the info using the `print()` method. This can take extra args, including `debug`

```python
crawl.print(debug=True)
```

```
────────────────────┬───────────────────────────────────────────┬───────────────┬───────────────┬───────────────────┬───────────────────┬───────────
assignment          │ value                                     │ classname     │ source        │ entity            │ parent            │ nchildren
────────────────────┼───────────────────────────────────────────┼───────────────┼───────────────┼───────────────────┼───────────────────┼───────────
~                   │ <__main__.Meal object at 0x762f4d65de10>  │ Meal          │ None          │ Entity #47004730  │ None              │ 2
├─ name             │ Cheesy Beans on Toast                     │ str           │ Meal          │ Entity #91735648  │ Entity #47004730  │ 0
└─ ingredients      │ iterable: list                            │ list          │ Meal          │ Entity #43691166  │ Entity #47004730  │ 3
│  ├─ 0             │ Food(Cheese)                              │ Food          │ Meal          │ Entity #27979510  │ Entity #43691166  │ 1
│  │  └─ name       │ Cheese                                    │ str           │ Food          │ Entity #27472819  │ Entity #27979510  │ 0
│  ├─ 1             │ PreparedFood(Beans, 10)                   │ PreparedFood  │ Meal          │ Entity #62084209  │ Entity #43691166  │ 2
│  │  ├─ prep_time  │ 10                                        │ int           │ PreparedFood  │ Entity #04848920  │ Entity #62084209  │ 0
│  │  └─ name       │ Beans                                     │ str           │ Food          │ Entity #13535757  │ Entity #62084209  │ 0
│  └─ 2             │ PreparedFood(Toast, 5)                    │ PreparedFood  │ Meal          │ Entity #55272230  │ Entity #43691166  │ 2
│  │  ├─ prep_time  │ 5                                         │ int           │ PreparedFood  │ Entity #32701778  │ Entity #55272230  │ 0
│  │  └─ name       │ Toast                                     │ str           │ Food          │ Entity #67167938  │ Entity #55272230  │ 0
```

### Debug output

To understand what we're seeing here it can be helpful to know what's going on inside this table.

Each row is represented by an `Entity` object. This stores some information about each attribute of the original object, but most importantly it stores the hierarchy of children.

The extra columns added expose this information.

The `entity` column contains part of the hash for the `Entity` in _that row_.

The `parent` column contains part of the hash for the `Entity` that _provided_ the `Entity` in that row.

The `nchildren` column is a counter of how many children that entity has, and is used for tree generation.

## Formatting

Similar to the debug, `print()` can also take some basic formatting arguments, `whitespace` and `branch_len`.

`whitespace` dictates the amount of padding added to the end of each column, whereas `branch_len` controls the length of each "branch" in the tree.

The best way to understand these args is to demonstrate them:

### whitespace

```python
crawl.print(whitespace=10)
```

```
────────────────────────────┬───────────────────────────────────────────────────┬───────────────────────┬───────────────────────
assignment                  │ value                                             │ classname             │ source
────────────────────────────┼───────────────────────────────────────────────────┼───────────────────────┼───────────────────────
~                           │ <__main__.Meal object at 0x762f4d65de10>          │ Meal                  │ None
├─ name                     │ Cheesy Beans on Toast                             │ str                   │ Meal
└─ ingredients              │ iterable: list                                    │ list                  │ Meal
│  ├─ 0                     │ Food(Cheese)                                      │ Food                  │ Meal
│  │  └─ name               │ Cheese                                            │ str                   │ Food
│  ├─ 1                     │ PreparedFood(Beans, 10)                           │ PreparedFood          │ Meal
│  │  ├─ prep_time          │ 10                                                │ int                   │ PreparedFood
│  │  └─ name               │ Beans                                             │ str                   │ Food
│  └─ 2                     │ PreparedFood(Toast, 5)                            │ PreparedFood          │ Meal
│  │  ├─ prep_time          │ 5                                                 │ int                   │ PreparedFood
│  │  └─ name               │ Toast                                             │ str                   │ Food


```

### branch_len

```python
crawl.print(branch_len=4)
```

```
─────────────────────────────┬───────────────────────────────────────────┬───────────────┬───────────────
assignment                   │ value                                     │ classname     │ source
─────────────────────────────┼───────────────────────────────────────────┼───────────────┼───────────────
~                            │ <__main__.Meal object at 0x762f4d65de10>  │ Meal          │ None
├──── name                   │ Cheesy Beans on Toast                     │ str           │ Meal
└──── ingredients            │ iterable: list                            │ list          │ Meal
│     ├──── 0                │ Food(Cheese)                              │ Food          │ Meal
│     │     └──── name       │ Cheese                                    │ str           │ Food
│     ├──── 1                │ PreparedFood(Beans, 10)                   │ PreparedFood  │ Meal
│     │     ├──── prep_time  │ 10                                        │ int           │ PreparedFood
│     │     └──── name       │ Beans                                     │ str           │ Food
│     └──── 2                │ PreparedFood(Toast, 5)                    │ PreparedFood  │ Meal
│     │     ├──── prep_time  │ 5                                         │ int           │ PreparedFood
│     │     └──── name       │ Toast                                     │ str           │ Food


```
