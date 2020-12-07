<template>
  <div class="admin-container">
    <input type="checkbox" id="check" />
    <label for="check">
      <i class="fa fa-bars" aria-hidden="true" id="show"></i>
      <i class="fa fa-times" aria-hidden="true" id="cancel"></i>
    </label>
    <div class="siderbar">
      <header>
        <h1 class="title" @click="goHome">帧秒分</h1>
      </header>
      <ul class="menu-list">
        <li>
          <div @click="userManage">
            <i class="fa fa-paper-plane"></i>用户管理
          </div>
        </li>
        <li>
          <div @click="videoManage">
            <i class="fa fa-paper-plane"></i>视频管理
          </div>
        </li>
        <li>
          <div @click="projectManage">
            <i class="fa fa-paper-plane"></i>项目管理
          </div>
        </li>
        <li>
          <div @click="meetingManage">
            <i class="fa fa-paper-plane"></i>会议管理
          </div>
        </li>
        <li>
          <div @click="roleManage">
            <i class="fa fa-paper-plane"></i>权限管理
          </div>
        </li>
        <li>
          <div @click="viewManage">
            <i class="fa fa-paper-plane"></i>视图管理
          </div>
        </li>
      </ul>
    </div>
    <section class="section-main">
      <div class="main">
        <router-view></router-view>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "Admin",
  data() {
    return {};
  },
  methods: {
    goHome() {
      this.$router.push("/");
    },
    userManage() {
      if (this.$route.path != "/admin/userManage") {
        console.log(1);
        this.$router.push("/admin/userManage");
      }
    },
    videoManage() {
      if (this.$route.path != "/admin/videoManage") {
        console.log(1);
        this.$router.push("/admin/videoManage");
      }
    },
    projectManage() {
      if (this.$route.path != "/admin/projectManage") {
        this.$router.push("/admin/projectManage");
      }
    },
    meetingManage() {
      if (this.$route.path != "/admin/meetingManage") {
        this.$router.push("/admin/meetingManage");
      }
    },
    roleManage() {
      if (this.$route.path != "/admin/roleManage") {
        this.$router.push("/admin/roleManage");
      }
    },
    viewManage() {
      if (this.$route.path != "/admin/viewManage") {
        this.$router.push("/admin/viewManage");
      }
    }
  }
};
</script>

<style scoped>
.admin-container {
  height: 100vh;
}
ul {
  list-style: none;
}

.siderbar {
  position: fixed;
  width: 250px;
  height: 100%;
  top: 0;
  left: -250px;
  background-color: #042331;
  transition: all 0.5s;
  z-index: 998;
}

.title {
  margin: 0;
  width: 100%;
  height: 100px;
  line-height: 100px;
  text-align: center;
  user-select: none;
  font-size: 30px;
  color: #fff;
  background-color: #063146;
  border-bottom: 1px solid black;
}
.menu-list {
  overflow: hidden;
}
.siderbar ul div {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 60px;
  box-sizing: border-box;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid black;
  color: #aaa;
  text-decoration: none;
  font-size: 18px;
  transition: all 0.5s;
  cursor: pointer;
}
.siderbar li div i {
  margin-right: 20px;
}
.siderbar ul div:hover {
  margin-left: 10px;
  color: #eee;
}
#check {
  display: none;
}
#show {
  background-color: #063146;
  color: #aaa;
  width: 24px;
  height: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;

  padding: 5px;
  position: fixed;
  top: 20px;
  left: 20px;
  transition: all 0.5s;
  cursor: pointer;
  z-index: 997;
}
#cancel {
  background-color: #042331;
  color: #aaa;
  width: 20px;
  height: 20px;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2px;
  position: fixed;
  top: 43px;
  left: -40px;
  z-index: 999;
  cursor: pointer;
  transition: all 0.5s;
}
#show:hover,
#cancel:hover {
  color: #eee;
}
#show::before,
#cancel::before {
  line-height: 20px;
}
#check:checked ~ .siderbar {
  left: 0px;
}
#check:checked ~ label #cancel {
  left: 210px;
}
.admin-container .section-main {
  background: url("../../static/images/people-in-couch-1024248.jpg") repeat
    center;
  background-color: #c0c0c0;
  -webkit-background-size: cover;
  background-size: cover;
  z-index: 1;
  transition: all 0.5s;
  height: 100vh;

  box-sizing: border-box;
}
#check:checked ~ .section-main {
  margin-left: 250px;
}
.main {
  padding: 0px 20px;
  border-radius: 20px;
  box-sizing: border-box;
  overflow: auto;
  -ms-overflow-style: none;
}
</style>
