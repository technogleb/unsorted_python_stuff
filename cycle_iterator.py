class CycleIterator:
    """Iterator that infinitely loops over a collection"""

    def __init__(self, base_list):
        self.base_list = base_list
        self.length = len(base_list)
        self.counter = -1

    def __next__(self):
        if self.counter == self.length-1:
            self.counter = -1

        self.counter += 1
        return self.base_list[self.counter]


iterator = CycleIterator([1, 2, 3])

for i in range(10):
    print(next(iterator))
