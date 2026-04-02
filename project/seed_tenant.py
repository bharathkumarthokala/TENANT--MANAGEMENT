from database import SessionLocal
from models import Tenant, TenantStatus

def seed_tenant():
    db = SessionLocal()
    try:
        # Create a sample tenant
        new_tenant = Tenant(
            name="School One",
            domain="school1",
            status=TenantStatus.active
        )
        db.add(new_tenant)
        db.commit()
        db.refresh(new_tenant)
        print("✅ Tenant inserted:", new_tenant.id, new_tenant.name, new_tenant.status)
    except Exception as e:
        print("❌ Error inserting tenant:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_tenant()

from database import SessionLocal
from models import Tenant, TenantStatus

def seed_tenants():
    db = SessionLocal()
    try:
        tenants = [
            Tenant(name="School One", domain="school1", status=TenantStatus.active),
            Tenant(name="School Two", domain="school2", status=TenantStatus.active),
            Tenant(name="School Three", domain="school3", status=TenantStatus.trial),
            Tenant(name="School Four", domain="school4", status=TenantStatus.suspended),
            Tenant(name="School Five", domain="school5", status=TenantStatus.active),
        ]
        db.add_all(tenants)
        db.commit()
        for t in tenants:
            db.refresh(t)
            print(f"✅ Inserted Tenant: ID={t.id}, Name={t.name}, Status={t.status}")
    except Exception as e:
        print("❌ Error inserting tenants:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_tenants()
