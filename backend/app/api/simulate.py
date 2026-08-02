from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Simulation"]
)

@router.post("/simulate")
def simulate():
    return {
        "message": "Simulation completed successfully"
    }
