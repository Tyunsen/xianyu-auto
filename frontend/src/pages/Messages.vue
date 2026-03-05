<template>
  <div class="messages-page">
    <div class="page-header"><h1>消息管理</h1></div>

    <el-row :gutter="20">
      <el-col :span="10">
        <el-card class="list-card">
          <template #header><span>消息列表</span></template>
          <el-table :data="messages" v-loading="loading" @row-click="selectMessage" highlight-current-row>
            <el-table-column prop="from_user" label="来自" width="120" />
            <el-table-column prop="content" label="内容" show-overflow-tooltip />
            <el-table-column prop="is_read" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_read ? 'info' : 'warning'" size="small">{{ row.is_read ? '已读' : '未读' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间" width="120">
              <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
            </el-table-column>
          </el-table>
          <div class="pagination">
            <el-pagination v-model:current-page="currentPage" :page-size="20" :total="total"
              layout="prev, pager, next" @current-change="fetchMessages" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card class="detail-card">
          <template #header>
            <span>对话详情 - {{ selectedUser || '请选择消息' }}</span>
          </template>
          <div class="conversation" v-if="conversation.length">
            <div v-for="msg in conversation" :key="msg.id" :class="['msg', msg.reply_content ? 'reply' : 'received']">
              <div class="msg-content">{{ msg.reply_content || msg.content }}</div>
              <div class="msg-time">{{ formatDate(msg.created_at) }}</div>
            </div>
          </div>
          <el-empty v-else description="请选择一条消息查看详情" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api, type Message } from '@/api/client'

const messages = ref<Message[]>([])
const conversation = ref<Message[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const selectedUser = ref('')
const selectedAccountId = ref(1)

const fetchMessages = async () => {
  loading.value = true
  try {
    const res = await api.getMessages({ skip: (currentPage.value - 1) * 20, limit: 20 })
    messages.value = res.items
    total.value = res.total
  } catch { ElMessage.error('获取消息失败') }
  finally { loading.value = false }
}

const selectMessage = async (row: Message) => {
  selectedUser.value = row.from_user
  selectedAccountId.value = row.account_id
  try {
    const res = await api.getConversation(row.account_id, row.from_user)
    conversation.value = res.items
  } catch { ElMessage.error('获取对话失败') }
}

const formatDate = (d: string) => new Date(d).toLocaleString('zh-CN')

onMounted(() => fetchMessages())
</script>

<style scoped>
.messages-page { padding: 20px; }
.page-header h1 { margin: 0 0 20px; font-size: 24px; color: #2c2c24; }
.list-card, .detail-card { border-radius: 16px; height: 600px; }
.conversation { max-height: 480px; overflow-y: auto; }
.msg { margin-bottom: 16px; padding: 12px; border-radius: 12px; max-width: 80%; }
.msg.received { background: #f0f2f5; margin-right: auto; }
.msg.reply { background: #e6f4ff; margin-left: auto; }
.msg-content { word-break: break-all; }
.msg-time { font-size: 12px; color: #999; margin-top: 4px; }
.pagination { margin-top: 16px; justify-content: center; display: flex; }
</style>
