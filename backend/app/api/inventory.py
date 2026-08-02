from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Inventory"]
)

@router.get("/inventory/rebalance")
def rebalance_inventory():
    return {
        "recommendation": "Transfer 100 units from Warehouse A to Warehouse B"
    }