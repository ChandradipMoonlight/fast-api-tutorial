from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix = "/users", tags=["Users API"])


class User(BaseModel):
    id: int
    name: str
    age: int

user_data = [
    User(id = 1, name = "Ram", age =21),
    User(id = 2, name = "Krushna", age = 20)
]


@router.get("/")
def get_all_users():
    return {
        "success" : True,
        "data" : user_data
    }


@router.post("/add")
async def add_user_data(user : User):
    user_data.append(user)
    return {
        "success" : True,
        "message" : "user data added successfully"
    }

def check_auth():
    raise HTTPException(status_code = 401, detail="Unauthorized")

@router.get("/exception")
def exception_test(auth = Depends(check_auth)):
    return "you will never see this"

@router.get("/{id}")
def get_user_by_id(id: int):
    for user in user_data:
        if(user.id == id):
            return {
                "success" : True,
                "data" : user
            }
    return {
        "success" : False,
        "message" : f"user data not found for given user Id : {id}"
    }