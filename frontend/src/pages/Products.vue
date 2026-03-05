<template>
  <div class="products-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>商品管理</h1>
      <el-button type="primary" @click="showAddDialog = true">
        添加商品
      </el-button>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="搜索">
          <el-input v-model="search" placeholder="商品标题" clearable @keyup.enter="fetchProducts" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable>
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已下架" value="offline" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchProducts">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 商品列表 -->
    <el-card class="products-card">
      <el-table :data="products" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="商品标题" min-width="200" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">
            ¥{{ row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="xianyu_id" label="闲鱼ID" width="120">
          <template #default="{ row }">
            {{ row.xianyu_id || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button
              v-if="row.status === 'draft'"
              size="small"
              type="success"
              @click="handlePublish(row)"
            >
              上架
            </el-button>
            <el-button
              v-else-if="row.status === 'published'"
              size="small"
              @click="handleUnpublish(row)"
            >
              下架
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
          @size-change="fetchProducts"
          @current-change="fetchProducts"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="isEdit ? '编辑商品' : '添加商品'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入商品标题" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="4" />
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
import { ElMessage } from 'element-plus'
import { api, type Product, type ProductCreate, type ProductUpdate } from '@/api/client'

const products = ref<Product[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const search = ref('')
const statusFilter = ref('')

const showAddDialog = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref()
const editingId = ref<number | null>(null)

const form = reactive<ProductCreate>({
  title: '',
  price: '0',
  description: '',
})

const formRules = {
  title: [{ required: true, message: '请输入商品标题', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
}

const fetchProducts = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const res = await api.getProducts({
      skip,
      limit: pageSize.value,
      status: statusFilter.value || undefined,
      search: search.value || undefined,
    })
    products.value = res.items
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    draft: 'info',
    published: 'success',
    offline: 'warning',
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    draft: '草稿',
    published: '已发布',
    offline: '已下架',
  }
  return texts[status] || status
}

const formatDate = (date: string) => new Date(date).toLocaleString('zh-CN')

const handleEdit = (row: Product) => {
  isEdit.value = true
  editingId.value = row.id
  form.title = row.title
  form.price = row.price
  form.description = row.description || ''
  showAddDialog.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  submitting.value = true

  try {
    if (isEdit.value && editingId.value) {
      const data: ProductUpdate = {
        title: form.title,
        price: form.price,
        description: form.description,
      }
      await api.updateProduct(editingId.value, data)
      ElMessage.success('更新成功')
    } else {
      await api.createProduct(form)
      ElMessage.success('添加成功')
    }
    showAddDialog.value = false
    resetForm()
    fetchProducts()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  } finally {
    submitting.value = false
  }
}

const handlePublish = async (row: Product) => {
  try {
    await api.publishProduct(row.id)
    ElMessage.success('上架成功')
    fetchProducts()
  } catch (error) {
    ElMessage.error('上架失败')
  }
}

const handleUnpublish = async (row: Product) => {
  try {
    await api.unpublishProduct(row.id)
    ElMessage.success('下架成功')
    fetchProducts()
  } catch (error) {
    ElMessage.error('下架失败')
  }
}

const resetForm = () => {
  isEdit.value = false
  editingId.value = null
  form.title = ''
  form.price = '0'
  form.description = ''
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.products-page { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { margin: 0; font-size: 24px; color: #2c2c24; }
.search-card { margin-bottom: 20px; }
.products-card { border-radius: 16px; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
