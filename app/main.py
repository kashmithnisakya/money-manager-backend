from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.routers import expense, user, auth
from app.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(expense.router)
