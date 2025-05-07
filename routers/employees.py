from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
import pandas as pd
from database import SessionLocal
import models, schemas
from sqlalchemy import text

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

@router.get("/hires-by-quarter/")
def hires_by_quarter(db: Session = Depends(get_db)):
    try:
        query = text("""
        SELECT 
            d.department_name AS department,
            j.job_name AS job,
            ((CAST(STRFTIME('%m', e.hire_date) AS INTEGER) - 1) / 3) + 1 AS quarter,
            CAST(COUNT(*) AS INTEGER) AS num_hired
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE STRFTIME('%Y', e.hire_date) = '2021'
        GROUP BY d.department_name, j.job_name, quarter
        ORDER BY d.department_name, j.job_name
        """)
        result = db.execute(query).fetchall()

        # Convert to pandas DataFrame for pivot-style aggregation
        df = pd.DataFrame(result, columns=["department", "job", "quarter", "num_hired"])
        pivot = df.pivot_table(index=["department", "job"], columns="quarter", values="num_hired", fill_value=0).reset_index()
        pivot.columns = [
            f"Q{col}" if isinstance(col, int) else col
            for col in pivot.columns
        ]
        # Build HTML table manually
        html = "<html><head><title>Hires by Quarter (2021)</title></head><body>"
        html += "<h2>Hires by Job and Department - 2021</h2>"
        html += "<table border='1' cellpadding='5' cellspacing='0'><thead><tr>"

        # Add header
        for col in pivot.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"

        # Add data rows
        for _, row in pivot.iterrows():
            html += "<tr>" + "".join(f"<td>{row[col]}</td>" for col in pivot.columns) + "</tr>"

        html += "</tbody></table></body></html>"
        return HTMLResponse(content=html, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# 2. Departments above average hiring in 2021
@router.get("/departments-above-mean/")
def departments_above_mean(db: Session = Depends(get_db)):
    query = text("""
        WITH dept_counts AS (
            SELECT department_id, COUNT(*) AS num_hired
            FROM employees
            WHERE STRFTIME('%Y', hire_date) = '2021'
            GROUP BY department_id
        ),
        avg_hire AS (
            SELECT AVG(num_hired) AS avg_hired FROM dept_counts
        )
        SELECT 
            d.id AS department_id,
            d.department_name,
            dc.num_hired
        FROM dept_counts dc
        JOIN avg_hire ah
        JOIN departments d ON d.id = dc.department_id
        WHERE dc.num_hired > ah.avg_hired
        ORDER BY dc.num_hired DESC
    """)
    result = db.execute(query).fetchall()
    df = pd.DataFrame(result, columns=["department_id", "department", "num_hired"])

    html = "<html><head><title>Departments Above Mean</title></head><body>"
    html += "<h2>Departments Hiring Above the 2021 Mean</h2><table border='1' cellpadding='5'><thead><tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>" + "".join(f"<td>{row[col]}</td>" for col in df.columns) + "</tr>"
    html += "</tbody></table></body></html>"
    return HTMLResponse(content=html, status_code=200)

@router.post("/sql-test/")
def sql_test(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    try:
        result = db.execute(text(query))
        rows = [dict(row) for row in result.mappings()]
        columns = list(result.keys())
        return JSONResponse(content={"columns": columns, "rows": rows})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
