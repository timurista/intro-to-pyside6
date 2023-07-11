from fastapi import FastAPI
from .routers import checklist

app = FastAPI()

app.include_router(checklist.router)
