from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Replace with a secure authentication mechanism in production
USERS = {
    "user1": "password1"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user1")
    correct_password = secrets.compare_digest(credentials.password, USERS["user1"])
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
