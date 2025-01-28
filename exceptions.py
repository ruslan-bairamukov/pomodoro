class UserNotFoundError(Exception):
    def __init__(
        self, message: str = "UserNotFoundError"
    ) -> None:
        self.message = message


class IncorrectPasswordError(Exception):
    def __init__(
        self,
        message: str = "IncorrectPasswordError",
    ) -> None:
        self.message = message


class InvalidJWTTokenError(Exception):
    def __init__(
        self,
        message: str = "InvalidJWTTokenError",
    ) -> None:
        self.message = message


class TaskNotFoundError(Exception):
    def __init__(
        self,
        message: str = "TaskNotFoundError",
    ) -> None:
        self.message = message
