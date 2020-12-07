<template>
  <div id="header" >
    <div class="logo">try视频审阅平台</div>
    <nav >
      <a href="#home">首页</a>
      <a href="#about-us">关于我们</a>
      <a href="#showcases">成功案例</a>
      <a href="#team-intro">团队介绍</a>
      <div class="header-right">
        <el-button type="text" v-if="hasToken" @click="goLogin"> 登陆</el-button>
        <el-button type="danger"  @click="goHome">进入分秒帧</el-button>
      </div>
    </nav>


  </div>
</template>

<script>
  export default {
    name: "Header2",
    data() {
      return {
        sticky: false,
        isOpen:false
      };
    },
    methods:{
      goLogin(){
        this.$router.push('/login')
      },
      goHome(){
        if(!window.localStorage.getItem('token')){
          this.$router.push('/login')
        }
        this.$router.push('/')
      }
    },
    computed:{
      hasToken(){
       return false ? window.localStorage.getItem('token'):true
      }
    },
    mounted() {

    }
  };
</script>

<style scoped>
  #header {
    height: 80px;
    line-height: 80px;
    display: grid;
    padding: 0 40px;
    grid-template-columns: 250px 1fr;
    align-content: center;
    position: relative;
    z-index: 200;
    position: relative;
  }
  .logo {
    font-size: 28px;
    font-weight: 600;
    color: #e7e9ec;
  }
  #header nav {
    justify-self: start;
  }
  #header nav i {
    color: #e7e9ec;
  }
  #header nav a {
    color: #e7e9ec;
    text-decoration: none;
    margin: 0 24px;
    font-size: 16px;
  }

  .header-right{
    position: absolute;
    right: 40px;
    top:0
  }
</style>
