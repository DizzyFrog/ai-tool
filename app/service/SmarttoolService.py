from app.log import logger
import pandas as pd
import openpyxl
import json
class SmarttoolService:
    
    
    def __init__(self):
        self.task_json_path = "web/public/resource/task.json"
        pass
    
    async def validateExcel(self, file):
        # 在这里添加Excel验证逻辑
        #  raise ValueError("Excel文件格式不正确或数据不完整")
        #读取文件名和第三个sheet页的名字

        filename = file.name
        logger.info(filename)
        workbook = openpyxl.load_workbook(file)
        sheet_names = workbook.sheetnames
        logger.info(sheet_names)
        
        # 构建配置字典
        config = {
            "excel_file_name": filename,
            "sheet_name": sheet_names[2],
        }
        
        # 更新配置文件
        await self.update_config(config)

    async def update_config(self, config: dict):
        
        try:
            # 读取现有配置
            with open(self.task_json_path, 'r', encoding='utf-8') as f:
                current_config = json.load(f)
            
            # 更新配置
            current_config.update(config)
            
            # 写入文件
            with open(self.task_json_path, 'w', encoding='utf-8') as f:
                json.dump(current_config, f, ensure_ascii=False, indent=2)
                
            logger.info(f"配置文件更新成功: {config}")
        except Exception as e:
            logger.error(f"更新配置文件失败: {str(e)}")
            raise ValueError(f"更新配置文件失败: {str(e)}")
    

    

smarttool_service = SmarttoolService()  # 修正类名拼写错误