from .aiclient import aiclient
import uuid
import concurrent.futures
import subprocess
from pathlib import Path
from app.log import logger

def get_description(key, functions):
    problem = f'现在有一个功能需求:{key},其功能过程有:{functions} 。//你的任务有：1.根据需求和功能过程，写出100字左右的功能概述'
    answer = aiclient.get_response_with_tongyi(problem)
    logger.info("gen： "+key)
    return answer





def get_structure(key, functions):
    content = ""
    for function in functions:
        content += key + "-->" + function + "\n"
    mermaid_code = f'''
flowchart TD
{content}
'''
    uuid_ = uuid.uuid4()
    filename = Path("web/public/resource/file/output/cache/images") / f"{uuid_}.png"
    generate_png_async(filename, mermaid_code)
    return str(filename)  # 返回字符串而不是 Path 对象


def get_flow_chart(role, process):
    A,B,C = role
    # step1,step2,step3 = process
    step1 = process[0]
    step3 = process[-1]
    mid = len(process)//2
    step2 = process[mid]

    mermaid_code = f'''
sequenceDiagram
  participant  a as {A}
  participant  b as {B}
  participant  c as {C}

  a ->> b: {step1}
  b ->> c: {step2}
  b ->> a: {step3}
    '''
    uuid_ = uuid.uuid4()
    filename = Path("web/public/resource/file/output/cache/images") / f"{uuid_}.png"
    generate_png_async(filename, mermaid_code)
    return str(filename)  # 返回字符串而不是 Path 对象
    # return mermaid_code


def gen_png(filename,mermaid):

    # 定义命令
    command = f'''
cat << EOF  | mmdc  -o {filename} --input -
{mermaid}
EOF
'''
    # 执行命令并捕获输出
    try:
        # 执行命令并捕获输出
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        print(output)
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获错误信息
        print("命令执行失败:", e.output)
        


def generate_png_async(filename, mermaid):
    # 定义一个函数，用于在线程中执行生成图片的任务
    def generate():
        gen_png(filename, mermaid)

    # 创建一个线程池，并设置最大线程数为10
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务到线程池
        future = executor.submit(generate)
        # 获取任务的结果（这里可以不用获取结果，因为没有返回值i）
        _ = future.result()





