from fastapi import APIRouter, File, UploadFile, Form, Path
from typing import Dict
from app.controllers.smarttool import smarttool_controller
from app.schemas import SuccessExtra
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

router = APIRouter()

@router.get("/download-template/{template_name}", summary="下载 Excel 模板")
async def download_template(template_name: str = Path(..., description="模板名称")):
    """
    下载指定名称的模板文件
    """
    return await smarttool_controller.download_template(template_name)


# 处理 Excel 文件上传
@router.post("/upload_file",summary="处理 Excel 文件上传")
async def upload_file(file: UploadFile = File):
    return await smarttool_controller.upload_file(file)

# 处理表单提交
@router.post("/submit_form",summary="处理表单提交")
async def submit_form(form_data: Dict[str, str]):
    return await smarttool_controller.submit_form(form_data)

# 开始执行任务
@router.post("/start_task",summary="开始执行任务")
async def start_task(background_tasks: BackgroundTasks):
    return await smarttool_controller.start_task(background_tasks)

#查询进度
@router.get("/get_progress",summary="查询进度")
async def get_progress():
    return await smarttool_controller.get_task_progress()

# 确认下载文件
@router.get("/confirm_download",summary="确认下载文件") 
async def confirm_download():
    return await smarttool_controller.confirm_download()