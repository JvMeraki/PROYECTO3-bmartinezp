from abc import ABC, abstractmethod


class IProducto(ABC):
    
    @abstractmethod
    def calcular_costo(self):
        pass
    
    @abstractmethod
    def calcular_rentabilidad(self):
        pass
    
    @abstractmethod
    def calcular_calorias(self):
        pass
