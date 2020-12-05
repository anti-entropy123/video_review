<template>
  <div class="file-container">
    <el-row class="search-header">
      <el-col :span="6">
        <span class="project-name">{{ projectName }}</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;共{{this.videoList.length}}个视频</span>
      </el-col>

      <el-col :span="4">
        <el-input prefix-icon="el-icon-search" class="project-search" placeholder="搜索文件"></el-input>
      </el-col>

      <el-col :offset="6" :span="7">
        <div class="user-list">
          <template v-for="(user, index) in userList">
            <div
              class="user-item"
              :key="index"
              :style="`zIndex:${10 - index}`"
              @click="showUserList"
              v-if="index<3"
            >
              <el-tooltip class="item" effect="light" :content="user.userName" placement="bottom  ">
                <el-avatar :src="user.avatar"></el-avatar>
              </el-tooltip>
            </div>
          </template>
          <div
            v-if="userList.length>3"
            class="user-item user-num"
            @click="showUserList"
          >{{ userList.length }}</div>
        </div>
      </el-col>
      <el-col :span="1">
        <el-tooltip effect="light" content="邀请成员" placement="bottom">
          <div class="user-add" @click="inviteUser">
            <i class="fas fa-user-plus"></i>
          </div>
        </el-tooltip>
      </el-col>
    </el-row>
    <div class="file-upload" v-if="showList">
      <!--      <ele-upload-video-->
      <!--        :projectId="projectId"-->
      <!--        :fileSize="20"-->
      <!--        @error="handleUploadError"-->
      <!--        :responseFn="handleResponse"-->
      <!--        :httpRequest="request"-->
      <!--        style="margin: 50px"-->
      <!--        action="http://188.131.227.20:1314/api/video/"-->
      <!--        v-model="video"-->
      <!--      />-->
      <upload-video
        @refreshVideo="getProjectInfo(projectId)"
        class="video-upload"
        :projectId="projectId"
      ></upload-video>
    </div>
    <div v-else class="video-list">
      <upload-video
        @refreshVideo="getProjectInfo(projectId)"
        class="video-upload"
        :projectId="projectId"
      ></upload-video>
      <div v-for="video in videoList" :key="video.videoId" class="video-item">
        <div class="video-cover-div">
          <el-image
            class= "video-cover "
            :src="video.cover"
            fit="cover"
            @click="goMeeting()"
            @mouseover="mouseOver(video.coverList)"
            @mouseleave="mouseLeave(video.coverList)"
          ></el-image>
        </div>

        <div class="video-duration">{{video.duration| timeFormat}}</div>
        <div class="video-description">{{ video.videoName }}</div>
        <div class="video-time">
          {{
          video.createDate | dateFormat
          }}
        </div>
        <el-popover placement="bottom" trigger="click" width="150px">
          <div style="display: flex;flex-direction: column;">
            <!-- <el-button type="text"></el-button>
            <el-button type="text" icon="el-icon-delete">分享</el-button>-->
            <el-button type="text" icon="el-icon-delete" @click="deleteVideo(video,video.videoId)">删除</el-button>
          </div>

          <i class="el-icon-more require-more" slot="reference"></i>
        </el-popover>
      </div>
    </div>
    <el-dialog :title="projectName" :visible.sync="showUserListVisible" width="30%">
      <div class="show-user-list">
        <el-row v-for="user in userList" :key="user.userId">
          <el-col :offset="2" :span="15" class="flex-center">
            <el-avatar style="width: 35px;height: 35px;object-fit: scale-down" :src="user.avatar"></el-avatar>
            <span style="margin-left: 5px">{{ user.userName }}</span>
          </el-col>
          <el-col :span="4" class="flex-center">
            <div>{{ user.title }}</div>
          </el-col>
          <el-col :span="2" class="flex-center">
            <el-popover placement="right" width="100" trigger="click">
              <el-button-group style="display: flex;flex-direction: column">
                <el-button type="text" @click.native="removeUserById(user.userId)">移除成员</el-button>
                <el-button type="text">设为管理员</el-button>
              </el-button-group>

              <el-button
                slot="reference"
                type="text"
                icon="el-icon-more"
                style="transform:rotate(90deg);margin-left: 15px"
              ></el-button>
            </el-popover>
          </el-col>
        </el-row>
      </div>
      <div
        style="height: 32px;line-height: 32px;border: 1px solid #e0e0e0;border-radius: 10px;display: flex;justify-content: center;margin-top: 5px;cursor: pointer"
        @click="inviteUser"
      >邀请更多成员</div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showUserListVisible = false">取 消</el-button>
        <el-button type="primary" @click="showUserListVisible = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="邀请用户"
      :visible.sync="showVisitUserVisible"
      width="30%"
      @close="VisitUserClose"
    >
      <el-form>
        <el-row>
          <el-input placeholder="请输入用户信息" v-model="inviteInput" prefix-icon="el-icon-search">
            <template slot="append">
              <el-button @click="searchUser">搜索</el-button>
            </template>
          </el-input>
        </el-row>
        <div v-if="visitUser.length === 0">未找到指定用户</div>
        <div class="visit-list">
          <el-row type="flex" class="visit-user" v-for="user in visitUser" :key="user.userId">
            <el-col :span="4" class="visit-user-col">
              <el-avatar style="width: 35px;height: 35px;object-fit: scale-down" :src="user.avatar"></el-avatar>
            </el-col>
            <el-col :span="4" class="visit-user-col">
              <span>{{ user.username }}</span>
            </el-col>
            <el-col :offset="2" :span="8" class="visit-user-col">
              <span>{{ user.mobileNum }}</span>
            </el-col>
            <el-col :offset="3" :span="3" class="visit-user-col">
              <el-button @click="inviteUserbyId(user.userId)" type="text">邀请</el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showVisitUserVisible = false">取 消</el-button>
        <el-button type="primary" @click="showUserListVisible = false">邀请</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import UploadVideo from "./UploadVideo";
