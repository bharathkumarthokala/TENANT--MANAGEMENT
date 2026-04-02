from fastapi import FastAPI
import api
from models import Base
from database import engine

app = FastAPI(title="Tenant Management System", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(api.router)

@app.get("/")
def read_root():
    return {"message": "Tenant Management API is running"}

from models import Base
from database import engine

Base.metadata.create_all(bind=engine)
