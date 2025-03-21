<template>
  <div class="container">
    <h1 class="title">智能工具</h1>

    <!-- 步骤条 -->
    <n-steps :current="currentStep">
      <n-step title="Excel 处理" description="下载模板并上传 Excel" />
      <n-step title="参数填写" description="输入参数并提交" />
      <n-step title="执行任务" description="查看进度，任务完成后弹框" />
    </n-steps>

    <!-- 模块1：Excel 操作 -->
    <n-card v-if="currentStep === 1" title="Excel 处理">
      <n-space vertical>
        <n-select v-model:value="selectedTemplate" :options="templates" placeholder="请选择模板" />
        <n-button type="primary" @click="downloadExcel" :disabled="!selectedTemplate">下载 Excel 文件</n-button>
        
        <!-- 修改文件上传组件 -->
        <n-upload
          ref="uploadRef"
          accept=".xlsx,.xls"
          :default-upload="false"
          :max="1"
          @change="handleUploadChange"
        >
          <n-button>选择文件</n-button>
        </n-upload>
        <n-button 
          type="primary" 
          :disabled="!selectedFile"
          @click="handleUploadClick"
        >
          确认上传并继续
        </n-button>
      </n-space>
    </n-card>

    <!-- 模块2：参数填写 -->
    <n-card v-if="currentStep === 2" title="参数填写">
      <n-form ref="formRef" :model="formData">
        <n-grid cols="2" x-gap="12">
          <n-gi><n-form-item label="baseurl"><n-input v-model:value="formData.base_url" /></n-form-item></n-gi>
          <n-gi><n-form-item label="api-key"><n-input v-model:value="formData.api_key" /></n-form-item></n-gi>
          <n-gi><n-form-item label="模型"><n-input v-model:value="formData.model" /></n-form-item></n-gi>
          <n-gi><n-form-item label="缺省值"><n-input v-model:value="formData.default" /></n-form-item></n-gi>
        </n-grid>
        <n-space>
          <n-button type="default" @click="prevStep">上一步</n-button>
          <n-button type="primary" @click="submitForm">提交并下一步</n-button>
        </n-space>
      </n-form>
    </n-card>

    <!-- 模块3：执行任务 -->
    <n-card v-if="currentStep === 3" title="执行任务">
      <n-space vertical>
        <!-- 配置信息展示 -->
        <div class="task-info">
          <n-table :single-line="false" size="small">
            <thead>
              <tr>
                <th>配置项</th>
                <th>值</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(value, key) in taskConfig" :key="key">
                <td>{{ key }}</td>
                <td>{{ value }}</td>
              </tr>
            </tbody>
          </n-table>
        </div>

        <n-button type="warning" @click="startTask" :disabled="isRunning">开始执行任务</n-button>
        <n-progress type="line" :percentage="progress" />
        <n-button type="default" @click="prevStep">上一步</n-button>
      </n-space>
    </n-card>

    <!-- 任务完成弹窗 -->
    <n-modal v-model:show="showTaskCompleteModal">
      <n-card title="任务完成">
        <p>任务已成功完成！请确认下载文件。</p>
        <template #footer>
          <n-button type="primary" @click="confirmDownload">确认下载</n-button>
          <n-button type="default" @click="showTaskCompleteModal = false">取消</n-button>
        </template>
      </n-card>
    </n-modal>

    <!-- 表单提交弹窗 -->
    <n-modal v-model:show="showFormModal">
      <n-card title="表单提交成功">
        <p>您的参数已成功提交！</p>
        <template #footer>
          <n-button type="primary" @click="closeFormModal">确定</n-button>
        </template>
      </n-card>
    </n-modal>

    <!-- 文件归档弹窗 -->
    <n-modal v-model:show="showArchiveModal">
      <n-card title="文件已归档">
        <p>文件已成功归档！</p>
        <template #footer>
          <n-button type="primary" @click="resetToStepOne">确定</n-button>
        </template>
      </n-card>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { NSelect, NButton, NForm, NFormItem, NInput, NUpload, NGrid, NGi, NCard, NSpace, NProgress, NModal, NSteps, NStep, NTable } from 'naive-ui';
import { useMessage, useDialog } from 'naive-ui';  // 添加 useDialog

import api from '@/api'
const message = useMessage();
const dialog = useDialog();  // 初始化 dialog

const currentStep = ref(1);
const templates = ref([
  { label: '模板1', value: 'template1' },
  { label: '模板2', value: 'template2' },
  { label: '模板3', value: 'template3' }
]);

