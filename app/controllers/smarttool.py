import os
from fastapi.responses import FileResponse
from fastapi import UploadFile
import shutil
from pathlib import Path
from ..service.SmarttoolService import smarttool_service

class SmarttoolController:
    def __init__(self):
        self.template_dir = Path("web/public/resource/file")
        self.upload_dir = Path("web/public/resource/file/uploads")

    async def download_template(self, template_name: str):
        template_file = self.template_dir / f"{template_name}.xlsx"
        if template_file.exists():
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