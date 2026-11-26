from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (সব টেবিল লোড করে)
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, users, projects, skills, messages

# ডাটাবেসে টেবিল তৈরি
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API")

# যে ফ্রন্টএন্ড গুলো ব্যাকএন্ডে রিকোয়েস্ট পাঠাতে পারবে
allowed_origins = [
    "http://localhost:3000",
    settings.frontend_url.rstrip("/"),  # শেষের / বাদ
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Vercel প্রিভিউ URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# রাউটার
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(messages.router)


@app.get("/")
def home():
    return {"message": "Portfolio API is running"}


# চালানোর কমান্ড: uvicorn main:app --port 8001 --reload