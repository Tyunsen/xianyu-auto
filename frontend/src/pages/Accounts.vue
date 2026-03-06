<template>
  <div class="accounts-page">
    <div class="page-header">
      <h1>账号管理</h1>
      <el-button type="primary" @click="openAddDialog">添加账号</el-button>
    </div>

    <el-card class="accounts-card">
      <el-table :data="accounts" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="nickname" label="昵称" min-width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleQRLogin(row)">扫码登录</el-button>
            <el-button size="small" @click="handleRefreshStatus(row)">刷新状态</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total" :page-sizes="[10,20,50,100]" layout="total,sizes,prev,pager,next" @size-change="fetchAccounts" @current-change="fetchAccounts" />
      </div>
    </el-card>

    <el-dialog v-model="showAddDialog" title="添加账号" width="500px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入账号昵称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeAddDialog">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 二维码登录对话框 -->
    <el-dialog v-model="showQRDialog" :title="'扫码登录 - ' + (currentAccount?.nickname || '')" width="400px" :close-on-click-modal="false" @close="cancelQRLogin">
      <div v-loading="qrLoading" style="text-align:center;min-height:200px">
        <div v-if="qrError" style="color:#f56c6c">
          <p>{{ qrError }}</p>
          <el-button type="primary" size="small" @click="retryQRLogin">重试</el-button>
        </div>
        <div v-else-if="qrCode">
          <p style="margin-bottom:15px;color:#909399">请使用闲鱼APP扫码登录</p>
          <img :src="qrCode" alt="二维码" style="max-width:250px;border-radius:8px" />
          <p v-if="loginStatus === 'waiting'" style="margin-top:15px;color:#909399">
            <el-icon class="is-loading"><Loading /></el-icon>
            等待扫码中...
          </p>
          <p v-else-if="loginSuccess" style="margin-top:15px;color:#67c23a">
            <el-icon><CircleCheck /></el-icon>
            登录成功！
          </p>
        </div>
        <div v-else style="color:#909399">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
          <p>正在获取二维码...</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="cancelQRLogin">取消</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑账号" width="400px">
      <el-form label-width="80px">
        <el-form-item label="昵称"><el-input v-model="editForm.nickname" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="editForm.status">
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="过期" value="expired" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog=false">取消</el-button>
        <el-button type="primary" @click="handleUpdate" :loading="updating">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Loading, CircleCheck } from '@element-plus/icons-vue'
import { api, type Account } from '@/api/client'

const accounts = ref<Account[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const showAddDialog = ref(false)
const formRef = ref()
const submitting = ref(false)
const form = reactive({ nickname: '' })
const formRules = { nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }] }

const showEditDialog = ref(false)
const editingId = ref<number|null>(null)
const updating = ref(false)
const editForm = reactive({ nickname: '', status: 'offline' })

// 二维码登录相关
const showQRDialog = ref(false)
const currentAccount = ref<Account | null>(null)
const qrLoading = ref(false)
const qrCode = ref('')
const qrError = ref('')
const loginStatus = ref<'idle' | 'waiting' | 'success' | 'error'>('idle')
const loginSuccess = ref(false)
let qrCheckTimer: ReturnType<typeof setInterval> | null = null

const fetchAccounts = async () => {
  loading.value = true
  try {
    const res = await api.getAccounts({ skip: (currentPage.value-1)*pageSize.value, limit: pageSize.value })
    accounts.value = res.items
    total.value = res.total
  } catch (e) { ElMessage.error('获取失败') }
  finally { loading.value = false }
}

const getStatusType = (s: string) => ({ online: 'success', offline: 'info', expired: 'danger', error: 'danger' }[s] || 'info')
const getStatusText = (s: string) => ({ online: '在线', offline: '离线', expired: '已过期', error: '错误' }[s] || s)

// 打开添加对话框时自动生成默认昵称
const openAddDialog = () => {
  // 自动生成默认昵称：闲鱼账号1, 闲鱼账号2, ...
  const maxNum = accounts.value.reduce((max, acc) => {
    const match = acc.nickname.match(/^闲鱼账号(\d+)$/)
    return match ? Math.max(max, parseInt(match[1])) : max
  }, 0)
  form.nickname = `闲鱼账号${maxNum + 1}`
  if (formRef.value) {
    formRef.value.clearValidate()
  }
  showAddDialog.value = true
}

