<template>
  <div id="content">
    <Menu v-on:page="getPage"></Menu>
      <div id="main">
  <!--顶部导航-->
        <div id="top">
           <a-menu id="topmenu" v-model="current" mode="horizontal"
                   :theme="theme"
                   :default-selected-keys="['files']"
                   @click="handleClick">
            <a-menu-item key="files"> <a-icon type="folder" />文件</a-menu-item>
            <a-menu-item key="rubbish"> <a-icon type="delete" />回收站</a-menu-item>
           </a-menu>
            <div id="users" v-for="n in 4">
              <div id="user"
                   :style="`
                 zIndex:  ${n?n:0};
                 transform: translate(${position(n)})`">
                <a-avatar  size="large" icon="user" />
              </div>
            </div>
          <a-icon id="plus" key="plus" type="plus-circle" style="fontSize:36px;"></a-icon>
        </div>
  <!--卡片循环-->
       <div class="cards" v-if="e == 3 && topMenu=='files'">
         <router-link  to="/meeting" >
        <a-card  class="card" hoverable v-for="n in 3">
        <img
          slot="cover"
          alt="example"
          src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
        />
        <template slot="actions" class="ant-card-actions">
          <a-icon key="ellipsis" type="ellipsis" />
        </template>
        <a-card-meta title="title" description="This is the description">
          <a-avatar
            slot="avatar"
            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
          />
        </a-card-meta>
      </a-card>
         </router-link>
      </div>
        <div class="cards" v-else-if="e==4 && topMenu=='files'" >
          <a-card class="card" hoverable  v-for="n in 4">
            <img
              slot="cover"
              alt="example"
              src="https://s1.ax1x.com/2020/10/18/0OwePK.jpg"
            />
            <template slot="actions" class="ant-card-actions">
              <a-icon key="ellipsis" type="ellipsis" />
            </template>
            <a-card-meta title="花花" description="18.9鸟巢饭拍">
              <a-avatar
                slot="avatar"
                src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
              />
            </a-card-meta>
          </a-card>
        </div>
    </div>
  </div>
</template>

<style>
  .cards{
    /*margin-top: 44px;*/
    /*margin-left: 36px;*/
    float: left;
  }
  .card{
    float: left;
    margin-top: 36px;
    margin-left: 36px;
    width: 276px;
  }

  #content {
    /*background: black;*/
    width: 100%;
    height: 100%;
    float: left;
  }
  #main{
    position: absolute;
    margin-left: 256px;
    width: 83%;
  }

  #top{
    width: 100%;
    float: left;
  }
  #topmenu{
    width: 100%;
    background: #ffffff;
    float: left;
    /*position: absolute;*/
  }
  #users{
    float: right;
    align-items: center;
    margin-right: 260px;
    margin-top: -46px;
  }
  #user{
    position: absolute;
    margin-left: 10px;
  }
  #plus{
    fontSize:36px;
    color:#7b7b7b;
    float: right;
    /*position: absolute;*/
    align-items: center;
    margin-right: 72px;
    margin-top: -46px;
  }
</style>

<script>
  import Menu from "./Menu"

  export default {
    components: {Menu},
    name: "Main",
    data() {
      return {
        collapsed: false,
        theme: 'light',
        current: ['files'],
        e:1,
        topMenu:'files'
      };
    },
    mounted() {

    },
    methods:{
        getPage:function(e) {
            this.e = e
            console.log(e)
        },
        handleClick(e) {
          this.topMenu=e.key
          console.log('click', e.key);
          console.log(this.topMenu)
        },
      position(n) {
        return `${(n) * 22}px, ${(n) * 0}px`
      },
    }
  };
</script>

