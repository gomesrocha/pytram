# PyTram

**PyTram** é um framework Python para orquestração de Sagas assíncronas, inspirado no [Eventuate Tram](https://eventuate.io/docs/manual/eventuate-tram/). Ele foi criado para facilitar a coordenação de transações distribuídas em sistemas baseados em microsserviços.

---

## ✨ Recursos

- Orquestração de Sagas com múltiplos passos
- Suporte a comandos e compensações
- Adaptador para RabbitMQ (via `aio-pika`)
- Repositório de Sagas em memória
- Suporte a tolerância a falhas via `pyfaulttolerance`
- Totalmente assíncrono e extensível

---

## 📦 Instalação

Você pode instalar via PyPI:

```bash
pip install pytram-saga
```

---
## 🚀 Exemplo de Uso

```python
from pytram.saga.step import SagaStep
from pytram.saga.orchestrator import SagaOrchestrator
from pytram.persistence.memory import InMemorySagaRepository
from pytram.messaging.rabbitmq import RabbitMQAdapter

async def main():
    broker = RabbitMQAdapter("amqp://user:pass@host/vhost")
    await broker.connect()

    steps = [
        SagaStep(command="step1"),
        SagaStep(command="step2", compensation="compensate_step2"),
        SagaStep(command="step3")
    ]

    repo = InMemorySagaRepository()

    orchestrator = SagaOrchestrator("MySaga", steps, broker, repo)

    await orchestrator.start("saga-001", {"user_id": 42, "amount": 100.0})

```

---

## 📚 Estrutura da Arquitetura
```
+--------------------+
|  SagaOrchestrator  |
+---------+----------+
          |
          v
+--------------------+
| SagaStep Executor  |
+---------+----------+
          |
          v
+--------------------+
|  RabbitMQAdapter   | ---> Fila de Comando (via aio-pika)
+--------------------+

Repositório: InMemorySagaRepository

```
---
## 🙋 Contribuições

Contribuições são bem-vindas! Por favor, abra um issue ou envie um pull request.