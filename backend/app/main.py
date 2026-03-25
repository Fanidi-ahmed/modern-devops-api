from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import SessionLocal, engine, Base
from .models import User
from .schemas import UserCreate, UserOut
import os
import redis
import json
import time
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Modern DevOps API")
Instrumentator().instrument(app).expose(app)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    attempts = 10
    for i in range(1, attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except Exception as e:
            print(f"[startup] DB not ready (attempt {i}/{attempts}): {e}")
            time.sleep(2)

    Base.metadata.create_all(bind=engine)
    print("[startup] DB ready, tables ensured.")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    r.delete("users_cache")
    return db_user

@app.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    cached = r.get("users_cache")
    if cached:
        return json.loads(cached)

    users = db.query(User).all()
    payload = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    r.setex("users_cache", 60, json.dumps(payload))
    return payload
