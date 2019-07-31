class Storage:
    __storage = dict()

    def __new__(cls, name, *args, **kwargs):
        return Storage.__storage.get(name, None) or super().__new__(cls)

    def __init__(self, name):
        Storage.__storage.update({name: self})
        self.protected = set()

    def __get_attr(self):
        """
        :return: list of not protected attributes
        """
        attrs = dict(self.__dict__)
        attrs.pop('protected', None)
        for name in self.protected:
            attrs.pop(name, None)
        return list(attrs.keys())

    def clean(self, protected=False):
        if protected:
            self.__dict__.clear()
            self.protected = set()
        else:
            for key in self.__get_attr():
                delattr(self, key)

    def set_attr(self, name, value, protected=False):
        setattr(self, name, value)
        if protected:
            self.protected.add(name)

    @classmethod
    def get_storage(cls, name=None):
        item = Storage.__storage.get(name, None)
        if item:
            return item
        else:
            return Storage()


def get_storage(name=None):
    return Storage.get_storage(name)
