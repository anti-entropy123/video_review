// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// element-ui
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(ElementUI, { size: "small", zIndex: 3000 });

//tjs
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';// 加载 CSS
import VueSocketIO from 'vue-socket.io'
import VideoPlayer from 'vue-video-player';
import 'video.js/dist/video-js.css';
import 'vue-video-player/src/custom-theme.css';
Vue.use(VideoPlayer)
Vue.use(Antd)
Vue.use(new VueSocketIO({
  debug: true,
  connection: 'https://api.video-review.top:1314/meetingRoom',
}
))


Vue.config.productionTip = false
// //全局样式
import './assets/css/global.css'

// 进度条和富文本配置
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
Vue.use(VueQuillEditor)
// axios配置

import axios from "axios";
Vue.prototype.$http = axios;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "https://api.video-review.top:1314/api/";
axios.defaults.headers.post["Content-Type"] = "application/json";

// 请求头拦截
axios.interceptors.request.use(config => {
  //在最后必须 return config
  NProgress.start()
  // config.headers.Authorization =
  //   "Bearer " +  window.localStorage.getItem("adm-token");
  config.headers.Authorization =
  "Bearer " +  window.localStorage.getItem("token");
  return config;
});
axios.interceptors.response.use(config => {
  NProgress.done()
  return config
})


// 过滤器
//videoName 过滤
Vue.filter('videoNameFormat',name=>{
  return name.slice(0,name.lastIndexOf('.'))
})

// 转换时间的格式
Vue.filter('dateFormat', (originVal) => {
  originVal = originVal
  const dt = new Date(originVal)
  const y = dt.getFullYear()
  const m = (dt.getMonth() + 1 + '').padStart(2, '0')
  const d = (dt.getDate() + '').padStart(2, '0')
  const hh = (dt.getHours() + '').padStart(2, '0')
  const mm = (dt.getMinutes() + '').padStart(2, '0')
  const ss = (dt.getSeconds() + '').padStart(2, '0')
  return `${y}-${m}-${d} ${hh}:${mm}:${ss}`
})
Vue.filter('timeFormat',(time) =>{
  var hours = Math.floor(time / 3600)
  var minutes = Math.floor(time %3600 /60 )
  var seconds = time % 60
  minutes = minutes>10? minutes:'0'+minutes
  seconds = seconds>10 ? seconds:'0'+seconds
  return `${hours}:${minutes}:${seconds}`
})
Vue.filter('messageType',(type) =>{
  let message =''
  switch (type) {
      case 0:  message="在上传了新的视频";break;
    case 1: message='审阅了你上传的视频';break;
      case 2: message='你的某个项目里的成员预定了新的会议';break;
    case 3: message='邀请你加入项目';break;
    case 4: message='处理了你的邀请';break;
    case 5:message= '你被移除出了项目';break;

    default:
      break;
  }
 return message

} )
Vue.filter('dataFilter',(value)=>{//这里的value是拿到json里面的关于时间的值
  // value=value*1000
  var year = 24*60*60*1000*365;//拿到一年的毫秒数
  var month = 24*60*60*1000*30;//拿到一个月的毫秒数
  var day = 24*60*60*1000;//拿到一天的毫秒数
  var hour = 60*60*1000;//拿到一个小时的毫秒数
  var minute = 60*1000;//拿到一分钟的毫秒数

   //getTime()   返回从 1970 年 1 月 1 日至今的毫秒数
  var newDate = new Date().getTime();//拿到1970年1月1日距当前的时间的毫秒数
  var time = new Date(value).getTime();//拿到json里面的关于时间的值，计算1970.1.1距json给的时间的毫秒数
  var date = newDate - time;//计算两个时间的差值

 //使用三目运算
  var years = parseInt(date/year)>0 ? `${parseInt(date/year)}年前` : ""; //两个时间的差值，除以一年的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var months = parseInt(date/month)>0 ? `${parseInt(date/month)}月前` : "";//两个时间的差值，除以一月的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var days = parseInt(date/day)>0 ? `${parseInt(date/day)}天前` : "";//两个时间的差值，除以一天的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var hours = parseInt(date/hour)>0 ? `${parseInt(date/hour)}小时前` : "";//两个时间的差值，除以一小时的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var minutes = parseInt(date/minute)>0 ? `${parseInt(date/minute)}分钟前` : "";//两个时间的差值，除以一分钟的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。


  if(years.length != 0){
    return years;
  } else if(months.length != 0){
    return months;
  } else if(days.length != 0){
    return days;
  } else if(hours.length != 0){
    return hours;
  } else if(minutes.length != 0){
    return minutes;
  } else {
    return parseInt((date)/1000)>0?`${parseInt((date)/1000)}秒前`:"";
  }
}

)

