<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
*{
  margin: 0;
  padding: 0;
}
body{
  background: #ffffff;
}
  #app{
    width: 100%;
    height: 100%;
  }
.video-js.vjs-paused .vjs-big-play-button{
  z-index:100;
}
.vjs-has-started .vjs-control-bar{
  z-index:100;
}
</style>
