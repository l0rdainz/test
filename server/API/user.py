from http.client import HTTPException
from operator import gt
from server.Others.logging import APILogger
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
import jwt
from server.API.common import user_helper,user_collection
from dotenv import load_dotenv
import os
import math

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')
logger = APILogger(__name__, 'user')
#initialise logger here so that when each function is called, the logger will write to the logs.

#retrieve all users
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    logger.record("All user retrieved", "Admin Action") 
    return users

#checks for duplicate email before saving into database
# Add new user into to the database
async def add_user(user_data: dict) -> dict:
    #hash the password before saving into the database
    user_data['HashedPassword'] = bcrypt.hash(user_data["HashedPassword"])
    dup = await user_collection.find_one({"id": user_data["id"]})
    if dup:
        logger.error("add_user", user_data["id"],"Duplicate user")
        return False
  #ensure that there are no duplicate users ie unique user Id     
    else:
        user = await user_collection.insert_one(user_data)
        new_user = await user_collection.find_one({"_id": user.inserted_id})
        newuser=user_helper(new_user)
        logger.record(function="New user added", arguments=newuser['id'])
        #logger record the new user id created
        return (newuser)
#can use bcrypt.using(rounds=13).hash("password")
#change round to change salt

async def add_friend(id:str,data:str) -> dict:
    user = await user_collection.find_one({"id": id}) #first check if the userId exist
    if user:
        updated_user = await user_collection.update_one(
         {"id": id}, {"$push": {'friends':data['friends']}} #if it does add into the friendlist
    )
    if updated_user:
            logger.record(function="Friend updated", arguments=user['id']) #update with logging
            return True
    logger.error(function="add_friend", arguments=user['id'],reason="Invalid id")
    return False


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"id": id})
    if user:
        logger.record(function="User retrieved", arguments=user['id']) #log userid because it is suspicious to be fetching the same user over and over again
        return user_helper(user)
    else:       
        logger.error(function="retrieve_user", arguments=id, reason="User not found")
        raise HTTPException("user not found")

#retrieve nearby users
async def get_nearby_users(id: str) -> dict:
    user = await user_collection.find_one({"id": id})
    if user:
        
        address=user['address']
        latfloor=math.floor(address[0]) #create lowerbond for lat
        latceiling=math.ceil(address[0])  #upperbound for lat
        longfloor=math.floor(address[1])  #lowerbond for long
        longceiling=math.ceil(address[1]) #upperbound for long
        nearbyusers=[]
        async for nearbyuser in user_collection.find({"address.0":{"$gt":latfloor}} and {"address.0":{"$lt":latceiling}} and {"address.1":{"$gt":longfloor}} and {"address.1":{"$lt":longceiling}}):
            if nearbyuser["id"] in user["friends"]: #check if person is in friendlist
                nearbyusers.append(user_helper(nearbyuser)) 
            #append results into a list
        logger.record(function="Nearby users retrieved", arguments=id)
        # print(nearbyusers)
        return (nearbyusers)
    
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
            {"_id": ObjectId(id)}, {"$set": data} #update the database depending on the data sent
        )
        if updated_user:
            logger.record(function="User's detail updated", arguments=user['id']) #record the user name
            return True
    logger.error(function="update_user", arguments=user['id'],reason="Invalid id")
    return False


# Delete 
async def delete_user(id: str):
    user = await user_collection.find_one({"id": id})
    if user:
        await user_collection.delete_one({"id": id})
        logger.record("user removed", 'userid:'+ user["id"]+ "Admin action") #delete user
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

