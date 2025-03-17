from typing import Optional
from tortoise.expressions import Q

from app.core.crud import CRUDBase
from app.models.admin import Student, Course
from app.schemas.students import StudentCreate, StudentUpdate

class StudentController(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def __init__(self):
        super().__init__(model=Student)
    
    async def get_student_list(
        self,
        page: int,
        page_size: int,
        name: Optional[str] = None,
        student_id: Optional[str] = None
    ):
        q = Q()
        if name:
            q &= Q(name__icontains=name)
        if student_id:
            q &= Q(student_id__icontains=student_id)
            
        student_objs = await self.model.filter(q).prefetch_related(
            'courses'
        ).offset((page - 1) * page_size).limit(page_size)
        total = await self.model.filter(q).count()
        
        return student_objs, total
    
    async def create_student(self, obj_in: StudentCreate):
        student_obj = await self.create(obj_in=obj_in)
        if obj_in.course_ids:
            courses = await Course.filter(id__in=obj_in.course_ids)
            await student_obj.courses.add(*courses)
        return student_obj
    
    async def update_student(self, obj_in: StudentUpdate):
        student_obj = await self.get(id=obj_in.id)
        # 更新基本信息
        await student_obj.update_from_dict(obj_in.dict(exclude_unset=True))
        await student_obj.save()
        
        # 更新课程关系
        if obj_in.course_ids is not None:
            await student_obj.courses.clear()
            if obj_in.course_ids:
                courses = await Course.filter(id__in=obj_in.course_ids)
                await student_obj.courses.add(*courses)
        
        return student_obj
    
    async def delete_student(self, student_id: int):
        student_obj = await self.get(id=student_id)
        # 删除课程关系
        await student_obj.courses.clear()
        # 删除学生
        await student_obj.delete()

student_controller = StudentController()