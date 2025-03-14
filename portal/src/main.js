import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import store from './stores/index.js'
import './index.css'

createApp(App).use(router).use(store).mount('#app')
