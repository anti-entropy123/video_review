<template>
  <div class="file-container">
       <div class="video-list">
      <div v-for="video in videoList" :key="video.videoId" class="video-item">
        <div class="video-cover-div">
          <el-image
            class="video-cover"
            :src="video.cover[0]"
            fit="cover"
            @click="goMeeting()"
            @mouseover="mouseOver(video.coverList)"
            @mouseleave="mouseLeave(video.coverList)"
          ></el-image>
        </div>

        <div class="video-duration">{{video.duration| timeFormat}}</div>
        <div class="video-description">{{ video.videoName|videoNameFormat }}</div>
        <div class="video-time">
          {{
          video.createDate | dateFormat
          }}
        </div>
        <el-popover placement="bottom" trigger="click" width="150px">
          <div style="display: flex;flex-direction: column;">
            <!-- <el-button type="text"></el-button>
            <el-button type="text" icon="el-icon-delete">分享</el-button>-->
            <el-button
              type="text"
              icon="el-icon-delete"
              @click="deleteVideo(video,video.videoId)"
            >删除</el-button>
          </div>

          <i class="el-icon-more require-more" slot="reference"></i>
        </el-popover>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "MyVideo",
    data(){
      return{
          video: "",
      imageUrl: "",
      srcList: [],

      videoList: [],
      //存放封面的数组
      index: [],
      video: null
      }
    },
    methods:{
      async getPersonal(){
        const { data: res } = await this.$http.get(`video/mine/`);
        if (res.result === 1) {

         this.videoList=res.data
        } else {

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
  height: 82vh;
  margin-top:80px;
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
  color: rgb(24, 128, 232);
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
  padding: 20px 50px;
  grid-template-rows: repeat(2, 200px);
}
.video-upload {
  border-radius: 10px;
  border: 2px dashed rgb(124 154 250 / 33%);
  overflow: hidden;
}
.video-upload-else{
  padding:15px 0;
  width: 350px;
  height: 250px;
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
