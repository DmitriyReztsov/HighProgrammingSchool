from fastapi import HTTPException


# класс кастомного исключения для ошибок
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message
