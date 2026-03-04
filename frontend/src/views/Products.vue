<template>
  <div class="products">
    <h2>商品管理</h2>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>商品列表</span>
          <el-button type="primary" @click="handleAdd">添加商品</el-button>
        </div>
      </template>
      <el-table :data="[]" empty-text="暂无商品">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="商品标题" />
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="stock" label="库存" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag>待添加</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default>
            <el-button size="small">编辑</el-button>
            <el-button size="small" type="danger">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
const handleAdd = () => {
  // TODO: 添加商品
}
</script>

<style scoped>
.products h2 { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
