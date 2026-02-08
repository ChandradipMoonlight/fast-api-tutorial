# user schema

from sqlmodel import Field, SQLModel, Session, select

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    age: int = Field(nullable=False)
    password: str = Field(nullable=False)

    def create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
    
    def update(self, user_data, session: Session):
        for key, value in user_data.model_dump(exclude={'id'}).items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
    
    def delete(self, session: Session):
        session.delete(self)
        session.commit()
        return self

    @classmethod
    def get_all_with_pagination(cls, session: Session, page: int = 1, page_size: int = 10):
        return session.exec(select(cls).order_by(cls.id.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    
    @classmethod
    def get_all(cls, session: Session):
        return session.exec(select(cls).order_by(cls.id.desc())).all()
    
    @classmethod
    def get_by_id(cls, session: Session, id: int):
        return session.exec(select(cls).where(cls.id == id)).first()

    @classmethod
    def get_by_email(cls, session: Session, email: str):
        return session.exec(select(cls).where(cls.email == email)).first()

    
   