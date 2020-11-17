<template>
  <el-card >
        <div class="upload-box">
          <el-upload
            class="video-upload"
            action="http://188.131.227.20:1314/api/video/"
            :http-request="request"
            :on-progress="uploadVideoProcess"
            :on-success="handleVideoSuccess"
            :before-upload="beforeUploadVideo"
            :withCredentials="true"
            :show-file-list="false"
            multiple
          >
            <video
              v-if="videoForm.showVideoPath !='' && !videoFlag"
              v-bind:src="videoForm.showVideoPath"
              class="avatar video-avatar"
              controls="controls"
            >您的浏览器不支持视频播放</video>
            <i
              v-else-if="videoForm.showVideoPath =='' && !videoFlag"
              class="el-icon-plus upload-icon"
            ></i>
            <el-progress
              v-if="videoFlag == true"
              type="circle"
              v-bind:percentage="videoUploadPercent"
              style="margin-top:7px;"
            ></el-progress>
          </el-upload>
        </div>

    <p class="Upload_pictures">
      <span></span>
      <span>最多可以上传1个视频，建议大小50M，推荐格式mp4</span>
    </p>
  </el-card>
</template>

<script>
import axios from "axios";
export default {
  name: "UploadVideo",
  props:{
    projectId:String,
  },
  data() {
    return {
      videoFlag: false,
      //是否显示进度条
      videoUploadPercent: "",
      //进度条的进度，
      isShowUploadVideo: false,
      //显示上传按钮
      videoForm: {
        showVideoPath: ""
      },
      dataObj: new FormData(),
      headerobj: {
        Authorization: "Bearer " + window.sessionStorage.getItem("token"),
        "Content-Type": "multipart/form-data"
      }
    };
  },
  methods: {
    async request(file, isVideo, videoDiv) {

      var self = this;
      const { data } = await axios.post(
        "http://188.131.227.20:1314/api/video/",
        this.dataObj,
        {
          headers: self.headerobj
        }
      );
    },
    //上传前回调
    beforeUploadVideo(file) {
      console.log(file);
      this.dataObj.append("videoName", file.name);
      this.dataObj.append("description", file.type);
      this.dataObj.append("permission", "0");
      this.dataObj.append("uploadToProject", this.projectId);
      this.dataObj.append("video", file);

      var fileSize = file.size / 1024 / 1024 < 50;
      if (
        [
          "video/mp4",
          "video/ogg",
          "video/flv",
          "video/avi",
          "video/wmv",
          "video/rmvb",
          "video/mov"
        ].indexOf(file.type) == -1
      ) {
        return false;
      }
      if (!fileSize) {
        return false;
      }
      this.isShowUploadVideo = false;
    },
    //进度条
    uploadVideoProcess(event, file, fileList) {
      this.videoFlag = true;
      this.videoUploadPercent = file.percentage.toFixed(0) * 1;
    },
    //上传成功回调
    handleVideoSuccess(res, file) {
      this.isShowUploadVideo = true;
      this.videoFlag = false;
      this.videoUploadPercent = 0;

      //前台上传地址
      //if (file.status == 'success' ) {
      //    this.videoForm.showVideoPath = file.url;
      //} else {
      //     layer.msg("上传失败，请重新上传");
      //}

      //后台上传地址
      // if (res.Code == 0) {
      //   this.videoForm.showVideoPath = res.Data;
      // } else {
      //   // layer.msg(res.Message);
      // }
    }
  }
};
</script>

<style scoped>
.upload-box{
  border: 1px solid #c0c0c0;
  display: flex;
  justify-content: center;

}
.upload-icon{
font-size: 100px;
color: #ccc;
}
</style>
