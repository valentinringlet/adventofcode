from abc import abstractmethod, ABCMeta


class Challenge(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def solve(self):
        pass

    @classmethod
    @abstractmethod
    def id(cls):
        pass
