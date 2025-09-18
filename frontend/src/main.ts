import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

axios.defaults.baseURL = "http://bookclub.qa.guru:8000"

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const authStore = useAuthStore()
authStore.loadState()
if (authStore.isAuthenticated && authStore.accessToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.accessToken}`
  authStore.fetchUser().catch(() => authStore.logout())
}

app.mount('#app')
