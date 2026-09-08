from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Inventory, Warehouse, Product
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
)

router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"]
)


@router.post("/", response_model=InventoryResponse)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    warehouse = db.query(Warehouse).filter(
        Warehouse.id == inventory.warehouse_id
    ).first()

    product = db.query(Product).filter(
        Product.id == inventory.product_id
    ).first()

    if not warehouse or not product:
        raise HTTPException(
            status_code=400,
            detail="Invalid warehouse_id or product_id"
        )

    new_inventory = Inventory(
        warehouse_id=inventory.warehouse_id,
        product_id=inventory.product_id,
        quantity=inventory.quantity
    )

    try:
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return {
            "id": new_inventory.id,
            "warehouse_id": new_inventory.warehouse_id,
            "warehouse_name": warehouse.name,
            "product_id": new_inventory.product_id,
            "product_name": product.name,
            "quantity": new_inventory.quantity
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid warehouse_id or product_id"
        )


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    inventory.quantity = inventory_update.quantity

    db.commit()
    db.refresh(inventory)

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == inventory.warehouse_id
    ).first()

    product = db.query(Product).filter(
        Product.id == inventory.product_id
    ).first()

    return {
        "id": inventory.id,
        "warehouse_id": inventory.warehouse_id,
        "warehouse_name": warehouse.name,
        "product_id": inventory.product_id,
        "product_name": product.name,
        "quantity": inventory.quantity
    }


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    db.delete(inventory)
    db.commit()

    return {
        "message": "Inventory item deleted successfully"
    }


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    inventory_items = (
        db.query(Inventory, Warehouse, Product)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .join(Product, Inventory.product_id == Product.id)
        .all()
    )

    return [
        {
            "id": inventory.id,
            "warehouse_id": inventory.warehouse_id,
            "warehouse_name": warehouse.name,
            "product_id": inventory.product_id,
            "product_name": product.name,
            "quantity": inventory.quantity
        }
        for inventory, warehouse, product in inventory_items
    ]