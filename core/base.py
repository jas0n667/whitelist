from fastapi import APIRouter


from employee.api.employee import router as employee_router
from permission.api.permission import router as permission_router

router = APIRouter(prefix="/api")

router.include_router(employee_router, tags=["employee"])
router.include_router(permission_router, tags=["permission"])