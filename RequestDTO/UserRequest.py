from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    firstName: str
    lastName: str
    role: str

    