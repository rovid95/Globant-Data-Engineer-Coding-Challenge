from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from database import SessionLocal
import models, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    column_names = ["id", "name", "hire_date", "department_id", "job_id"]
    df = pd.read_csv(file.file, header=None, names=column_names)
    records = df.to_dict(orient="records")
    print("Parsed records:", records)

    db.bulk_insert_mappings(models.Employee, records)
    db.commit()
    return {"message": "Data uploaded successfully", "rows_inserted": len(records)}


@router.post("/batch_insert/")
async def batch_insert(data: list[schemas.EmployeeCreate], db: Session = Depends(get_db)):
    if len(data) > 1000:
        raise HTTPException(status_code=400, detail="Max 1000 rows allowed.")

    db.bulk_save_objects([models.Employee(**item.dict()) for item in data])
    db.commit()
    return {"message": "Batch inserted successfully", "rows_inserted": len(data)}


@router.get("/all/")
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@router.delete("/clear/")
def clear_employees(db: Session = Depends(get_db)):
    db.query(models.Employee).delete()
    db.commit()
    return {"message": "Employee table cleared"}
