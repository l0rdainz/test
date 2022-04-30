from http.client import HTTPException
from server.Others.logging import APILogger
from bson.objectid import ObjectId

from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
import jwt
from server.API.common import user_helper,user_collection
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')
logger = APILogger(__name__, 'user')


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    logger.record("All user retrieved", "Admin Action")
    return users

#checks for duplicate email before saving into database
# Add new user into to the database
async def add_user(user_data: dict) -> dict:
    user_data['HashedPassword'] = bcrypt.hash(user_data["HashedPassword"])
    dup = await user_collection.find_one({"Email": user_data["Email"]})
    if dup:
        logger.error("add_user", user_data["Email"],"Duplicate user")
        return False
        
    else:
        user = await user_collection.insert_one(user_data)
        new_user = await user_collection.find_one({"_id": user.inserted_id})
        newuser=user_helper(new_user)
        logger.record(function="New user added", arguments=newuser['Email'])
        return (newuser)
#can use bcrypt.using(rounds=13).hash("password")
#change round to change salt

# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        logger.record(function="User retrieved", arguments=user['Email'])
        return user_helper(user)
    else:       
        logger.error(function="retrieve_user", arguments=id, reason="User not found")
        raise HTTPException("user not found")

async def get_user_from_token(token: str)->dict:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        email = payload.get("Email")
        user = await user_collection.find_one({"Email": email})
        if user:
            logger.record(function="User retrieved from token", arguments=user['Email'])
            return user_helper(user)
        else:
            logger.error(function="get_user_from_token", arguments=token, reason="Token not valid")
            raise HTTPException("Error")

# Update 
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            logger.record(function="User's detail updated", arguments=user['Email'])
            return True
    logger.error(function="update_user", arguments=user['Email'],reason="Invalid id")
    return False


# Delete 
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        logger.record("user removed", user["Email"]+ "Admin action")
        return True

#Authentication
async def verify_password(password,HashedPassword):
        return bcrypt.verify(password, HashedPassword)

async def authenticate_user(username: str, password: str):
    user = await user_collection.find_one({"Email":username})
    if not user:
        logger.error(function="authenticate_user", arguments=user['Email'],reason="Invalid email")
        return False 
    password = await verify_password(password, user["HashedPassword"])
    if not password:
        logger.error(function="authenticate_user", arguments=user['Email'],reason="Invalid password")    
        return False
    logger.record(function="User has been logged in successfully", arguments=user['Email']) 
    return user

