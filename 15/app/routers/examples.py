from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.item import DBItem, Item
from app.core.database import get_db

router = APIRouter()

# 創建測試數據
@router.on_event("startup")
async def startup_event():
    from app.core.database import SessionLocal, Base, engine
    # 創建資料庫表格（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(DBItem).count() == 0:
            items = [
                DBItem(name="範例項目1", description="第一個測試項目"),
                DBItem(name="範例項目2", description="第二個測試項目")
            ]
            db.add_all(items)
            db.commit()
    finally:
        db.close()

# GET 範例 - 獲取所有項目
@router.get("/items", response_model=list[Item])
async def get_items(db: Session = Depends(get_db)):
    return db.query(DBItem).all()

# POST 範例 - 創建新項目
@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = DBItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# GET 單一項目範例
@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="項目不存在")
    return item

# PUT 範例 - 更新項目
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="項目不存在")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# DELETE 範例 - 刪除項目
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="項目不存在")
    
    db.delete(item)
    db.commit()
    return