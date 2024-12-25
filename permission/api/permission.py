from fastapi import FastAPI, HTTPException,APIRouter
from permission.models.permission import ( EmployeePermissionDate )
from core.database import db
from bson import ObjectId
from datetime import datetime
import pytz

router = APIRouter(
    prefix="/permission", tags=["permission"]
)


@router.post("/")
async def create_permission(permission: EmployeePermissionDate):
    collection = db.get_collection("permission")
    existing_employee = await collection.find_one({"employee_id": permission.employee_id})
    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail=f"Сотрудник с ID {permission.employee_id} уже существует."
        )
    permission_data = permission.dict()
    
    result = await collection.insert_one(permission_data)
    
    return {"Permission installed succesfully"}


@router.get("/{employee_id}")
async def get_permission(employee_id: str): 
    collection = db.get_collection("permission")
    permission = await collection.find_one({"employee_id": employee_id})

    time_range = EmployeePermissionDate(**permission)
    current_time = datetime.now()

    return time_range.is_valid_time(current_time)


@router.put("/")
async def update_permission(updated_permission: EmployeePermissionDate):
    collection = db.get_collection("permission")
    updated_data = updated_permission.dict()
    
    result = await collection.update_one(
        {"employee_id": updated_data['employee_id']},
        {"$set": updated_data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")

    return {"message": "Permission updated successfully"}
    
    
@router.delete("/{employee_id}")
async def delete_permission(employee_id: str):

    collection = db.get_collection("permission")

    result = await collection.delete_one({"employee_id": employee_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")

    return {"message": "Permission deleted successfully"}