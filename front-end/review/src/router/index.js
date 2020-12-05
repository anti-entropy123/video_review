import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Login from '@/views/Login'
import Meet from '@/views/Meet'
import Palette from '@/views/Palette'
import Draw from '@/views/Draw'
Vue.use(Router)
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },{
    path:'/login',
    name: 'Login',
    component: Login
  },{
    path: '/meeting',
    name:'Meet',
    component: Meet
  },{
    path:'/palette',
    name:'Palette',
    component: Palette
  },
  {
    path:'/draw',
    name:'Draw',
    component: Draw
  },
]


const router = new Router({
  mode: "history",
  routes
});

// 路由导航守卫
router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    return next();
  }
  const tokenStr = window.sessionStorage.getItem("token");
  if (!tokenStr) {
    return next("/login");
  }
  next();
});

export default router;
