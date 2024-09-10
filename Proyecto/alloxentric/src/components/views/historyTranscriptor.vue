<template>
    <v-container class="centered-container">
      <v-card class="custom-card">
        <v-card-title class="custom-title">
          Historial de Transcripciones
        </v-card-title>
        <v-card flat>
          
            <v-container class="filtros">
              <v-container class="search">
                <v-text-field id="search" v-model="search" label="Search" prepend-inner-icon="mdi-magnify"
                  variant="outlined" hide-details single-line></v-text-field>
              </v-container>
              <v-container class="filtroFecha">
                <v-select v-model="selectedYear" :items="years" label="Año" outlined></v-select>
                <v-select v-model="selectedMonth" :items="months" label="Mes" outlined></v-select>
              </v-container>
            </v-container>
          
          <v-data-table :headers="headers" :items="filteredDesserts" :search="search"></v-data-table>
        </v-card>
      </v-card>
    </v-container>
  
  </template>
  
  <script>
  export default {
    data() {
      const currentYear = new Date().getFullYear();
      const startYear = 2023;  // Puedes cambiarlo al año en el que comienzas a almacenar datos
  
      const years = [{ title: 'Todos los años', value: null }];
      for (let year = startYear; year <= currentYear; year++) {
        years.push({ title: year.toString(), value: year });
      }
  
      return {
        search: '',
        selectedYear: null,
        selectedMonth: null,
        headers: [
          {
            align: 'start',
            key: 'data_transcrito',
            sortable: false,
            title: 'Mensaje Transcrito',
          },
          {
            align: 'start',
            key: 'fecha',
            sortable: false,
            title: 'Fecha/Hora',
          },
        ],
  
        desserts: [
          {
            data_transcrito: 'Hola, oye, no voy a poder llegar a la reunión a las 10. ¿Podemos moverla para las 11? Avísame si te sirve, porfa.',
            fecha: '2024-09-02',
          },
          {
            data_transcrito: 'Ah, me olvidé de decirte que la cena es mañana a las 8 en casa de Juan. No te preocupes por llevar nada, ya está todo listo.',
            fecha: '2024-09-03',
          },
          {
            data_transcrito: 'Hey, ¿puedes comprar leche cuando vengas? Se me olvidó cuando fui al súper. Gracias, nos vemos en un rato.',
            fecha: '2024-09-05',
          },
          {
            data_transcrito: 'Hola, Juan, acabo de ver el correo. Estoy revisando el documento que me mandaste, te envío los comentarios en una hora.',
            fecha: '2024-09-08',
          },
          {
            data_transcrito: 'Ah, me olvidé de decirte que el pato arrugó de nuevo y no va a entrar a jugar Cs, calladito champiñon.',
            fecha: '2024-09-09',
          },
          {
            data_transcrito: 'Necesito que me envíes el reporte antes de las 5 pm. Es urgente.',
            fecha: '2023-08-15',
          },
          {
            data_transcrito: 'Recuerda que la reunión de equipo es el viernes a las 10 am.',
            fecha: '2023-07-12',
          },
          {
            data_transcrito: 'El proyecto ha sido aprobado por el cliente. ¡Buen trabajo!',
            fecha: '2023-06-22',
          },
          {
            data_transcrito: '¿Podrías revisar el documento adjunto y darme tu feedback?',
            fecha: '2023-05-30',
          },
          {
            data_transcrito: 'El servidor estará en mantenimiento el próximo lunes de 2 am a 4 am.',
            fecha: '2023-04-17',
          },
          {
            data_transcrito: 'Hola, el paquete ha sido enviado y debería llegar el jueves.',
            fecha: '2022-11-03',
          },
          {
            data_transcrito: 'Recuerda que tienes una cita con el dentista el próximo miércoles.',
            fecha: '2022-10-20',
          },
          {
            data_transcrito: 'El evento se ha reprogramado para el próximo mes debido a la situación actual.',
            fecha: '2022-09-15',
          },
          {
            data_transcrito: 'Te envié la factura por correo. Por favor, confírmame si la recibiste.',
            fecha: '2022-08-09',
          },
          {
            data_transcrito: 'La presentación del proyecto es mañana a las 9 am. ¡No faltes!',
            fecha: '2022-07-05',
          },
          {
            data_transcrito: 'El cliente ha solicitado cambios en el diseño. Te paso los detalles en un rato.',
            fecha: '2022-06-18',
          },
          {
            data_transcrito: '¡Feliz cumpleaños! Espero que tengas un día increíble.',
            fecha: '2022-05-12',
          },
          {
            data_transcrito: 'El equipo ha completado la primera fase del proyecto. Ahora pasaremos a la siguiente.',
            fecha: '2022-04-30',
          },
          {
            data_transcrito: 'La reunión de seguimiento será el próximo lunes a las 2 pm.',
            fecha: '2022-03-21',
          },
          {
            data_transcrito: 'El curso de capacitación comienza el 1 de febrero. Por favor, regístrate a tiempo.',
            fecha: '2022-02-01',
          },
          {
            data_transcrito: 'El informe trimestral está listo y ha sido enviado a la dirección.',
            fecha: '2022-01-15',
          },
        ],
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
        ],
      }
    },
    computed: {
      filteredDesserts() {
        return this.desserts.filter(item => {
          // Filtrar por palabra clave
          const matchesSearch = item.data_transcrito.toLowerCase().includes(this.search.toLowerCase());
  
          // Filtrar por año y mes
          const itemDate = new Date(item.fecha);
          const matchesYear = this.selectedYear ? itemDate.getFullYear() === this.selectedYear : true;
          const matchesMonth = this.selectedMonth ? itemDate.getMonth() + 1 === this.selectedMonth : true;
  
          return matchesSearch && matchesYear && matchesMonth;
        });
      }
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
  
  .custom-title {
    font-size: 34px;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
  }
  
  .centered-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: #ffffff;
  }
  
  .custom-card {
    width: 80%;
    box-sizing: border-box;
    /* Asegura que el padding y el borde estén incluidos en el ancho total */
  }
  
  .filtros {
    display: flex;
    flex-direction: row;
  }
  
  .search {
    width: 100%;
  }
  
  .filtroFecha{
    display: flex;
    width: 50%;
  }
  
  </style>
  