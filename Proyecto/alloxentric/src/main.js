import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import keycloak from './keycloak'
import '@mdi/font/css/materialdesignicons.css'

loadFonts();

keycloak.init({ 
  onLoad: 'check-sso',  // Cambia 'login-required' por 'check-sso'
  checkLoginIframe: true 
}).then(() => {
  const app = createApp(App);
  app.config.globalProperties.$keycloak = keycloak;
  app.use(router).use(vuetify).mount('#app');

}).catch((err) => {
  console.error("Error al inicializar Keycloak", err);
});
