from fastapi import FastAPI, HTTPException,APIRouter
from employee.models.employee import ( EmployeeBase ,EmployeeRead )
from core.database import db
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/employee", tags=["employee"]
)

@router.post('/', response_model=EmployeeRead)
async def create_employee(employee: EmployeeBase):
    collection = db.get_collection("employee")
    
    employee_data = employee.dict() 
    
    employee_data["_id"] = ObjectId()
    employee_data["employee_id"] = str(employee_data["_id"])
    
    result = await collection.insert_one(employee_data)
    
    
    return { **employee_data, "id": employee_data["employee_id"] }

@router.get("/{employee_id}", response_model=EmployeeBase)
async def get_employee(employee_id: str):
    collection = db.get_collection("employee")
    
    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    
    employee = await collection.find_one({"_id": emp_id})
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {**employee}
    
@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(employee_id: str, employee: EmployeeBase):
    collection = db.get_collection("employee")
    
    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    
    updated_data = employee.dict(exclude_unset=True)  

    result = await collection.update_one(
        {"_id": emp_id}, 
        {"$set": updated_data} 
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    
    updated_employee = await collection.find_one({"_id": emp_id})
    return {**updated_employee, "id": updated_employee["employee_id"]}

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    collection = db.get_collection("employee")
    
    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    
    result = await collection.delete_one({"_id": emp_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    
    return {"employee_id": employee_id, "status": "deleted"}

@router.get("/", response_model=List[EmployeeRead])
async def get_all_employees():
    collection = db.get_collection("employee")
    
    employees = await collection.find().to_list(100)  
    
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")
    
    return employees
