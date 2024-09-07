import { createRouter, createWebHashHistory } from 'vue-router'
import Page1 from '@/views/Page1.vue'
import Page2 from '@/views/Page2.vue'
import Page3 from '@/views/Page3.vue'
import Show from '@/views/Show.vue'
import Test from '@/views/Test.vue'
import Animation from '@/views/Animation.vue'


const router = createRouter({
  history: createWebHashHistory(),  // 使用 Hash 模式的路由历史记录
  routes: [
    {path: "/",redirect: "/animation"}, // 访问根路径时重定向到 /home,
    { path: '/page1', component: Page1 },
    { path: '/page2', component: Page2 },
    { path: '/page3', component: Page3 },
    { path: '/show', component: Show },
    { path: '/test', component: Test },
    { path: '/animation', component: Animation },
  ]
})

export default router
