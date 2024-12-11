<template>
  <h1 class="pagoRealizado">¡Pago Realizado Correctamente!</h1>
  
  <v-container class="text-center pt-12">
    <v-card outlined class="mx-auto mt-6" max-width="600px" elevation="2">
      <v-card-text>
        <h2 class="text-h5 mb-4">Datos de Facturación</h2>
        <v-divider></v-divider>
        <v-list v-if="dataLoaded">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6">Monto Pagado</v-list-item-title>
              <v-list-item-subtitle class="text-h4 font-weight-bold">{{ formatCurrency(price) }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6 font-weight-bold">Tipo de Plan</v-list-item-title>
              <v-list-item-subtitle class="text-h6 font-weight-bold">{{ planName }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6 font-weight-bold">Nombre del Usuario</v-list-item-title>
              <v-list-item-subtitle class="text-h6 font-weight-bold">{{ userName }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6 font-weight-bold">Correo</v-list-item-title>
              <v-list-item-subtitle class="text-h6 font-weight-bold">{{ userEmail }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-h6 font-weight-bold">Numero de Telefono</v-list-item-title>
              <v-list-item-subtitle class="text-h6 font-weight-bold">{{ numeroTelefono }}</v-list-item-subtitle>
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
import keycloak from '@/keycloak';


export default {
  data() {
    return {
      planName: '',
      price: '',
      userName: '',
      userEmail: '',
      numeroTelefono: '',
      dataLoaded: false,
      error: null
    };
  },
  async created() {
    // Obtener el parámetro session_id de la URL
    const queryParams = new URLSearchParams(window.location.search);
    const sessionId = queryParams.get('session_id');
   
    // Verificar que session_id esté presente
    if (sessionId) {
      if(keycloak.authenticated){
        // Extraer nombre completo del token
        const firstName = keycloak.tokenParsed?.given_name || '';  // Usar el campo given_name si existe
        const lastName = keycloak.tokenParsed?.family_name || '';  // Usar el campo family_name si existe
        const fullName = `${firstName} ${lastName}`.trim();  // Formatear el nombre completo
        try {
          
          const response = await fetch(`http://localhost:8000/payment-details?session_id=${sessionId}`);
          
          // Verificar que la respuesta esté bien
          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
          }

          // Procesar la respuesta JSON
          const data = await response.json();

          // Asignar los valores al estado local del componente
          this.planName = data.planName || 'No disponible';
          this.price = data.price ? data.price.toFixed(2) : 'No disponible';
          this.userName = fullName || 'No disponible';  // Mostrar nombre de usuario
          this.userEmail = data.userEmail || 'No disponible';
          this.numeroTelefono = keycloak.tokenParsed?.telefono || 'No disponible';
          this.dataLoaded = true;
          // Registrar la venta en la base de datos
          await this.recordSale(sessionId); // Llama al endpoint para registrar la venta
        } catch (error) {
        console.error("Error:", error);
        this.error = `Error al cargar los datos: ${error.message}`;
        }
      }
    } else {
      this.error = "No se encontró ID de sesión en la URL";
    }
  }
  ,
  methods: {
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },

    
    async recordSale(sessionId) {
      const token = keycloak.token; // Obtén el token de Keycloak
      try {
        // Enviar `session_id` como parámetro de consulta en la URL
        const response = await fetch(`http://localhost:8000/record-sale?session_id=${sessionId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
      } catch (error) {
        console.error("Error al registrar la venta:", error);
      }
    }
}}

</script>

<style scoped>
.pagoRealizado {
  padding: 100px;
  width: 100%;
  background-color: #1ebea4;
  color: white;
  text-align: center;
  font-size: 2.5rem;
}
</style>