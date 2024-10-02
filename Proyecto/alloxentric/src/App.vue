<template>
  <v-app id="app" class="d-flex flex-column min-vh-100">
    <v-app-bar app color="#ffffff" dark>
      <v-container class="d-flex align-center">
        <router-link to="/" class="d-flex align-center" style="text-decoration: none;"> 
          <img
            :src="require('@/assets/alloxentric_logo_only.png')"
            alt="Alloxentric Logo"
            class="custom-logo"
          />
        </router-link>
        
        <v-spacer></v-spacer>

        <nav class="d-none d-md-flex align-center">
          <v-btn text to="/" color="#42b983">Inicio</v-btn>
          <v-btn text to="/planDetails" color="#42b983">Planes</v-btn>
          <v-btn v-if="!isAuthenticated" text to="/RegistroUsuario" color="#42b983">Registrarse</v-btn>
          <v-btn v-if="isAdmin" text to="/CuadraturaMensual" color="#42b983">Cuadratura Mensual</v-btn>
          <v-btn v-if="isAdmin" text to="/crudPlanes" color="#42b983">Administrador de Planes</v-btn>
          <v-btn v-if="isAdmin" text to="/ventasReport" color="#42b983">Administrador de Ventas</v-btn>
          <v-btn v-if="!isAuthenticated" text @click="handleAuthAction" id="authButton" color="#42b983">
           Iniciar Sesión
          </v-btn>
          <v-btn v-if="isAuthenticated" text to="/miCuenta" class="d-flex align-center">
            <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')"
              subtitle="Bienvenido"
              :title="userName"
              class="custom-title"
              ></v-list-item>
          </v-btn>
        </nav>

        <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <!-- Drawer para el menú desplegable -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item to="/" link>
          <v-list-item-title>Inicio</v-list-item-title>
        </v-list-item>
        <v-list-item to="/planDetails" link>
          <v-list-item-title>Planes</v-list-item-title>
        </v-list-item>
        <v-list-item to="/RegistroUsuario" link>
          <v-list-item-title>Registrarse</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/CuadraturaMensual" link>
          <v-list-item-title>Cuadratura Mensual</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/crudPlanes" link>
          <v-list-item-title>Administrador de Planes</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/ventasReport" link>
          <v-list-item-title>Administrador de Ventas</v-list-item-title>
        </v-list-item>
        <v-list-item @click="handleAuthAction" link>
          <v-list-item-title>{{ isAuthenticated ? '' : 'Iniciar Sesión' }}</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" to="/miCuenta" link>
          <v-list-item-avatar>
            <v-img :src="require('@/assets/icon-account.png')" alt="User Avatar"></v-img>
          </v-list-item-avatar>
          <v-list-item-title>{{ userName }}</v-list-item-title>
          <v-list-item-subtitle>Bienvenido</v-list-item-subtitle>
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

        console.log('Sesión cerrada')
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
.v-application {
  background-color: white !important;
}
.custom-logo {
  height: 40px;
  width: auto;
}

.v-main {
  flex: 1;
}

nav v-btn  {
  color: #42b983;
}

.custom-title {
  color: #256649;
}

</style>