<template>
  <div class="file-container">
    <el-row class="search-header">
      <el-col :span="3">
        <span class="project-name">个人中心</span>
      </el-col>
      <el-col :offset="1" :span="2">
        <span>3项,73.84MB</span>
      </el-col>
      <el-col :offset="1" :span="4">
        <el-input prefix-icon="el-icon-search" class="project-search">
        </el-input>
      </el-col>
      <el-col :span="4" style="display: flex">
        <el-select v-model="value" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <div>
          <i class="el-icon-s-operation"></i>
        </div>
      </el-col>

    </el-row>

    <div class="video-list">
      <el-card
        v-for="(video, index) in videoList"
        :key="video.videoId"
        class="video-item"
      >
        <el-image
          class="video-cover"
          style="width: 270px; height: 150px"
          :src="video.cover[0]"
          :preview-src-list="srcList"
          fit="scale-down"
        >
        </el-image>
        <div class="video-description">{{ video.videoName }}</div>
        <span style="font-size: 9px;color:#333">{{ video.duration }}</span>
        <el-popover
          placement="bottom"
          trigger="click">
          <div style="display: flex;flex-direction: column;">
            <el-button type="text"></el-button>
            <el-button type="text" icon="el-icon-delete">分享</el-button>
            <el-button type="text" icon="el-icon-delete" @click="deleteVideo(video.videoId)">删除</el-button>
          </div>
          <i class="el-icon-more require-more"  slot="reference" ></i>
        </el-popover>
      </el-card>
    </div>
  </div>

</template>

<script>
  import { Message } from "element-ui";

  export default {
    name: "Personal",
    data(){
      return{
          videoList:[]
      }
    },
    methods:{
      async getPersonal(){
        const { data: res } = await this.$http.get(`video/mine/`);
        if (res.result === 1) {
          // this.$message({
          //   message: "获取个人中心",
          //   type: "success"
          // });
          Message.success("获取个人中心")
         this.videoList=res.data
        } else {
          // this.$message({
          //   message: res.message,
          //   type: "error"
          // });
          Message.error("error")
        }
      },
    },
    mounted() {
      this.getPersonal()
    }
  }
</script>

<style scoped>
  .file-container {
    position: relative;
    margin-top:60px
  }
  .search-header {
    height: 38px;
    line-height: 38px;
    border-bottom: 1px solid #c0c0c0;
  }
  .project-search {
    width: 180px;
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
    height: 35px;
    width: 35px;
    border-radius: 50%;
    background-color: #c0c0c0;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #303030;
  }
  .user-item .el-avatar {
    height: 100%;
    width: 100%;
  }
  .user-add {
    font-size: 40px;
    margin-left: 20px;
    color: #c0c0c0;
    margin-top: -3px;
  }
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409eff;
  }

  .video-list {
    width: 100%;

    display: grid;
    grid-template-columns: repeat(4, 25%);
    grid-template-rows: repeat(auto-fill, 250px);
  }
  .video-item {
    margin: 10px;
  }

  .file-upload {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200px;
    height: 200px;
    transform: translate(-50%, -50%);
    border: 1px dashed #8c939d;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .video-list {
    display: grid;
    grid-template-columns: repeat(4, 25%);
    grid-template-rows: repeat(auto-fill, 250px);
  }
  .video-item {
    margin: 10px;
    position: relative;
  }

  .project-name {
    background: linear-gradient(to right, red, blue);
    -webkit-background-clip: text;
    color: transparent;
    -webkit-text-fill-color: transparent;
    text-fill-color: transparent;
  }
  .require-more{
    transform: rotate(90deg);
    position: absolute;
    right:20px;
    cursor: pointer;
  }
</style>
