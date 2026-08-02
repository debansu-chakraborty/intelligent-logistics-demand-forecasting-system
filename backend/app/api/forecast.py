from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Forecast"]
)

@router.get("/forecast")
def get_forecast():
    return {
        "warehouse": "Warehouse A",
        "forecast": [
            {
                "date": "2026-08-01",
                "predicted_demand": 250
            }
        ]
    }