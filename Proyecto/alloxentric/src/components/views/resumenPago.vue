<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card outlined>
          <v-card-title class="text-h4 text-center">Pago</v-card-title>
          <v-card-text>
            <v-divider></v-divider>
            <v-row>
              <v-col>
                <h5>Resumen</h5>
                <p class="text-h3 font-weight-bold">$ {{ plan.precio }} a pagar</p>
                <p><strong>Tipo de Plan:</strong> {{ plan.nombre }}</p>
                <p><strong>Nombre de usuario:</strong> {{ usuario.nombre }}</p>
                <p><strong>Número de Teléfono:</strong> {{ usuario.telefono }}</p>
                <p><strong>Prefijo:</strong> {{ usuario.prefijo }}</p>
                <p><strong>Correo:</strong> {{ usuario.email }}</p>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" block @click="realizarPago">Checkout</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      plan: {
        nombre: 'Basic Plan',
        precio: 1000, // Precio en centavos (por ejemplo, $10.00)
      },
      usuario: {
        nombre: 'NOMBRE',
        telefono: 'NUMERO',
        prefijo: 'PREFIJO',
        email: 'EMAIL',
      },
    };
  },
  methods: {
  async realizarPago() {
    try {
      const response = await axios.post('http://localhost:8000/create-checkout-session', {
        plan_name: this.plan.nombre,
        price: this.plan.precio,  // Precio en centavos, por ejemplo, $10.00
        user_email: "usuario@example.com"
      });
      console.log(response.data)
      // Verifica que la URL no esté indefinida
      if (response.data.url) {
        window.location.href = response.data.url;
      } else {
        console.error("URL de Stripe no recibida:", response.data);
      }
    } catch (error) {
      console.error("Error al iniciar el pago:", error);
    }
  }
}};
</script>


<style scoped>
  .resumenpago {
  padding: 100px;
  width: 100%;
  background-color: #f5f5f5;
  text-align: center;
  font-size: 5rem
}
  .text-h4 {
    margin-bottom: 16px;
  }
</style>
  