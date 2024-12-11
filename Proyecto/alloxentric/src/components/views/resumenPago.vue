<template>
  <h1 class="resumenpago">Resumen Pago</h1>
  <v-alert v-if="showAlert" type="error" dismissible>
  El usuario ya tiene una suscripción activa, porfavor actualice desde el apartado Mi Cuenta.
  </v-alert>

  <v-container>
    <v-row justify="center" class="row">
      <v-col cols="12" md="8">
        <v-card outlined>
          <v-card-text>
            <v-row>
              <v-col class="d-flex flex-column justify-center align-center text-center">
                <p class="text-h3 font-weight-bold"> El monto a pagar es: {{ formatCurrency(plan.precio / 100)}} </p>
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
      usuario: {},
      showAlert: false
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
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },
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
            user_name: this.usuario.nombre,  // Incluir el nombre completo del usuario
            id_usuario: keycloak.tokenParsed.sub  // ID único del usuario
          });

          // Verifica que la URL de Stripe esté presente en la respuesta
          if (response.data.url) {
            window.location.href = response.data.url;  // Redirigir al usuario a Stripe
          } else {
            this.showAlert = true;
            console.error("URL de Stripe no recibida:", response.data);
          }
        } else {
          console.error("El usuario no está autenticado");
          this.showAlert = true;  // Mostrar alerta si no está autenticado
        }
      } catch (error) {
        // Manejar errores específicos como la falta de autenticación o problemas de red
        if (error.response) {
          console.error("Error en la respuesta del servidor:", error.response.data);
        } else if (error.request) {
          console.error("No se recibió respuesta del servidor:", error.request);
        } else {
          console.error("Error al iniciar el pago:", error.message);
        }

        this.showAlert = true;  // Mostrar alerta si ocurre algún error
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

.row {
  padding-top: 50px;
}
</style>