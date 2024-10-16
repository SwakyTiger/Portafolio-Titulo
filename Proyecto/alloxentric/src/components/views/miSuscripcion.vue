<template>
    <v-container fluid class="pa-0">
      <v-card flat>
        <v-card-title class="custom-title text-h4 font-weight-bold white--text pb-4">
          <h1>Historial de Suscripciones</h1>
        </v-card-title>
  
        <v-row no-gutters>
          <v-col cols="12" md="3">
            <v-card flat class="h-100">
              <v-list>
                <v-list-item
                  :prepend-avatar="require('@/assets/icon-account.png')"
                  :title="fullName"
                  :subtitle="email"
                ></v-list-item>
              </v-list>
              <v-divider></v-divider>
              <v-list nav density="compact">
                <v-list-item
                  prepend-icon="mdi-view-dashboard"
                  title="Mi Cuenta"
                  value="home"
                  to="/miCuenta"
                ></v-list-item>
                <v-list-item
                  prepend-icon="mdi-forum"
                  title="Historial"
                  value="about"
                  to="/historyTranscriptor"
                ></v-list-item>
                <v-list-item prepend-icon="mdi-forum" title="Mis Suscripciones" value="about"
                                to="/miSuscripcion"></v-list-item>
                <v-list-item
                  prepend-icon="mdi-logout"
                  :title="isAuthenticated ? 'Cerrar Sesión' : ''"
                  @click="handleAuthAction"
                  id="authButton"
                  class="error--text"
                ></v-list-item>
              </v-list>
            </v-card>
          </v-col>
  
          <v-col cols="12" md="9">
            <v-card flat class="pa-6">
              <v-data-table
                :headers="headers"
                :items="subscriptions"
                :search="search"
                :items-per-page="10"
                class="mt-4"
              >
              </v-data-table>
              
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import axios from "axios";
  import keycloak from "@/keycloak";
  
  export default {
    name: "HistorialTranscriptor",
    data() {
      return {
        fullName: "",
        email: "",
        search: "",
        subscriptions: [], // Aquí se almacenarán las suscripciones del usuario
        headers: [
          {
            align: "start",
            key: "nombre_plan",
            sortable: false,
            title: "Plan",
          },
          {
            align: "start",
            key: "fecha_vencimiento",
            sortable: true,
            title: "Fecha de Vencimiento",
          },
          {
            align: "start",
            key: "estado",
            sortable: true,
            title: "Estado",
          },
        ],
        isAuthenticated: false,
      };
    },
    methods: {
      handleAuthAction() {
        if (this.isAuthenticated) {
          keycloak.logout({
            redirectUri: window.location.origin,
          });
        } else {
          keycloak.login();
        }
      },
      get_user_data() {
        if (keycloak.authenticated) {
          const token = keycloak.tokenParsed;
          this.fullName = token.name || "";
          this.email = token.email || "";
          this.getUserSubscriptions(token.sub); // Obtener las suscripciones del usuario
        }
      },
      // Nuevo método para obtener las suscripciones del usuario desde el backend
      async getUserSubscriptions(userId) {
        try {
          const response = await axios.get(`http://localhost:8000/suscripciones/${userId}`, {
            headers: {
              Authorization: `Bearer ${keycloak.token}`,
            },
          });
          this.subscriptions = response.data; // Guardar las suscripciones obtenidas
        } catch (error) {
          console.error("Error al obtener suscripciones:", error);
        }
      },
      formatDate(dateString) {
        const options = {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        };
        return new Date(dateString).toLocaleDateString("es-ES", options);
      },
    },
    mounted() {
      this.isAuthenticated = keycloak.authenticated;
      keycloak.onAuthLogout = () => {
        this.isAuthenticated = false;
      };
      this.get_user_data();
    },
  };
  </script>
  
  <style scoped>
  .v-card {
    border-radius: 8px;
  }
  .v-list-item--active {
    background-color: #e6f7f0;
  }
  #authButton {
    font-size: 14px;
    color: #ff5252;
  }
  .v-data-table {
    background-color: white;
  }
  
  .custom-title {
    background-color: #1ebea4;
    width: 100%;
    height: 200px;
    display: flex;
    /* Asegura que el título esté centrado */
    align-items: center;
    justify-content: center;
    color: white;
  }
  </style>
  