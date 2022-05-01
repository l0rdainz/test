from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum



class user(BaseModel):
    name: str = Field(...)
    Email: EmailStr = Field(...)
    address: list=Field(...) #expect a list eg [-80.3411,100.2312]
    id:str=Field(...)
    dob: str=Field(...)
    description: str=Field(...)
    HashedPassword: str = Field(...)
    createdAt: str=date.today().strftime("%d/%m/%Y")
    friends: Optional[list]
    
    @validator ("address")
    def valid_add(cls,value):
        if value[0] > -90 and value[0] <90 and value[1] > -180 and value [1] < 180 :
            return value
        else:
            raise ValueError('Invalid GPS Cordinates')

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "Email": "jdoe@x.edu.ng",
                "address": [-80.3411,100.2312],
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

def ResponseModel(data, message): #if successful return response code 200
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

#else return error 404 or smth