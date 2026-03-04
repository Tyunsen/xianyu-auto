<template>
  <div class="messages">
    <h2>消息管理</h2>
    <el-card>
      <template #header>
        <span>消息列表</span>
      </template>
      <el-table :data="[]" empty-text="暂无消息">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="from_user" label="发送人" />
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag type="info">未读</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.messages h2 { margin-bottom: 20px; }
</style>
