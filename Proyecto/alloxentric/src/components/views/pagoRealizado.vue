<template>
  <v-container class="text-center pt-12">
    <h1 class="pagoRealizado">¡Pago Realizado Correctamente!</h1>
    <v-card outlined class="mx-auto mt-6" max-width="600px" elevation="2">
      <v-card-text>
        <h2 class="text-h5 mb-4">Datos de Facturación</h2>
        <v-divider></v-divider>
        <v-list v-if="dataLoaded">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6">Monto Pagado</v-list-item-title>
              <v-list-item-subtitle class="text-h4 font-weight-bold">$ {{ price }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Tipo de Plan</v-list-item-title>
              <v-list-item-subtitle>{{ planName }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Nombre del Usuario</v-list-item-title>
              <v-list-item-subtitle>{{ userName }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Correo</v-list-item-title>
              <v-list-item-subtitle>{{ userEmail }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-alert v-else-if="error" type="error">
          {{ error }}
        </v-alert>
        <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      planName: '',
      price: '',
      userName: '',
      userEmail: '',
      dataLoaded: false,
      error: null
    };
  },
  async created() {
    const queryParams = new URLSearchParams(window.location.search);
    const sessionId = queryParams.get('session_id');

    if (sessionId) {
      try {
        console.log("Session ID:", sessionId); // Log the session ID
        const response = await fetch(`http://localhost:8000/payment-details?session_id=${sessionId}`);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        console.log("Received data:", data); // Log the received data
        this.planName = data.planName || 'No disponible';
        this.price = data.price ? data.price.toFixed(2) : 'No disponible';
        this.userName = data.userName || 'No disponible';
        this.userEmail = data.userEmail || 'No disponible';
        this.dataLoaded = true;
      } catch (error) {
        console.error("Error:", error);
        this.error = `Error al cargar los datos: ${error.message}`;
      }
    } else {
      this.error = "No se encontró ID de sesión en la URL";
    }
  }
}
</script>

<style scoped>
.pagoRealizado {
  padding: 20px;
  width: 100%;
  background-color: #f5f5f5;
  text-align: center;
  font-size: 2.5rem;
}
</style>