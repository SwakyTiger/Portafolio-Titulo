<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-row>
        <v-card-title class="custom-title">
          Dashboard
        </v-card-title>
      </v-row>

      <v-row>
        <v-col cols="12" md="6" lg="4">
          <v-card class="mb-4" elevation="2">
            <v-card-text>
              <div class="text-overline mb-1">Filtrar por Año</div>
              <v-select v-model="selectedYear" :items="years" item-title="title" item-value="value" label="Seleccionar Año" hide-details
                outlined dense class="mb-4"
              ></v-select>
              <v-btn
                color="primary"
                @click="fetchVentas"
                :loading="loading"
                :disabled="loading || buttonDisabled"
                block
              >
                <v-icon left>mdi-filter</v-icon>
                Filtrar Ventas
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6" lg="4">
          <v-card class="mb-4" elevation="2">
            <v-card-text>
              <div class="text-overline mb-1">Total de Ventas</div>
              <div class="text-h4 font-weight-bold">{{ totalVentasCount }}</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6" lg="4">
          <v-card class="mb-4" elevation="2">
            <v-card-text>
              <div class="text-overline mb-1">Total de Suscripciones activas</div>
              <div class="text-h4 font-weight-bold">{{ totalSuscritosCount }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6" lg="8">
          <v-card elevation="2">
            <v-card-title class="text-h5 font-weight-bold">
              <v-icon large left color="primary">mdi-chart-bar</v-icon>
              Ventas Mensuales por año
            </v-card-title>
            <v-card-text>
              <canvas id="ventasChart" ref="ventasChart"></canvas>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6" lg="4">
          <v-card elevation="2">
            <v-card-title class="text-h5 font-weight-bold">
              <v-icon large left color="secondary">mdi-chart-pie</v-icon>
              Suscriptores activos por Plan
            </v-card-title>
            <v-card-text>
              <canvas id="planChart" ref="planChart"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

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
      ventas: [],
      totalVentasCount: 0,
      totalSuscritosCount: 0,
      suscriptores: [],
      selectedYear: null,
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
      chart: null,
      planChart: null,
      loading: false,
      generatingPDF: false,
      buttonDisabled: false, // Variable para manejar el estado del botón
    };
  },
  methods: {
    async fetchVentas() {
      this.loading = true;
      this.buttonDisabled = true; // Deshabilitar el botón
      try {
        const responseVentas = await axios.get('http://localhost:8000/ventas');
        this.ventas = responseVentas.data.ventas;

        // **Filtrar por Año**
        this.ventas = this.ventas.filter((venta) => {
          const ventaFecha = new Date(venta.fecha_venta);
          const ventaYear = ventaFecha.getFullYear();
          return !this.selectedYear || ventaYear === this.selectedYear;
        });

        this.totalVentas();
        this.updateChart();
      } catch (error) {
        console.error('Error fetching ventas:', error);
      } finally {
        this.loading = false;
        // se pone un delay de 1 segundo para evitar errores con la creacion del grafico
        setTimeout(() => {
          this.buttonDisabled = false;
        }, 1000); // segundos de espera
      }
    },

    async fetchSuscriptores() {
      this.loading = true;
      try {
        const responseSuscriptores = await axios.get('http://localhost:8000/suscripciones');
        this.suscriptores = responseSuscriptores.data.ventas;

        this.totalSuscritos();
        this.updatePlanChart();
      } catch (error) {
        console.error('Error fetching suscriptores:', error);
      } finally {
        this.loading = false;
      }
    },
    totalVentas() {
      this.totalVentasCount = this.ventas.length;
    },
    totalSuscritos() {
      this.totalSuscritosCount = this.suscriptores.length;
    },
    updateChart() {
      const salesCountByMonth = Array(12).fill(0);

      this.ventas.forEach((venta) => {
        const date = new Date(venta.fecha_venta);
        const month = date.getMonth();
        salesCountByMonth[month] += 1;
      });

      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = this.$refs.ventasChart.getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.months.slice(1).map((month) => month.title),
          datasets: [
            {
              label: 'Número de Ventas',
              data: salesCountByMonth,
              backgroundColor: 'rgba(29, 190, 168, 0.6)',
              borderColor: 'rgba(29, 190, 168, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            tooltip: {
              callbacks: {
                title: function (context) {
                  return `Mes: ${context[0].label}`;
                },
                label: function (context) {
                  const totalVentas = context.raw;
                  return `Ventas realizadas: ${totalVentas}`;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Número de Ventas',
              },
            },
          },
        },
      });
    },
    updatePlanChart() {
      const planCounts = this.suscriptores.reduce((acc, subscriber) => {
        const planType = subscriber.plan_info?.nombre || 'Sin plan';
        if (!acc[planType]) {
          acc[planType] = 0;
        }
        acc[planType]++;
        return acc;
      }, {});

      const planLabels = Object.keys(planCounts);
      const planData = Object.values(planCounts);

      if (this.planChart) {
        this.planChart.destroy();
      }

      const ctx = this.$refs.planChart.getContext('2d');
      this.planChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: planLabels,
          datasets: [
            {
              label: 'Suscriptores por Plan',
              data: planData,
              backgroundColor: ['#4CAF50', '#FF9800', '#2196F3', '#FF5722', '#9C27B0'],
              borderColor: '#ffffff',
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
        },
      });
    },
  },
  mounted() {
    this.fetchVentas();
    this.fetchSuscriptores();
  },
};
</script>
    <style scoped>
  .v-card {
    transition: box-shadow 0.3s ease-in-out;
  }
  
  .v-card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
  }
  
  .v-btn {
    text-transform: none;
  }
  .custom-title {
  font-size: 34px;
  font-family: 'Arial', sans-serif;
  font-weight: bold;
}
.custom-card {
  max-width: 80%;
  width: 100%;
  box-sizing: border-box;
  /* Asegura que el padding y el borde estén incluidos en el ancho total */
}
.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  background-color: #ffffff;
}
  </style>