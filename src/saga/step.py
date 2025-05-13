class SagaStep:
    def __init__(self, command: str, compensation: str = None):
        self.command = command
        self.compensation = compensation
