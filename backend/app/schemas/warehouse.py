from pydantic import BaseModel


class WarehouseCreate(BaseModel):
    name: str
    city: str


class WarehouseResponse(BaseModel):
    id: int
    name: str
    city: str

    class Config:
        from_attributes = True