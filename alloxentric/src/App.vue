<template>
  <div id="app">
    <nav>
      <router-link to="/">Inicio</router-link>
      <router-link to="/planDetails">Planes</router-link>
      <router-link to="/RegistroUsuario">Registrarse</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
nav {
  padding: 15px;
  background-color: #f8f8f8;
}
nav a {
  margin-right: 15px;
  text-decoration: none;
  color: #42b983;
}
</style>