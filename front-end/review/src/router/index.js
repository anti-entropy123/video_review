import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/views/Login'
import Home from '@/views/Home'
import File from '@/components/projects/File'
import Recycle from '@/components/projects/Recycle'
import Personal from '@/components/projects/Personal'

import User from '@/views/User'
import UserInfo from '@/components/user/UserInfo'
import Message from '@/components/user/Message'
import MyVideo from '@/components/user/MyVideo'
import Welcome from '@/views/Welcome'
import Admin from '@/views/Admin'
import UserManage from "../components/admin/UserManage";
import MeetingManage from "../components/admin/MeetingManage";
import VideoManage from "../components/admin/VideoManage";
import RoleManage from "../components/admin/RoleManage";
import ProjectManage from "../components/admin/ProjectManage";
import ViewManage from "../components/admin/ViewManage";
import AdminLogin from "../components/admin/AdminLogin";
import MyMeeting from "../components/user/MyMeeting";
import Meeting from "../components/projects/Meeting"
import Review from "@/views/Review";
import Account from "../components/user/Account";

Vue.use(Router)
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    redirect:'/file/0',
    children:[
      {
        path:'/file/:id',
        name: 'File',
        component:File
      },
      {
         path:'/recycle/:id',
        name:'Recycle',
        component:Recycle
      },
      {
        path:'/meeting/:id',
        name:'Meeting',
        component:Meeting
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    redirect:'/user/userInfo',
    children:[
      {
        path: '/user/userInfo',
        name: 'UserInfo',
        component: UserInfo,
      },
      {
        path: '/user/message',
        name: 'Message',
        component: Message,
      },
      {
        path: '/user/myVideo',
        name: 'MyVideo',
        component: MyVideo,
      },{
        path: '/user/account',
        name: 'Account',
        component: Account,
      },{
      path:'/user/myMeeting',
        name:'MyMeeting',
        component:MyMeeting
      },
      {
        path:'/user/personal',
        name:'Personal',
        component:Personal
      }
    ]
  },{
  path:'/welcome',
    name:'Welcome',
    component:Welcome
  },
  {
    path:'/admin',
    name:"Admin",
    component: Admin,
    redirect:'/admin/userManage',
    children:[
      {
        path:'/admin/userManage',
        name:"UserManage",
        component: UserManage,
      },
      {
        path:'/admin/projectManage',
        name:"ProjectManage",
        component: ProjectManage,
      },
      {
        path:'/admin/videoManage',
        name:"VideoManage",
        component: VideoManage,
      },
      {
        path:'/admin/meetingManage',
        name:"MeetingManage",
        component: MeetingManage,
      }, {
        path:'/admin/roleManage',
        name:"RoleManage",
        component: RoleManage,
      },
      {
        path:'/admin/viewManage',
        name:"ViewManage",
        component: ViewManage,
      }
    ]
  },
  ,{
    path:'/review',
    name:'Review',
    component:Review
  },{
  path:'/admin/login',
    name:'AdminLogin',
    component:AdminLogin
  },
]

const router = new Router({
  mode: "history",
  routes
});


// 路由导航守卫
router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    window.localStorage.removeItem('token');
    window.localStorage.removeItem('userId')
    window.localStorage.removeItem('mobileNum')
    return next();
  }

  if (to.path === "/welcome") {
    return next();
  }
  if(to.path === '/admin/login'){
    window.localStorage.removeItem('adm-token')
    return next()
  }
   const admTokenStr = window.localStorage.getItem('adm-token')
  const tokenStr = window.localStorage.getItem("token");
   if (to.path ==='/admin' || to.path==='/admin/viewManage' ||to.path==='/admin/meetingManage'||to.path==='/admin/videoManage' || to.path==='/admin/roleManage' || to.path === '/admin/userManage' || to.path==='/admin/projectManage'){
     if (!admTokenStr){
       return next("/admin/login");
     }
   }else{
     if (!tokenStr) {
       return next("/welcome");
     }
   }

  next();
});

export default router;
