<template>
  <div class="logs">
    <h2>运行日志</h2>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>日志列表</span>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </template>
      <el-table :data="[]" empty-text="暂无日志">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="level" label="级别" width="100">
          <template #default="{ row }">
            <el-tag :type="row.level === 'ERROR' ? 'danger' : 'info'">{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="消息" />
        <el-table-column prop="created_at" label="时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
const handleRefresh = () => { }
</script>

<style scoped>
.logs h2 { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
