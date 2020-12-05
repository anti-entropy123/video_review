<template>
  <el-container>
    <el-header class="user-header">
    <el-image class="header-title" src="../../static/images/logo.png" @click="goHome"></el-image>
    <div class="header-right">
            <el-button @click="goAdmin" type="text">管理员界面</el-button>
               <el-button style="height:36px" @click="goLoginOut"  type="danger" >退出登陆</el-button>
    </div>


    </el-header>

    <el-container>
      <el-aside width="200px" class="user-aside">
        <el-card style="  width: 100%;">
          <div class="btn-group">
            <el-button >  账号中心</el-button>
            <el-button type="text" @click="goToUserInfo">个人信息</el-button>
            <!-- <el-button type="text"  @click="goToMessage">消息中心</el-button> -->
            <el-button type="text" @click="goToMyMeeting" >我的会议</el-button>
            <el-button type="text" @click="goToMyVideo" >我的审阅</el-button>
               <el-button type="text" @click="goToPerson" >个人中心</el-button>
            <el-button type="text" @click="goToAccount" >账号安全</el-button>
          </div>
        </el-card>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  export default {
    name: "User",
    data() {
      return {
        userInfo: {},
        disabled: true,
        fileList: [
          {
            name: "food.jpeg",
            url:
              "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100"
          }
        ]
      };
    },
    methods: {
      goHome(){
        this.$router.push('/')
      },
      goToUserInfo(){
        this.$router.push('/user/userInfo')
      },
      goToMessage(){
        this.$router.push('/user/message')
      },
      goToMyVideo(){
        this.$router.push('/user/myVideo')
      },
      goToAccount(){
        this.$router.push('/user/account')
      },
      goToMyMeeting(){
        this.$router.push('/user/myMeeting')
      },
      goToPerson(){
          this.$router.push('/user/personal')
      },
       goLoginOut(){
          this.$router.push('/login')
        },
        goAdmin(){
          this.$router.push('/admin')
        }
    },
    mounted() {

    }
  };
</script>

<style scoped>
.user-header{
  top: 0;
  width: 100%;
  position: fixed;
  z-index: 9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  display: flex;
}
.user-aside{
  display: flex;
  height: 82vh;
  margin: 88px 50px 0 50px;
}
.header-title {
  cursor: pointer;
  width: 120px;
}
.header-right {
  display: flex;
  flex: 1;
  justify-content: flex-end;
  align-items: center;
}
  .btn-group{
    height: 82vh;
    display: flex;
    flex-direction: column;
  }
</style>
