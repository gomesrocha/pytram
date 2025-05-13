from abc import ABC, abstractmethod
from typing import Callable, Any

class BrokerAdapter(ABC):
    """
    Interface base para adaptadores de mensageria.
    """

    @abstractmethod
    async def connect(self) -> None:
        """
        Conecta ao broker de mensagens.
        """
        pass

    @abstractmethod
    async def publish(self, destination: str, message: dict) -> None:
        """
        Publica uma mensagem para um destino (fila, tópico, etc).
        """
        pass

    @abstractmethod
    async def subscribe(self, queue: str, handler: Callable[[dict], Any]) -> None:
        """
        Inscreve-se em uma fila e chama o handler ao receber mensagens.
        """
        pass
