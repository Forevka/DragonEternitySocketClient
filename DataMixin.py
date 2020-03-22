class DataMixin:
    @property
    def data(self):
        data = getattr(self, '_data', None)
        if data is None:
            data = {}
            setattr(self, '_data', data)
        return data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def get(self, key, default=None):
        return self.data.get(key, default)