# objectcrawler

Basic and lightweight python tool for inspecting small python classes exposing `__slots__`

## Installation

1) Create a fork of this repo
2) Clone the forked repo to your machine
3) Install with `pip install ObjectCrawler`

For development you can install using the pip `-e` editable flag.

Feel free to file a pull request if you make any changes!

## Usage

Inspecting an object is simple, import the `SlotsCrawler` class and feed it the object in question:

```python
from objectcrawler import SlotsCrawler
print(SlotsCrawler(...))
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
from objectcrawler import SlotsCrawler
a = Food("Apple")
print(SlotsCrawler(a))
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
print(SlotsCrawler(b))
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

Iterators are a special case, since they are implicit storage containers, an attempt is made to "unpack" them into the data tree

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
print(SlotsCrawler(c))
```

```
────────────────────┬───────────────────────────────────────────┬───────────────┬───────────────
assignment          │ value                                     │ classname     │ source        
────────────────────┼───────────────────────────────────────────┼───────────────┼───────────────
~                   │ <__main__.Meal object at 0x7f4c9448d720>  │ Meal          │ None          
├─ name             │ Cheesy Beans on Toast                     │ str           │ Meal          
└─ ingredients      │ iterable: list                            │ list          │ Meal          
│  └─ 0             │ Food(Cheese)                              │ Food          │ Meal          
│  │  └─ name       │ Cheese                                    │ str           │ Food          
│  └─ 1             │ PreparedFood(Beans, 10)                   │ PreparedFood  │ Meal          
│  │  ├─ prep_time  │ 10                                        │ int           │ PreparedFood  
│  │  └─ name       │ Beans                                     │ str           │ Food          
│  └─ 2             │ PreparedFood(Toast, 5)                    │ PreparedFood  │ Meal          
│  │  ├─ prep_time  │ 5                                         │ int           │ PreparedFood  
│  │  └─ name       │ Toast                                     │ str           │ Food          
```

