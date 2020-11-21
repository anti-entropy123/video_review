<template>
    <el-header class="home-header">
      <div class="header-title">帧秒分</div>
      <div class="header-left">
        <el-badge :value="12" style="font-size:10px" >
          <i class="el-icon-message-solid" style="font-size:26px"></i>
        </el-badge>
      <div class="header-user" @click="emitUserInfo">
          <div class="user-box">
            <div class="user-image">
              <img
              class="cursor"
              style="width: 100%; height: 100%;"
              :src="userInfo.name"
              />
            </div>
            <div>{{ userInfo.name }}</div>
          </div>
      </div>
      </div>
    </el-header>
</template>

<script>
    export default {
        name: "HomeHeader",
      props:{

      },
      data(){
          return {
            userInfo: {
              name: "rlj",
              avatar: "../../static/tiger.png"
            }
          }
      },
      methods:{
          emitUserInfo(){
            this.$emit('goUserInfo')
          }
      }
    }
</script>

<style scoped>
.home-header{
  top: 0;
  width: 100%;
  background-color: #fff;
  position: fixed;
  z-index: 9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  display: flex;
}

.header-left{
  display: flex;
  flex: 1;
  justify-content: flex-end;
  align-items: center;
}
.user-box{
  margin-left: 20px;
}

  .header-title{
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
  }
</style>
