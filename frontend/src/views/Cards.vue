<template>
  <div class="cards">
    <h2>卡密管理</h2>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>卡密列表</span>
          <el-button type="primary" @click="handleAdd">添加卡密</el-button>
        </div>
      </template>
      <el-table :data="[]" empty-text="暂无卡密">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="card_key" label="卡密" />
        <el-table-column prop="product_id" label="所属商品" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag type="success">待使用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="添加时间" />
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
const handleAdd = () => { }
</script>

<style scoped>
.cards h2 { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
