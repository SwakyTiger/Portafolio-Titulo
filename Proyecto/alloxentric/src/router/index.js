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
import home from '@/components/views/Home.vue'
import editarInfoUser from '@/components/views/editarInfoUser.vue'
import miSuscripcion from '@/components/views/miSuscripcion.vue'
import transcriptorWeb from '@/components/views/transcriptorWeb.vue'
import keycloak from '@/keycloak';

const routes = [
  {
    path: '/',
    name: 'home',
    component: home
  },
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
    component: resumenPago,
    meta: { requiresAuth: true }
  },
  {
    path: '/pagoRealizado',
    name: 'pagoRealizado',
    component: pagoRealizado,
    meta: { requiresAuth: true }
  },
  {
    path: '/historyTranscriptor',
    name: 'historyTranscriptor',
    component: historyTranscriptor,
    meta: { requiresAuth: true }
  },
  {
    path: '/miCuenta',
    name: 'miCuenta',
    component: miCuenta,
    meta: { requiresAuth: true }
  },
  {
    path: '/editarInfoUser',
    name: 'editarInfoUser',
    component: editarInfoUser
  },
  {
    path: '/miSuscripcion',
    name: 'miSuscripcion',
    component: miSuscripcion
  },
  {
    path: '/transcriptorWeb',
    name: 'transcriptorWeb',
    component: transcriptorWeb,
    meta: { requiresAuth: true }
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
  // Verificar si la ruta requiere autenticación
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!keycloak.authenticated) {
      console.log('No autenticado, redirigiendo al login.');
      keycloak.login(); // Redirigir al login si no está autenticado
    } else {
      console.log('Usuario autenticado, permitiendo acceso.');
      next(); // Permitir acceso si está autenticado
    }
  } else if (to.matched.some(record => record.meta.requiresAdmin)) {
    // Verificar si la ruta requiere rol de admin
    if (!keycloak.authenticated) {
      console.log('No autenticado, redirigiendo al login.');
      keycloak.login(); // Redirigir al login si no está autenticado
    } else if (!checkAdminRole()) {
      console.log('No es admin, redirigiendo a la página de inicio.');
      next('/'); // Redirigir a la página de inicio si no es admin
    } else {
      console.log('Usuario autenticado y es admin, permitiendo acceso.');
      next(); // Permitir acceso si el usuario es admin
    }
  } else {
    console.log('Ruta no requiere autenticación, permitiendo acceso.');
    next(); // Permitir acceso si la ruta no requiere autenticación
  }
});

export default router;