from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# класс кастомного исключения для ошибок
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class UserNameException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400, message: str = None, **kwargs):
        super().__init__(status_code=status_code, detail=detail, **kwargs)
        self.message = message


async def username_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"username": exc.detail})


async def http_exception_handler(request, exc: RequestValidationError):
    # return PlainTextResponse(str(exc), status_code=422)
    return JSONResponse(content=jsonable_encoder(exc.errors()), status_code=422)


async def user_not_found_handler(request, exc: Exception):
    return JSONResponse(status_code=exc.status_code, content={exc.detail: exc.message}, headers=exc.headers)
