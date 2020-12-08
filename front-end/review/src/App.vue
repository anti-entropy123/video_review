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
.video-js.vjs-paused .vjs-big-play-button{
  z-index:100;
}
.vjs-has-started .vjs-control-bar{
  z-index:100;
}
</style>
