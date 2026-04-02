from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class TenantStatus(enum.Enum):
    active = "active"
    suspended = "suspended"
    trial = "trial"
    expired = "expired"
    archived = "archived"

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)   # School name
    domain = Column(String, unique=True)             # Subdomain/custom domain
    status = Column(Enum(TenantStatus), default=TenantStatus.trial)


from pydantic import BaseModel
from typing import Optional

class TenantBase(BaseModel):
    name: str
    domain: str
    status: str

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int

    class Config:
        orm_mode = True


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# Database User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True   # replaces orm_mode in Pydantic v2

from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from database import Base

class TenantStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    trial = "trial"
    expired = "expired"
    archived = "archived"

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String, unique=True, index=True)
    status = Column(SqlEnum(TenantStatus), default=TenantStatus.active)

from database import Base

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
