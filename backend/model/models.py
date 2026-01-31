from pydantic import BaseModel

class MessageIn(BaseModel):
    user_id:str
    message_text:str