<template>
    <div class="login-container">
      <h1 class="login-title">Iniciar sesión</h1> <!-- Título arriba del cuadro -->
      <div class="login-box">
        <h2 class="sub-title">Transcriptor WhatsApp</h2>
        <img class="logo" src="https://alloxentric.com/wp-content/uploads/2020/11/alloxentric_logo-3x.png" alt="Logo" />
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="phone">Teléfono:</label>
            <input type="text" id="phone" v-model="phone" placeholder="Ingresa tu teléfono" />
          </div>
          <div class="input-group">
            <label for="password">Contraseña:</label>
            <input type="password" id="password" v-model="password" placeholder="Ingresa tu contraseña" />
          </div>
          <button class="login-button" type="submit">Iniciar sesión</button>
        </form>
        <div class="links">
          <a href="#" class="link">¿Olvidaste tu contraseña?</a>
          <a href="#" class="link">¿No estás registrado? Crear cuenta</a>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        phone: '',
        password: ''
      }
    },
    methods: {
      handleLogin() {
        // Aquí iría la lógica para manejar el inicio de sesión
        console.log('Iniciar sesión con', this.phone, this.password);
      }
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column; /* Apilar el título y el cuadro de login verticalmente */
    align-items: center;
    justify-content: center;
    padding-top: 4%;
  }

  .login-title {
    font-size: 2.5em; /* Tamaño del título arriba del cuadro */
    font-weight: bold;
    color: #000000;
    margin-bottom: 20px; /* Espacio entre el título y el cuadro de login */
  }
  
  .login-box {
    display: flex;
    flex-direction: column;
    align-items: center; 
    width: 40%;
    background-image: linear-gradient(#ffffff, #1DBEA8);
    border: 1px solid #000; /* Borde negro alrededor del cuadro */
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .sub-title {
    font-size: 1.5em;
    color: #000000;
    margin-bottom: 20px;
  }
  
  .logo {
    width: 200px; /* Ajusta el tamaño de la imagen del logo según sea necesario */
    margin-bottom: 20px;
  }
  
  .input-group {
    width: 80%;
    margin-bottom: 15px;
  }
  
  .input-group label {
    width: 100%;
    display: block;
    margin-bottom: 5px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .login-button {
    background-color: #007E6F; /* Color del botón igual que el footer en la página anterior */
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 10px;
    cursor: pointer;
    width: 80%;
  }
  
  .login-button:hover {
    background-color: #005f4f; /* Color del botón al pasar el mouse */
  }
  
  .links {
    margin-top: 20px;
  }
  
  .link {
    display: block;
    color: #000000; /* Color del texto de los enlaces */
    text-decoration: none;
    margin-top: 10px;
  }
  
  .link:hover {
    text-decoration: underline;
  }
  </style>
  