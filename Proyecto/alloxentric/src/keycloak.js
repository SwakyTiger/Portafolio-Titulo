import Keycloak from "keycloak-js";
import config from "@/config";

// Configura Keycloak con los detalles de tu cliente
const keycloak = new Keycloak({
  url: `${config.BASE_URL}:8081/`, // URL del servidor Keycloak
  realm: 'Transcriptor',               // Nombre del realm utilizado
  clientId: 'transcriptor_alloxentric'          // ID del cliente 
});

export default keycloak;
