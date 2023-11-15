from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import degreeAdding,degreeVerifying,student
from config import settings
import uvicorn
import models
from database import engine

origins = [f"https://{settings.host_domain}"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(degreeAdding.router)
app.include_router(degreeVerifying.router)
app.include_router(student.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)