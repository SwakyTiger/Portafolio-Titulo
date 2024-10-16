<template>
    <v-footer class="footer" color="#5A5A5A">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="12" md="4" class="d-flex flex-column align-items-start">
            <img
              :src="require('@/assets/alloxentric_logo.png')"
              alt="Alloxentric"
              class="logo-footer"
            />
            <div class="social-icons">
              <v-icon>mdi-facebook</v-icon>
              <v-icon>mdi-twitter</v-icon>
              <v-icon>mdi-instagram</v-icon>
              <v-icon>mdi-linkedin</v-icon>
              <v-icon>mdi-whatsapp</v-icon>
            </div>
          </v-col>

          <v-col cols="12" md="4">
            <h4>Servicios</h4>
            <p>Desarrollo Web</p>
            <p>Consultoría</p>
            <p>Soporte Técnico</p>
            <p>Política de Privacidad</p>
            <p>Términos de Servicio</p>
            <p>Preguntas Frecuentes</p>
          </v-col>
          
          <v-col cols="12" md="4" >
            <h4>Contacto</h4>
            <p>Tel: +123 456 789</p>
            <p>Email: info@gmail.com</p>
          </v-col>
          
        </v-row>
  
        <v-row justify="center" class="mt-4">
          <v-col class="text-center" cols="12">
            <span>&copy; 2024 Alloxentric. Todos los derechos reservados.</span>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </template>
  
  <script>
  export default {
    name: 'MainFooter'
  }
  </script>
  
  <style scoped>
  .logo-footer {

    width: 200px;
    margin-bottom: 20px;
  }
  
  .footer {
    color: white;
    margin-top: 40px;
    padding: 40px 20px;
    width: 100%;
    position: relative;
    bottom: 0;
  }
  
  .social-icons {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }
  
  .social-icons v-icon {
    font-size: 24px;
    cursor: pointer;
  }
  </style>
  