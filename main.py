import asyncio
from pytram.saga.orchestrator import SagaOrchestrator
from pytram.saga.step import SagaStep
from pytram.persistence.memory import InMemorySagaRepository
from pytram.messaging.rabbitmq import RabbitMQAdapter
from dispatcher import dispatch_message
from pytram.registry.command import command_handler

@command_handler("CreateOrder")
async def create_order(data: dict):
    print("[COMANDO] Criando pedido:", data)

@command_handler("ReservePayment")
async def reserve_payment(data: dict):
    print("[COMANDO] Reservando pagamento:", data)

@command_handler("NotifyUser")
async def notify_user(data: dict):
    print("[COMANDO] Notificando usuário:", data)

@command_handler("CancelOrder")
async def cancel_order(data: dict):
    print("[COMPENSAÇÃO] Cancelando pedido:", data)

@command_handler("CancelPayment")
async def cancel_payment(data: dict):
    print("[COMPENSAÇÃO] Cancelando pagamento:", data)

async def main():
    broker = RabbitMQAdapter("amqp://guest:guest@localhost/")
    await broker.connect()

    # Inscreve consumidor para cada comando
    await broker.subscribe("CreateOrder", dispatch_message)
    await broker.subscribe("ReservePayment", dispatch_message)
    await broker.subscribe("NotifyUser", dispatch_message)
    await broker.subscribe("CancelOrder", dispatch_message)
    await broker.subscribe("CancelPayment", dispatch_message)

    # Define os passos da saga
    steps = [
        SagaStep("CreateOrder", "CancelOrder"),
        SagaStep("ReservePayment", "CancelPayment"),
        SagaStep("NotifyUser")
    ]

    repo = InMemorySagaRepository()
    orchestrator = SagaOrchestrator("CreateOrderSaga", steps, broker, repo)

    # Inicia a saga com ID e payload
    await orchestrator.start("saga-001", {"order_id": 99, "amount": 150.0})

if __name__ == "__main__":
    asyncio.run(main())
