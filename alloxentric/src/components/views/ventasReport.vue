<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-card-title class="custom-title">
        Administrador de Ventas
      </v-card-title>
      <v-data-table 
        :headers="headers"
        :items="ventas"
        :items-per-page="10"
        v-model:page="page"
        class="custom-table"
      >
        <template v-slot:[`item.precio`]="{ item }">
          <span>{{ formatCurrency(item.precio) }}</span>
        </template>
        <template v-slot:[`item.details`]="{ item }">
          <v-btn @click="showDetails(item)" outlined>
            <template v-slot:prepend>
              <img :src="require('@/assets/icon-detalle.png')" alt="Detalles" class="custom-icon"/>Detalle
            </template>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <div class="titulo-total-container">
      <div class="titulo-total">
        <h1>Total de ventas: {{ formatCurrency(venta) }}</h1>
      </div>
      <div class="botones-reportes">
        <v-btn class="reporte-btn">Generar Reportes Diarios</v-btn>
        <v-btn class="reporte-btn">Generar Reportes Mensuales</v-btn>
      </div>
    </div>

    <!-- Ventana emergente -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">Detalles de Compra</v-card-title>
        <v-card-text>
          <p><strong>Código:</strong> {{ selectedItem.id_venta }}</p>
          <p><strong>Fecha/Hora:</strong> {{ selectedItem.fecha_venta }}</p>
          <p><strong>Tipo de Plan:</strong> {{ selectedItem.plan }}</p>
          <p><strong>Precio:</strong> {{ formatCurrency(selectedItem.precio) }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VentasReport',
  data() {
    return {
      page: 1,
      ventas: [],  // Datos de la API
      venta: 0,    // Total de ventas
      headers: [
        { title: 'Código', value: 'id_venta' },
        { title: 'Fecha/Hora', value: 'fecha_venta' },
        { title: 'Tipo de Plan', value: 'plan' }, // Aquí 'plan' corresponde al nombre del plan
        { title: 'Precio', value: 'precio' },
        { title: 'Detalles de compra', value: 'details' }
      ],
      dialog: false,
      selectedItem: {}
    }
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('http://localhost:8000/ventas');
        this.ventas = response.data;
        this.calculateTotalVenta();
      } catch (error) {
        console.error('Error fetching items:', error);
      }
    },
    showDetails(item) {
      this.selectedItem = item;
      this.dialog = true;
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },
    calculateTotalVenta() {
      this.venta = this.ventas.reduce((sum, item) => sum + item.precio, 0);
    }
  },
  mounted() {
    this.fetchItems();
  }
}
</script>
