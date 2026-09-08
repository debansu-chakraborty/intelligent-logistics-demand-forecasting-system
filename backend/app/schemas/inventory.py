from pydantic import BaseModel


class InventoryCreate(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int


class InventoryUpdate(BaseModel):
    quantity: int


class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    warehouse_name: str
    product_id: int
    product_name: str
    quantity: int