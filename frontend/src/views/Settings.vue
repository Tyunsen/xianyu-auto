<template>
  <div class="settings">
    <h2>系统设置</h2>
    <el-card>
      <template #header>
        <span>基础设置</span>
      </template>
      <el-form label-width="120px">
        <el-form-item label="任务运行间隔">
          <el-input-number v-model="settings.interval" :min="1" :max="10" />
          <span style="margin-left: 10px">分钟</span>
        </el-form-item>
        <el-form-item label="随机延迟范围">
          <el-input-number v-model="settings.random_delay" :min="0" :max="60" />
          <span style="margin-left: 10px">秒</span>
        </el-form-item>
        <el-form-item label="操作限流">
          <el-input-number v-model="settings.max_per_hour" :min="1" :max="100" />
          <span style="margin-left: 10label">次/小时</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const settings = reactive({
  interval: 1,
  random_delay: 30,
  max_per_hour: 20
})

const handleSave = () => { }
</script>

<style scoped>
.settings h2 { margin-bottom: 20px; }
</style>
