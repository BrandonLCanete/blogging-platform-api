class CustomException(Exception):
    """Base Custom Exception."""
    pass

class ValidationException(Exception):
    """Raised for validation errors, including ENUM or data constraints."""
    def __init__(self, field, message="Invalid value"):
        self.message = f"{message} for field '{field}'"
        super().__init__(self.message)


class NotFoundException(CustomException):
    def __init__(self, resource, identifier):
        self.message = f"{resource} not found with identifier: {identifier}"
        super().__init__(self.message)


class ConflictException(CustomException):
    def __init__(self, resource, field, value):
        self.message = f"{resource} already exists with {field}: {value}"
        super().__init__(self.message)


class GenericException(CustomException):
    def __init__(self, message="Something went wrong"):
        self.message = message
        super().__init__(self.message)
