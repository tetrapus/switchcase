# switchcase
A "better" switch statement for Python

> **WARNING**: *this isn't a serious attempt at adding switch/case to Python because it's a terrible idea, I just wanted to come up with a better syntax than https://github.com/mikeckennedy/python-switch*

## Usage
### Traditional Switch/Case
This version uses metaclasses and variable annotations to define switches. It supports all the usual stuff including fallthrough via `return False`

```python
from switchcase import Switch

class _(Switch):
    switch: 1 + 1
    def case(when: 1):
        print("Not a match")
    def case(when: 2):
        print("First match!")
    def case(when: 3):
        print("Oh no, I fell through")
        return False
    def case(when: 4):
        print("Oops! Too far!")
    def default():
        print("Not triggered")

# Prints:
# First match!
# Oh no, I fell through
# Note that the switch is run when the class is defined, you do not need to instantiate it.
```

### Context manager form without fallthrough
```python
from switchcase import select

with select as (switch, case):
    try: switch(2)
    except case(1):
        print("wrong")
    except case(2):
        print("right")
# Prints:
# right
```

### Global form without implicit default or fallthrough
```python
from switchcase import switch, case

try: switch(2)
except case(1):
    print("wrong")
except case(2):
    print("right")
else:
    pass
```
