from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field
from enum import Enum



class user(BaseModel):
    name: str = Field(...)
    Email: EmailStr = Field(...)
    address: str=Field(...)
    id:str=Field(...)
    dob: str=Field(...)
    description: str=Field(...)
    HashedPassword: str = Field(...)
    createdAt: str=date.today().strftime("%d/%m/%Y")

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "Email": "jdoe@x.edu.ng",
                "address": "10 Anson Road, #17-06, International Plaza, 097903, 097903",
                "id": "l0rdainz",
                "dob":"08/03/97",
                "description":"this is a testing acc",
                "HashedPassword": 'verysercurepassword'
            }
        }


class Updateuser(BaseModel):
    name: Optional[str]
    id: Optional[str]
    dob: Optional[str]
    address: Optional[str]
    description: Optional[str]
    class Config:
        schema_extra = {
            "example": {
                "name": "New John Doe",
                "address": "SG 91237224"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
