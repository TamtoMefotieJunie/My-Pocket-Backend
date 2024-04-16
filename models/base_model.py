from abc import ABC,abstractmethod

class AbstractBaseClass(ABC):

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def delete(self):
        pass