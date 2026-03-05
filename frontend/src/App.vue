<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="$route.path"
          router
          class="el-menu-vertical"
        >
          <el-menu-item index="/accounts">
            <span>账号管理</span>
          </el-menu-item>
          <el-menu-item index="/products">
            <span>商品管理</span>
          </el-menu-item>
          <el-menu-item index="/card-keys">
            <span>卡密管理</span>
          </el-menu-item>
          <el-menu-item index="/orders">
            <span>订单管理</span>
          </el-menu-item>
          <el-menu-item index="/messages">
            <span>消息管理</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/logs">
            <span>运行日志</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header>
          <h2>闲鱼自动管理系统</h2>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
}

.el-menu-vertical {
  border-right: none;
}

.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
}

.el-main {
  background-color: #f0f2f5;
}
</style>
