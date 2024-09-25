import { createRouter, createWebHistory } from 'vue-router'
import planDetails from '@/components/views/planDetails.vue'
import RegistroUsuario from '@/components/views/RegistroUsuario.vue'
import crudPlanes from '@/components/views/crudPlanes.vue'
import cuadraturaMensual from '@/components/views/cuadraturaMensual.vue'
import login from '@/components/views/login.vue'
import ventasReport from '@/components/views/ventasReport.vue'
import resumenPago from '@/components/views/resumenPago.vue'
import pagoRealizado from '@/components/views/pagoRealizado.vue'
import historyTranscriptor from '@/components/views/historyTranscriptor.vue'
import miCuenta from '@/components/views/miCuenta.vue'
import keycloak from '@/keycloak';

const routes = [
  {
    path: '/planDetails',
    name: 'planDetails',
    component: planDetails
  },
  {
    path: '/RegistroUsuario',
    name: 'RegistroUsuario',
    component: RegistroUsuario
  },
  {
    path: '/crudPlanes',
    name: 'crudPlanes',
    component: crudPlanes,
    meta: { requiresAdmin: true }
  },
  {
    path: '/CuadraturaMensual',
    name: 'cuadraturaMensual',
    component: cuadraturaMensual,
    meta: { requiresAdmin: true }
  },
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/ventasReport',
    name: 'ventasReport',
    component: ventasReport,
    meta: { requiresAdmin: true }
  },
  {
    path: '/resumenPago',
    name: 'resumenPago',
    component: resumenPago
  },
  {
    path: '/pagoRealizado',
    name: 'pagoRealizado',
    component: pagoRealizado
  },
  {
    path: '/historyTranscriptor',
    name: 'historyTranscriptor',
    component: historyTranscriptor
  },
  {
    path: '/miCuenta',
    name: 'miCuenta',
    component: miCuenta
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Función para verificar si el usuario tiene el rol 'admin'
function checkAdminRole() {
  if (keycloak.authenticated) {
    const token = keycloak.tokenParsed;
    const clientRoles = token.resource_access?.['transcriptor_alloxentric']?.roles || [];
    console.log('Roles del cliente:', clientRoles); // Depuración
    return clientRoles.includes('admin');
  }
  return false;
}

// Guardia de navegación global para proteger rutas
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!keycloak.authenticated) {
      console.log('No autenticado, redirigiendo al login.');
      // keycloak.login(); // Redirigir al login si no está autenticado
      next('/');
    } else if (!checkAdminRole()) {
      console.log('No es admin, redirigiendo a la página de inicio.');
      next('/'); // Redirigir a la página de inicio si no es admin
    } else {
      console.log('Usuario autenticado y es admin, permitiendo acceso.');
      next(); // Permitir acceso si el usuario es admin
    }
  } else {
    console.log('Ruta no requiere rol de admin, permitiendo acceso.');
    next(); // Permitir acceso si la ruta no requiere rol de admin
  }
});


export default router;