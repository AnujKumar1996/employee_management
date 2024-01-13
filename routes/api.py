from fastapi import APIRouter
from src.endpoints import (employee_management)

router = APIRouter()

router.include_router(employee_management.router)
