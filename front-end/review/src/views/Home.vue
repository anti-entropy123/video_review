<template>
  <div>
    <Header></Header>
  <div id="content">
    <Menu></Menu>
    <div id="main">
    <Main></Main>
    </div>
  </div>
  </div>
</template>

<script>
import Header from "./Header";
import Main from "./Main";
import Menu from "./Menu"
export default {
  components: {Header,Main,Menu}
}
</script>

<style>
#content{
  background: black;
  width: 100%;
  height: 100%;
  float: left;
}
  Main{
    position: absolute;
    margin-left: 100px;
  }
  #main{
    position: absolute;
    margin-left: 256px;
    width: 74%;
  }

</style>
