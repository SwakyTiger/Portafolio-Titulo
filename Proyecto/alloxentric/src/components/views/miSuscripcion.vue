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
              <v-list-item 
                prepend-icon="mdi mdi-credit-card" 
                title="Mis Suscripciones" 
                value="about"
                to="/miSuscripcion"
              ></v-list-item>
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
            <v-card-item v-if="subscription">
              <v-card-title class="text-h3 text-center">
                Nombre Plan: {{ subscription.nombre_plan }}
              </v-card-title>
              
              <v-card-text class="text-h5 text-center pt-2">
                Total Pagado: ${{ subscription.total_pagado / 100 }} USD
              </v-card-text>
            </v-card-item>
            <v-card-text v-if="subscription">
              <v-list density="compact" class="text-h5 text-center pt-2 ">
                <v-list-item>Fecha Vencimiento: {{ formatDate(subscription.fecha_vencimiento) }}</v-list-item>
              </v-list>
            </v-card-text>

            <v-card-text v-if="subscription">
              <v-list density="compact" class="text-h5 text-center pt-2 ">
                <v-list-item>Creditos Actuales: {{ (subscription.creditos) }}</v-list-item>
              </v-list>
            </v-card-text>

            <v-card-text v-if="subscription">
              <v-list density="compact" class="text-h5 text-center pt-2 ">
                <v-list-item>Estado: {{ getStatusText(subscription.estado) }}</v-list-item>
              </v-list>
            </v-card-text>

            <v-card-actions v-if="subscription" class="justify-center pb-4">
              <v-btn variant="elevated" color="error" @click="confirmCancelSubscription" :disabled="subscription.estado === 'cancel_at_period_end'">Cancelar Suscripción</v-btn>
              <v-btn variant="elevated" color="primary" @click="openPlanDialog">
                Actualizar Plan
              </v-btn>
            </v-card-actions>

            <!-- Mensaje cuando no hay suscripción -->
            <v-card-text v-else class="text-h5 text-center">
              No tienes ninguna suscripción activa.
            </v-card-text>
            <!-- Diálogo de confirmación de cancelación -->
            <v-dialog v-model="isCancelDialogOpen" max-width="500px">
              <v-card class="cancelar">
                <v-card-title class="text-h5">¿Estás seguro de que deseas cancelar la suscripción?</v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="isCancelDialogOpen = false">No</v-btn>
                  <v-btn color="red darken-1" text @click="performCancelSubscription">Sí, cancelar</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="isPlanDialogOpen" max-width="500px">
            <v-card>
              <v-alert v-if="showAlert" type="error" dismissible>
                No hay planes disponibles para actualizar.
              </v-alert>
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
                <v-btn color="green darken-1" text @click="updateSubscription" :disabled="availablePlans.length === 0">Actualizar</v-btn>
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
import config from "@/config";

export default {
data() {
  return {
    fullName: "",
    email: "",
    subscription: {}, // Objeto para almacenar la suscripción del usuario
    isAuthenticated: false,
    isPlanDialogOpen: false,
    isCancelDialogOpen: false,
    selectedPlan: null,
    availablePlans: [],
    showAlert: false
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
    this.selectedPlan = planId;
  },
  confirmCancelSubscription() {
    this.isCancelDialogOpen = true;
  },
  openPlanDialog() {
    this.selectedPlan = null; // Reset la selección cuando se abre el diálogo
    this.fetchAvailablePlans();
    this.isPlanDialogOpen = true;
    this.showAlert = false;
    
  },
  formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
  },
  async fetchAvailablePlans() {
    // Llama al backend para obtener los planes disponibles
    const response = await axios.get(`${config.BASE_URL}:8000/plans`, {
      headers: {
        Authorization: `Bearer ${keycloak.token}`,
      },
    });

    // Filtrar los planes para que solo se muestren los que tienen un precio mayor al plan actual
    this.availablePlans = response.data.filter(plan => plan.precio >= this.subscription.total_pagado);

    this.showAlert = this.availablePlans.length === 0;

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
      const response = await axios.get(`${config.BASE_URL}:8000/suscripciones/${userId}`, {
        headers: {
          Authorization: `Bearer ${keycloak.token}`,
        },
      });
      this.subscription = response.data.length ? response.data[0] : null; // Asigna null si no hay suscripción
    } catch (error) {
      console.error("Error al obtener suscripción:", error);
    }
  },
  async performCancelSubscription() {
    try {
      const response = await axios.post(`${config.BASE_URL}:8000/cancelar_suscripcion/${this.subscription.id_suscripcion}`);
      
      if (response.data.message) {
        await this.fetchSubscriptionData();
      }

      this.isCancelDialogOpen = false;
      window.location.reload();
    } catch (error) {
      console.error("Error al cancelar la suscripción:", error);
     
    }
  },
async updateSubscription() {
  try {
    const response = await axios.post(`${config.BASE_URL}:8000/actualizar_suscripcion/${this.subscription.id_suscripcion}/${this.selectedPlan}`, {
    headers: {
      Authorization: `Bearer ${keycloak.token}`,
    }
    });
    if (response.data) {
          this.isPlanDialogOpen = false;
          window.location.reload();
        }
    else {
      this.showAlert = true;
    }
  } catch (error) {
    console.error("Error al actualizar la suscripción:", error);
  }
},
async fetchSubscriptionData() {
  // Lógica para obtener los datos actualizados de las suscripciones del usuario
  // Esto debería hacer una llamada a la API para recuperar la suscripción actualizada
},
getStatusText(status) {
    const statusText = {
      'active': 'Activo',
      'past_due': 'Atrasado',
      'unpaid': 'No pagado',
      'canceled': 'Cancelado',
      'cancel_at_period_end': 'Cancelado a fin de Mes'
    };
    return statusText[status] || status;
  }
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
.cancelar{
  width: 150%;
}
</style>
