class BaseError(Exception):
    pass


class TaskNotFoundError(BaseError):
    pass


class TaskError(BaseError):
    pass


class FileError(BaseError):
    pass
