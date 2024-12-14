<template>
  <v-container class="centered-container">
    <v-card class="custom-card">
      <v-card-title class="custom-title">
        Administrador de Planes
      </v-card-title>
      <v-data-table :headers="headers" :items="planes" :items-per-page="10" v-model:page="page" class="custom-table">
        <template v-slot:[`item.precio`]="{ item }">
          <span>{{ formatCurrency(item.precio / 100) }}</span>
        </template>
        <template v-slot:[`item.fecha_modificacion`]="{ item }">
          <span>{{ handleDate(item.fecha_modificacion) }}</span>
        </template>
        <template v-slot:[`item.edit`]="{ item }">
          <v-btn @click="showEdit(item)" outlined color="red">
            <template v-slot:prepend>
              <img :src="require('@/assets/icon-editar.png')" alt="Editar" class="custom-icon" />
              Editar
            </template>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <div class="titulo-total-container">
      <div class="botones-reportes">
        <v-btn class="reporte-btn" @click="openCreateDialog">+ Crear nuevo Plan</v-btn>
      </div>
    </div>

    <!-- Crear Nuevo Plan -->
    <v-dialog v-model="createDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">Crear Nuevo Plan</v-card-title>
        <v-alert v-model="showAlert" type="error" dismissible class="mb-4">
          {{ errorMessage }}
        </v-alert>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="newPlan.id_plan" label="Código" required></v-text-field>
            <v-text-field v-model="newPlan.nombre" label="Nombre del Plan" required></v-text-field>
            <span>Precio ingresado: {{ formatCurrency(newPlan.precio / 100) }}</span>
            <v-text-field v-model="newPlan.precio" label="Precio" type="number" step="0.01" required></v-text-field>
            <v-text-field v-model="newPlan.creditos" label="Creditos" type="number" step="0.01"></v-text-field>
            <v-textarea v-model="newPlan.descripcion" label="Descripción"></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="savePlan">Guardar</v-btn>
          <v-btn @click="createDialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Editar Plan -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">Editar Plan</v-card-title>
        <v-card-text>
          <p>
            <strong>Fecha de última modificación:</strong>
            {{ handleDate(selectedPlan.fecha_modificacion) }}
          </p>
          <v-form ref="form">
            <v-text-field v-model="selectedPlan.id_plan" label="Código" required disabled></v-text-field>
            <v-text-field v-model="selectedPlan.nombre" label="Nombre del Plan" required></v-text-field>
            <span>Precio ingresado: {{ formatCurrency(selectedPlan.precio / 100) }}</span>
            <v-text-field v-model="selectedPlan.precio" label="Precio" type="number" step="0.01"
              required></v-text-field>
            <v-text-field v-model="selectedPlan.creditos" label="Creditos" type="number" step="0.01"></v-text-field>
            <v-textarea v-model="selectedPlan.descripcion" label="Descripción"></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="updatePlan">Guardar</v-btn>
          <v-btn @click="dialog = false">Cancelar</v-btn>
          <v-btn color="red" text @click="openDeleteDialog(selectedPlan)">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Confirmación para Eliminar -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">Confirmación</v-card-title>
        <v-card-text>
          ¿Estás seguro de que deseas eliminar el "<strong>{{ selectedPlan?.nombre }}</strong>"?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="confirmDeletePlan">Eliminar</v-btn>
          <v-btn text @click="deleteDialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>


<script>
import axios from "axios";
import config from "@/config";

export default {
  data() {
    return {
      planes: [],
      headers: [
        { title: "Código", value: "id_plan" },
        { title: "Fecha de Modificación", value: "fecha_modificacion" },
        { title: "Nombre del Plan", value: "nombre" },
        { title: "Precio", value: "precio" },
        { title: "Creditos", value: "creditos" },
        { title: "Acciones", value: "edit", sortable: false },
      ],
      page: 1,
      createDialog: false,
      dialog: false,
      deleteDialog: false,
      selectedPlan: null,
      newPlan: {
        id_plan: "",
        nombre: "",
        precio: 0,
        creditos: 0,
        descripcion: "",
      },
      errorMessage: "",
      showAlert: false,
    };
  },
  created() {
    this.fetchPlanes();
  },
  methods: {
    handleDate(date) {
      if (typeof date === "string" && isNaN(Date.parse(date))) {
        return date;
      }
      return this.formatDate(date);
    },
    formatDate(date) {
      const options = { year: "numeric", month: "2-digit", day: "2-digit" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat("es-ES", {
        style: "currency",
        currency: "USD",
      }).format(amount);
    },
    async fetchPlanes() {
      try {
        const response = await axios.get(`${config.BASE_URL}:8000/plans`);
        this.planes = response.data;
      } catch (error) {
        console.error("Error fetching Planes:", error);
      }
    },
    openCreateDialog() {
      this.newPlan = { id_plan: "", nombre: "", precio: 0, creditos: 0, descripcion: "" };
      this.createDialog = true;
      this.showAlert = false;
    },
    async savePlan() {

      try {
        const planData = { ...this.newPlan, fecha_modificacion: new Date().toISOString() };
        await axios.post(`${config.BASE_URL}:8000/plans`, planData);
        this.createDialog = false;
        this.fetchPlanes();
      } catch (error) {
        console.error("Error:", error); // Imprime el error para depuración

      }
    },
    showEdit(plan) {
      this.selectedPlan = plan;
      this.dialog = true;
    },
    async updatePlan() {
      try {

        this.selectedPlan.fecha_modificacion = new Date().toISOString();
        await axios.post(`${config.BASE_URL}:8000/plans/${this.selectedPlan.id_plan}`, this.selectedPlan);
        this.dialog = false;
        this.fetchPlanes();
      } catch (error) {
        console.error("Error updating Plan:", error);

      }
    },
    openDeleteDialog(plan) {
      this.selectedPlan = plan;
      this.deleteDialog = true;
    },
    async confirmDeletePlan() {
      try {
        await axios.delete(`${config.BASE_URL}:8000/plans/${this.selectedPlan.id_plan}`);
        this.dialog = false;
        this.deleteDialog = false;
        this.fetchPlanes();
      } catch (error) {
        console.error("Error deleting Plan:", error.response?.data || error);
      }
    },
  },
};
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
  font-family: "Arial", sans-serif;
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
  background-color: #1dbea8;
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
</style>
