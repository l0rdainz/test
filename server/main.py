from fastapi import FastAPI
from server.routes.user import router as userRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import pytest
from httpx import AsyncClient


tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    },

   
]
app = FastAPI(
    title="Ryde Back-end Developer",
    description="REST API and Static Web Server",
    version="0.0.1",
   
   openapi_tags=tags_metadata,
)

#need to edit this before putting into prod
origins = [
    "http://localhost:8000",
    "*"
  
    
    

]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter, tags=["User"], prefix="/user")


@app.get('/')
def redirect_web():
    return RedirectResponse('/docs')

#solely for dev purpose

