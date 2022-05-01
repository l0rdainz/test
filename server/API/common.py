import motor.motor_asyncio
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
load_dotenv()

#connection to db established here
MONGO_DETAILS = os.getenv('MONGO_DETAILS')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.get_database('Ryde')
user_collection= db.get_collection("user_col")

#helper functions to help return response into a nice dictionary
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "Name": user["name"],
        "Userid":user["id"],
        "Email": user["Email"],
        "Description": user["description"],
        "CreatedAt": user["createdAt"],
        "Dateofbirth":user["dob"],
        "Addr":user["address"],
        "HashedPassword": user["HashedPassword"]
       
    }
