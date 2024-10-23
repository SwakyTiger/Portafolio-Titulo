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
            <v-card height="100%" class="tarjeta" border>
              <v-card-item>
                <v-card-title class="text-h3 text-center">
                  Nombre Plan: {{ subscription.nombre_plan }}
                </v-card-title>
                
                <v-card-text class="text-h5 text-center pt-2">
                  Total Pagado: ${{ subscription.total_pagado / 100 }} USD
                </v-card-text>
              </v-card-item>

              <v-card-text>
                <v-list density="compact" class="text-h5 text-center pt-2 ">
                  <v-list-item>Estado: {{ subscription.estado }}</v-list-item>
                </v-list>
              </v-card-text>

              <v-spacer></v-spacer>

              <v-card-actions class="justify-center pb-4">
                <v-btn variant="elevated" color="error" @click="cancelSubscription(subscription.id_suscripcion)">
                  Cancelar Suscripción
                </v-btn>
                <v-btn variant="elevated" color="primary" @click="openPlanDialog">
                  Actualizar Plan
                </v-btn>
              </v-card-actions>
              <v-dialog v-model="isPlanDialogOpen" max-width="500px">
              <v-card>
                <v-card-title class="text-h5">Selecciona un nuevo plan</v-card-title>
                <v-card-text>
                  <v-radio-group v-model="selectedPlan">
                    <v-radio
                      v-for="plan in availablePlans"
                      :key="plan.id"
                      :label="`${plan.nombre} - $${plan.precio/100} USD`"
                      :value="plan.stripe_price_id"
                      :color="primary"
                    ></v-radio>
                  </v-radio-group>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="isPlanDialogOpen = false">Cancelar</v-btn>
                  <v-btn color="green darken-1" text @click="updateSubscription">Actualizar</v-btn>
                </v-card-actions>
                </v-card>
              </v-dialog>
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
  data() {
    return {
      fullName: "",
      email: "",
      subscription: {}, // Objeto para almacenar la suscripción del usuario
      isAuthenticated: false,
      isPlanDialogOpen: false,
      selectedPlan: null,
      availablePlans: [],
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
    handlePlanSelection(planId) {
      console.log('Plan seleccionado:', planId);
      this.selectedPlan = planId;
    },
    openPlanDialog() {
      this.selectedPlan = null; // Reset la selección cuando se abre el diálogo
      this.fetchAvailablePlans();
      this.isPlanDialogOpen = true;
      console.log(this.availablePlans.stripe_price_id)
      
    },
    async fetchAvailablePlans() {
      try {
        // Llama al backend para obtener los planes disponibles
        const response = await axios.get("http://localhost:8000/plans", {
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        });
        this.availablePlans = response.data; // Almacena los planes en el array availablePlans
        console.log(this.availablePlans)
      } catch (error) {
        console.error("Error al obtener planes:", error);
        this.$toast.error("Hubo un problema al obtener los planes.");
      }
    },
    get_user_data() {
      if (keycloak.authenticated) {
        const token = keycloak.tokenParsed;
        this.fullName = token.name || "";
        this.email = token.email || "";
        this.getUserSubscription(token.sub); // Obtener la suscripción del usuario
      }
    },
    // Obtener la suscripción del usuario desde el backend
    async getUserSubscription(userId) {
      try {
        const response = await axios.get(`http://localhost:8000/suscripciones/${userId}`, {
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        });
        this.subscription = response.data[0]
      } catch (error) {
        console.error("Error al obtener suscripción:", error);
      }
    },
    async cancelSubscription(subscriptionId) {
    try {
      console.log(`Cancelar suscripción: ${subscriptionId}`);

      // Realiza la solicitud HTTP al backend para cancelar la suscripción
      const response = await axios.post(`http://localhost:8000/suscripciones/cancelar_suscripcion/${subscriptionId}`);
      
      if (response.data.message) {
        // Mostrar un mensaje de éxito o actualizar la UI según sea necesario
        this.$toast.success("Suscripción configurada para cancelarse al final del período.");
        console.log(response.data.message);
        // Opcional: Refrescar los datos de suscripción
        await this.fetchSubscriptionData();
      }
    } catch (error) {
      console.error("Error al cancelar la suscripción:", error);
      this.$toast.error("Hubo un problema al cancelar la suscripción. Inténtalo de nuevo más tarde.");
    }
  },
  async updateSubscription() {
    console.log('Iniciando actualización de suscripción');
    console.log('Plan seleccionado:', this.selectedPlan);
    console.log('Suscripción actual:', this.subscription.id_suscripcion);
  try {
    const response = await axios.post(`http://localhost:8000/actualizar_suscripcion/${this.subscription.id_suscripcion}/${this.selectedPlan}`, {
    headers: {
      Authorization: `Bearer ${keycloak.token}`,
    }
    });
    if (response.data) {
          this.isPlanDialogOpen = false;
        }
  } catch (error) {
    console.error("Error al actualizar la suscripción:", error);
    this.$toast.error("Hubo un problema al actualizar la suscripción.");
  }
  },
  async fetchSubscriptionData() {
    // Lógica para obtener los datos actualizados de las suscripciones del usuario
    // Esto debería hacer una llamada a la API para recuperar la suscripción actualizada
  },
  },
  mounted() {
    this.fetchAvailablePlans();
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
  .tarjeta{
    padding: 50px;
  }
  </style>
  