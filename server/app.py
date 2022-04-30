
from fastapi import FastAPI
from server.routes.user import router as userRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse


app = FastAPI(
    title="Ryde Back-end Developer",
    description="REST API and Static Web Server",
    version="0.0.1",
    openapi_url="/openapi.json",
    # openapi_url=None
    # docs_url=None
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081/",
    "http://127.0.0.1:8081",
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

