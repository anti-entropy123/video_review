<template>
  <el-container class="home-container" v-drag>
    <el-header class="home-header">
      <el-image
        class="header-title"
        src="../../static/images/logo.png"
        @click="goWelcome"
      ></el-image>
      <h1 class="header-title2" @click="goWelcome">视频审阅平台</h1>
      <div class="header-right">
        <el-popover placement="bottom-start" width="250" trigger="click">
          <div class="message-list">
            <h2 style="font-size:16px">消息</h2>
            <div class="divider"></div>
            <el-row
              v-for="message in messageList.slice(0, 3)"
              :key="message.messageId"
              class="message-item"
              @click.native="handleRead(message.messageId)"
            >
              <el-col :span="6">
                <el-avatar :src="message.avatar"></el-avatar>
              </el-col>
              <el-col :span="18">
                <div class="message-content">
                  {{ message.sentence }}
                  <span class="message-time">{{
                    message.date | dataFilter
                  }}</span>
                </div>
                <div class="message-handle">
                  <div v-if="message.hasProcess === 1 || message.type != 3">
                    已处理
                  </div>
                  <div v-if="message.hasProcess === 0 && message.type === 3">
                    <el-button
                      @click="
                        pocessVisit(message.messageId, message.projectId, 1)
                      "
                      size="mini"
                      plain
                      >同意</el-button
                    >
                    <el-button
                      size="mini"
                      type="danger"
                      @click="
                        pocessVisit(message.messageId, message.projectId, 0)
                      "
                      plain
                      >拒绝</el-button
                    >
                  </div>
                </div>
              </el-col>
              <div
                class="message-item-isread"
                v-if="message.hasRead === 0"
              ></div>
            </el-row>
            <template v-if="showMore">
              <el-row
                v-for="message in messageList.slice(3, messageListLength)"
                :key="message.messageId"
                class="message-item"
                @click="handleRead(message.messageId)"
              >
                <el-col :span="6">
                  <el-avatar :src="message.avatar"></el-avatar>
                </el-col>
                <el-col :span="18">
                  <div class="message-content">
                    {{ message.fromName }}{{ message.type | messageType }}
                    <span class="message-time">{{
                      message.date | dataFilter
                    }}</span>
                  </div>
                  <div class="message-handle">
                    <div v-if="message.hasProcess === 1 || message.type != 3">
                      已处理
                    </div>
                    <div v-if="message.hasProcess === 0 && message.type === 3">
                      <button
                        class="agree-btn"
                        @click.stop="pocessVisit(message.messageId, 1)"
                      >
                        同意
                      </button>
                      <button
                        class="refuse-btn"
                        type="danger"
                        @click.stop="
                          pocessVisit(message.messageId, message.projectId, 0)
                        "
                      >
                        拒绝
                      </button>
                    </div>
                  </div>
                </el-col>
                <div
                  class="message-item-isread"
                  v-if="message.hasRead === 0"
                ></div>
              </el-row>
            </template>
            <div class="divider"></div>
            <div
              v-if="messageListLength > 3 && !showMore"
              class="get-more"
              @click="showMore = true"
            >
              显示更多
            </div>
          </div>

          <i
            class="el-icon-message-solid message-icon"
            style="font-size:28px;color:#333"
            slot="reference"
          >
            <div class="not-read" v-show="userInfo.messageToRead > 0">
              {{ userInfo.messageToRead }}
            </div>
          </i>
        </el-popover>

        <el-tooltip
          class="item"
          effect="light"
          :content="userInfo.username"
          placement="bottom"
        >
          <div class="header-user" @click="goUserInfo">
            <el-avatar size="medium" :src="userInfo.avatar"></el-avatar>
          </div>
        </el-tooltip>
      </div>
    </el-header>
    <el-container style="margin-top: 60px">
      <el-aside class="home-aside" width="240px">
        <div class="aside-header">
          <template v-if="!searchProject">
            <div class="aside-project">
              <i class="fas fa-list"></i> 项目群组
            </div>
            <el-tooltip
              class="item"
              effect="light"
              content="搜索项目"
              placement="top-start"
            >
              <i
                class="el-icon-search"
                style="  cursor: pointer;"
                @click="searchProject = true"
              ></i>
            </el-tooltip>
          </template>
          <template v-else>
            <el-input
              class="search-input"
              v-model="searchInput"
              placeholder="搜索项目"
              @keyup.enter="search"
            ></el-input>
            <i class="el-icon-close" @click="searchProject = false"></i>
          </template>
        </div>
        <el-divider></el-divider>
        <div class="project-list">
          <div class="project-add" @click="addProjectVisible = true">
            <i class="icon"></i>
            <span>新建项目</span>
          </div>
          <div
            v-for="(project, index) in projectList"
            :key="index"
            :class="[
              'project-item',
              activeIndex === index ? 'project-item-active' : ''
            ]"
            @click="changeProject(project, index)"
          >
            <div class="project-name">
              <i class="fas fa-cube" style="margin-right:4px; "></i>
              {{ project.projectName }}
              <el-popover placement="right" trigger="hover">
                <div class="btns" style="display: flex;flex-direction: column;">
                  <!-- <el-button type="text"></el-button> -->
                  <!-- <el-button
                    type="text"
                    icon="el-icon-delete"
                    @click="exitProject(project)"
                  >退出项目</el-button>-->
                  <el-button
                    type="text"
                    icon="el-icon-delete"
                    @click="deleteProject(project.projectId)"
                    >删除项目</el-button
                  >
                </div>
                <i slot="reference" class="el-icon-more project-more"></i>
              </el-popover>
            </div>
          </div>
        </div>
        <el-divider></el-divider>
        <div class="user-space">
          <el-button type="info" @click="goPersonal">个人空间</el-button>
        </div>
      </el-aside>

      <el-container>
        <el-header class="container-header">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="文件" name="file"></el-tab-pane>
            <el-tab-pane label="会议" name="meeting"></el-tab-pane>
            <el-tab-pane label="回收站" name="recycle"></el-tab-pane>
          </el-tabs>
        </el-header>
        <el-main class="content-wrap">
          <router-view
            :active="isActive"
            :projectName="projectName"
          ></router-view>
        </el-main>
      </el-container>
    </el-container>

    <el-dialog
      title="创建项目"
      :visible.sync="addProjectVisible"
      width="30%"
      @close="AddProjectClose"
    >
      <el-form
        ref="addProjectFormRef"
        :model="addProjectForm"
        label-width="80px"
      >
        <el-form-item label="项目名称">
          <el-input v-model="addProjectForm.projectName"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addProjectVisible = false">取 消</el-button>
        <el-button type="primary" @click="addProject">确 定</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
