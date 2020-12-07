<template>
<div id="components-layout-demo-basic">
  <a-layout-header class="user">
    <div class="title">
      视频协作平台
    </div>
    <div class="message">
      <div class="bell">
        <a-dropdown >
         <a class="ant-dropdown-link" @click="e => e.preventDefault()">
         <a-icon type="bell" :style="{ fontSize: '23px', color: '#ffffff' }"/></a>
         <a-menu slot="overlay">
        <a-menu-item key="0">
          <a target="_blank" rel="noopener noreferrer" href="http://www.alipay.com/">1min 前**同意了你的申请</a>
        </a-menu-item>
        <a-menu-item key="1">
          <a target="_blank" rel="noopener noreferrer" href="http://www.baidu.com/">15min后**会议召开</a>
        </a-menu-item>
        <a-menu-divider/>
      </a-menu>
    </a-dropdown>
      </div>
      <a-avatar  size="large" icon="user" />
    </div>
  </a-layout-header>

</div>
</template>

<script>
    export default {
        name: "Header"
    }
</script>

<style scoped>

#components-layout-demo-basic {
  /*text-align: center;*/
}
#components-layout-demo-basic .ant-layout-header,
#components-layout-demo-basic .ant-layout-footer {
  background: #0f68bc;
  color: #fff;
}
  .user{
    align-items: center;
  }
  .title{
    float: left;
    color: white;
    font-size: 17px;
  }
  .message{
    margin-right: 14px;
    align-items: center;
    float: right;
  }
  .bell{
    margin-right: 20px;
    float: left;
    margin-top: 4px;
  }
</style>
