<template>
  <v-container fluid class="cuadratura-mensual pa-6 bg-grey-lighten-4">
    <v-row justify="center">
      <v-col cols="12" lg="10">
        <v-card elevation="2" rounded="lg" class="pa-6">
          <v-card-title class="text-h4 font-weight-bold mb-6">Cuadratura Mensual</v-card-title>

          <v-row>
            <v-col cols="12" md="3">
              <v-card outlined class="pa-4 colores">
                <v-select v-model="selectedEstado" :items="estadoOptions" label="Filtrar por Estado" outlined dense
                  hide-details class="mb-4" color="white" item-color="primary">
                  <template v-slot:prepend-item>
                    <v-list-item ripple @click="clearEstadoFilter">
                      <v-list-item-title>Mostrar todos</v-list-item-title>
                    </v-list-item>
                    <v-divider class="mt-2"></v-divider>
                  </template>
                </v-select>

                <v-divider class="my-4"></v-divider>

                <v-list-item two-line>
                  <v-list-item-icon>
                    <v-icon color="white">mdi-account-group</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="white--text totales ">Total Clientes</v-list-item-title>
                    <v-list-item-subtitle class="white--text font-weight-medium">{{ totalClientes
                      }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item two-line>
                  <v-list-item-icon>
                    <v-icon color="white">mdi-cash-multiple</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="white--text totales ">Total Vendido</v-list-item-title>
                    <v-list-item-subtitle class="white--text font-weight-medium">{{ formatCurrency(totalVenta)
                      }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-card>
            </v-col>

            <v-col cols="12" md="9">
              <v-data-table :headers="headers" :items="filteredVentas" :items-per-page="10" :footer-props="{
                'items-per-page-options': [10, 20, 50, -1],
                'items-per-page-text': 'Filas por página:',
              }" class="elevation-1">
                <template v-slot:[`item.fecha_venta`]="{ item }">
                  {{ formatDate(item.fecha_venta) }}
                </template>
                <template v-slot:[`item.fecha_vencimiento`]="{ item }">
                  {{ formatDate(item.fecha_vencimiento) }}
                </template>
                <template v-slot:[`item.total_pagado`]="{ item }">
                  {{ formatCurrency(item.total_pagado / 100) }}
                </template>
                <template v-slot:[`item.estado`]="{ item }">
                  <v-chip :color="getStatusColor(item.estado)" text-color="white" small>
                    {{ getStatusText(item.estado) }}
                  </v-chip>
                </template>
                <template v-slot:[`item.actions`]="{ item }">
                  <v-btn class="colores" small outlined @click="showDetails(item)">
                    <v-icon left small>mdi-information-outline</v-icon>
                    Detalle
                  </v-btn>
                </template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="headline colores white--text">Detalles de la Venta</v-card-title>
        <v-card-text class="pa-4">
          <v-list>
            <v-subheader>Información del Comprador</v-subheader>
            <v-list-item v-for="(value, key) in selectedVentaUserInfo" :key="key">
              <v-list-item-content>
                <v-list-item-title>{{ key }}</v-list-item-title>
                <v-list-item-subtitle>{{ value }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-divider class="my-4"></v-divider>

            <v-subheader>Información de la Venta</v-subheader>
            <v-list-item v-for="(value, key) in selectedVentaSaleInfo" :key="key">
              <v-list-item-content>
                <v-list-item-title>{{ key }}</v-list-item-title>
                <v-list-item-subtitle>{{ value }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
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
  name: 'CuadraturaMensual',
  data() {
    return {
      ventas: [],
      totalVenta: 0,
      totalClientes: 0,
      headers: [
        { title: 'Nombre de Usuario', value: 'usuario_info.username' },
        { title: 'Fecha/Hora', value: 'fecha_venta' },
        { title: 'Fecha vencimiento', value: 'fecha_vencimiento' },
        { title: 'Tipo de Plan', value: 'plan_info.nombre' },
        { title: 'Precio', value: 'total_pagado' },
        { title: 'Estado', value: 'estado' },
        { title: 'Acciones', value: 'actions', sortable: false }
      ],
      dialog: false,
      selectedVenta: null,
      selectedPlanType: null,
      selectedEstado: null,
      planTypes: [],
      estadoOptions: [
      { title: 'Activo', value: 'active' },
      { title: 'Atrasado', value: 'past_due' },
      { title: 'No pagado', value: 'unpaid' },
      { title: 'Cancelado', value: 'canceled' },
      { title: 'Cancelado a fin de Mes', value: 'cancel_at_period_end' }
    ],
    }
  },
  computed: {
    filteredVentas() {
      let ventas = this.ventas;

      if (this.selectedEstado) {
        ventas = ventas.filter(venta => venta.estado === this.selectedEstado);
      }

      return ventas;
    },
    selectedVentaUserInfo() {
      return {
        'Nombre': `${this.selectedVenta.usuario_info.nombre} ${this.selectedVenta.usuario_info.apellido}`,
        'Correo': this.selectedVenta.usuario_info.email,
        'País': this.selectedVenta.pais,
        'Número Telefónico': `${this.selectedVenta.usuario_info.prefijo} ${this.selectedVenta.usuario_info.numero_telefono}`
      };
    },
    selectedVentaSaleInfo() {
      return {
        'Tipo de plan': this.selectedVenta.plan_info.nombre,
        'Precio': this.formatCurrency(this.selectedVenta.total_pagado),
        'Fecha de Venta': this.formatDate(this.selectedVenta.fecha_venta),
        'Fecha de Vencimiento': this.formatDate(this.selectedVenta.fecha_vencimiento),
        'Estado': this.getStatusText(this.selectedVenta.estado)
      };
    }
  },
  methods: {
    async fetchVentas() {
      try {
        const response = await axios.get('http://localhost:8000/suscripciones');
        this.ventas = response.data.ventas;
        this.totalClientes = response.data.total_clientes;
        this.calculateTotalVenta();
        this.planTypes = [...new Set(this.ventas.map(venta => venta.nombre_plan))];
      } catch (error) {
        console.error('Error fetching ventas:', error);
      }
    },
    showDetails(venta) {
      this.selectedVenta = venta;
      this.dialog = true;
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
    calculateTotalVenta() {
      this.totalVenta = this.ventas.reduce((sum, venta) => sum + venta.total_pagado, 0);
    },
    clearEstadoFilter() {
      this.selectedEstado = null;
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
    },
    getStatusColor(status) {
      const colors = {
        'active': 'success',
        'past_due': 'warning',
        'unpaid': 'error',
        'canceled': 'grey'
      };
      return colors[status] || 'primary';
    }
  },
  mounted() {
    this.fetchVentas();
  }
}
</script>

<style scoped>
.cuadratura-mensual {
  min-height: 100vh;
}

.totales {
  color: #ffffff !important;
}

.colores {
  color: #ffffff;
  background-color: #54af86;
}
</style>