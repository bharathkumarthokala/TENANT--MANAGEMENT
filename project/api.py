from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from auth import authenticate_user, create_access_token, get_current_user, hash_password
from models import Tenant, TenantResponse, UserCreate, UserResponse, User
from services import create_tenant, get_tenant, get_all_tenants, update_status, delete_tenant
from database import get_db

router = APIRouter()

# -------------------------------
# User registration
# -------------------------------
@router.post("/register", response_model=UserResponse, tags=["Users"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -------------------------------
# Login endpoint (JWT token)
# -------------------------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------------
# Tenant endpoints (protected)
# -------------------------------

@router.post("/tenants/", response_model=TenantResponse, tags=["Tenants"])
def create_tenant_api(
    name: str,
    domain: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return create_tenant(db, name, domain)

@router.get("/tenants/{tenant_id}", response_model=TenantResponse, tags=["Tenants"])
def get_tenant_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return get_tenant(db, tenant_id)

from typing import List

@router.get("/tenants/")
def get_all_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants

@router.put("/tenants/{tenant_id}/status", response_model=TenantResponse, tags=["Tenants"])
def update_tenant_status_api(
    tenant_id: int,
    status: TenantStatus,   # <-- restricts values
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return update_status(db, tenant_id, status.value)



    return update_status(db, tenant_id, status)

@router.delete("/tenants/{tenant_id}", response_model=dict, tags=["Tenants"])
def delete_tenant_api(
    tenant_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return delete_tenant(db, tenant_id)

from enum import Enum

class TenantStatus(str, Enum):
    active = "active"
    inactive = "inactive"

    from pydantic import BaseModel

class TenantSchema(BaseModel):
    id: int
    name: str
    domain: str
    status: str

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

