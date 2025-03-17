from fastapi import APIRouter

from .student import router
student_router = APIRouter()
student_router.include_router(router,tags=["学生模块"])

__all__ = ["student_router"]
