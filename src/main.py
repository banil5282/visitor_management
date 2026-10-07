from fastapi import FastAPI
from .week1 import routes as week1_routes
from .week2 import routes as week2_routes
import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app = FastAPI(title="Visitor Management")

# Include routes from all weeks
app.include_router(week1_routes.router)
app.include_router(week2_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Visitor Management"}

__all__ = ["app"]
