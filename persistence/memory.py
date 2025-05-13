from typing import Dict
from pytram.saga.instance import SagaInstance

class InMemorySagaRepository:
    def __init__(self):
        self._store: Dict[str, SagaInstance] = {}

    async def save(self, instance: SagaInstance):
        self._store[instance.id] = instance

    async def update(self, instance: SagaInstance):
        self._store[instance.id] = instance

    async def get(self, saga_id: str) -> SagaInstance:
        return self._store.get(saga_id)
