from typing import Callable, Dict, Any

_command_registry: Dict[str, Callable[[dict], Any]] = {}

def command_handler(command_type: str):
    def decorator(func: Callable[[dict], Any]):
        _command_registry[command_type] = func
        return func
    return decorator

def get_command_handler(command_type: str) -> Callable[[dict], Any] | None:
    return _command_registry.get(command_type)
