<template>
  <h1 class="resumenpago">Resumen Pago</h1>
  <v-container>
    <v-row justify="center" class="row">
      <v-col cols="12" md="8" >
        <v-card outlined >
          <v-card-text>
            <v-row>
              <v-col class="d-flex flex-column justify-center align-center text-center">
                <p class="text-h3 font-weight-bold"> El monto a pagar es: ${{ plan.precio /100}} </p>
                <p><strong>Tipo de Plan:</strong> {{ plan.nombre }}</p>
                <p><strong>Nombre de usuario:</strong> {{ usuario.nombre }}</p>
                <p><strong>Número de Teléfono:</strong> {{ usuario.telefono }}</p>
                <p><strong>Prefijo:</strong> {{ usuario.prefijo }}</p>
                <p><strong>Correo:</strong> {{ usuario.email }}</p>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="elevated" color="#42b983" block @click="realizarPago">Checkout</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import keycloak from '@/keycloak';

export default {
  data() {
    return {
      plan: {},
      usuario: {}
    };
  },
  mounted() {
    // Recuperar el objeto almacenado en localStorage
    const resumenData = localStorage.getItem('resumenPago');

    if (resumenData) {
      const parsedData = JSON.parse(resumenData);
      this.plan = parsedData.plan;
      this.usuario = parsedData.usuario;
    } else {
      console.error("No se encontraron datos en localStorage");
    }
  },
  methods: {
    // Método para realizar el pago usando el plan seleccionado
    async realizarPago() {
      try {
        // Verificar si keycloak está autenticado
        if (keycloak.authenticated) {

          // Realizar la solicitud al backend con el nombre del usuario
          const response = await axios.post('http://localhost:8000/create-checkout-session', {
            plan_name: this.plan.nombre,
            price: this.plan.precio,
            user_email: this.usuario.email,  // Obtener el email desde el token
            user_name: this.usuario.nombre  // Incluir el nombre completo del usuario
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
};
</script>


<style scoped>
  .resumenpago {
  padding: 100px;
  width: 100%;
  background-color: #1ebea4;
  color: white;
  text-align: center;
  font-size: 5rem
}
  .text-h3 {
    padding: 25px;
  }
.row{
  padding-top: 50px;
}
</style>
  