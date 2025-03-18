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
        <n-upload :action="uploadUrl" :headers="headers" :data="formData" @success="handleUploadSuccess">
          <n-button type="success">上传填好的 Excel 文件</n-button>
        </n-upload>
        <n-button type="warning" @click="nextStep">下一步</n-button>
      </n-space>
    </n-card>

    <!-- 模块2：参数填写 -->
    <n-card v-if="currentStep === 2" title="参数填写">
      <n-form ref="formRef" :model="formData">
        <n-grid cols="2" x-gap="12">
          <n-gi><n-form-item label="Key"><n-input v-model:value="formData.key" /></n-form-item></n-gi>
          <n-gi><n-form-item label="参数1"><n-input v-model:value="formData.param1" /></n-form-item></n-gi>
          <n-gi><n-form-item label="参数2"><n-input v-model:value="formData.param2" /></n-form-item></n-gi>
          <n-gi><n-form-item label="参数3"><n-input v-model:value="formData.param3" /></n-form-item></n-gi>
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
import { ref } from 'vue';
import { NSelect, NButton, NForm, NFormItem, NInput, NUpload, NGrid, NGi, NCard, NSpace, NProgress, NModal, NSteps, NStep } from 'naive-ui';
import { useMessage } from 'naive-ui';

import api from '@/api'
const message = useMessage();

const currentStep = ref(1);
const templates = ref([
  { label: '模板1', value: 'template1' },
  { label: '模板2', value: 'template2' },
  { label: '模板3', value: 'template3' }
]);

const selectedTemplate = ref('');
const formData = ref({ key: '', param1: '', param2: '', param3: '' });
const uploadUrl = ref('/api/v1/smarttool/upload'); // 修改为正确的上传路径
const headers = ref({ 'Content-Type': 'multipart/form-data' });
const uploadSuccess = ref(false);

// 下载Excel模板
const downloadExcel = async () => {
  try {
    await api.downloadTemplate(selectedTemplate.value);
    message.success('模板下载成功');
  } catch (error) {
    message.error('模板下载失败');
    console.error('下载模板错误:', error);
  }
};

// 处理上传成功
const handleUploadSuccess = () => { 
  uploadSuccess.value = true; 
  message.success('上传成功');
};

const nextStep = () => { currentStep.value += 1; };
const prevStep = () => { currentStep.value -= 1; };

const showFormModal = ref(false); 
const submitForm = async () => {
  try {
    await api.submitSmartToolForm(formData.value);
    showFormModal.value = true;
  } catch (error) {
    message.error('表单提交失败');
    console.error('提交表单错误:', error);
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

// 开始任务
const startTask = async () => {
  if (isRunning.value) return;
  isRunning.value = true;
  progress.value = 0;
  
  try {
    await api.startSmartToolTask();
    
    const interval = setInterval(() => {
      if (progress.value >= 100) {
        clearInterval(interval);
        isRunning.value = false;
        showTaskCompleteModal.value = true; // 显示任务完成弹窗
      } else {
        progress.value += 10;
      }
    }, 500);
  } catch (error) {
    isRunning.value = false;
    message.error('任务启动失败');
    console.error('启动任务错误:', error);
  }
};

// 确认下载文件
const confirmDownload = async () => {
  showTaskCompleteModal.value = false; // 关闭任务完成弹窗
  
  try {
    await api.confirmSmartToolDownload();
    message.success('文件下载成功');
    showArchiveModal.value = true; // 显示文件归档弹窗
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
  formData.value = { key: '', param1: '', param2: '', param3: '' }; // 重置表单数据
  selectedTemplate.value = ''; // 重置模板选择
  uploadSuccess.value = false; // 重置上传状态
};
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