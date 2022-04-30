import motor.motor_asyncio
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
load_dotenv()

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
# name: str = Field(...)
#     Email: EmailStr = Field(...)
#     address: str=Field(...)
#     id:str=Field(...)
#     dob: str=Field(...)
#     description: str=Field(...)
#     HashedPassword: str = Field(...)
#     createdAt: str=date.today().strftime("%d/%m/%Y")

def job_helper(job) -> dict:
    return {
        "id": str(job["_id"]),
        "Numhours": job["Numhours"],
        "Cell": job["Cell"],
        "Size": job["Size"],
        "Medium": job["Medium"],
        "Replicates": job["Replicates"],
        "Tempmin": job["Tempmin"],
        "Tempmax": job["Tempmax"],
        "Tempinc": job["Tempinc"],
        "Status": job["Status"],
        'Expreq':job["Expreq"],
        "Experimentid": job['Experimentid'],
        "Bioreactorsreq": job['Bioreactorsreq'],
        "Bioreactorids": job['Bioreactorids'],
        "Userid": job['Userid'],
        'Schema':job['Schema'],
        'Alias':job['Alias'],
        'Comments':job['Comments'],
        'location':job['location'],
        'Antibiotics':job['Antibiotics'],
        'Serum':job["Serum"]
      
    }

def exp_helper(exp) -> dict:
    return {
        "id": str(exp["_id"]),
        "Numhours": exp["Numhours"],
        "Size": exp["Size"],
        "Medium": exp["Medium"],
        "Status": exp["Status"],
        "Cell": exp["Cell"],
        "Setpoint": exp["Setpoint"],
        "Currentreading": exp["Currentreading"],
        "Currenttime":exp["Currenttime"],
        "Timestarted": exp['Timestarted'],
        "BioreactorID": exp["BioreactorID"],
        "WellID": exp["WellID"],
        "SensorID": exp["SensorID"],
        "UserID":exp['Userid'],
        "JobID":exp['Jobid'],
        'Schema':exp['Schema'],
        'Antibiotics':exp['Antibiotics'],
        'Serum':exp["Serum"]
    }


def bioreactor_helper(br) -> dict:
    return {
        "id": str(br["_id"]),
        "JobID": br["Jobid"],
        "ExperimentID": br["Experimentid"],
        "WellID": br["Wellid"],
        "SensorID": br["Sensorid"],
        "Setpoints":br['Setpoints'],
        "Status":br["Status"],
        'Cell': br['Cell'],
    'Medium': br["Medium"],
    'Numhours': br["Numhours"],
    'location':br['location'],
    'Schema':br['Schema'],
    'Antibiotics':br['Antibiotics'],
    'Serum':br['Serum']
    }

def mat_helper(mat) -> dict:
    return {
        "id": str(mat["_id"]),
        "Cell": mat["Cell"],
        "Medium": mat["Medium"],
        'Schema':mat['Schema'],
        'Antibiotics':mat['Antibiotics'],
        'Serum':mat['Serum']
    }


def bug_helper(bug) -> dict:
    return {
        "id": str(bug["_id"]),
        "URL": bug["URL"],
        "OS": bug["OS"],
        "Browser":bug['Browser'],
        "Category":bug['Category'],
        'Description':bug['Description'],
        'Schema':bug['Schema'],
        'Userid':bug["Userid"]
    }
