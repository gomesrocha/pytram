from pytram.registry.command import get_command_handler
from pytram.registry.event import get_event_handler

async def dispatch_message(message: dict):
    kind = message.get("kind")  # "command" ou "event"
    type_ = message.get("type")
    data = message.get("payload")

    if kind == "command":
        handler = get_command_handler(type_)
    elif kind == "event":
        handler = get_event_handler(type_)
    else:
        handler = None

    if handler:
        await handler(data)
    else:
        print(f"[WARNING] Nenhum handler registrado para: {kind}:{type_}")
