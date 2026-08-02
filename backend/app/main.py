from fastapi import FastAPI

from app.api.forecast import router as forecast_router
from app.api.inventory import router as inventory_router
from app.api.simulate import router as simulate_router

from app.database.database import engine
from app.database.models import Base

app = FastAPI(
    title="Intelligent Logistics API",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(forecast_router)
app.include_router(inventory_router)
app.include_router(simulate_router)


@app.get("/")
def home():
    return {"message": "Welcome to Intelligent Logistics API"}


@app.get("/health")
def health():
    return {"status": "healthy"}