import { Message } from "element-ui";

export default {
  name: "Home",
  data() {
    return {
      activeIndex: 0,
      isActive: true,
      searchInput: "",
      searchProject: false,
      addProjectVisible: false,
      projectName: "",
      addProjectForm: {
        projectName: ""
      },
      messageList: [],
      activeName: "file",
      userInfo: {},
      projectList: [],
      currentProjectId: "",
      showMore: false
    };
  },
  methods: {
    goUserInfo() {
      this.$router.push("/user/userInfo");
    },

    goPersonal() {
      this.$router.push("/user");
    },
    goWelcome() {
      this.$router.push("/welcome");
    },
    handleClick(tab, event) {
      let projectId = window.sessionStorage.getItem("projectId");
      let path = "/" + this.activeName + "/" + projectId;
      this.$router.push(path);
    },
    async getMessageList() {
      const { data: res } = await this.$http.get("messages/");
      if (res.result === 1) {
        this.messageList = res.data;
      } else {
       
        Message.error(res.message);
      }
    },
    async pocessVisit(messageId, projectId, n) {
      let isAgree = n === 1;
      console.log(isAgree);
      const { data: res } = await this.$http.post(
        `project/${projectId}/join/`,
        {
          isAgree,
          messageId: messageId
        }
      );
      if (res.result === 1) {
        this.getProjects();
      } else {
  
        Message.error(res.message);
      }
    },

    changeProject(project, index) {
      window.sessionStorage.setItem("projectId", project.projectId);
      this.activeIndex = index;
      this.projectName = project.projectName;
      this.currentProjectId = project.projectId;

      console.log("test" + this.currentProjectId);
      this.activeName = "file";
      this.$router.replace(`/file/${this.currentProjectId}`);
    },
    AddProjectClose() {
      this.addProjectForm = {};
    },
    async getInfo() {
      let userId = window.localStorage.getItem("userId");
      const { data: res } = await this.$http.get(`user/${userId}`);
      if (res.result === 1) {
        this.userInfo = res.data;
      } else {
  
        Message.error(res.message);
      }
    },

    async addProject() {
      this.addProjectVisible = false;
      const { data: res } = await this.$http
        .post(`project/`, this.addProjectForm)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        this.getProjects();
        let _this = this;
        setTimeout(function() {
          console.log(_this.projectList);
          _this.activeIndex = _this.projectList.length - 1;
          _this.changeProject(
            _this.projectList[_this.activeIndex],
            _this.activeIndex
          );
        }, 300);
      } else {
    
        Message.error(res.message);
      }
    },
    async getProjects() {
      const { data: res } = await this.$http
        .get(`projects`)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        console.log("test1");

        this.projectList = res.data;
      } else {

        Message.error(res.message);
      }
    },
    async exitProject(id) {
      console.log(id + "exit");
      this.projectList = this.projectList.filter(project => {
        return id != project;
      });
      const { data: res } = await this.$http
        .post(`project/${id}/leave`)
        .catch(function(error) {
          console.log(error);
        });
    },
    async deleteProject(id) {
      console.log(id + "delete");
      // this.projectList = this.projectList.filter(project=>{
      //   return id!=project
      // })
      const { data: res } = await this.$http
        .post(`project/${id}/leave`)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result === 1) {
        this.init();
      }
    },
    init() {
      this.getProjects();
      let _this = this;
      setTimeout(function() {
        if (_this.projectList.length != 0) {
          _this.currentProjectId = _this.projectList[0].projectId;
          _this.projectName = _this.projectList[0].projectName;
          _this.$router.push(`/file/${_this.currentProjectId}`);
        }
      }, 300);

      if (window.localStorage.getItem("userId")) {
        this.getInfo();
      }
    },
    async handleRead(id) {
      const { data: res } = await this.$http
        .get(`message/${id}`)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result === 1) {
        this.getMessageList();
      }
    }
  },
  computed: {
    messageListLength() {
      return this.messageList.length;
    }
  },
  mounted() {
    this.getProjects();
    this.getMessageList();
    this.activeIndex = 0;
    let _this = this;
    setTimeout(function() {
      if (_this.projectList.length != 0) {
        _this.currentProjectId = _this.projectList[0].projectId;
        window.sessionStorage.setItem("projectId", _this.currentProjectId);
        _this.projectName = _this.projectList[0].projectName;
        _this.$router.push(`/file/${_this.currentProjectId}`);
      }
    }, 100);

    if (window.localStorage.getItem("userId")) {
      this.getInfo();
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
  position: fixed;
  z-index: 9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
}
.header-title {
  cursor: pointer;
  height: 46px;
  width: 100px;
}
.header-title2 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 28px;
  cursor: pointer;
}
.header-right {
  display: flex;
  flex: 1;
  justify-content: flex-end;
  align-items: center;
}
.message-icon {
  position: relative;
  cursor: pointer;
}
.header-user {
  margin-left: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
/* 侧边栏 */
.home-aside {
  display: flex;
  flex-direction: column;
  height: 90vh;
  margin-left: 5px;
  border-right: 1px solid #dfdfdf;
}
.aside-header {
  margin: 15px 0 -20px 18px;
  display: flex;
  align-items: center;
  height: 56px;
}
.aside-project {
  flex: 1;
  font-size: 20px;
}
.aside-project i {
  font-size: 18px;
}
.el-icon-search,
.el-icon-close {
  font-size: 16px;
  margin-right: 16px;
}
.project-list {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.project-add {
  margin: -16px 40px 10px 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 42px;
  border-radius: 25px;
  width: 120px;
  background-color: #fff;
  border: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 1s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.project-add:hover {
  margin-left: 35px;
}
.project-add .icon {
  display: inline-block;
  height: 15px;
  width: 15px;
  background-size: 25px 25px;
  background-image: url("../../static/images/addProject.png");
  background-position: center;
  margin-right: 4px;
}
.project-add span {
  font-size: 16px;
  color: #333;
}

.project-item {
  height: 42px;
  line-height: 42px;
  width: 100%;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 5px 0 20px;
  transition: all 0.5s;
  position: relative;
}
.project-more {
  position: absolute;
  right: 2px;
  top: 14px;
  transform: rotate(90deg);

  opacity: 0;
}
.project-item:hover .project-more {
  opacity: 1;
}
.btns .el-button--text {
  color: #333;
}
.project-item-active {
  background-color: rgb(228, 241, 255);
}
.project-item-active .project-name {
  color: rgb(45, 145, 245);
}
.project-name {
  color: #333333;
  transition: all 0.1s;
}

.project-item:hover {
  background-color: rgba(228, 241, 255, 0.589);
}
.project-item:hover .project-name {
  color: rgb(45, 145, 245);
}
.user-space {
  margin-bottom: 20px;
  align-self: center;
}
.container-header {
  margin-top: 23px;
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
.message-list {
  height: 380px;
  overflow-y: auto;
}
.message-item {
  height: 100px;
  position: relative;
}
.message-item-isread {
  height: 8px;
  width: 8px;
  border-radius: 50%;
  background-color: red;
  position: absolute;
  top: -8px;
  right: 0px;
}
.message-content {
  height: 50px;
  position: relative;
  cursor: pointer;
}
.message-time {
  position: absolute;
  bottom: 0;
  right: 0;
  font-size: 8px;
}

.get-more {
  width: 100%;
  text-align: center;
  cursor: pointer;
}
.divider {
  width: 100%;
  height: 1px;
  border: 1px solid #f0f0f0;
  margin: 4px 0 12px 0;
}

.not-read {
  position: absolute;
  top: -5px;
  right: -5px;
  height: 14px;
  width: 14px;
  background-color: red;
  border-radius: 50%;
  font-size: 9px;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
