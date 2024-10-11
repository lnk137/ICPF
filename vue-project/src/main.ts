
import { createApp } from 'vue'
import App from './App.vue'
import '@/styles/variables.css'
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';
import { createPinia } from 'pinia';
import router from './router'

const app = createApp(App)
const pinia = createPinia();

// 使用 Pinia
app.use(pinia);
app.use(router)

app.mount('#app')
