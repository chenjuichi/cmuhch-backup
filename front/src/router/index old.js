import Vue from 'vue'
import VueRouter from 'vue-router'
//import Home from '../views/Home.vue'
import Navbar from '../components/Navbar.vue'
import App1 from '../views/menu/App1.vue'
import App2 from '../views/menu/App2.vue'
import App3 from '../views/menu/App3.vue'
import App4 from '../views/menu/App4.vue'
import About from '../views/About.vue'
import Login from '../views/LoginForm.vue'
import Employer from '../views/menu/Employer.vue'
import Reagent from '../views/menu/Reagent.vue'
import Grids from '../views/menu/Grids.vue'
import GridsForLed from '../views/menu/Grids.vue'
import Led1 from '../views/menu/Led1.vue'
import Department from '../views/menu/Department.vue'
import Supplier from '../views/menu/Supplier.vue'
import SupplierForProduct from '../views/menu/SupplierForProduct.vue'
import Permission from '../views/menu/permission.vue'
import StockInTag from '../views/menu/StockInTag.vue'
import StockInTagPrint from '../views/menu/StockInTagPrint.vue'
import StockIn from '../views/menu/StockIn.vue'
import StockOutTag from '../views/menu/StockOutTag.vue'
import StockOutTagPrint from '../views/menu/StockOutTagPrint.vue'
//import BarCode from '../components/BarCode.vue'
import ReqRecord from '../views/menu/ReqRecord.vue'
import StockRecord from '../views/menu/StockRecord.vue'
import Inventory from '../views/menu/Inventory.vue'


Vue.use(VueRouter)

const routes = [
  { path: '/',      name: 'Login', component: Login},
  //{ path: '/about', name: 'About',  component: () => import('../views/About.vue') },
  { path: '/about', name: 'About',  component: About},
  { path: '/emp',   name: 'Employer', component: Employer},
  { path: '/reag',  name: 'Reagent', component: Reagent},
  { path: '/grid',  name: 'Grids', component: Grids},
  { path: '/gridsForLed',  name: 'GridsForLed', component: GridsForLed,
    children: [
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'station1',
        component: Led1,
      },
      {
        // UserPosts will be rendered inside User's <router-view>
        // when /user/:id/posts is matched
        path: 'station2',
        component: UserPosts,
      },
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'station3',
        component: UserProfile,
      },
    ],

  },
  { path: '/dep',  name: 'Department', component: Department},
  { path: '/sup',  name: 'Supplier', component: Supplier},
  { path: '/supAndPrd',  name: 'SupplierForProduct', component: SupplierForProduct},
  { path: '/perm',  name: 'Permission', component: Permission},
  { path: '/stockIn', name: 'StockIn', component: StockIn},
  { path: '/inTag', name: 'StockInTag', component: StockInTag},
  { path: '/inTagPrint',   name: 'StockInTagPrint', component: StockInTagPrint},
  { path: '/outTag', name: 'StockOutTag', component: StockOutTag},
  { path: '/outTagPrint',   name: 'StockOutTagPrint', component: StockOutTagPrint},
  { path: '/app1', name: 'App1', component: App1},
  { path: '/app2', name: 'App2', component: App2},
  { path: '/app3', name: 'App3', component: App3},
  { path: '/app4', name: 'App4', component: App4},
  { path: '/navbar', name: 'Navbar', component: Navbar},
  { path: '/reqRec', name: 'ReqRecord', component: ReqRecord},
  { path: '/stockRec', name: 'StockRecord', component: StockRecord},
  { path: '/invent', name: 'Inventory', component: Inventory},
  //{ path: '/barcode', name: 'BarCode', component: BarCode}, //for test
]

const router = new VueRouter({
  mode: 'history',
  // base: process.env.BASE_URL,
  base: '/',
  routes
})
/*
router.beforeEach((to, from, next) => {
  let isAuthenticated=localStorage.getItem('Authenticated');
  if (isAuthenticated == null) {
    isAuthenticated=false;
    localStorage.setItem('Authenticated', isAuthenticated);
  }
  console.log("routing is:", to.name, isAuthenticated);

  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login'});
  } else {
    next();
  }
})
*/
export default router
