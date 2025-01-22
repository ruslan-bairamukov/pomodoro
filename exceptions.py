class UserNotFoundException(Exception):
    def __init__(
        self, message: str = "UserNotFoundException"
    ) -> None:
        self.message = message


class UserIncorrectPasswordException(Exception):
    def __init__(
        self,
        message: str = "UserIncorrectPasswordException",
    ) -> None:
        self.message = message
