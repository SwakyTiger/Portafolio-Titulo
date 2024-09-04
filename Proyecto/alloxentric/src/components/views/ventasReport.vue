<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-card-title class="custom-title">
        Administrador de Ventas
      </v-card-title>
      <v-select v-model="selectedYear" :items="years" label="Año" outlined></v-select>
      <v-select v-model="selectedMonth" :items="months" label="Mes" outlined></v-select>
      <v-btn @click="fetchVentas">Filtrar Ventas</v-btn>
      <v-data-table :headers="headers" :items="ventas" :items-per-page="10" v-model:page="page" class="custom-table">
        <template v-slot:[`item.fecha_venta`]="{ item }">
          <span>{{ formatDate(item.fecha_venta) }}</span>
        </template>
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
        <v-btn  @click="generatePDF">Generar Reporte de la Tabla</v-btn>
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
                <p>- Fecha de Venta: {{ formatDate(selectedVenta.fecha_venta) }}</p>
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
    const currentYear = new Date().getFullYear();
    const startYear = 2023;  // Puedes cambiarlo al año en el que comienzas a almacenar datos

    // Generar lista de años desde startYear hasta el año actual
    const years = [{ title: 'Todos los años', value: null }];
    for (let year = startYear; year <= currentYear; year++) {
      years.push({ title: year.toString(), value: year });
    }

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
      selectedYear: null,
      selectedMonth: null,
      years: years,  // Lista de años con opción de "sin filtro"
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
        { title: 'Diciembre', value: 12 }
      ],  // Lista de meses con nombres
    }
  },
  methods: {
    async fetchVentas() {
      try {
        const response = await axios.get('http://localhost:8000/ventas', {
          params: {
            anio: this.selectedYear || null,  // Enviar null si no hay filtro
            mes: this.selectedMonth || null   // Enviar null si no hay filtro
          }
        });
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
    formatDate(date) {
      const formattedDate = new Date(date);
      const year = formattedDate.getFullYear();
      const month = String(formattedDate.getMonth() + 1).padStart(2, '0');
      const day = String(formattedDate.getDate()).padStart(2, '0');
      const hours = String(formattedDate.getHours()).padStart(2, '0');
      const minutes = String(formattedDate.getMinutes()).padStart(2, '0');
      const seconds = String(formattedDate.getSeconds()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    calculateTotalVenta() {
      this.venta = this.ventas.reduce((sum, venta) => sum + venta.precio, 0);
    },
    generatePDF() {
      const doc = new jsPDF();

      // Título
      doc.setFontSize(18);
      doc.text('Administrador de Ventas', 14, 22);

      // Agregar el filtro seleccionado al PDF
      const selectedYearText = this.selectedYear ? `Año ${this.selectedYear}` : 'Todos los años';
      const selectedMonthText = this.selectedMonth
        ? this.months.find(month => month.value === this.selectedMonth).title
        : 'Todos los meses';
      doc.setFontSize(14);
      doc.text(`${selectedYearText} - ${selectedMonthText}`, 14, 30);

      // Espacio entre el título y la tabla
      const startY = 40;

      // Agregar tabla
      const columns = ["Código de Venta", "Fecha", "Tipo de Plan", "Precio"];
      const rows = this.ventas.map(item => [
        item.id_venta,
        this.formatDate(item.fecha_venta),
        item.nombre_plan,
        this.formatCurrency(item.precio)
      ]);

      doc.autoTable({
        startY,
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
html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  /* Oculta el desbordamiento horizontal en toda la página */
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
  box-sizing: border-box;
  /* Asegura que el padding y el borde estén incluidos en el ancho total */
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
  box-sizing: border-box;
  /* Asegura que el padding y el borde estén incluidos en el ancho total */
}

.v-data-table>.v-data-table__tr:nth-child(even) {
  background-color: #f5f5f5;
  /* Fondo gris claro para filas pares */
}

/* Estilo para el botón */
.custom-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 16px;
  /* Ajusta el padding según sea necesario */
}

/* Estilo para el logo dentro del botón */
.custom-icon {
  width: 24px;
  /* Ajusta el tamaño del logo según tus preferencias */
  height: 24px;
  /* Ajusta el tamaño del logo según tus preferencias */
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
  margin-right: 20px;
  /* Alinea los botones en una columna */
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}

.reporte-btn {
  background-color: #1DBEA8;
  /* Cambia el color de fondo del botón */
  color: #ffffff;
  /* Cambia el color del texto del botón */
  margin: 5px;
  /* Espacio entre los botones */
}

/* Estilo para el título */
.titulo-total {
  flex-grow: 1;
  /* Asegura que el título ocupe el espacio restante */
}

.titulo-total h1 {
  text-align: start;
}

.detalles p {
  margin: 5px 0px 5px 15px;
}
</style>
