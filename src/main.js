import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App)

//路由
import { createRouter, createWebHistory } from 'vue-router'
import routes from './router/index'
const router = createRouter({
    history: createWebHistory(),
    routes
})
app.use(router)
app.provide('$route', router.currentRoute)

// 设置axios全局配置
import axios from 'axios';
app.config.globalProperties.$axios = axios;
axios.defaults.baseURL = 'http://aa7415157.e2.luyouxia.net:28152';

//element ui
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(ElementPlus)



//全局变量
import store from './store';
app.use(store)

app.mount('#app')