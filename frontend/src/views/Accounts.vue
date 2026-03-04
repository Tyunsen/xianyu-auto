<template>
  <div class="accounts">
    <h2>账号管理</h2>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账号列表</span>
          <el-button type="primary" @click="handleAdd">添加账号</el-button>
        </div>
      </template>
      <el-table :data="[]" empty-text="暂无账号">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="账号名称" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag>待添加</el-tag>
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
const handleAdd = () => {
  // TODO: 添加账号
}
</script>

<style scoped>
.accounts h2 {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
