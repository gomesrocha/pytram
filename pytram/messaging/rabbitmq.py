import aio_pika
import json
from typing import Callable, Any
from .base import BrokerAdapter

class RabbitMQAdapter(BrokerAdapter):
    """
    Implementação do BrokerAdapter usando RabbitMQ com o aio-pika.
    """

    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def publish(self, destination: str, message: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({
                    "kind": "command",
                    "type": destination,
                    "payload": message
                }).encode()
            ),
            routing_key=destination
        )

    async def subscribe(self, queue: str, handler: Callable[[dict], Any]):
        q = await self.channel.declare_queue(queue, durable=True)

        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                body = json.loads(message.body.decode())
                await handler(body)

        await q.consume(callback)
