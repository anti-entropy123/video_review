<template>
  <el-container class="home-container">
    <!--    <home-header @goUserInfo="handleUserInfo"></home-header>-->
    <el-header class="home-header">
      <div class="header-title">帧秒分</div>
      <div class="header-right">
        <el-badge :value="12" style="font-size:10px;">
          <i class="el-icon-message-solid" style="font-size:26px" @click="goMessage"></i>
        </el-badge>
        <div class="header-user" @click="goUserInfo">
          <el-avatar size="small" :src="userInfo.avatar"></el-avatar>
          <div class="user-name">{{ userInfo.name }}</div>
        </div>
      </div>
    </el-header>
    <el-container style="margin-top: 60px">
      <el-aside class="home-aside" width="160px">
        <div class="aside-header">
          <template v-if="!searchProject">
            <div class="aside-project">
              <i class="el-icon-s-tools"></i>项目群组
            </div>
            <el-tooltip class="item" effect="light" content="搜索项目" placement="top-start">
              <i class="el-icon-search" @click="searchProject=true"></i>
            </el-tooltip>
          </template>
          <template v-else>
            <el-input class="search-input" v-model="searchInput" placeholder="搜索项目"></el-input>
            <i class="el-icon-close" @click="searchProject=false"></i>
          </template>
          <el-tooltip class="item" effect="light" content="创建项目" placement="top-start">
            <i class="el-icon-plus" @click="addProjectVisible=true"></i>
          </el-tooltip>
        </div>
        <div class="project-list">
          <div
            v-for="(project,index) in projectList"
            :key="index"
            class="project-item"
            @click="changeProject(project.projectId);projectName=project.projectName"
          >{{project.projectName}}</div>
        </div>
        <div class="user-space">
          <el-button type="info" @click="goPersonal" >个人空间</el-button>

        </div>
      </el-aside>
      <el-container>
        <el-header v-if="!isUserInfo">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="文件" name="file"></el-tab-pane>
            <el-tab-pane label="分享" name="share"></el-tab-pane>
            <el-tab-pane label="回收站" name="recycle"></el-tab-pane>
          </el-tabs>
          <div class="user-list" >
            <div
              class="user-item"
              v-for="(user,index) in userList"
              :key="index"
              :style="`zIndex:${10-index}`"
              @click="showUserList"
            >
              <el-avatar style="width:100%;height:100%" :src="user.avatar"></el-avatar>
            </div>
            <div class="user-item user-num" @click="showUserList">{{userList.length}}</div>
            <el-tooltip class="item" effect="light" content="邀请成员" placement="bottom">
              <div class="user-add" @click="inviteUser">
                <i class="el-icon-circle-plus"></i>
              </div>
            </el-tooltip>
          </div>
        </el-header>
        <el-main class="content-wrap">
          <router-view :active="isActive" :list="list" :projectId="currentProjectId" :projectName="projectName" ></router-view>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog
      title="创建项目"
      :visible.sync="addProjectVisible"
      width="30%"
      :before-close="AddProjectClose"
    >
      <el-form ref="addProjectFormRef" :model="addProjectForm" label-width="80px">
        <el-form-item label="项目名称">
          <el-input v-model="addProjectForm.projectName"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addProjectVisible = false">取 消</el-button>
        <el-button type="primary" @click="addProject">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="项目名字"
      :visible.sync="showUserListVisible"
      width="30%"
      :before-close="AddProjectClose"
    >
      <div class="show-user-list">
        <div v-for="user in userList" :key="user.userId" class="show-user-item">
          <div>
          <el-avatar :src="user.avatar"></el-avatar>
          <div>{{user.userName}}
           </div>
         </div>
          <div>{{user.title}}</div>
          <i class="el-icon-more" style="transform：rotate(90deg);"></i>
      </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showUserListVisible = false">取 消</el-button>
        <el-button type="primary" @click="showUserListVisible=false">确 定</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
