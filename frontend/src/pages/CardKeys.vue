<template>
  <div class="cardkeys-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>卡密管理</h1>
      <el-button type="primary" @click="showImportDialog = true">
        导入卡密
      </el-button>
    </div>

    <!-- 库存统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">总数量</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card success">
          <div class="stat-value">{{ stats.available }}</div>
          <div class="stat-label">可用</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card warning">
          <div class="stat-value">{{ stats.used }}</div>
          <div class="stat-label">已使用</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选 -->
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="商品">
          <el-select v-model="productFilter" placeholder="全部" clearable @change="fetchCardKeys">
            <el-option v-for="p in products" :key="p.id" :label="p.title" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable @change="fetchCardKeys">
            <el-option label="可用" value="available" />
            <el-option label="已使用" value="used" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 卡密列表 -->
    <el-card class="cardkeys-card">
      <el-table :data="cardKeys" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="key" label="卡密" min-width="200" show-overflow-tooltip />
        <el-table-column prop="product_id" label="商品ID" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'available' ? 'success' : 'info'">
              {{ row.status === 'available' ? '可用' : '已使用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="used_at" label="使用时间" width="180">
          <template #default="{ row }">
            {{ row.used_at ? formatDate(row.used_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
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
          @size-change="fetchCardKeys"
          @current-change="fetchCardKeys"
        />
      </div>
    </el-card>

    <!-- 导入对话框 -->
    <el-dialog v-model="showImportDialog" title="导入卡密" width="500px">
      <el-form ref="importFormRef" :model="importForm" :rules="importRules" label-width="80px">
        <el-form-item label="商品" prop="product_id">
          <el-select v-model="importForm.product_id" placeholder="选择商品">
            <el-option v-for="p in products" :key="p.id" :label="p.title" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            accept=".txt,.csv"
            :on-change="handleFileChange"
          >
            <el-button>选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 txt/csv 格式，每行一个卡密</div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button type="primary" @click="handleImport" :loading="importing">
          导入
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api, type CardKey, type Product, type CardKeyStats } from '@/api/client'

const cardKeys = ref<CardKey[]>([])
const products = ref<Product[]>([])
const stats = ref<CardKeyStats>({ total: 0, available: 0, used: 0 })
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const productFilter = ref<number>()
const statusFilter = ref('')

const showImportDialog = ref(false)
const importing = ref(false)
const importFormRef = ref()
const importForm = reactive({ product_id: null as number | null })
const importRules = { product_id: [{ required: true, message: '请选择商品', trigger: 'change' }] }
const selectedFile = ref<File | null>(null)

const fetchCardKeys = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const res = await api.getCardKeys({
      skip,
      limit: pageSize.value,
      product_id: productFilter.value,
      status: statusFilter.value || undefined,
    })
    cardKeys.value = res.items
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取卡密列表失败')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    stats.value = await api.getCardKeyStats(productFilter.value)
  } catch (error) {
    console.error('获取统计失败')
  }
}

const fetchProducts = async () => {
  try {
    const res = await api.getProducts({ limit: 100 })
    products.value = res.items
  } catch (error) {
    console.error('获取商品列表失败')
  }
}

const formatDate = (date: string) => new Date(date).toLocaleString('zh-CN')

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleImport = async () => {
  if (!importFormRef.value) return
  await importFormRef.value.validate((valid: boolean) => {
    if (!valid) {
      ElMessage.warning('请选择文件')
      return
    }
  })
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }
  if (!importForm.product_id) {
    ElMessage.warning('请选择商品')
    return
  }

  importing.value = true
  try {
    const result = await api.importCardKeys(selectedFile.value, importForm.product_id)
    ElMessage.success(`导入成功: ${result.imported} 个，失败: ${result.failed} 个`)
    showImportDialog.value = false
    fetchCardKeys()
    fetchStats()
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    importing.value = false
  }
}

onMounted(() => {
  fetchProducts()
  fetchCardKeys()
  fetchStats()
})
</script>

<style scoped>
.cardkeys-page { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { margin: 0; font-size: 24px; color: #2c2c24; }
.stats-row { margin-bottom: 20px; }
.stat-card { text-align: center; border-radius: 16px; }
.stat-value { font-size: 32px; font-weight: bold; color: #5d7052; }
.stat-card.success .stat-value { color: #67c23a; }
.stat-card.warning .stat-value { color: #e6a23c; }
.stat-label { color: #78786c; margin-top: 8px; }
.search-card { margin-bottom: 20px; }
.cardkeys-card { border-radius: 16px; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
