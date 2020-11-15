<template>
<!--  <div class="menu">-->
    <a-menu id = "menu"
      :default-selected-keys="['1']"
      :open-keys.sync="openKeys"
      :theme="theme"
      mode="inline"
      checked-children="dark"
      @click="handleClick">

      <a-sub-menu key="sub1" @titleClick="titleClick">
        <span slot="title"><a-icon type="appstore" /><span>项目组</span></span>
        <a-menu-item key="0">
          Doggie现场
        </a-menu-item>
        <a-menu-item key="1">
          姜云升现场
        </a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="sub2">
        <span slot="title"><a-icon type="setting" /><span>个人空间</span></span>
        <a-menu-item key="9">
          Doggie广州
        </a-menu-item>
        <a-menu-item key="10">
          Doggie北京1
        </a-menu-item>
        <a-menu-item key="11">
          Doggie天津
        </a-menu-item>
        <a-menu-item key="12">
          Doggie北京2
        </a-menu-item>
      </a-sub-menu>
    </a-menu>
<!--  </div>-->
</template>
<script>
  export default {
    name: "Menu",
    data() {
      return {
        current: ['mail'],
        openKeys: ['sub1'],
        theme: 'light',
      };
    },
    watch: {
      openKeys(val) {
        console.log('openKeys', val);
      },
    },
    methods: {
      handleClick(e) {
        console.log('click', e);
      },
      titleClick(e) {
        console.log('titleClick', e);
      },
    },
  };
</script>


<style scoped>
#menu{
  width: 256px;
  height:92%;
  position: absolute;
  top: 64px;
  bottom:0
}
</style>
