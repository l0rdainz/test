from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import datetime 
import json


JWT_SECRET = '7889ecd3b023c325b8a7852268eb85c339df5da29f9cbc0ce5e381ebdac58767'
#put in .env file then generate smth more secure using openssl rand -hex 32

from server.API.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    authenticate_user,
    get_user_from_token,
    get_nearby_users,
    add_friend
)
from server.schema.user import (
    ErrorResponseModel,
    ResponseModel,
    Updateuser,
    user,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
router = APIRouter()

#Different Api endpoints
@router.post("/create", response_description="user data added into the database")
async def add_user_data(user: user = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if new_user == False:
         raise HTTPException(
            status_code=404,
            detail="Duplicate User ID",        
        )
    else:
        return ResponseModel(new_user, "Added successfully.")

#note it is encoded by not encrypted yet!!!, need to ensure that jwt does not contain sensitive information 
#else, shld sign then encrypt
@router.post('/token',response_description="Successfully authenticated")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    del user["_id"]
    del user["HashedPassword"]
    user['exp']= (datetime.datetime.now() + datetime.timedelta(minutes=30))
    #change token expiry here
    token = jwt.encode(user, JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}

@router.get('/getuser',response_description="Successfully authenticated")
async def get_user(token= Depends(oauth2_scheme)):
    try:
        user= await get_user_from_token (token)
        del user["HashedPassword"]
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/all", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "No users found")

@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

@router.get("/nearby/{id}", response_description="Nearby users retrieved")
async def get_user_data(id):
    users = await get_nearby_users(id)
    if users:
        return ResponseModel(users, "Nearby users retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

@router.put("/update/{id}")
async def update_user_data(id: str, req: Updateuser = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} has been updated successfully".format(id),
            "updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the data.",
    )
@router.put("/friend/{id}")
async def update_user_friend_data(id: str, req: Updateuser = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await add_friend(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} has been updated successfully".format(id),
            "updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the data.",
    )

@router.delete("/delete/{id}", response_description="User data removed from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
