<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Rtc from "./views/Rtc"

export default {
  name: 'App',
  components: {
    // 挂载子组件 (其它组件通过router加载, 所以不需要写在这里)
    Rtc
  }
}
</script>

<style>
.video-js.vjs-paused .vjs-big-play-button{
  z-index:100;
}
.vjs-has-started .vjs-control-bar{
  z-index:100;
}
</style>
