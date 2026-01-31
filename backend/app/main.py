from fastapi import FastAPI,Depends
from app.auth import verify_firebase_token 
import User as User

app = FastAPI()

@app.get("/user")
async def get_user(decoded_token: dict = Depends(verify_firebase_token)):
    return User(
        uid = decoded_token["uid"],
        phone_number = decoded_token.get("phone_number")


    )
