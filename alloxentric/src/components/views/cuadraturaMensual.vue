<template>
    <div class="cuadratura-mensual">
      <div class="header">
        <h1 class="title">Cuadratura Mensual</h1> <!-- Título alineado a la izquierda -->
      </div>
      <div class="card">
        <div class="content">
          <div class="left-section">
            <div class="search-bar" style="border-top: 2px;">
              <input type="text" placeholder="Buscar usuario" />
              <button class="filter-button">Filtrar por mes</button>
            </div>
            <div class="user-info">
              <p>ID: 12345</p>
              <p>Tipo de plan: Normal</p>
              <button class="details-button" @click="fetchUserData(12345)">Detalle</button>
            </div>
            <div class="user-info">
              <p>ID: 12345</p>
              <p>Tipo de plan: Normal</p>
              <button class="details-button" @click="fetchUserData(12345)">Detalle</button>
            </div>
            <div class="user-info">
              <p>ID: 12345</p>
              <p>Tipo de plan: Normal</p>
              <button class="details-button" @click="fetchUserData(12345)">Detalle</button>
            </div>
            <div class="user-info">
              <p>ID: 12345</p>
              <p>Tipo de plan: Normal</p>
              <button class="details-button" @click="fetchUserData(12345)">Detalle</button>
            </div>
            <div class="user-info">
              <p>ID: 12345</p>
              <p>Tipo de plan: Normal</p>
              <button class="details-button" @click="fetchUserData(12345)">Detalle</button>
            </div>
          </div>
          <div class="right-section">
            <h2>Información Detallada</h2>
            <!-- Muestra solo cuando se haya cargado la información -->
            <div v-if="userData">
              <p><strong>ID:</strong> {{ userData.id }}</p>
              <p><strong>Nombre:</strong> {{ userData.name }}</p>
              <p><strong>Tipo de plan:</strong> {{ userData.plan }}</p>
            </div>
            <p v-else>No se ha seleccionado ningún usuario.</p>
          </div>
        </div>
        <div class="footer">
          <span class="footer-text">Total vendido: 220 USD</span>
          <span class="footer-text">Clientes totales: 50</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CuadraturaMensual',
    data() {
      return {
        userData: null // Para almacenar la información del usuario
      }
    },
    methods: {
      async fetchUserData(userId) {
        try {
          // Hacer una solicitud HTTP para obtener datos del usuario
          const response = await fetch(`https://api.example.com/users/${userId}`);
          if (response.ok) {
            this.userData = await response.json(); // Almacenar los datos recibidos
          } else {
            console.error('Error al obtener los datos del usuario');
          }
        } catch (error) {
          console.error('Error en la solicitud:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .cuadratura-mensual {
    display: flex;
    flex-direction: column; /* Para apilar el título y el contenido */
    align-items: center; /* Centra horizontalmente el contenedor */
    height: 100vh;
    background-color: #f0f0f0; /* Fondo gris claro para contraste */
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
  
  .right-section {
    width: 70%;
    padding: 20px;
    box-sizing: border-box;
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
    font-size: 1.2em; /* Tamaño de fuente más grande */
    margin-right: 40px; /* Espacio entre los textos */
  }
  </style>
  