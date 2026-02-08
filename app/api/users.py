from fastapi import APIRouter, HTTPException, Query, status, Path
from app.schemas.user import UserResponse, UserRequest
from app.models.user import User
from app.core.database import SessionDep
from typing import Annotated, List
router = APIRouter(prefix = "/users", tags=["Users API"])

"""
This is the endpoint to create a new user
It takes a UserRequest object and returns a UserResponse object
It returns a 201 Created status code if the user is created successfully
It returns a 400 Bad Request status code if the user is not created successfully
"""
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserRequest, session: SessionDep) -> UserResponse:
    # check if the user already exists
    if User.get_by_email(session, user_request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    # check if the user is valid
    if not user_request.is_valid():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user request")
    user = user_request.to_model()
    user.create(session)
    return UserResponse.from_model(user)

"""
This is the endpoint to get all users with pagination
It returns a list of UserResponse objects
It takes two optional parameters: page and page_size
Page is the page number and page_size is the number of users per page
If no page or page_size is provided, it defaults to 1 and 10 respectively
"""
@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users_with_pagination(session: SessionDep, page: Annotated[int, Query()] =1, page_size: Annotated[int, Query(le=100)] =10) -> List[UserResponse]:
    users = User.get_all_with_pagination(session, page, page_size)
    return [UserResponse.from_model(user) for user in users]

"""
This is the endpoint to get a user by id
It returns a UserResponse object
It takes one required parameter: id
"""
@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, session: SessionDep) -> UserResponse:
    user = User.get_by_id(session, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_model(user)

"""
This is the endpoint to get a user by email
It returns a UserResponse object
It takes one required parameter: email
"""
@router.get("/email/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_email(email: Annotated[str, Path(min_length=3, max_length=100)], session: SessionDep) -> UserResponse:
    user = User.get_by_email(session, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_model(user)

"""
This is the endpoint to update a user
It returns a UserResponse object
It takes one required parameter: id
"""
@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, user_request: UserRequest, session: SessionDep) -> UserResponse:
    user = User.get_by_id(session, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user_request.is_valid():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user request")
    user.update(user_request, session)
    return UserResponse.from_model(user)

"""
This is the endpoint to delete a user
It returns a UserResponse object
It takes one required parameter: id
"""
@router.delete("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(id: int, session: SessionDep) -> UserResponse:
    user = User.get_by_id(session, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.delete(session)
    return UserResponse.from_model(user)