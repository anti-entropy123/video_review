<template>
  <div class="ele-upload-video">
    <!-- 上传组件 -->
    <el-upload
      :accept="accept"
      action="http://188.131.227.20:1314/api/video/"
      :before-upload="handleBeforeUploadVideo"
      :httpRequest="httpRequest"
      :disabled="videoUploadPercent > 0 && videoUploadPercent < 100"
      :on-error="handleUploadError"
      :on-progress="handleUploadProcess"
      :on-success="handleUploadSuccess"
      :show-file-list="false"
      :withCredentials="withCredentials"
      drag
      v-if="!value"
    >
      <!-- 上传进度 -->
      <el-progress
        :percentage="videoUploadPercent"
        style="margin-top: 20px;"
        type="circle"
        v-if="videoUploadPercent > 0"
      />

      <!-- 上传提示 -->
      <template v-else>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将视频拖到此处，或
          <em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip" v-if="showTip">
          请上传
          <span style="color: #f56c6c;"
          >&nbsp;{{
              this.fileType ? this.fileType.join("/") : "视频"
            }}&nbsp;</span
          >格式文件
          <template v-if="fileSize">
            ，且文件大小不超过
            <span style="color: #f56c6c;">{{ fileSize }}</span
            >&nbsp;MB
          </template>
        </div>
      </template>
    </el-upload>

    <!-- 视频缩略 -->
    <vue-hover-mask v-if="value">
      <video
        :autoplay="false"
        :src="value"
        :style="{
          width: width + 'px',
          height: height ? height + 'px' : 'auto',
        }"
      >
        您的浏览器不支持视频播放
      </video>
      <template v-slot:action>
        <span @click="handlePlayerVideo" class="ele-upload-video_mask__item">
          <i class="el-icon-zoom-in"></i>
        </span>
        <span @click="handleRemove" class="ele-upload-video_mask__item">
          <i class="el-icon-delete"></i>
        </span>
      </template>
    </vue-hover-mask>

    <!-- 弹窗播放 -->
    <el-dialog :visible.sync="isShowVideo" append-to-body>
      <video
        :autoplay="true"
        :src="value"
        controls="controls"
        style="width: 100%;"
        v-if="isShowVideo"
      >
        您的浏览器不支持视频播放
      </video>
    </el-dialog>
  </div>
</template>

<script>
  import VueHoverMask from "vue-hover-mask";
  import axios from "axios";
  import { Message } from "element-ui";
  export default {
    name: "EleUploadVideo",
    components: {
      VueHoverMask,
    },
    props: {
      projectId:String,
      // 值
      value: {
        type: String,
      },
      // 上传地址
      action: {
        type: String,
        required: true,
      },
      // 响应处理函数
      responseFn: Function,
      // 文件大小限制(Mb)
      fileSize: {
        type: Number,
      },
      // 显示宽度(px)
      width: {
        type: Number,
        default: 360,
      },
      // 显示高度(默认auto)
      height: {
        type: Number,
      },
      // 是否显示提示
      isShowTip: {
        type: Boolean,
        default: true,
      },
      // 是否显示上传成功的提示
      isShowSuccessTip: {
        type: Boolean,
        default: true,
      },
      // 文件类型
      fileType: {
        type: Array,
      },
      // 设置上传的请求头部(同官网)
      headers: Object,
      // 支持发送 cookie 凭证信息 (同官网)
      withCredentials: {
        type: Boolean,
        default: false,
      },
      // 上传时附带的额外参数(同官网)
      data: {
        type: Object,
      },

      // 覆盖默认的上传行为，可以自定义上传的实现 (同官网)
      accept: String,
      // 删除前的操作(同官网)
      beforeRemove: Function,
    },
    data() {
      return {
        isShowVideo: false,
        videoUploadPercent: 0,
        dataObj: new FormData(),
        headerobj: {
          Authorization: "Bearer " + window.sessionStorage.getItem("token"),
          "Content-Type": "multipart/form-data"
        }

      };
    },
    computed: {
      // 是否显示提示
      showTip() {
        return this.isShowTip && (this.fileType || this.fileSize);
      },
    },
    methods: {
      // 上传大小和格式检测
      handleBeforeUploadVideo(file) {

        this.dataObj.append("videoName", file.name);
        this.dataObj.append("description", file.type);
        this.dataObj.append("permission", "0");
        this.dataObj.append("uploadToProject", this.projectId);
        this.dataObj.append("video", file);

        // 校检格式
        let isVideo = false;
        if (Array.isArray(this.fileType)) {
          const type = file.type.split("/");
          isVideo = type[0] === "video" && this.fileType.includes(type[1]);
        } else {
          isVideo = file.type.includes("video");
        }

        if (!isVideo) {
          // this.$message.error(`${file.name}格式不正确, 请上传格式正确的视频`);
          Message.error(`${file.name}格式不正确, 请上传格式正确的视频`)
          return false;
        }

        // 校检文件大小
        if (this.fileSize) {
          const isLt = file.size / 1024 / 1024 < this.fileSize;
          if (!isLt) {
            // this.$message.error(`上传视频大小不能超过${this.fileSize}MB哦!`);
            Message.error(`上传视频大小不能超过${this.fileSize}MB哦!`)
            return false;
          }
        }
        return true;
      },

      // 上传进度
      handleUploadProcess(event, file) {
        this.videoUploadPercent = Number(file.percentage.toFixed(0));
      },

      // 上传成功
      handleUploadSuccess(response, file) {
        this.videoUploadPercent = 0;
        if (this.isShowSuccessTip) {
          // this.$message.success("上传成功!");
          Message.success("上传成功!")
        }
        if (this.responseFn) {
          this.$emit("input", this.responseFn(response, file));
        } else {
          this.$emit("input", response);
        }
        this.dataObj=new FormData(),
          this.getProjectInfo(this.projectId)
      },
      async getProjectInfo(project) {
        const { data: res } = await this.$http
          .get(`project/${project}/userAndVideo`)
          .catch(function(error) {
            console.log(error);
          });
        if (res.result == 1) {
       
          // Message.success("获取项目视频列表和用户列表成功");
          this.videoList = res.data.videoList;
          this.userList = res.data.userList;
        } else {
     
          Message.error(res.message)
        }
      },
      // 上传失败
      handleUploadError(err, file, fileList) {
       
        Message.error("上传失败, 请重试!");
        this.videoUploadPercent = 0;
        this.$emit(res.message, err, file, fileList);
      },
      async  httpRequest(file, isVideo, videoDiv) {

        var self = this;
        const { data } = await axios.post(
          "http://188.131.227.20:1314/api/video/",
          this.dataObj,
          {
            headers: self.headerobj
          }
        );
      },

      // 删除视频
      doRemove() {
        this.$emit("delete");
        this.$emit("input", null);
      },

      handleRemove() {
        if (!this.beforeRemove) {
          this.doRemove();
        } else if (typeof this.beforeRemove === "function") {
          const before = this.beforeRemove(this.value);
          if (before && before.then) {
            before.then(
              () => {
                this.doRemove();
              },
              () => {}
            );
          } else if (before !== false) {
            this.doRemove();
          }
        }
      },
      // 播放视频
      handlePlayerVideo() {
        this.isShowVideo = true;
      },
    },
  };
</script>

<style>
  .ele-upload-video_mask__item {
    padding: 0 10px;
  }

  .ele-upload-video .el-upload__tip {
    line-height: 12px;
  }
</style>
