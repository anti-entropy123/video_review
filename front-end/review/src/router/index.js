import Vue from 'vue'
import Router from 'vue-router'
<<<<<<< HEAD
import Home from '@/views/Home'
import Login from '@/views/Login'

=======
import Home from '../views/Home'
import Login from "../views/Login";
import UserInfo from "../views/UserInfo";
import Recycle from "../components/Recycle";
import File from "../components/File";
import Share from "../components/Share";
import Message from "../components/Message";
import Personal from "../components/Personal";
>>>>>>> rlj
Vue.use(Router)
const routes = [
  {
    path: '/',
    name: 'Home',
<<<<<<< HEAD
    component: Home
=======
    component: Home,
    redirect:'/file',
    children:[
      {
        path: '/recycle',
        name: 'Recycle',
        component:Recycle
      },
      {
        path: '/share',
        name: 'Share',
        component:Share
      },
      {
        path: '/file',
        name: 'File',
        component:File
      },
      {
        path:'/personal',
        name:'Personal',
        component:Personal
      },
      {
        path:'/userInfo',
          name:'UserInfo',
          component:UserInfo
        },
        {
          path:'/message',
            name:'Message',
            component: Message
          }
    ]
>>>>>>> rlj
  },{
    path:'/login',
    name: 'Login',
    component: Login
<<<<<<< HEAD
  }
=======
  },

>>>>>>> rlj
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
