import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/accounts',
    },
    {
      path: '/accounts',
      name: 'Accounts',
      component: () => import('@/pages/Accounts.vue'),
    },
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/pages/Products.vue'),
    },
    {
      path: '/card-keys',
      name: 'CardKeys',
      component: () => import('@/pages/CardKeys.vue'),
    },
    {
      path: '/orders',
      name: 'Orders',
      component: () => import('@/pages/Orders.vue'),
    },
    {
      path: '/messages',
      name: 'Messages',
      component: () => import('@/pages/Messages.vue'),
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: () => import('@/pages/Statistics.vue'),
    },
    {
      path: '/logs',
      name: 'Logs',
      component: () => import('@/pages/Logs.vue'),
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/pages/Settings.vue'),
    },
  ],
})

export default router
