import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import Vueform from '@vueform/vueform'
import vueformConfig from './../vueform.config'

const app = createApp(App).use(Vueform, vueformConfig).use(router).mount('#app')
