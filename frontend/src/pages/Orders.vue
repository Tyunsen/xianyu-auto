<template>
  <div class="orders-page">
    <div class="page-header"><h1>订单管理</h1></div>

    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable @change="fetchOrders">
            <el-option label="待处理" value="pending" />
            <el-option label="已支付" value="paid" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="orders-card">
      <el-table :data="orders" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="buyer_nickname" label="买家" width="120" />
        <el-table-column prop="product_id" label="商品ID" width="100" />
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="{ row }">¥{{ row.amount }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === 'paid'" size="small" type="success" @click="handleShip(row)">发货</el-button>
            <el-button v-if="row.status === 'shipped'" size="small" @click="handleComplete(row)">完成</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
          :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next"
          @size-change="fetchOrders" @current-change="fetchOrders" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api, type Order } from '@/api/client'

const orders = ref<Order[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const statusFilter = ref('')

const fetchOrders = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const res = await api.getOrders({ skip, limit: pageSize.value, status: statusFilter.value || undefined })
    orders.value = res.items
    total.value = res.total
  } catch { ElMessage.error('获取订单失败') }
  finally { loading.value = false }
}

const getStatusType = (s: string) => ({ pending: 'info', paid: 'warning', shipped: 'primary', completed: 'success', cancelled: 'danger' }[s] || 'info')
const getStatusText = (s: string) => ({ pending: '待处理', paid: '已支付', shipped: '已发货', completed: '已完成', cancelled: '已取消' }[s] || s)
const formatDate = (d: string) => new Date(d).toLocaleString('zh-CN')

const handleShip = async (row: Order) => {
  try { await api.shipOrder(row.id); ElMessage.success('发货成功'); fetchOrders() }
  catch { ElMessage.error('发货失败') }
}

const handleComplete = async (row: Order) => {
  try { await api.completeOrder(row.id); ElMessage.success('完成成功'); fetchOrders() }
  catch { ElMessage.error('操作失败') }
}

onMounted(() => fetchOrders())
</script>

<style scoped>
.orders-page { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { margin: 0; font-size: 24px; color: #2c2c24; }
.search-card { margin-bottom: 20px; }
.orders-card { border-radius: 16px; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
