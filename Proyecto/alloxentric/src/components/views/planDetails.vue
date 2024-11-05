<template>
  <h1 class="planesyprecios">Planes Y Precios</h1>
  <v-alert v-if="showAlert" type="error" dismissible @click="showAlert = false">
      El usuario no está autenticado. Por favor, inicia sesión para continuar.
  </v-alert>
  <v-container>
    <h2 class="transcriptor">Transcriptor Whatsapp</h2>
    <v-row>
      <v-col v-for="plan in plans" :key="plan.id_plan" cols="12" sm="4">
        <v-card height="100%" class="d-flex flex-column custom-border" border>
          <v-card-item>
            <v-card-title class="text-h5 text-center">
              {{ plan.nombre }}
            </v-card-title>
            
            <v-card-subtitle class="text-h3 text-center pt-2 ">
              {{formatCurrency(plan.precio / 100)}}
            </v-card-subtitle>
          </v-card-item>
          
          <v-card-text>
            <v-list density="compact" class="bg-transparent">
              <v-list-item >{{ plan.descripcion }}</v-list-item>
            </v-list>
          </v-card-text>
          
          <v-spacer></v-spacer>
          
          <v-card-actions class="justify-center pb-4">
            <v-btn variant="elevated" color="#42b983" @click="realizarPago(plan)">CONTRATAR</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import keycloak from '@/keycloak';

// Asume que 'keycloak' es un objeto global configurado en tu aplicación
// Asegúrate de que keycloak se haya autenticado antes de intentar obtener los datos

export default {
  data() {
    return {
      showAlert: false, // Variable para mostrar/ocultar la alerta
      plans: []
    }
  },
  created() {
    this.fetchPlans();
  },
  methods: {
  // Método para obtener la lista de planes desde el backend
  async fetchPlans() {
    try {
      const response = await axios.get('http://localhost:8000/plans');
      this.plans = response.data;
    } catch (error) {
      console.error("Error fetching plans:", error);
    }
  },
  
  formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },

  // Método para redirigir al resumen de pago
  async realizarPago(plan) {
    try {
      // Verificar si keycloak está autenticado
      if (keycloak.authenticated) {
        // Extraer información del usuario desde el token de Keycloak
        const firstName = keycloak.tokenParsed?.given_name || '';
        const lastName = keycloak.tokenParsed?.family_name || '';
        const fullName = `${firstName} ${lastName}`.trim();
        const emailUser = keycloak.tokenParsed?.email || '';
        const phonePrefix = keycloak.tokenParsed?.prefijo || '';
        const phoneNumber = keycloak.tokenParsed?.telefono || '';

        // Construir un objeto que contenga los datos del plan y del usuario
        const resumenData = {
          plan: {
            nombre: plan.nombre,
            precio: plan.precio
          },
          usuario: {
            nombre: fullName,
            email: emailUser,
            telefono: phoneNumber,
            prefijo: phonePrefix
          }
        };

        // Almacenar el objeto en localStorage
        localStorage.setItem('resumenPago', JSON.stringify(resumenData));

        // Redirigir a la vista de ResumenPago
        this.$router.push({ name: 'resumenPago' });
      } else {
        console.error("El usuario no está autenticado");
        this.showAlert = true;
      }
    } catch (error) {
      console.error("Error al redirigir al resumen de pago:", error);
    }
  }
}

}
</script>


<style scoped>
.planesyprecios {
  padding: 100px;
  width: 100%;
  background-color: #1ebea4;
  color: white;
  text-align: center;
  font-size: 5rem
}
.transcriptor{
  font-size: 50px;
  padding: 60px;
  text-align: center;
  color: #42b983;
}
.v-card{
  height: 100%;
}
.planDetails {
  text-align: center;
  padding: 50px;
}
.custom-border {
  border-color: #1ebea4 !important;
}

.plan-container {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.plan {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 5px;
  width: 30%;
}

.plan button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.plan button:hover {
  background-color: #0056b3;
}
</style>

  