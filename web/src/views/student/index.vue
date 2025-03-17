<script setup>
import { onMounted, ref } from 'vue'
import { NInput, NSelect, NSpace, NButton } from 'naive-ui'
import { useDialog } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import api from '@/api'

defineOptions({ name: '学生管理' })

const dialog = useDialog()
const $table = ref(null)
const queryItems = ref({})

onMounted(() => {
  $table.value?.handleSearch()
})

const columns = [
  {
    title: '学号',
    key: 'student_id',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '姓名',
    key: 'name',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '选修课程',
    key: 'courses',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render: (row) => {
      return row.courses?.map(course => course.name).join(', ') || '暂无课程'
    }
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    align: 'center',
    fixed: 'right',
    render: (row) => {
      return h(NSpace, { justify: 'center' }, [
        h(
          NButton,
          {
            type: 'primary',
            size: 'small',
            onClick: () => handleEdit(row),
          },
          { default: () => '编辑' }
        ),
        h(
          NButton,
          {
            type: 'error',
            size: 'small',
            onClick: () => handleDelete(row),
          },
          { default: () => '删除' }
        ),
      ])
    }
  }
]

const handleEdit = (row) => {
  // TODO: 实现编辑功能
}

const handleDelete = (row) => {
  dialog.warning({
    title: '警告',
    content: '确定要删除该学生吗？',
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      await api.deleteStudent(row.id)
      $table.value?.handleSearch()
    }
  })
}

const showForm = ref(false)
const formData = ref({})
const formType = ref('create')

const handleAdd = () => {
  formType.value = 'create'
  formData.value = {}
  showForm.value = true
}

const handleSubmit = async () => {
  if (formType.value === 'create') {
    await api.createStudent(formData.value)
  } else {
    await api.updateStudent(formData.value)
  }
  message.success('操作成功')
  showForm.value = false
  $table.value?.handleSearch()
}
</script>

<template>
  <CommonPage>
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getStudentList"
    >
      <template #queryBar>
        <QueryBarItem label="学号" :label-width="70">
          <NInput
            v-model:value="queryItems.student_id"
            clearable
            type="text"
            placeholder="请输入学号"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="姓名" :label-width="70">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入姓名"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
      
      <template #tableTitle>
        <NButton type="primary" @click="handleAdd">新增学生</NButton>
      </template>
    </CrudTable>

    <StudentForm
      v-model:show="showForm"
      :type="formType"
      :data="formData"
      @success="$table?.handleSearch()"
    />
  </CommonPage>
</template>