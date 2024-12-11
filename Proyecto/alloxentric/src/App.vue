<template>
  <v-app id="app" class="d-flex flex-column min-vh-100">
    <v-app-bar app color="#ffffff">
      <router-link  to="/" class="d-flex align-center" >
          <img :src="require('@/assets/alloxentric_logo_only.png')" alt="Alloxentric Logo" class="custom-logo" />
      </router-link>
      <v-container class="d-flex align-center" style="margin-right: 0px;">
        

        <nav class="d-none d-md-flex align-center">
          <v-btn text to="/" color="#42b983"><v-icon>mdi-home</v-icon>Inicio</v-btn>
          
          <v-btn text to="/planDetails" color="#42b983"><v-icon>mdi-cash</v-icon>Planes</v-btn>
          <v-btn v-if="!isAuthenticated" text
            href="http://localhost:8081/realms/Transcriptor/protocol/openid-connect/registrations?client_id=transcriptor_alloxentric&response_type=code&scope=openid&redirect_uri=http://localhost:8080/"
            color="#42b983">Registrarse</v-btn>
          <v-btn v-if="isAuthenticated" text to="/transcriptorWeb" color="#42b983"><v-icon>mdi-text-to-speech</v-icon>Transcriptor Web</v-btn>
          
          <v-menu v-if="isAdmin" transition="slide-y-transition">
            <template v-slot:activator="{ props }">
              <v-btn color="#42b983" v-bind="props" >
                Administrador <v-icon class="mdi mdi-menu-down"></v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in menuItems"
                :key="i"
                @click="navigate(item.to)"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <v-btn v-if="!isAuthenticated" text @click="handleAuthAction" id="authButton" color="#42b983">
            Iniciar Sesión
          </v-btn>
          <v-btn v-if="isAuthenticated" text to="/miCuenta" class="d-flex align-center">
            <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')" subtitle="Bienvenido"
              :title="userName" class="custom-title"></v-list-item>
          </v-btn>
        </nav>

        <v-app-bar-nav-icon @click="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <!-- Drawer para el menú desplegable -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item v-if="isAuthenticated" to="/miCuenta" link>
          <v-list-item lines="two" :prepend-avatar="require('@/assets/icon-account.png')"
            class="custom-title"><v-list-item-title class="custom-title">{{ userName }}</v-list-item-title>
            <v-list-item-subtitle>Bienvenido</v-list-item-subtitle></v-list-item>
        </v-list-item>

        <v-divider v-if="isAuthenticated" class="my-2"></v-divider>

        <v-list-item to="/" link>
          <v-list-item-title> <v-icon>mdi-home</v-icon> Inicio</v-list-item-title>
        </v-list-item>
        <v-list-item to="/planDetails" link>
          <v-list-item-title><v-icon>mdi-cash</v-icon>Planes</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAuthenticated" to="/transcriptorWeb" link>
          <v-list-item-title><v-icon>mdi-text-to-speech</v-icon>Transcriptor Web</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated"
          href="http://localhost:8081/realms/Transcriptor/protocol/openid-connect/registrations?client_id=transcriptor_alloxentric&response_type=code&scope=openid&redirect_uri=http://localhost:8080/">
          <v-list-item-title>Registrarse</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/CuadraturaMensual" link>
          <v-list-item-title><v-icon>mdi-calculator</v-icon>Cuadratura Mensual</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/crudPlanes" link>
          <v-list-item-title><v-icon>mdi-view-list</v-icon>Administrador de Planes</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/ventasReport" link>
          <v-list-item-title><v-icon>mdi-chart-bar</v-icon>Administrador de Ventas</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="isAdmin" to="/dashboard" link>
          <v-list-item-title><v-icon>mdi mdi-monitor-dashboard</v-icon>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" @click="handleAuthAction" link>
          <v-list-item-title>Iniciar Sesión</v-list-item-title>
        </v-list-item>

        <template v-if="isAuthenticated">
          <v-spacer></v-spacer>
          <v-list-item @click="handleAuthAction" link>
            <v-list-item-title class="error--text"><v-icon color="error">mdi-logout</v-icon>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </template>
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
      isAdmin: false, // Estado para verificar si el usuario es admin
      userName: '',
      menuItems: [
        { title: "Cuadratura Mensual", to: "/CuadraturaMensual" },
        { title: "Administrador de Planes", to: "/crudPlanes" },
        { title: "Administrador de Ventas", to: "/ventasReport" },
        { title: "Dashboard", to: "/dashboard" }
      ]
    };
  },
  methods: {
    navigate(route) {
      this.$router.push(route); // Navega usando Vue Router
    },
    handleAuthAction() {
      if (this.isAuthenticated) {
        keycloak.logout({
          redirectUri: `${window.location.origin}/`
        });
      } else {
        keycloak.login({
          redirectUri: `${window.location.origin}/`
        });
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
      this.userName = this.get_name_user();
    };
    keycloak.onAuthLogout = () => {
      this.isAuthenticated = false;
      this.isAdmin = false; // Restablece el rol de admin cuando se cierre sesión
      this.userName = '';
    };

    this.userName = this.get_name_user();
  }
}
</script>

<style>
.d-flex{
  display: flex !important;
  justify-content: end !important;
}


.custom-logo {
  padding-left: 10px;
  height: 40px;
  width: auto;
}

@media (max-width: 1280px) {
  .custom-logo{
    display: none !important;
  }
}

.v-icon {
  margin-right: 5px;
}

.v-application {
  background-color: white !important;
}


.v-main {
  flex: 1;
}

nav v-btn {
  color: #42b983;
}

.custom-title {
  color: #256649;
  font-weight: bold;
}

.v-list-item__avatar {
  margin-right: 16px;
}

.v-list-item-title{
  color: #42b983 !important;
}

.error--text {
  color: #ff5252 !important;
}
</style>