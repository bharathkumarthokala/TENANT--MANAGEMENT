from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from models import Tenant, TenantStatus

async def tenant_resolver(request: Request, db: Session):
    host = request.headers.get("host")
    tenant = db.query(Tenant).filter(Tenant.domain == host).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if tenant.status in [TenantStatus.suspended, TenantStatus.expired]:
        raise HTTPException(status_code=403, detail="Tenant inactive")
    request.state.tenant = tenant

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Tenant, TenantStatus

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db: Session = SessionLocal()

        tenant_id = None

        # 1. Try subdomain (host header)
        host = request.headers.get("host")
        if host and "." in host:
            subdomain = host.split(".")[0]
            tenant_id = subdomain

        # 2. Try custom header
        if not tenant_id:
            tenant_id = request.headers.get("X-Tenant-ID")

        # 3. Fallback: authenticated user context
        if not tenant_id and hasattr(request.state, "user"):
            tenant_id = request.state.user.tenant_id

        # 4. Resolve tenant
        tenant = None
        if tenant_id:
            tenant = db.query(Tenant).filter(Tenant.domain == tenant_id).first()

        if not tenant:
            raise HTTPException(status_code=400, detail="Tenant could not be resolved")

        if tenant.status in [TenantStatus.suspended, TenantStatus.expired]:
            raise HTTPException(status_code=403, detail="Tenant is inactive or suspended")

        # Attach tenant context
        request.state.tenant = tenant

        response = await call_next(request)
        return response
