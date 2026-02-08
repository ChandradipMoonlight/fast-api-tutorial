from pydantic import BaseModel, EmailStr, Field
from app.models.user import User
# this is the request schema for the user
class UserRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=100, description="Age must be between 0 and 100", default=18)
    password: str = Field(min_length=8, max_length=100, description="Password must be between 8 and 100 characters")

    def to_model(self):
        return User(name=self.name, email=self.email, age=self.age, password=self.password)

    def is_valid(self):
        if not self.name:
            raise ValueError("Name is required")    
        if not self.email:
            raise ValueError("Email is required")
        if not self.age:
            raise ValueError("Age is required")
        if not self.password:
            raise ValueError("Password is required")
        return True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    password: str

    @classmethod
    def from_model(cls, user: User):
        return cls(id=user.id, name=user.name, email=user.email, age=user.age, password=user.password)