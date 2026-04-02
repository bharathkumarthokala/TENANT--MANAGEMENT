from database import SessionLocal
from models import Tenant

def test_connection():
    db = SessionLocal()
    try:
        # Try a simple query
        tenants = db.query(Tenant).all()
        print("✅ Database connected successfully!")
        print("Tenants found:", tenants)
    except Exception as e:
        print("❌ Database connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()