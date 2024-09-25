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
          <router-link v-if="isAdmin" to="/CuadraturaMensual">Cuadratura Mensual</router-link>
          <router-link v-if="isAdmin" to="/crudPlanes">Administrador de Planes</router-link>
          <router-link v-if="isAdmin" to="/ventasReport">Administrador de Ventas</router-link>
          <router-link to="/resumenPago">Resumen Pago Prueba</router-link>
          <router-link to="/historyTranscriptor">Historial</router-link>
          <v-link @click="handleAuthAction" id="authButton">
          {{ isAuthenticated ? 'Logout' : 'Login' }}
          </v-link>
          <router-link v-if="isAuthenticated" to="/miCuenta">
            <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')"
              subtitle="Bienvenido"
              :title="userName"
              ></v-list-item>
          </router-link>
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
          <v-link @click="handleAuthAction" id="authButton">
          {{ isAuthenticated ? 'Logout' : 'Login' }}
          </v-link>
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
import keycloak from '@/keycloak'; // Importa tu instancia de Keycloak

export default {
  name: 'App',
  components: {
    MainFooter
  },
  data() {
    return {
      drawer: false,
      isAuthenticated: false, // Estado de autenticación
      isAdmin: false // Estado para verificar si el usuario es admin
    };
  },
  methods: {
    handleAuthAction() {
      if (this.isAuthenticated) {
        keycloak.logout(); // Cierra sesión
      } else {
        keycloak.login(); // Inicia sesión
      }
    },
    checkUserRole() {
      if (this.isAuthenticated) {
        // Obtén el token del usuario
        const token = keycloak.tokenParsed;

        // Verifica si el usuario tiene el rol 'admin' en el cliente 'transcriptor_alloxentric'
        const clientRoles = token.resource_access?.['transcriptor_alloxentric']?.roles || [];
        this.isAdmin = clientRoles.includes('admin');
      }
    },
    get_name_user() {
      if (keycloak.authenticated) {
        const token = keycloak.tokenParsed;

        // Aquí asumo que el nombre y el apellido están en las propiedades 'given_name' y 'family_name'.
        const firstName = token.given_name; // Cambia esto si el nombre está en otro campo
        const lastName = token.family_name; // Cambia esto si el apellido está en otro campo

        return `${firstName} ${lastName}`; // Retorna el nombre completo
      }
      return ''; // Retorna vacío si no está autenticado
    }
  },
  mounted() {
    // Verificar el estado de autenticación al montar el componente
    this.isAuthenticated = keycloak.authenticated;
    this.checkUserRole();

    // Escuchar los cambios de autenticación de Keycloak
    keycloak.onAuthSuccess = () => {
      this.isAuthenticated = true;
      this.checkUserRole(); // Verifica el rol del usuario cuando se autentique
    };
    keycloak.onAuthLogout = () => {
      this.isAuthenticated = false;
      this.isAdmin = false; // Restablece el rol de admin cuando se cierre sesión
    };

    this.userName = this.get_name_user();
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

#authButton {
  color: #42b983;
  font-family: 'Roboto', sans-serif;
  text-transform: none;
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
  text-decoration: none;
}

#authButton:hover {
  background: none;
}
</style>