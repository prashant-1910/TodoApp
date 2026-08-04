from pydantic import BaseModel


class userVarification(BaseModel):
    password: str
    new_password: str
