from typing import Callable, Dict, Any

_event_registry: Dict[str, Callable[[dict], Any]] = {}

def event_handler(event_type: str):
    def decorator(func: Callable[[dict], Any]):
        _event_registry[event_type] = func
        return func
    return decorator

def get_event_handler(event_type: str) -> Callable[[dict], Any] | None:
    return _event_registry.get(event_type)
