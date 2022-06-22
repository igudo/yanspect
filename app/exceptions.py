from fastapi.exceptions import HTTPException
from models import StatusCode


class NotFoundException(HTTPException):
    def __init__(self, detail, *args):
        super().__init__(StatusCode.NOT_FOUND_404, detail, *args)
