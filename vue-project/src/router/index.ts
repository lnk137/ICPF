import { createRouter, createWebHashHistory } from 'vue-router'
import Set from '@/views/Set.vue'
import Upload from '@/views/Upload.vue'
import Result from '@/views/Result.vue'
import Test from '@/views/Test.vue'
import Animation from '@/views/Animation.vue'


const router = createRouter({
  history: createWebHashHistory(),  // 使用 Hash 模式的路由历史记录
  routes: [
    {path: "/",redirect: "/animation"}, // 访问根路径时重定向到 /home,
    { path: '/set', component: Set },
    { path: '/upload', component: Upload },
    { path: '/result', component: Result },
    { path: '/test', component: Test },
    { path: '/animation', component: Animation },
  ]
})

export default router
