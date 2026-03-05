<template>
  <div class="statistics-page">
    <div class="page-header"><h1>数据统计</h1></div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon"><el-icon :size="32"><User /></el-icon></div>
          <div class="stat-value">{{ stats.accounts }}</div>
          <div class="stat-label">账号数量</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon"><el-icon :size="32"><Goods /></el-icon></div>
          <div class="stat-value">{{ stats.products }}</div>
          <div class="stat-label">商品数量</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon"><el-icon :size="32"><Ticket /></el-icon></div>
          <div class="stat-value">{{ stats.cardKeys }}</div>
          <div class="stat-label">卡密库存</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon"><el-icon :size="32"><Coin /></el-icon></div>
          <div class="stat-value">¥{{ stats.sales }}</div>
          <div class="stat-label">销售额</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header><span>订单趋势</span></template>
          <div class="chart-placeholder">订单趋势图表</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header><span>销售统计</span></template>
          <div class="chart-placeholder">销售统计图表</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { User, Goods, Ticket, Coin } from '@element-plus/icons-vue'
import { api } from '@/api/client'

const stats = ref({ accounts: 0, products: 0, cardKeys: 0, sales: 0 })

const fetchStats = async () => {
  try {
    const [accountsRes, productsRes, cardKeysRes, ordersRes] = await Promise.all([
      api.getAccounts({ limit: 1 }),
      api.getProducts({ limit: 1 }),
      api.getCardKeyStats(),
      api.getOrders({ limit: 100 }),
    ])
    stats.value.accounts = accountsRes.total
    stats.value.products = productsRes.total
    stats.value.cardKeys = cardKeysRes.value.available
    stats.value.sales = ordersRes.items.reduce((sum: number, o: any) => sum + parseFloat(o.amount || '0'), 0).toFixed(2)
  } catch (e) {
    console.error('获取统计失败', e)
  }
}

onMounted(() => fetchStats())
</script>

<style scoped>
.statistics-page { padding: 20px; }
.page-header h1 { margin: 0 0 20px; font-size: 24px; color: #2c2c24; }
.stats-row { margin-bottom: 20px; }
.stat-card { text-align: center; border-radius: 16px; }
.stat-icon { color: #5d7052; margin-bottom: 12px; }
.stat-value { font-size: 28px; font-weight: bold; color: #2c2c24; }
.stat-label { color: #78786c; margin-top: 8px; }
.chart-card { border-radius: 16px; height: 300px; }
.chart-placeholder { height: 240px; display: flex; align-items: center; justify-content: center; color: #999; }
</style>
