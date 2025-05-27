import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入 router

createApp(App)
  .use(router) // 使用 router
  .mount('#app');
