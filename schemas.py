from pydantic import BaseModel

class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    class Config:
        orm_mode = True

# Repeat similarly for Job and Employee classes...

class JobBase(BaseModel):
    job_name: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    name: str
    hire_date: str
    department_id: int
    job_id: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    class Config:
        orm_mode = True