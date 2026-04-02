from models import Tenant, TenantStatus
from sqlalchemy.orm import Session

def create_tenant(db: Session, name: str, domain: str):
    tenant = Tenant(name=name, domain=domain)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Tenant

def update_status(db: Session, tenant_id: int, status: str):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    tenant.status = status
    db.commit()
    db.refresh(tenant)
    return tenant



def get_tenant(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

from sqlalchemy.orm import Session
from models import Tenant

def get_all_tenants(db: Session):
    tenants = db.query(Tenant).all()
    return tenants



def delete_tenant(db: Session, tenant_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()
        return {"message": f"Tenant {tenant_id} deleted successfully"}
    return {"error": f"Tenant {tenant_id} not found"}
