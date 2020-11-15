<template>
  <div >
<!--    顶部导航-->
    <a-menu id="topmenu" v-model="current" mode="horizontal" :theme="theme">
      <a-menu-item key="mail"> <a-icon type="mail" />文件 </a-menu-item>
      <a-menu-item key="app"> <a-icon type="appstore" />回收站 </a-menu-item>
    </a-menu>
<!--卡片循环-->
    <div id="cards">
      <a-card hoverable style="width: 300px">
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
    </div>
  </div>
</template>

<style>

  #cards{
    margin-top: 36px;
    margin-left: 36px;
  }
  #topmenu{
    width: 100%;
    background: #ffffff;
  }
</style>

<script>
  export default {
    name: "Main",
    data() {
      return {
        collapsed: false,
        theme: 'light',
        current: ['mail'],
      };
    },
  };
</script>

