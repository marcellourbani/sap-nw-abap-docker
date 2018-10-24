"""Mock pyrfc for testing"""


class Connection(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self, function_module, **kwargs):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass
