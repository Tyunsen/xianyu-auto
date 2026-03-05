<template>
  <div class="accounts-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>账号管理</h1>
      <el-button type="primary" @click="showAddDialog = true">
        添加账号
      </el-button>
    </div>

    <!-- 账号列表 -->
    <el-card class="accounts-card">
      <el-table :data="accounts" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nickname" label="昵称" min-width="150" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login ? formatDate(row.last_login) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(row)"
              :disabled="row.status === 'online'"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="fetchAccounts"
          @current-change="fetchAccounts"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="isEdit ? '编辑账号' : '添加账号'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入账号昵称" />
        </el-form-item>

        <el-form-item label="状态" v-if="isEdit">
          <el-select v-model="form.status" placeholder="选择状态">
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="过期" value="expired" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api, type Account, type AccountCreate, type AccountUpdate } from '@/api/client'

const accounts = ref<Account[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const showAddDialog = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref()
const editingId = ref<number | null>(null)

const form = reactive<AccountCreate & AccountUpdate>({
  nickname: '',
  status: 'offline',
})

const formRules = {
  nickname: [{ required: true, message: '请输入账号昵称', trigger: 'blur' }],
}

// 获取账号列表
const fetchAccounts = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const res = await api.getAccounts({ skip, limit: pageSize.value })
    accounts.value = res.items
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取账号列表失败')
  } finally {
    loading.value = false
  }
}

// 状态相关
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    online: 'success',
    offline: 'info',
    expired: 'danger',
    error: 'danger',
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    online: '在线',
    offline: '离线',
    expired: '已过期',
    error: '错误',
  }
  return texts[status] || status
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

// 编辑
const handleEdit = (row: Account) => {
  isEdit.value = true
  editingId.value = row.id
  form.nickname = row.nickname
  form.status = row.status
  showAddDialog.value = true
}

// 删除
const handleDelete = async (row: Account) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除账号 "${row.nickname}" 吗？`,
      '删除确认',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )

    await api.deleteAccount(row.id)
    ElMessage.success('删除成功')
    fetchAccounts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate()
  submitting.value = true

  try {
    if (isEdit.value && editingId.value) {
      const data: AccountUpdate = {
        nickname: form.nickname,
        status: form.status,
      }
      await api.updateAccount(editingId.value, data)
      ElMessage.success('更新成功')
    } else {
      await api.createAccount({ nickname: form.nickname })
      ElMessage.success('添加成功')
    }

    showAddDialog.value = false
    resetForm()
    fetchAccounts()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  isEdit.value = false
  editingId.value = null
  form.nickname = ''
  form.status = 'offline'
}

onMounted(() => {
  fetchAccounts()
})
</script>

<style scoped>
.accounts-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #2c2c24;
}

.accounts-card {
  border-radius: 16px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
