// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';// 加载 CSS
// import Video from 'video.js'
// import 'video.js/dist/video-js.css'
import VueSocketIO from 'vue-socket.io'
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
import VideoPlayer from 'vue-video-player';
import 'video.js/dist/video-js.css';
import 'vue-video-player/src/custom-theme.css';


Vue.use(VideoPlayer)
Vue.config.productionTip = false;
Vue.use(Antd)
Vue.use(ViewUI);
// Vue.use(Video)
Vue.use(ElementUI, { size: "small", zIndex: 3000 });
Vue.config.productionTip = false;
Vue.use(new VueSocketIO({
    debug: true,
    connection: '188.131.227.20:1314/meetingRoom',
  }
))


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
