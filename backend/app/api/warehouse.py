from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Warehouse"]
)


@router.get("/warehouses", response_model=list[WarehouseResponse])
def get_warehouses(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()


@router.post("/warehouses", response_model=WarehouseResponse)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db)
):
    new_warehouse = Warehouse(
        name=warehouse.name,
        city=warehouse.city
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse