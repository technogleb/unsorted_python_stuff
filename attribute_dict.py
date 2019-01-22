class AttributeDict(dict):
    """Upgraded dict class, which keys can be obtained as attributes"""

    def __init__(self, base_dict):
        super().__init__(base_dict)
        self.base_dict = base_dict

    def __getattr__(self, item):
        if item not in self.keys():
            return NotImplementedError
        else:
            return self[item]

upgraded_dict = AttributeDict({'a': 5, 'b': 7})
print(upgraded_dict['a'])
