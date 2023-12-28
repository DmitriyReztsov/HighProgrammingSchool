from fastapi import HTTPException
from fastapi.responses import JSONResponse


# класс кастомного исключения для ошибок
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class UserNameException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


async def username_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"username": exc.detail})
