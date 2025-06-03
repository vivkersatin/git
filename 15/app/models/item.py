from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.core.database import Base  # 使用統一的 Base

# ORM 模型
class DBItem(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(200), nullable=True)

# Pydantic 模型
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True  # Pydantic V2 使用 from_attributes 替代 orm_mode