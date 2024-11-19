<template>
  <v-container fluid class="pa-0">
    <v-card class="mx-auto" max-width="1400">
      <v-card-title class="text-h4 font-weight-bold primary white--text py-4">
        Administrador de Ventas
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="4" lg="3">
            <v-select v-model="selectedYear" :items="years" label="Año" outlined dense
              @change="filterVentas"></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="4" lg="3">
            <v-select v-model="selectedMonth" :items="months" label="Mes" outlined dense
              @change="filterVentas"></v-select>
          </v-col>
        </v-row>  

        <v-data-table :headers="headers" :items="filteredVentas" :items-per-page="10" v-model:page="page"
          class="elevation-1">
          <template v-slot:no-data>
            <v-alert type="info" class="ma-2">
              No hay ventas disponibles para los filtros seleccionados.
            </v-alert>
          </template>
          <template v-slot:[`item.usuario_info.username`]="{ item }">
            {{ item.usuario_info.username || 'N/A' }}
          </template>
          <template v-slot:[`item.fecha_venta`]="{ item }">
            {{ formatDate(item.fecha_venta) }}
          </template>
          <template v-slot:[`item.plan_info.nombre`]="{ item }">
            {{ item.plan_info.nombre || 'N/A' }}
          </template>
          <template v-slot:[`item.total_pagado`]="{ item }">
            {{ formatCurrency(item.total_pagado / 100) }}
          </template>
          <template v-slot:[`item.details`]="{ item }">
            <v-btn class="colores" small outlined @click="showDetails(item)">
              <template v-slot:prepend>
                <v-icon left small>mdi-information-outline</v-icon>
                Detalle
              </template>
            </v-btn>
          </template>
        </v-data-table>

        <v-row class="mt-4" align="center">
          <v-col cols="12" sm="6">
            <h2 class="text-h5">Total de ventas: {{ formatCurrency(totalVenta / 100) }}</h2>
          </v-col>
          <v-col cols="12" sm="6" class="text-sm-right">
            <v-btn @click="generatePDF" color="primary">
              <v-icon left>mdi-file-pdf-box</v-icon>
              Generar Reporte de la Tabla
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

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
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import axios from 'axios';

export default {
  name: 'VentasReport',
  data() {
    const currentYear = new Date().getFullYear();
    const startYear = 2023;

    const years = [{ title: 'Todos los años', value: null }];
    for (let year = startYear; year <= currentYear; year++) {
      years.push({ title: year.toString(), value: year });
    }

    return {
      page: 1,
      ventas: [],
      totalVenta: 0,
      headers: [
        { title: 'Nombre de Usuario', value: 'usuario_info.username' },
        { title: 'Fecha/Hora', value: 'fecha_venta' },
        { title: 'Tipo de Plan', value: 'plan_info.nombre' },
        { title: 'Precio', value: 'total_pagado' },
        { title: 'Detalles de compra', value: 'details' },
      ],
      dialog: false,
      selectedVenta: null,
      selectedYear: null,
      selectedMonth: null,
      years: years,
      months: [
        { title: 'Todos los meses', value: null },
        { title: 'Enero', value: 1 },
        { title: 'Febrero', value: 2 },
        { title: 'Marzo', value: 3 },
        { title: 'Abril', value: 4 },
        { title: 'Mayo', value: 5 },
        { title: 'Junio', value: 6 },
        { title: 'Julio', value: 7 },
        { title: 'Agosto', value: 8 },
        { title: 'Septiembre', value: 9 },
        { title: 'Octubre', value: 10 },
        { title: 'Noviembre', value: 11 },
        { title: 'Diciembre', value: 12 },
      ],
    };
  },
  computed: {
    filteredVentas() {
      return this.ventas.filter(venta => {
        const yearMatch = this.selectedYear ? new Date(venta.fecha_venta).getFullYear() === this.selectedYear : true;
        const monthMatch = this.selectedMonth ? new Date(venta.fecha_venta).getMonth() + 1 === this.selectedMonth : true;
        return yearMatch && monthMatch;
      });
    },
    selectedVentaUserInfo() {
      if (!this.selectedVenta) return {};
      return {
        'Nombre': `${this.selectedVenta.usuario_info.nombre} ${this.selectedVenta.usuario_info.apellido}`,
        'Correo': this.selectedVenta.usuario_info.email,
        'Número Telefónico': `${this.selectedVenta.usuario_info.prefijo} ${this.selectedVenta.usuario_info.numero_telefono}`,
      };
    },
    selectedVentaSaleInfo() {
      if (!this.selectedVenta) return {};
      return {
        'Tipo de plan': this.selectedVenta.plan_info.nombre,
        'Precio': this.formatCurrency(this.selectedVenta.total_pagado / 100),
        'Fecha de Venta': this.formatDate(this.selectedVenta.fecha_venta),
      };
    },
  },
  methods: {
    async fetchVentas() {
      try {
        const response = await axios.get('http://localhost:8000/ventas');
        this.ventas = response.data.ventas;
        this.calculateTotalVenta();
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
      this.totalVenta = this.filteredVentas.reduce((sum, venta) => sum + venta.total_pagado, 0);
    },
    generatePDF() {
      try {
        const doc = new jsPDF();
        doc.setFontSize(18);
        doc.text('Administrador de Ventas', 14, 22);

        const selectedYearText = this.selectedYear ? `Año ${this.selectedYear}` : 'Todos los años';
        const selectedMonthText = this.selectedMonth
          ? this.months.find(month => month.value === this.selectedMonth).title
          : 'Todos los meses';
        doc.setFontSize(14);
        doc.text(`${selectedYearText} - ${selectedMonthText}`, 14, 30);

        const startY = 40;

        const columns = ["Usuario", "Fecha", "Tipo de Plan", "Precio"];
        const rows = this.filteredVentas.map(item => [
          item.usuario_info.username,
          this.formatDate(item.fecha_venta),
          item.plan_info.nombre,
          this.formatCurrency(item.total_pagado / 100),
        ]);

        doc.autoTable({
          startY,
          head: [columns],
          body: rows,
          theme: 'grid',
        });

        doc.text(`Total de ventas: ${this.formatCurrency(this.totalVenta  / 100)}`, 14, doc.lastAutoTable.finalY + 10);
        doc.save('reporte_ventas.pdf');
      } catch (error) {
        console.error('Error generating PDF:', error);
        this.$toast.error('Error al generar el PDF');
      }
    },
  },
  mounted() {
    this.fetchVentas();
  },
};
</script>

<style scoped>
.colores {
  color: #ffffff;
  background-color: #54af86;
}

.v-data-table ::v-deep .v-data-table__wrapper {
  overflow-x: auto;
}

.v-data-table ::v-deep .v-data-table__wrapper table {
  min-width: 600px;
}

@media (max-width: 600px) {
  .v-btn {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>