Vue.filter('dataFilter2',(value)=>{//这里的value是拿到json里面的关于时间的值
  var year = 24*60*60*1000*365;//拿到一年的毫秒数
  var month = 24*60*60*1000*30;//拿到一个月的毫秒数
  var day = 24*60*60*1000;//拿到一天的毫秒数
  var hour = 60*60*1000;//拿到一个小时的毫秒数
  var minute = 60*1000;//拿到一分钟的毫秒数


  var date = value

 //使用三目运算
  var years = parseInt(date/year)>0 ? `${parseInt(date/year)}年` : ""; //两个时间的差值，除以一年的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var months = parseInt(date%year/month)>0 ? `${parseInt(date%year/month)}月` : "";//两个时间的差值，除以一月的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var days = parseInt(date%month/day)>0 ? `${parseInt(date%month/day)}天` : "";//两个时间的差值，除以一天的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var hours = parseInt(date%day/hour)>0 ? `${parseInt(date%day/hour)}小时` : "";//两个时间的差值，除以一小时的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
  var minutes = parseInt(date%hour/minute)>0 ? `${parseInt(date%hour/minute)}分钟` : "";//两个时间的差值，除以一分钟的毫秒数，看整数是否大于0，如果是的话就返回,当前的整数数据，如果不是,返回空。
var seconds = parseInt((date%minute)/1000)>0?`${parseInt((date%minute)/1000)}秒`:"";

    return hours+minutes+seconds
}

)
 
// 定义directive
Vue.directive('drag', {

  inserted: function(el, binding, vnode) {
    var odiv = el.parentNode;
    odiv.onmousedown = function(eve) {
        eve = eve || window.event;
        var clientX = eve.clientX;
        var clientY = eve.clientY;
        var odivX = odiv.offsetLeft;
        var odivY = odiv.offsetTop;
        var odivLeft = clientX - odivX;
        var odivTop = clientY - odivY;
        var clientWidth = document.documentElement.clientWidth;
        var oWidth = odiv.clientWidth;
        var odivRight = clientWidth - oWidth;
        var clientHeight = document.documentElement.clientHeight;
        var oHeight = odiv.clientHeight;
        var odivBottom = clientHeight - oHeight;
        document.onmousemove = function(e) {
            e.preventDefault();
            var left = e.clientX - odivLeft;
            if (left < 0) {
                left = 0
            }
            if (left > odivRight) {
                left = odivRight
            }
            var Top = e.clientY - odivTop;
            if (Top < 0) {
                Top = 0
            }
            if (Top > odivBottom) {
                Top = odivBottom
            }
            odiv.style.left = left + "px";
            odiv.style.top = Top + "px";
        }
        document.onmouseup = function() {
            document.onmouseup = "";
            document.onmousemove = "";
        }
    }
}
})
Vue.directive(
  'stopdrag',{
    inserted: function(el, binding, vnode) {
      let element = el;
      element.onmousedown = function(e) {
          e.stopPropagation()
      }
  }
  }
)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})


const headerEl = document.querySelector("header");
const glide = new Glide(".glide", {
  type: "carousel",
  startAt: 0,
  autoplay: 3500,
});
const captionsEL = document.querySelectorAll(".slide-caption");

glide.on(["mount.after", "run.after"], () => {
  const caption = captionsEL[glide.index];
  anime({
    targets: caption.children,
    opacity: [0, 1],
    duration: 400,
    easing: "spring(1, 80, 10, 0)",
    delay: anime.stagger(400, { start: 300 }),
    translateY: [anime.stagger([40, 10]), 0],
  });
});
glide.on("run.before", () => {
  document.querySelectorAll(".slide-caption > *").forEach((el) => {
    el.style.opacity = 0;
  });
});

glide.mount();


// 通用滑动出现动画配置项
const staggeringOption = {
  delay: 300,
  distance: "50px",
  duration: 500,
  easing: "ease-in-out",
  origin: "bottom",
};

// interval设置等待时间
ScrollReveal().reveal(".feature", { ...staggeringOption, interval: 350 });

ScrollReveal().reveal(".service-item", { ...staggeringOption, interval: 350 });

const dataSectionEl = document.querySelector(".data-section");

ScrollReveal().reveal(".data-section", {
  beforeReveal: () => {
    anime({
      targets: ".data-piece .num",
      innerHTML: (el) => {
        return [0, el.innerHTML];
      },
      duration: 1500,
      round: 1,
      easinge: "easeInExpo",
    });
    dataSectionEl.style.backgroundPosition =
      "center calc(50% - ${dataSectionEl.getBoundingClientRect().bottom/5}px)";
  },
});



//平滑滚动
const scroll = new SmoothScroll(
  'nav a[href*="#"] , .scroll-to-top a[href*="#"]',
  {
    header: "header",
    offset: 50,
  }
);


