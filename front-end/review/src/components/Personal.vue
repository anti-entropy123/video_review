<template>
  <div class="file-container">
    <div class="search-header">
      <span class="project-name">{{projectName}}</span>

      <span>3项,73.84MB</span>
      <el-input
        prefix-icon="el-icon-search"
        class="project-search"
      >
      </el-input>
      <el-select v-model="value" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <div>
        <i class="el-icon-s-operation"></i>
      </div>
    </div>
    <div class="file-upload" v-if="showList">
      <el-upload
        class="avatar-uploader"
        action="https://jsonplaceholder.typicode.com/posts/"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">上传文件</div>
      </el-upload>
    </div>
    <div v-else class="video-list">
      <upload-video class="video-item" :projectId="projectId">
      </upload-video>
      <el-card v-for="(video,index) in list" :key="index" class="video-item">
        <el-image  style="width:  270px; height: 150px"
                   :src="video.cover[0]"
                   :preview-src-list="srcList"
        >
        </el-image>
        <div class="video-description">{{video.videoName}}</div>
        <span>{{video.createDate}}</span>
      </el-card>
    </div>
  </div>
</template>

<script>
  import UploadVideo from "./UploadVideo";
  import SearchHeader from "./SearchHeader";

  export default {
    name: "Personal",
    components: {
      UploadVideo,
      SearchHeader,
    },
    props: {
      list: Array,
      projectId:String,
      projectName:String,
    },
    data() {
      return {
        imageUrl: "",
        srcList:[],
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        value: ''

      };
    },
    methods: {
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === "image/jpeg";
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error("上传头像图片只能是 JPG 格式!");
        }
        if (!isLt2M) {
          this.$message.error("上传头像图片大小不能超过 2MB!");
        }
        return isJPG && isLt2M;
      }
    },
    computed: {
      showList() {
        return this.list.length === 0;
      }
    }
  };
</script>

<style scoped>
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
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  .file-container {
    position: relative;
    height: 100%;
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
  }
  .search-header{
    display: flex;
  }
  .project-search{
    width: 150px;
  }
  .project-name{
    flex: 1;
  }
</style>
