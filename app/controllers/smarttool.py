import os
from fastapi.responses import FileResponse
from fastapi import UploadFile
import shutil
from pathlib import Path

class SmarttoolController:
    def __init__(self):
        # 创建必要的目录
        self.template_dir = Path("app/static/templates")
        self.upload_dir = Path("app/static/uploads")
        self.output_dir = Path("app/static/outputs")
        
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        

    async def download_template(self, template_name: str):
        template_file = self.template_dir / f"{template_name}.xlsx"
        
        if template_file.exists():
            # 使用 FileResponse，并添加自定义响应头
            return FileResponse(
                path=str(template_file),
                filename=f"{template_name}.xlsx",
                headers={
                    "X-Audit-Log-Skip": "true"  # 添加自定义头告诉中间件跳过审计日志
                }
            )
        else:
            # 返回标准的错误响应，中间件可以正常处理
            return {
                "code": 404,
                "message": f"模板 {template_name} 不存在"
            }

    async def upload_file(self, file: UploadFile, form_data: dict):
        # 保存上传的文件
        file_path = self.upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "message": "文件上传成功", 
            "filename": file.filename, 
            "form_data": form_data
        }

    async def submit_form(self, form_data: dict):
        # 处理表单数据
        return {
            "message": "表单提交成功", 
            "form_data": form_data
        }

    async def start_task(self):
        # 模拟任务处理，实际项目中可能需要更复杂的逻辑
        # 例如创建一个输出文件
        output_file = self.output_dir / "result.xlsx"
        with open(output_file, "wb") as f:
            f.write(b"Task result data")
            
        return {
            "message": "任务启动成功",
            "output_file": str(output_file)
        }

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