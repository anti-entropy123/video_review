// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
<<<<<<< HEAD
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';// 加载 CSS
// import {Button,Layout,Avatar} from 'ant-design-vue'
// Vue.use(Button).use(Layout).use(Avatar)
// Vue.component(Layout.name, Layout);
// import { Button } from 'ant-design-vue';

Vue.config.productionTip = false;
Vue.use(Antd)
=======

>>>>>>> 2238b8058cef644734cd614b6928fe000fa9b91a
Vue.use(ElementUI, { size: "small", zIndex: 3000 });
Vue.config.productionTip = false;

import axios from "axios";
Vue.prototype.$http = axios;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://188.131.227.20:1314/api/";
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.interceptors.request.use(config => {
  //在最后必须 return config
  config.headers.Authorization =
    "Bearer " + window.sessionStorage.getItem("token");
  return config;
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
