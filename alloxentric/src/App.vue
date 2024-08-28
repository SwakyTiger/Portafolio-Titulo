<template>
  <v-app id="app" class="d-flex flex-column min-vh-100">
    <v-app-bar app>
      <v-container class="d-flex align-center justify-space-between">
        <router-link to="/" class="d-flex align-center">
          <img
            :src="require('@/assets/alloxentric_logo_only.png')"
            alt="Alloxentric Logo"
            class="custom-logo"
          />
        </router-link>
        
        <nav class="d-none d-md-flex align-center">
          <router-link to="/">Inicio</router-link>
          <router-link to="/planDetails">Planes</router-link>
          <router-link to="/RegistroUsuario">Registrarse</router-link>
          <router-link to="/CuadraturaMensual">Cuadratura Mensual</router-link>
          <router-link to="/crudPlanes">Administrador de Planes</router-link>
          <router-link to="/ventasReport">Administrador de Ventas</router-link>
          <router-link to="/resumenPago">PRUEBA</router-link>
          <v-btn @click="handleAuthAction" color="primary" id="authButton">
          {{ isAuthenticated ? 'Logout' : 'Login' }}
          </v-btn>
        </nav>


        <!-- Menú -->
        <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <!-- Drawer para el menú desplegable -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item>
          <router-link to="/">Inicio</router-link>
        </v-list-item>
        <v-list-item>
          <router-link to="/planDetails">Planes</router-link>
        </v-list-item>
        <v-list-item>
          <router-link to="/RegistroUsuario">Registrarse</router-link>
        </v-list-item>
        <v-list-item>
          <router-link to="/CuadraturaMensual">Cuadratura Mensual</router-link>
        </v-list-item>
        <v-list-item>
          <router-link to="/crudPlanes">Administrador de Planes</router-link>
        </v-list-item>
        <v-list-item>
          <v-btn @click="handleAuthAction" color="primary" id="authButton">
          {{ isAuthenticated ? 'Logout' : 'Login' }}
          </v-btn>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Contenido principal -->
    <v-main class="flex-grow-1">
      <router-view />
    </v-main>

    <!-- Footer -->
    <MainFooter />
  </v-app>
</template>

<script>
import MainFooter from '@/components/views/MainFooter.vue';
import keycloak from '@/keycloak'; // Asegúrate de importar tu instancia de Keycloak

export default {
  name: 'App',
  components: {
    MainFooter
  },
  data() {
    return {
      drawer: false,
      isAuthenticated: keycloak.authenticated // Estado de autenticación
    };
  },
  methods: {
    handleAuthAction() {
      if (this.isAuthenticated) {
        keycloak.logout(); // Cierra sesión
      } else {
        keycloak.login(); // Inicia sesión
      }
    }
  },
  mounted() {
    // Escuchar los cambios de autenticación de Keycloak
    keycloak.onAuthSuccess = () => {
      this.isAuthenticated = true;
    };
    keycloak.onAuthLogout = () => {
      this.isAuthenticated = false;
    };
  }
}
</script>

<style>
.custom-logo {
  width: 50px;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

nav {
  background-color: #ffffff;
}

nav a {
  margin-right: 15px;
  text-decoration: none;
  color: #42b983;
}

.v-main {
  flex: 1;
}
</style>
