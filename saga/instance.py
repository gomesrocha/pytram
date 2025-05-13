from typing import Optional
from sqlmodel import SQLModel, Field

class SagaInstance(SQLModel, table=True):
    id: str = Field(primary_key=True)
    saga_name: str
    state: str
    step_index: int = 0
    data: dict