const closeAddDialog = () => {
  showAddDialog.value = false
}

const resetForm = () => {
  form.nickname = ''
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  submitting.value = true
  try {
    await api.createAccount({ nickname: form.nickname })
    ElMessage.success('添加成功')
    showAddDialog.value = false
    form.nickname = ''
    fetchAccounts()
  } catch (e) { ElMessage.error('添加失败') }
  finally { submitting.value = false }
}

const handleEdit = (row: Account) => {
  editingId.value = row.id
  editForm.nickname = row.nickname
  editForm.status = row.status
  showEditDialog.value = true
}

const handleUpdate = async () => {
  if (!editingId.value) return
  updating.value = true
  try {
    await api.updateAccount(editingId.value, editForm)
    ElMessage.success('更新成功')
    showEditDialog.value = false
    fetchAccounts()
  } catch (e) { ElMessage.error('更新失败') }
  finally { updating.value = false }
}

const handleDelete = async (row: Account) => {
  try {
    await ElMessageBox.confirm('删除 "' + row.nickname + '"？', '确认', { type: 'warning' })
    await api.deleteAccount(row.id)
    ElMessage.success('删除成功')
    fetchAccounts()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

// 二维码登录
const handleQRLogin = async (row: Account) => {
  currentAccount.value = row
  showQRDialog.value = true
  loginStatus.value = 'idle'
  loginSuccess.value = false
  qrCode.value = ''
  qrError.value = ''
  await startQRLogin()
}

const startQRLogin = async () => {
  if (!currentAccount.value) return

  qrLoading.value = true
  qrError.value = ''
  loginStatus.value = 'waiting'

  try {
    const res = await api.startQRLogin(currentAccount.value.id)
    if (res.success && res.qr_code) {
      qrCode.value = res.qr_code
      loginStatus.value = 'waiting'
      startQRCheck()
    } else {
      qrError.value = res.message || '获取二维码失败'
      loginStatus.value = 'error'
    }
  } catch (e: any) {
    qrError.value = e.message || '获取二维码失败'
    loginStatus.value = 'error'
  } finally {
    qrLoading.value = false
  }
}

const startQRCheck = () => {
  if (qrCheckTimer) {
    clearInterval(qrCheckTimer)
  }

  qrCheckTimer = setInterval(async () => {
    if (!currentAccount.value || loginStatus.value !== 'waiting') {
      stopQRCheck()
      return
    }

    try {
      const res = await api.checkQRLogin(currentAccount.value.id)
      if (res.success && res.status === 'success') {
        stopQRCheck()
        loginSuccess.value = true
        loginStatus.value = 'success'
        ElMessage.success('登录成功')
        setTimeout(() => {
          showQRDialog.value = false
          fetchAccounts()
        }, 1500)
      } else if (res.status === 'error') {
        stopQRCheck()
        qrError.value = res.message || '登录失败'
        loginStatus.value = 'error'
      }
    } catch (e: any) {
      console.error('检查登录状态失败:', e)
    }
  }, 2000)
}

const stopQRCheck = () => {
  if (qrCheckTimer) {
    clearInterval(qrCheckTimer)
    qrCheckTimer = null
  }
}

const cancelQRLogin = async () => {
  stopQRCheck()
  if (currentAccount.value) {
    try {
      await api.cancelQRLogin(currentAccount.value.id)
    } catch (e) {
      // 忽略取消登录的错误
    }
  }
  showQRDialog.value = false
  qrCode.value = ''
  loginStatus.value = 'idle'
  loginSuccess.value = false
}

const retryQRLogin = async () => {
  await startQRLogin()
}

// 刷新状态
const handleRefreshStatus = async (row: Account) => {
  try {
    await api.checkQRLogin(row.id)
    ElMessage.success('状态已刷新')
    fetchAccounts()
  } catch (e: any) {
    ElMessage.success('状态已刷新')
    fetchAccounts()
  }
}

onMounted(() => { fetchAccounts() })

onUnmounted(() => {
  stopQRCheck()
})
</script>

<style scoped>
.accounts-page { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { margin: 0; font-size: 24px; color: #2c2c24; }
.accounts-card { border-radius: 16px; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
