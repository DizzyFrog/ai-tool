from fastapi import APIRouter, Query
from app.schemas import SuccessExtra
from app.controllers.student import student_controller
from app.schemas.students import StudentCreate, StudentUpdate

router = APIRouter()

@router.get("/list", summary="学生列表")
async def get_student_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="学生姓名"),
    student_id: str = Query("", description="学号"),
):
    student_objs, total = await student_controller.get_student_list(
        page=page,
        page_size=page_size,
        name=name,
        student_id=student_id
    )
    data = [await student.to_dict() for student in student_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

@router.post("/create", summary="创建学生")
async def create_student(student: StudentCreate):
    await student_controller.create_student(student)
    return SuccessExtra()

@router.put("/update", summary="更新学生")
async def update_student(student: StudentUpdate):
    await student_controller.update_student(student)
    return SuccessExtra()

@router.delete("/delete/{id}", summary="删除学生")
async def delete_student(id: int):
    await student_controller.delete_student(id)
    return SuccessExtra()