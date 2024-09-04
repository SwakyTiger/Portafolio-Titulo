<template>
  <v-container class="cuadratura-mensual">
    <div class="header">
      <h1 class="title">Cuadratura Mensual</h1>
    </div>
    <v-card class="card">
      <div class="content">
        <v-card class="left-section">
          <!-- Filtro de tipo de plan -->
          <v-select 
            label="Filtrar por tipo de Plan" 
            :items="planTypes" 
            v-model="selectedPlanType"
          >
            <template v-slot:prepend-item>
              <v-list-item ripple @click="clearFilter">
                <v-list-item-content>
                  <v-list-item-title>Mostrar todos</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-select>
        </v-card>
        <v-card class="right-section">
          <v-data-table 
            :headers="headers"
            :items="filteredVentas"
            :items-per-page="10" 
            v-model:page="page" 
            class="custom-table" 
            hide-default-header
          >
            <template v-slot:item="props">
              <tr>
                <td>ID venta: {{ props.item.id_venta }}</td>
                <td>Tipo de plan: {{ props.item.nombre_plan }}</td>
                <td>
                  <v-btn @click="showDetails(props.item)" outlined>
                    <template v-slot:prepend>
                      <img :src="require('@/assets/icon-detalle.png')" alt="Detalles" class="custom-icon" />Detalle
                    </template>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </div>
      <div class="footer">
        <span class="footer-text">Total vendido: {{ formatCurrency(totalVenta) }}</span>
        <span class="footer-text">Clientes totales: {{ totalClientes }}</span>
      </div>
    </v-card>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-text>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-content class="detalles">
                <h1>Detalles de la Venta</h1>
                <h4>Detalles del Comprador</h4>
                <p>- Nombre: {{ selectedVenta.nombre_usuario }} {{ selectedVenta.apellido_usuario }}</p>
                <p>- Correo: {{ selectedVenta.email }} </p>
                <p>- País: {{ selectedVenta.pais }} </p>
                <p>- Numero Telefónico: {{ selectedVenta.prefijo }} {{ selectedVenta.numero_telefono }}</p>
                <h4>Detalles de Compra</h4>
                <p>- Tipo de plan: {{ selectedVenta.nombre_plan }}</p>
                <p>- Precio: {{ formatCurrency(selectedVenta.precio) }}</p>
                <p>- Fecha de Venta: {{ selectedVenta.fecha_venta }}</p>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
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
    return {
      page: 1,
      ventas: [],  // Datos de la API
      totalVenta: 0,    // Total de ventas
      totalClientes: 0, // Número total de clientes
      headers: [
        { title: 'Código', value: 'id_venta' },
        { title: 'Fecha/Hora', value: 'fecha_venta' },
        { title: 'Tipo de Plan', value: 'nombre_plan' },
        { title: 'Precio', value: 'precio' },
        { title: 'Detalles de compra', value: 'details' }
      ],
      dialog: false,
      selectedVenta: {},
      selectedPlanType: null,
      planTypes: []  // Array para los tipos de planes únicos
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
        this.ventas = response.data;
        this.calculateTotals();

        // Obtener los tipos de planes únicos para el filtro
        this.planTypes = [...new Set(this.ventas.map(venta => venta.nombre_plan))];
      } catch (error) {
        console.error('Error fetching items:', error);
      }
    },
    showDetails(venta) {
      this.selectedVenta = venta;
      this.dialog = true;
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'USD' }).format(amount);
    },
    calculateTotals() {
      this.totalVenta = this.ventas.reduce((sum, venta) => sum + venta.precio, 0);

      const uniqueClients = new Set(this.ventas.map(venta => venta.id_usuario));
      this.totalClientes = uniqueClients.size;
    },
    clearFilter() {
      this.selectedPlanType = null;
    },
    generatePDF() {
      const doc = new jsPDF();

      // Título
      doc.setFontSize(18);
      doc.text('Administrador de Ventas', 14, 22);

      // Agregar tabla
      const columns = ["Código de Venta", "Fecha", "Tipo de Plan", "Precio"];
      const rows = this.ventas.map(item => [
        item.id_venta,
        item.fecha_venta,
        item.nombre_plan,
        this.formatCurrency(item.precio)
      ]);

      doc.autoTable({
        startY: 30,
        head: [columns],
        body: rows,
        theme: 'grid',
      });

      // Total de ventas
      doc.text(`Total de ventas: ${this.formatCurrency(this.totalVenta)}`, 14, doc.lastAutoTable.finalY + 10);

      // Guardar el PDF
      doc.save('reporte_ventas.pdf');
    }
  },
  mounted() {
    this.fetchVentas();
  }
}
</script>

<style scoped>
.cuadratura-mensual {
  display: flex;
  flex-direction: column; /* Para apilar el título y el contenido */
  align-items: center; /* Centra horizontalmente el contenedor */
  background-color: #ffffff; /* Fondo gris claro para contraste */
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
}

.header {
  margin-top: 5%;
  width: 70%; 
  display: flex;
  justify-content: flex-start; 
}

.title {
  font-size: 2em; 
  font-weight: bold; 
  color: #000000; 
}

.card {
  display: flex;
  flex-direction: column;
  width: 70%;
  background-color: #fff;
  border: 1px solid #000; 
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.content {
  display: flex;
  flex: 1;
}

.left-section {
  width: 30%;
  background-color: #19BCA6; /* Color celeste */
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  border-right: 1px solid black;
}
.right-section {
  width: 70%;
  padding: 20px;
  box-sizing: border-box;
}
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.filter-button {
  background-color: #007E6F; /* Color del botón */
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  margin-right: 10px;
  cursor: pointer;
}

.filter-button:hover {
  background-color: #005f4f; /* Color del botón al pasar el mouse */
}

input[type="text"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.user-info {
  color: #fff;
  display: flex;
  align-items: center; 
  gap: 10px; /* Espacio entre los elementos */
  margin-top: auto;   
}

.details-button {
  background-color: #007E6F; 
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
}

.details-button:hover {
  background-color: #005f4f; /* Color del botón al pasar el mouse */
}

.footer {
  background-color: #007E6F; 
  padding: 10px;
  display: flex;
  justify-content: flex-start; 
  align-items: center; 
  border-top: 1px solid black;
}

.footer-text {
  color: #fff;
  font-size: 1.2em; /* Tamaño de fuente más grande para el total de ventas */
  font-weight: bold; /* Negrita */
  margin-right: 20px; /* Espacio entre el total y los clientes */
}
</style>
