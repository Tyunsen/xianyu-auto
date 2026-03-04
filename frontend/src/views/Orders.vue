<template>
  <div class="orders">
    <h2>订单管理</h2>
    <el-card>
      <template #header>
        <span>订单列表</span>
      </template>
      <el-table :data="[]" empty-text="暂无订单">
        <el-table-column prop="id" label="订单ID" width="100" />
        <el-table-column prop="product_title" label="商品" />
        <el-table-column prop="buyer" label="买家" />
        <el-table-column prop="price" label="金额" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag>待处理</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.orders h2 { margin-bottom: 20px; }
</style>
