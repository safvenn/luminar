from fastapi import Depends,HTTPException
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")



Api_header = APIKeyHeader(name='X-API-Key')
def verify_auth(API=Depends(Api_header)):
    if API != API_KEY:
        raise HTTPException(status_code=404,detail="Not authenticated")
    
    return API


    