import HomeHeader from "../components/HomeHeader";
export default {
  name: "Home",
  components: {
    HomeHeader
  },
  data() {
    return {
      isActive:true,
      searchInput: "",
      searchProject: true,
      addProjectVisible: false,
      showUserListVisible:false,
      projectName:'',
      addProjectForm: {
        projectName: ""
      },
      activeName: "file",
      userInfo: {
        name: "rlj",
        avatar:
          "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
      },
      projectList: [],
      userList: [
      ],
      currentProjectId: "",
      list: []
    };
  },
  methods: {
    goUserInfo() {
      this.$router.push("/userInfo");
    },
    handleClick(tab, event) {
      let path = "/" + this.activeName;
      console.log(path);
      this.$router.push(path);
    },
    goMessage() {
      this.$router.push("/message");
    },
    changeProject (project) {
      if(this.$route.path!='/'){
         this.$router.push('/')
      }
      this.currentProjectId = project;
         this.getProjectInfo(project);
      this.activeName='file'
    },
    AddProjectClose(done) {
      this.$confirm("确认关闭？")
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    async addProject() {
      this.addProjectVisible = false;
      const { data: res } = await this.$http.post(
        `project/`,
        this.addProjectForm
      ).catch(function(error){
        console.log(error);
      }
      );
      if (res.result == 1) {
        this.$message({
          message: "项目创建成功",
          type: "success"
        });
        console.log(res);
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    async getProjectInfo(project) {
      const { data: res } = await this.$http.get(
        `project/${project}/userAndVideo`
      ).catch(function(error){
        console.log(error);
      }
      );
      if (res.result == 1) {
        this.$message({
          message: "获取项目视频列表和用户列表成功",
          type: "success"
        });

        this.list = res.data.videoList;
        this.userList = res.data.userList;

      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    async getProjects() {
      const { data: res } = await this.$http.get(`projects`).catch(function(error){
        console.log(error);
      }
      );;
      if (res.result == 1) {
        this.$message({
          message: "获取项目列表成功",
          type: "success"
        });

        this.projectList = res.data;


      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    showUserList(){
      this.showUserListVisible=true
    },
    inviteUser(){

    },
    goPersonal(){
      if(this.$route.path!='/personal'){
        this.$router.push('/personal')
      }
    }
  },
  computed: {
    isUserInfo() {
      return (
        this.$route.path === "/userInfo" || this.$route.path === "/message"
      );
    }
  },
  mounted() {
        this.getProjects();
        if(this.projectList.length!=0){
        this.currentProjectId = this.projectList[0].projectId
        console.log(this.currentProjectId)
        this.getProjectInfo(this.currentProjectId)
    }

  }
};
</script>
<style scoped>
.home-container {
  min-height: 100vh;
}
.home-header {
  top: 0;
  width: 100%;
  background-color: #fff;

  position: fixed;
  z-index: 9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  display: flex;
}
.header-title {
  display: flex;
  justify-content: center;
  line-height: 60px;
  font-size: 20px;
}
.header-right {
  display: flex;
  flex: 1;
  justify-content: flex-end;
  align-items: center;
}
.header-user {
  margin-left: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.user-image {
  border-radius: 50%;
  overflow: hidden;
  height: 30px;
  width: 30px;
}

.home-aside {
  display: flex;
  flex-direction: column;
  height: 90vh;
  margin-left: 5px;
}
.aside-header {
  display: flex;
  align-items: center;
  height: 36px;
}
.aside-project {
  flex: 1;
}
.project-list {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.project-item {
  height: 32px;
  line-height: 32px;
  width: 100%;
  border-bottom: 1px solid  #e7e6e6;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  text-align: center;
  padding: 0 5px 0 5px;
}
.project-item:hover {
  background-color: #e7e6e6;
}
.user-space {
  margin-bottom: 20px;
  align-self: center;
}
.content-wrap {
  margin-top: -35px;
}
.search-input >>> .el-input__inner {
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 0px;
  border: 0px;
  width: 100%;
  padding-left: 0;
  height: 18px;
  border-bottom: 1px solid #409eff;
}
.user-list {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: -52px;
}

.user-item {
  margin-right: -10px;
  height: 35px;
  width: 35px;
}
.user-num {
  border-radius: 50%;
  background-color: #c0c0c0;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}
.user-add {
  border-radius: 50%;

  font-size: 35px;
  margin-left: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
  .show-user-list{
    display: flex;
    flex-direction: column;
  }
  .show-user-item{
    display: flex;
    justify-content: space-around;
  }
</style>