const selectedTemplate = ref('');
const formData = ref({ base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1',api_key: 'sk-14a2a30d135148dcaef8a673a21af02a', model: 'qwen-long', default: '0' });
const uploadSuccess = ref(false);

// 下载Excel模板
const downloadExcel = async () => {
  if (!selectedTemplate.value) return;
  
  try {
    const response = await api.downloadTemplate(selectedTemplate.value);
    if (response.code === 200 && response.data.url) {
      // 创建一个a标签来触发下载
      const link = document.createElement('a');
      link.href = response.data.url;
      link.download = `${selectedTemplate.value}.xlsx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      message.success('开始下载模板');
    } else {
      throw new Error(response.message || '下载失败');
    }
  } catch (error) {
    message.error('下载失败');
    console.error('下载模板错误:', error);
  }
};

const uploadRef = ref(null);
const selectedFile = ref(null);

// 处理文件状态变化
const handleUploadChange = (options) => {
  if (options.fileList.length === 0) {
    selectedFile.value = null;
    uploadSuccess.value = false;
  } else {
    selectedFile.value = options.fileList[0];
  }
};

// 处理文件上传
const handleUploadClick = async () => {
  if (!selectedFile.value) return;
  
  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value.file);
    
    const response = await api.uploadFile(formData);
    console.log('上传响应:', response);
    
    if (response.code === 200) {
      message.success('文件上传成功');
      uploadSuccess.value = true;
      nextStep();
    } else {
      throw new Error(response.message || '文件上传失败');
    }
  } catch (error) {
    const errorMessage = error.response?.data?.message || error.message || '文件上传失败';
    dialog.error({
      title: 'Excel 验证失败',
      content: error.error.message,
      positiveText: '确定',
     
    });
    console.error('上传文件错误1:', error.error.message);
  }
};

// 移除原来的 handleUpload 函数
const nextStep = () => { currentStep.value += 1; };
const prevStep = () => { currentStep.value -= 1; };

const showFormModal = ref(false); 
const submitForm = async () => {
  try {
    const response = await api.submitSmartToolForm(formData.value);
    // 处理成功响应
    message.success('参数提交成功');
    console.log('提交表单响应:', response);
    showFormModal.value = true;
  } catch (error) {
    // 处理请求失败的情况
    message.error(error.response?.data?.message || '参数提交失败');
  }
};

const closeFormModal = () => {
  showFormModal.value = false;
  nextStep();
};

const isRunning = ref(false);
const progress = ref(0);
const showTaskCompleteModal = ref(false);
const showArchiveModal = ref(false);
let progressInterval = null; // 添加轮询间隔变量

// 开始任务
const startTask = async () => {
  if (isRunning.value) return;
  isRunning.value = true;
  progress.value = 0;
  
  try {
    await api.startSmartToolTask();
    // 开始轮询进度
    progressInterval = setInterval(async () => {
      try {
        const response = await api.getProgress();
        if (response.code === 200) {
          progress.value = response.data.percentage;
          
          // 如果进度达到100%，停止轮询并显示完成弹窗
          if (progress.value >= 100) {
            clearInterval(progressInterval);
            isRunning.value = false;
            showTaskCompleteModal.value = true;
          }
        }
      } catch (error) {
        console.error('获取进度失败:', error);
        clearInterval(progressInterval);
        isRunning.value = false;
        message.error('获取进度信息失败');
      }
    }, 1000); // 每秒轮询一次
  } catch (error) {
    isRunning.value = false;
    message.error('任务启动失败');
    console.error('启动任务错误:', error);
  }
};

// 在组件卸载时清除轮询
onUnmounted(() => {
  if (progressInterval) {
    clearInterval(progressInterval);
  }
});

// 确认下载文件
const confirmDownload = async () => {
  showTaskCompleteModal.value = false; // 关闭任务完成弹窗
  
  try {
    const response = await api.confirmSmartToolDownload();
    if (response.code === 200 && response.data.url) {
      // 创建一个a标签来触发下载
      const link = document.createElement('a');
      link.href = response.data.url;
      link.download = 'data.docx';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      message.success('文件下载成功');
      showArchiveModal.value = true; // 显示文件归档弹窗
    } else {
      throw new Error(response.message || '下载失败');
    }
  } catch (error) {
    message.error('文件下载失败');
    console.error('确认下载错误:', error);
  }
};

// 重置并返回步骤一
const resetToStepOne = () => {
  showArchiveModal.value = false; // 关闭文件归档弹窗
  progress.value = 0; // 重置进度条
  currentStep.value = 1; // 返回步骤一
  isRunning.value = false; // 重置运行状态
  selectedTemplate.value = ''; // 重置模板选择
  uploadSuccess.value = false; // 重置上传状态
};

const taskConfig = ref({});

// 监听步骤变化，获取配置信息
watch(() => currentStep.value, async (newStep) => {
  if (newStep === 3) {
    try {
      const response = await fetch('/resource/task.json');
      taskConfig.value = await response.json();
    } catch (error) {
      console.error('获取配置信息失败:', error);
      message.error('获取配置信息失败');
    }
  }
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}
</style>