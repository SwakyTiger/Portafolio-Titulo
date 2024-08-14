<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-card-title class="custom-title">
        Administrador de Ventas
      </v-card-title>
      <v-data-table :headers="headers" :items="ventas" :items-per-page="10" v-model:page="page" class="custom-table">
        <template v-slot:[`item.precio`]="{ item }">
          <span>{{ formatCurrency(item.precio) }}</span>
        </template>
        <template v-slot:[`item.details`]="{ item }">
          <v-btn @click="showDetails(item)" outlined>
            <template v-slot:prepend>
              <img :src="require('@/assets/icon-detalle.png')" alt="Detalles" class="custom-icon" />Detalle
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
        <v-btn class="reporte-btn" @click="generatePDF">Generar Reportes Mensuales</v-btn>
        <v-btn class="reporte-btn" @click="generatePDF">Generar Reportes Anuales</v-btn>
      </div>
    </div>

    <!-- Ventana emergente para mostrar detalles de la venta -->
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
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
        <v-card-text>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-content class="detalles">
                <h4>Detalles de Compra</h4>
                <p>- Tipo de plan: {{ selectedVenta.nombre_plan }}</p>
                <p>- Precio: {{ formatCurrency(selectedVenta.precio) }}</p>
                <p>- Telefono afiliado: {{ selectedVenta.prefijo }} {{ selectedVenta.numero_telefono }}</p>
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
      venta: 0,    // Total de ventas
      headers: [
        { title: 'Código', value: 'id_venta' },
        { title: 'Fecha/Hora', value: 'fecha_venta' },
        { title: 'Tipo de Plan', value: 'nombre_plan' },
        { title: 'Precio', value: 'precio' },
        { title: 'Detalles de compra', value: 'details' }
      ],
      dialog: false,
      selectedVenta: {}
      // Detalles de la venta seleccionada
    }
  },
  methods: {
    async fetchVentas() {
      try {
        const response = await axios.get('http://localhost:8000/ventas');
        this.ventas = response.data;
        this.calculateTotalVenta();
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
    calculateTotalVenta() {
      this.venta = this.ventas.reduce((sum, venta) => sum + venta.precio, 0);
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
      doc.text(`Total de ventas: ${this.formatCurrency(this.venta)}`, 14, doc.lastAutoTable.finalY + 10);

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
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Oculta el desbordamiento horizontal en toda la página */
}

.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  background-color: #ffffff;
}

.custom-card {
  max-width: 80%;
  width: 100%;
  box-sizing: border-box; /* Asegura que el padding y el borde estén incluidos en el ancho total */
}

.custom-title {
  font-size: 34px;
  font-family: 'Arial', sans-serif;
  font-weight: bold;
}


.custom-table {
  width: 100%;
  border-radius: 5px;
  border: 1px solid #ddd;
  box-sizing: border-box; /* Asegura que el padding y el borde estén incluidos en el ancho total */
}

.v-data-table >.v-data-table__tr:nth-child(even) {
  background-color: #f5f5f5; /* Fondo gris claro para filas pares */
}

/* Estilo para el botón */
.custom-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 16px; /* Ajusta el padding según sea necesario */
}

/* Estilo para el logo dentro del botón */
.custom-icon {
  width: 24px; /* Ajusta el tamaño del logo según tus preferencias */
  height: 24px; /* Ajusta el tamaño del logo según tus preferencias */
}

.titulo-total-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 80%; 
  margin-top: 20px;
  box-sizing: border-box; 
}

.botones-reportes {
  margin-right: 20px; /* Alinea los botones en una columna */
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}

.reporte-btn {
  background-color: #1DBEA8; /* Cambia el color de fondo del botón */
  color: #ffffff; /* Cambia el color del texto del botón */
  margin: 5px; /* Espacio entre los botones */
}

/* Estilo para el título */
.titulo-total {
  flex-grow: 1; /* Asegura que el título ocupe el espacio restante */
}

.titulo-total h1 {
  text-align: start;
}

.detalles p{
  margin: 5px 0px 5px 15px;
}
</style>
