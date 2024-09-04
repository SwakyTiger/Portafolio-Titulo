<template>
    <h1 class="pagoRealizado">¡Pago Realizado Correctamente!</h1>
    <v-container class="text-center pt-12">
      
      <v-card outlined class="mx-auto" max-width="600px" elevation="2">
        <v-card-text>
          <h2 class="text-h5">Datos de Facturación</h2>
          <p class="text-h4 font-weight-bold">$ {{ price }} pagado</p>
          <p>Tipo de Plan: {{ planName }}</p>
          <p>Nombre del Usuario: {{ userName }}</p>
          <p>Correo: {{ userEmail }}</p>
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
        userEmail: ''
      };
    },
    created() {
      // Obtener los datos de la URL o del localStorage
      const queryParams = new URLSearchParams(window.location.search);
      this.planName = queryParams.get('planName') || '';
      this.price = queryParams.get('price') || '';
      this.userName = queryParams.get('userName') || '';
      this.userEmail = queryParams.get('userEmail') || '';
    }
  }
  </script>
  
  <style scoped>
  .pagoRealizado {
  padding: 100px;
  width: 100%;
  background-color: #f5f5f5;
  text-align: center;
  font-size: 5rem
}

  .display-1 {
    margin-top: 20px;
    margin-bottom: 40px;
    color: #333;
  }
  </style>
  