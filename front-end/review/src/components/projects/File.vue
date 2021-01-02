<template>
  <div class="file-container">
    <el-row class="search-header">
      <el-col :span="6">
        <span v-if="projectName" class="project-name">{{ projectName }}</span>
        <span v-else class="project-name">
          名称未加载出来
        </span> 
      </el-col>
      <el-col :span="2">
        <span> 共{{ this.videoList.length }}个视频</span>
      </el-col>
      <el-col :span="4">
        <el-input
          prefix-icon="el-icon-search"
          class="project-search"
          placeholder="搜索文件"
        ></el-input>
      </el-col>

      <el-col :offset="4" :span="7">
        <div class="user-list">
          <template v-for="(user, index) in userList">
            <div
              class="user-item"
              :key="index"
              :style="`zIndex:${10 - index}`"
              @click="showUserList"
              v-if="index < 3"
            >
              <el-tooltip
                class="item"
                effect="light"
                :content="user.userName"
                placement="bottom  "
              >
                <el-avatar :src="user.avatar"></el-avatar>
              </el-tooltip>
            </div>
          </template>
          <div
            v-if="userList.length > 3"
            class="user-item user-num"
            @click="showUserList"
          >
            {{ userList.length }}
          </div>
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
      
      <div class="video-upload-else" @click="uploadVisible = true">
        <i class="el-icon-plus upload-icon pointer"></i>
        <p class="Upload_pictures">
          <span style="color:rgb(134, 161, 236);font-size:24px;cursor:pointer"
            >点击上传</span
          >
        </p>
      </div>
 
    </div>
    <div v-else class="video-list">
      <div class="video-upload">
        <upload-video :projectId="projectId"></upload-video>
      </div>
      <div class="video-upload" @click="uploadVisible = true">
        <i class="el-icon-plus upload-icon pointer"></i>
        <p class="Upload_pictures">
          <span style="color:rgb(134, 161, 236);font-size:24px;cursor:pointer"
            >点击上传</span
          >
        </p>
      </div>
      <div
        v-for="(video, index) in videoList"
        :key="video.videoId"
        class="video-item"
        ref="vv"
        @mousemove="updateXY"
      >
        <div
          class="video-cover-div"
          @mouseover="mousein(video.coverList, index)"
          @click="goReviewOffline(video.videoId)"
        >
          <el-image
            class="video-cover"
            :src="video.cover"
            fit="contain"
          ></el-image>
        </div>

        <div class="video-duration">{{ video.duration | timeFormat }}</div>
        <div class="video-description">
          {{ video.videoName | videoNameFormat }}
        </div>
        <div class="video-time">
          {{ (video.createDate * 1000) | dateFormat }}
        </div>
        <el-popover placement="bottom" trigger="click" width="150px">
          <div style="display: flex;flex-direction: column;">
            <!-- <el-button type="text"></el-button>
            <el-button type="text" icon="el-icon-delete">分享</el-button>-->
            <el-button
              type="text"
              icon="el-icon-delete"
              @click="deleteVideo(video, video.videoId)"
              >删除</el-button
            >
          </div>

          <i class="el-icon-more require-more" slot="reference"></i>
        </el-popover>
      </div>
    </div>
    <el-dialog
      :title="projectName"
      :visible.sync="showUserListVisible"
      width="30%"
    >
      <div class="show-user-list">
        <el-row v-for="user in userList" :key="user.userId">
          <el-col :offset="2" :span="15" class="flex-center">
            <el-avatar
              style="width: 35px;height: 35px;object-fit: scale-down"
              :src="user.avatar"
            ></el-avatar>
            <span style="margin-left: 5px">{{ user.userName }}</span>
          </el-col>
          <el-col :span="4" class="flex-center">
            <div>{{ user.title }}</div>
          </el-col>
          <el-col :span="2" class="flex-center">
            <el-popover placement="right" width="100" trigger="click">
              <el-button-group style="display: flex;flex-direction: column">
                <el-button
                  type="text"
                  @click.native="removeUserById(user.userId)"
                  >移除成员</el-button
                >
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
      >
        邀请更多成员
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showUserListVisible = false">取 消</el-button>
        <el-button type="primary" @click="showUserListVisible = false"
          >确 定</el-button
        >
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
          <el-input
            placeholder="请输入用户信息"
            v-model="inviteInput"
            prefix-icon="el-icon-search"
            @keyup.enter.native="searchUser"
          >
            <template slot="append">
              <el-button @click="searchUser">搜索</el-button>
            </template>
          </el-input>
        </el-row>
        <div v-if="visitUser.length === 0">未找到指定用户</div>
        <div class="visit-list">
          <el-row
            type="flex"
            class="visit-user"
            v-for="user in visitUser"
            :key="user.userId"
          >
            <el-col :span="4" class="visit-user-col">
              <el-avatar
                style="width: 35px;height: 35px;object-fit: scale-down"
                :src="user.avatar"
              ></el-avatar>
            </el-col>
            <el-col :span="4" class="visit-user-col">
              <span>{{ user.username }}</span>
            </el-col>
            <el-col :offset="2" :span="8" class="visit-user-col">
              <span>{{ user.mobileNum }}</span>
            </el-col>
            <el-col :offset="3" :span="3" class="visit-user-col">
              <el-button @click="inviteUserbyId(user.userId)" type="text"
                >邀请</el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showVisitUserVisible = false">取 消</el-button>
        <el-button type="primary" @click="showUserListVisible = false"
          >邀请</el-button
        >
      </span>
    </el-dialog>
    <el-dialog
      title="添加视频"
      :visible.sync="uploadVisible"
      width="500px"
      @close="handleUploadClose"
    >
      <el-form
        :model="addForm"
        v-loading="loading"
        ref="addFormRef"
        label-width="100px"
         
      >
          <el-form-item label="项目Id">
          <el-input v-model="addForm.uploadToProject" disabled> </el-input>
        </el-form-item>
       <el-form-item label="视频上传">
          <div>
            <div class="no-submit bg-block">
              点击上传视频
              <form action="/" enctype="multipart/form-data" method="post">
                <input
                  class="card-input"
                  type="file"
                  name="file"
                  placeholder="file"
                  @change="uploadFile($event)"
                />
              </form>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="视频名称">
          <el-input v-model="addForm.videoName"> </el-input>
        </el-form-item>
        <el-form-item label="视频描述">
          <el-input v-model="addForm.description"> </el-input>
        </el-form-item>
    
       
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click.native="uploadVisible = false">取消上传</el-button>
        <el-button type="primary" @click.native="uploadVideo()">点击上传</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import UploadVideo from "./UploadVideo";

