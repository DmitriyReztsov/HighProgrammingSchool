from pydantic import BaseModel


class CustomException(BaseModel):
    status_code: int
    er_message: str
    er_details: str
