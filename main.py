from fastapi import FastAPI
from database import engine, Base
from routers import departments, jobs, employees

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DB Migration API")


@app.get("/")
def read_root():
    return {"message": "Data Engineer Coding Challenge Rest Local API"}


app.include_router(departments.router, prefix="/departments", tags=["departments"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
