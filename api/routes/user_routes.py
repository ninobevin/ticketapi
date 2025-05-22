from fastapi import APIRouter
from models.models import User
from database import user_collection

router = APIRouter()

# @router.get("/")
# async def get_users():
#     users = await user_collection.find().to_list(100)
#     return users

@router.post("/")
async def create_user(user: User):
    new_user = await user_collection.insert_one(user.dict())
    return {"message": "User created", "user_id": str(new_user.inserted_id)}

@router.get("/test")
async def test_insert():
    new_user = {
        "name" : "Auto a",
        "email" : "auto@example.a",
        "age" : 25
    }
    result = user_collection.insert_one(new_user)
    return {"message": "Test user inserted", "user_id": str(result)}