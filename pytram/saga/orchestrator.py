from typing import List
from pytram.saga.step import SagaStep
from pytram.saga.instance import SagaInstance
from pytram.persistence.memory import InMemorySagaRepository
from pytram.messaging.base import BrokerAdapter
from pyfaulttolerance.retry_async import retry_async
from pyfaulttolerance.circuit_breaker import circuit_breaker_async
from pyfaulttolerance.circuit_breaker import circuit_breaker

class SagaOrchestrator:
    def __init__(self, name: str, steps: List[SagaStep], broker: BrokerAdapter, repo: InMemorySagaRepository):
        self.name = name
        self.steps = steps
        self.broker = broker
        self.repo = repo

    @retry_async()
    @circuit_breaker_async()
    async def start(self, saga_id: str, data: dict):
        instance = SagaInstance(
            id=saga_id,
            saga_name=self.name,
            state="STARTED",
            step_index=0,
            data=data
        )
        await self.repo.save(instance)
        await self._execute_step(instance)

    async def _execute_step(self, instance: SagaInstance):
        if instance.step_index >= len(self.steps):
            instance.state = "COMPLETED"
            await self.repo.update(instance)
            return

        step = self.steps[instance.step_index]
        try:
            await self.broker.publish(step.command, instance.data)
            instance.step_index += 1
            await self.repo.update(instance)
            await self._execute_step(instance)
        except Exception as e:
            if step.compensation:
                await self._compensate(instance)
            instance.state = "FAILED"
            await self.repo.update(instance)

    async def _compensate(self, instance: SagaInstance):
        for i in reversed(range(instance.step_index)):
            step = self.steps[i]
            if step.compensation:
                await self.broker.publish(step.compensation, instance.data)
