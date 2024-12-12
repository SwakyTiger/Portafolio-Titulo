import Keycloak from "keycloak-js";

// Configura Keycloak con los detalles de tu cliente
const keycloak = new Keycloak({
  url: 'http://34.176.251.141:8081/', // URL del servidor Keycloak
  realm: 'Transcriptor',               // Nombre del realm utilizado
  clientId: 'transcriptor_alloxentric'          // ID del cliente 
});

export default keycloak;
