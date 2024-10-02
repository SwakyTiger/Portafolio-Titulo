<template>
  <h1 class="planesyprecios">Planes Y Precios</h1>
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
              ${{ plan.precio / 100 }} USD
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

    // Método para realizar el pago usando el plan seleccionado
    async realizarPago(plan) {
      try {
        // Verificar si keycloak está autenticado
        if (keycloak.authenticated) {
          // Extraer nombre completo del token
          const firstName = keycloak.tokenParsed?.given_name || '';  // Usar el campo given_name si existe
          const lastName = keycloak.tokenParsed?.family_name || '';  // Usar el campo family_name si existe
          const fullName = `${firstName} ${lastName}`.trim();  // Formatear el nombre completo

          // Realizar la solicitud al backend con el nombre del usuario
          const response = await axios.post('http://localhost:8000/create-checkout-session', {
            plan_name: plan.nombre,
            price: plan.precio,
            user_email: keycloak.tokenParsed.email,  // Obtener el email desde el token
            user_name: fullName  // Incluir el nombre completo del usuario
          });

          // Verifica que la URL de Stripe esté presente en la respuesta
          if (response.data.url) {
            window.location.href = response.data.url;
          } else {
            console.error("URL de Stripe no recibida:", response.data);
          }
        } else {
          console.error("El usuario no está autenticado");
        }
      } catch (error) {
        console.error("Error al iniciar el pago:", error);
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

  