import axios from "axios";
import { Message } from "element-ui";

export default {
  name: "File",
  components: {
    UploadVideo
  },
  props: {
    projectName: String
  },
  data() {
    return {
      addForm: {
        videoName: "",
        description: "",
        uploadToProject: "",
        permission: 0
      },

      loading: false,
      uploadVisible: false,

      video: "",
      imageUrl: "",
      srcList: [],
      userList: [],
      videoList: [],
      visitUser: [],
      //存放封面的数组
      index: [],
      showUserListVisible: false,
      showVisitUserVisible: false,
      showCreateMeetingVisible: false,
      projectId: "",
      inviteInput: "",
      // video: null
      x: 0,
      coverList: [],
      videoNum: 0,
      left: 0,
      right: 0,
      //上传
      param: new FormData(),
      config: {
        headers: {
          Authorization: "Bearer " + window.sessionStorage.getItem("token"),
          "Content-Type": "multipart/form-data"
        }
      }
    };
  },
  methods: {
    handleUploadClose(){
      this.addForm.videoName=''
      this.addForm.description=''
      this.params = new DataForm()
    },
    uploadFile(event) {
      let file = event.target.files[0];
      console.log('视频信息看这里')
      console.log(file);
      this.addForm.videoName = file.name.substring(0,file.name.length-4)
      let fileType = file.name
        .substring(file.name.lastIndexOf(".")   + 1)
        .toLowerCase();
      if (fileType !== "mp4" && fileType !== "mkv") {
        this.$message({
          type: "warning",
          message: "视频格式不符合规定"
        });
        return;
      }
      if (file.size > 1024 * 1024 * 100) {
        this.$message({
          type: "warning",
          message: "上传视频过大"
        });
        return;
      }
      console.log(file)
      this.param.append("video", file);
    },
    uploadVideo() {
      this.param.append("videoName", this.addForm.videoName);
      this.param.append("description", this.addForm.description);
      this.param.append("uploadToProject", this.addForm.uploadToProject);
      this.param.append("permission", this.addForm.permission);
      let _this = this;
      _this.loading = true;
      this.$http
        .post("/video/", _this.param, _this.config)
        .then(res => {
          console.log(res);
          _this.loading = false;
          _this.uploadVisible = false;
          _this.getProjectInfo(this.projectId)
        })
        .catch(() => {});
    },
    goReviewOffline(videoId) {
      this.$router.push({
        path: "/reviewOffline",
        query: {
          videoId: videoId,
          projectId: this.projectId
        }
      });
    },
    updateXY: function(event) {
      this.x = event.offsetX;
      // console.log(this.x);
      let coverLength = this.coverList.length;
      let coverNum = Math.floor(
        (this.x / (this.right - this.left)) * coverLength
      );
      // console.log(this.right - this.left);
      // console.log(coverNum);
      // console.log(this.coverList[coverNum]);
      // videolist [index] 这一项cover赋值
      let img = new Image();
      img.src = this.coverList[coverNum];
      let that = this;
      img.onload = function() {
        that.videoList[that.videoNum].cover = that.coverList[coverNum];
      };
    },
    mousein(coverList, index) {
      this.left = this.$refs.vv[index].getBoundingClientRect().left;
      this.right = this.$refs.vv[index].getBoundingClientRect().right;
      this.coverList = coverList;
      this.videoNum = index;
      // console.log(left);
      // console.log(right);
      // 获取x 坐标
      // console.log(coverNum);
      // console.log(coverList[coverNum])
      //videolist [index] 这一项
      // coverList[coverNum];
      // console.log(coverList);
    },
    async deleteVideo(video, id) {
      const { data: res } = await this.$http
        .delete(`project/${this.projectId}/removeVideo`, {
          params: {
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
        Message.error(res.message);
      }
    },
    CreateMeetingClose() {
      this.meeting = {};
    },
    async createMeeting() {
      const { data: res } = await this.$http.post("meeting/", this.meeting);
      if (res.result === 1) {
        Message.success("成功创建会议");
      } else {
        Message.error(res.message);
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
        "https://api.video-review.top:1314/api/video/",
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
        this.videoList = res.data.videoList;
        console.log(this.videoList);
        this.userList = res.data.userList;
      } else {
        Message.error(res.message);
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
        this.visitUser = res.data;
        let userlist = this.userList;
        console.log(userlist);
        userlist.forEach(user => {
          this.visitUser = this.visitUser.filter(v => {
            return v.userId != user.userId;
          });
        });
      } else {
        Message.error(res.message);
      }
    },
    async inviteUserbyId(id) {
      const { data: res } = await this.$http
        .post(`project/${this.projectId}/inviteUser/`, {
          userId: id,
          word: "info"
        })
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        Message.success("用户邀请成功");
      } else {
        Message.error(res.message);
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
        Message.success("用户删除成功");
      } else {
        Message.error(res.message);
      }
    },
    showUserList() {
      this.showUserListVisible = true;
    },
    inviteUser() {
      this.showUserListVisible = false;
      this.showVisitUserVisible = true;
      // this.searchUser();
    },

    VisitUserClose(done) {
      this.inviteInput = "";
      this.visitUser = [];
    },
    handleUploadError(error) {
      Message.error(error);
    },
    handleResponse(response) {}
  },
  computed: {
    showList() {
      return this.videoList.length === 0;
    }
  },
  mounted() {
    this.projectId = this.$route.params.id;
    this.addForm.uploadToProject = this.projectId;
    if (this.projectId != 0) {
      this.getProjectInfo(this.projectId);
    } else {
      Message.warning("点击项目,获取项目信息");
    }
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
  color: #409eff;

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
  color: rgb(137, 186, 235);
  margin-top: 2px;
}
.user-add i {
  font-size: 28px;
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
.video-list {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-row-gap: 20px;
  grid-column-gap: 60px;
  padding: 20px 50px;
  grid-template-rows: repeat(2, 180px);
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
  opacity: 0.9;
}
.video-item .video-cover-div {
  height: 126px;
  width: 100%;
  overflow: hidden;
  background-color: #454545;
}
.video-cover {
  width: 100%;
  height: 100%;
  cursor: pointer;
  transition: all 0.5s ease-in-out;
}
.video-item .video-description {
  height: 44px;
  margin-top: 2px;
  margin-left: 5px;
  white-space: nowrap;
  overflow: hidden;
  font-size: 16px;
  text-overflow: ellipsis;
}
.video-time {
  font-size: 9px;
  color: #333;
  position: absolute;
  bottom: 5px;
  left: 5px;
}

/*.video-cover:hover {*/
/*  transform: scale(1.1);*/
/*}*/
.require-more {
  transform: rotate(90deg);
  position: absolute;
  right: 10px;
  bottom: 10px;
  cursor: pointer;
  

}
.video-upload {
  border-radius: 10px;
  padding: 1em;
  background-image: url("../../../static/images/border.png");
  background-size: 100% 100%;
  overflow: hidden;
   display: flex;
    flex-direction: column;
    align-items: center;
   overflow: hidden;
}
.video-upload-else {
  padding: 35px 0 15px 0;
  width: 350px;
  height: 250px;
  border-radius: 10px;
  background-image: url("../../../static/images/border.png");
  background-size: 100% 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload-icon {
  font-size: 100px;
  color: rgb(134, 161, 236);
}
.Upload_pictures {
  margin-top: 10px;
  font-weight: bold;
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

/* 上传视频 */
.no-submit {
  position: relative;
  width: 150px;
  text-align: center;
}
.bg-card {
  width: 150px;
  display: flex;
  align-items: flex-end;
}
.bg-block {
  border-radius: 4px;
  border: 1.5px dashed #00a0e9;
  padding: 30px 0;
  font-size: 13px;
  color: #00a0e9;
}
.card-input {
  cursor: pointer;
  font-size: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  outline: none;
  background-color: transparent;
  opacity: 0;
}
</style>
