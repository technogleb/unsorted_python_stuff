"""This module implemets custom list class which can be used as dict key,
   i.e. hashable.
"""

class CustomList(list):
    def __hash__(self):
        return len(self)

custom_list = CustomList([1, 2, 3])
some_dict = {custom_list: '333'}