import EleUploadVideo from "./EleUploadVideo";
import axios from "axios";
export default {
  name: "File",
  components: {
    UploadVideo,
    EleUploadVideo
  },
  props: {
    projectName: String
  },
  data() {
    return {
      dataObj: new FormData(),
      headerobj: {
        Authorization: "Bearer " + window.sessionStorage.getItem("token"),
        "Content-Type": "multipart/form-data"
      },
      video: "",
      imageUrl: "",
      srcList: [],
      userList: [],
      videoList: [],
      visitUser: [],
      //存放封面的数组
      index:[],
      showUserListVisible: false,
      showVisitUserVisible: false,
      showCreateMeetingVisible: false,
      projectId: "",
      inviteInput: "",
      video: null
    };
  },
  methods: {
    async deleteVideo(video,id) {
      const { data: res } = await this.$http
        .delete(`project/${this.projectId}/removeVideo`, {
          params:{
            videoId: id
          }
        })
        .catch(function(error) {
          console.log(error);
        });
      if (res.result === 1) {
        this.videoList = this.videoList.filter(v => {
          return v != video;
        });
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    CreateMeetingClose() {
      this.meeting = {};
    },
    async createMeeting() {
      const { data: res } = await this.$http.post("meeting/", this.meeting);
      if (res.result === 1) {
        this.$message({
          message: "成功创建会议",
          type: "success"
        });
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
      this.showCreateMeetingVisible = false;
    },
    async request(file) {
      this.dataObj.append("videoName", file.name);
      this.dataObj.append("description", file.type);
      this.dataObj.append("permission", "0");
      this.dataObj.append("uploadToProject", this.projectId);
      this.dataObj.append("video", this.video);

      var self = this;
      const { data } = await axios.post(
        "http://188.131.227.20:1314/api/video/",
        this.dataObj,
        {
          headers: self.headerobj
        }
      );
    },

    async getProjectInfo(project) {
      const { data: res } = await this.$http
        .get(`project/${project}/userAndVideo`)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        this.$message({
          message: "获取项目视频列表和用户列表成功",
          type: "success"
        });

        this.videoList = res.data.videoList;
        this.userList = res.data.userList;
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    async searchUser() {
      const { data: res } = await this.$http
        .get("userlist/", {
          params: {
            data: this.inviteInput
          }
        })
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        this.$message({
          message: "获取用户列表成功",
          type: "success"
        });
        this.visitUser = res.data;
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    async inviteUserbyId(id) {
      const { data: res } = await this.$http
        .post(`project/${this.projectId}/inviteUser/`, {
          userId: id,
          word: "我喜欢你"
        })
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        this.$message({
          message: "邀请成功",
          type: "success"
        });
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    async removeUserById(id) {
      const { data: res } = await this.$http
        .delete(`project/${this.projectId}/removeUser`, {
          params: {
            userId: id
          }
        })
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        this.$message({
          message: "邀请成功",
          type: "success"
        });
      } else {
        this.$message({
          message: res.message,
          type: "error"
        });
      }
    },
    showUserList() {
      this.showUserListVisible = true;
    },
    inviteUser() {
      this.showUserListVisible = false;
      this.showVisitUserVisible = true;
      this.searchUser();
    },

    VisitUserClose(done) {
      this.inviteInput = "";
    },
    handleUploadError(error) {
      console.log("error", error);
    },
    handleResponse(response) {},
    mouseOver(cover) {
      console.log("over:" + cover);
    },
    mouseLeave(cover) {
      console.log("leave:" + cover);
    }
  },
  computed: {
    showList() {
      return this.videoList.length === 0;
    }
  },
  mounted() {
    this.token = window.sessionStorage.getItem("token");
    this.projectId = this.$route.params.id;
    console.log(this.projectId);
    this.getProjectInfo(this.projectId);
  },
  updated() {
    if (this.projectId != this.$route.params.id) {
      this.projectId = this.$route.params.id;
      console.log(this.projectId);
      this.getProjectInfo(this.projectId);
    }
  }
};
</script>

<style scoped>
.file-container {
  position: relative;
  height: 100%;
}
/* 文件 header */
.search-header {
  height: 46px;
  line-height: 46px;
  border-bottom: 1px solid #c0c0c0;
}
.project-search {
  width: 180px;
}
.project-name {

  color: rgb(24,128,232);

  font-size: 24px;
}
.user-list {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.user-item {
  margin-right: -10px;
  height: 35px;
  width: 35px;
}
.user-num {
  height: 34px;
  width: 34px;
  border-radius: 50%;
  background-color: rgb(137, 186, 235);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #303030;
}
.el-avatar {
  height: 100%;
  width: 100%;
}
.user-add {
  margin-left: 15px;
  color: rgb(24,128,232);
  margin-top: 2px;
}
.user-add i {
  font-size: 28px;
}

.video-list {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-row-gap: 20px;
  grid-column-gap: 60px;
  padding:20px 50px;
  grid-template-rows: repeat(2, 200px);
}
.video-upload {
  border-radius: 10px;
  border: 2px dashed rgb(124 154 250 / 33%);
  overflow: hidden;
}
.video-item {
  position: relative;
  border-radius: 10px;
  border: 1px solid #333;
  overflow: hidden;
}
.video-item .video-duration {
  position: absolute;
  bottom: 52px;
  right: 0px;
  color: #fff;
  z-index: 9;
  width: 48px;
  text-align: center;
  background-color: #333;
  font-size: 10px;
  opacity: 90%;
}
.video-item .video-cover-div {
  height: 146px;
  width: 280px;
  overflow: hidden;
}
.video-item .video-description {
  height: 44px;
  margin-top: 2px;
  margin-left: 5px;
  white-space: nowrap;
  overflow: hidden;

  text-overflow: ellipsis;
}
.video-time {
  font-size: 9px;
  color: #333;
  position: absolute;
  bottom: 5px;
  left: 5px;
}
.video-cover {
  height: 160px;
  width: 280px;
  cursor: pointer;
  transition: all 0.5s ease-in-out;
}
.video-cover:hover {
  transform: scale(1.1);
}
.require-more {
  transform: rotate(90deg);
  position: absolute;
  right: 10px;
  bottom: 10px;
  cursor: pointer;
}
.file-upload {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.show-user-list {
  display: flex;
  flex-direction: column;
}
.flex-center {
  display: flex;
  height: 40px;
  line-height: 40px;
}
.video-cover {
  cursor: pointer;
}
.visit-list {
  margin-top: 5px;
}
.visit-user {
  margin-bottom: 3px;
}
.visit-user-col {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
