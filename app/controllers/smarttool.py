import os
from fastapi.responses import FileResponse
from fastapi import UploadFile
import shutil
from pathlib import Path
from ..service.SmarttoolService import smarttool_service
from app.core.bgtask import BgTasks
from app.log import logger

class SmarttoolController:
    def __init__(self):
        self.template_dir = Path("web/public/resource/file")
        self.upload_dir = Path("web/public/resource/file/uploads")
        self.output_dir = Path("web/public/resource/file/output")
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def download_template(self, template_name: str):
        template_file = self.template_dir / f"{template_name}.xlsx"
        if template_file.exists():
            await smarttool_service.update_config({"template":template_name})
            # 返回文件的相对URL地址
            return {
                "code": 200,
                "data": {
                    "url": f"/resource/file/{template_name}.xlsx"
                }
            }
        else:
            # 返回标准的错误响应
            return {
                "code": 404,
                "message": f"模板 {template_name} 不存在"
            }
    async def upload_file(self, file: UploadFile):
        try:
            # 生成唯一的文件名
            file_name = file.filename
            file_path = self.upload_dir / file_name
            
            # 保存上传的文件
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                
            # 验证Excel文件
            try:
                await smarttool_service.validateExcel(file_path)
            except Exception as e:
                return {
                    "code": 400,
                    "message": f"Excel文件验证失败: {str(e)}"
                }
                
            
            return {
                "code": 200,
                "message": "文件上传成功",
                "data": {
                    "file_name": file_name,
                    "file_path": str(file_path)
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "message": f"文件上传失败: {str(e)}"
            }

    async def submit_form(self, form_data: dict):
        # 将表单数据更新到update_config
        await smarttool_service.update_config(form_data)
        # 处理表单数据
        return {
            "code": 200,
            "message": "表单提交成功",
            "data": {
                "form_data": form_data
            }
        }

    async def start_task(self):
        try:
            # 初始化后台任务对象
            await BgTasks.init_bg_tasks_obj()
            
            logger.info("开始处理任务 in controller")
            
            # 修改为调用 Service 层的方法
            await BgTasks.add_task(smarttool_service.process_task)
            # 确保任务执行
            await BgTasks.execute_tasks()
            
            return {
                "code": 200,
                "message": "任务启动成功",
                "data": {
                    "status": "processing"
                }
            }
        except Exception as e:
            return {
                "code": 500,
                "message": f"任务启动失败: {str(e)}"
            }

    # 删除原 controller 中的 process_task 方法
    async def confirm_download(self):
        # 返回输出文件
        output_file = self.output_dir / "result.xlsx"
        if output_file.exists():
            return FileResponse(
                path=str(output_file),
                filename="result.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            return {"message": "输出文件不存在"}

smarttool_controller = SmarttoolController()