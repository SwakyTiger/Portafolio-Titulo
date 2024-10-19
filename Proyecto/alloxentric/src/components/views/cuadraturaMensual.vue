<template>
  <v-container fluid class="cuadratura-mensual pa-0">
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 font-weight-bold mb-6">Cuadratura Mensual</h1>

        <v-card elevation="5" class="rounded-lg">
          <v-row no-gutters>
            <v-col cols="12" md="3">
              <v-card-text class="pa-6">
                <v-select v-model="selectedPlanType" :items="planTypes" label="Filtrar por tipo de Plan" outlined dense
                  class="mb-4" >
                  <template v-slot:prepend-item>
                    <v-list-item ripple @click="clearFilter">
                      <v-list-item-content>
                        <v-list-item-title>Mostrar todos</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-select>

                <v-divider class="my-4"></v-divider>

                <div class="white--text">
                  <v-icon color="white" class="mr-2">mdi-account-group</v-icon>
                  <span class="font-weight-medium">Total Clientes: {{ totalClientes }}</span>
                </div>

                <div class="white--text mt-4">
                  <v-icon color="white" class="mr-2">mdi-cash-multiple</v-icon>
                  <span class="font-weight-medium">Total Vendido: {{ formatCurrency(totalVenta) }}</span>
                </div>
              </v-card-text>
            </v-col>

            <v-col cols="12" md="9">
              <v-data-table :headers="headers" :items="filteredVentas" :items-per-page="10"
                class="elevation-0">
                <template v-slot:item="props">
                  <tr>
                    <td>{{ props.item.id_venta }}</td>
                    <td>{{ props.item.fecha_venta }}</td>
                    <td>{{ props.item.nombre_plan }}</td>
                    <td>{{ formatCurrency(props.item.precio) }}</td>
                    <td>
                      <v-btn color="primary" small outlined @click="showDetails(props.item)">
                        <v-icon left small>mdi-information-outline</v-icon>
                        Detalle
                      </v-btn>
                    </td>
                  </tr>
                </template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="headline">Detalles de la Venta</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Comprador</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.nombre_usuario }} {{ selectedVenta.apellido_usuario
                  }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Correo</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.email }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>País</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.pais }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Número Telefónico</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.prefijo }} {{ selectedVenta.numero_telefono
                  }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-divider></v-divider>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Tipo de plan</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.nombre_plan }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Precio</v-list-item-title>
                <v-list-item-subtitle>{{ formatCurrency(selectedVenta.precio) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Fecha de Venta</v-list-item-title>
                <v-list-item-subtitle>{{ selectedVenta.fecha_venta }}</v-list-item-subtitle>
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
      page: 1,
      ventas: [],
      totalVenta: 0,
      totalClientes: 0,
      headers: [
        { text: 'Código', value: 'id_venta' },
        { text: 'Fecha/Hora', value: 'fecha_venta' },
        { text: 'Tipo de Plan', value: 'nombre_plan' },
        { text: 'Precio', value: 'precio' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      dialog: false,
      selectedVenta: {},
      selectedPlanType: null,
      planTypes: []
    }
  },
  computed: {
    filteredVentas() {
      if (!this.selectedPlanType) return this.ventas;
      return this.ventas.filter(venta => venta.nombre_plan === this.selectedPlanType);
    }
  },
  methods: {
    async fetchVentas() {
      try {
        const response = await axios.get('http://localhost:8000/ventas');
        this.ventas = response.data.map(venta => ({
          ...venta,
          plan_info: venta.plan_info || { nombre: 'Sin plan' },
          usuario_info: venta.usuario_info || { nombre: 'Sin usuario' },
        }));
        this.calculateTotalVenta(); // Calcula el total después de obtener las ventas
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
    calculateTotalVenta() {
      this.venta = this.ventas.reduce((sum, venta) => sum + venta.total_pagado, 0);
    },
    clearFilter() {
      this.selectedPlanType = null;
    }
  },
  mounted() {
    this.fetchVentas();
  }
}
</script>

<style scoped>
.cuadratura-mensual {
  background-color: #f5f5f5;
  min-height: 100vh;
}
</style>