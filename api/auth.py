from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Replace with a secure authentication mechanism in production
USERS = {
    "user1": "password1"  # Dictionary of valid username-password pairs
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user1")  # Secure username comparison
    correct_password = secrets.compare_digest(credentials.password, USERS["user1"])  # Secure password comparison
    if not (correct_username and correct_password):  # If either check fails
        raise HTTPException(status_code=401, detail="Unauthorized")
