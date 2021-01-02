<template>
  <div>
    <el-card class="userInfo-container">
      <el-form ref="UserForm" :model="userInfo" label-width="80px">
        <el-form-item label="头像" size="medium">
          <el-avatar class="user-avatar" :src="userInfo.avatar"></el-avatar>
          <el-upload
            v-if="!disabled"
            class="upload-demo"
            action=""
            :http-request="request"
            :before-upload="onBeforeUpload"
            accept="image/jpeg, image/gif, image/png, image/jpg"
            :on-success="handleSuccess"
            :on-error="handleError"
            :on-exceed="handleExceed"
          >
            <el-button size="small" type="primary" >点击上传</el-button>
          </el-upload>
        </el-form-item>

        <el-form-item label="姓名">
          <el-input v-model="userInfo.username" :disabled="disabled"></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="userInfo.mobileNum" clearable :disabled="disabled"></el-input>
        </el-form-item>
        <el-form-item label="公司">
          <el-input v-model="userInfo.company" clearable :disabled="disabled"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="info" style="margin-left:80px" @click="changeDisabled">{{ this.disabled ? "修改个人信息" : "确定" }}</el-button>
    </el-card>
  </div>
</template>

<script>
  import { Message } from "element-ui";

  import axios from "axios";
export default {
  name: "UserInfo",
  data() {
    return {
      userInfo: {},
      disabled: true,
      dataObj: new FormData(),
      headerobj: {
        Authorization: "Bearer " + window.localStorage.getItem("token"),
        "Content-Type": "multipart/form-data"
      }
    };
  },
  methods: {
    async request(file) {
      console.log(file.file);

      const { data: res } = await axios.post(
        "https://api.video-review.top:1314/api/uploadImg/",
        this.dataObj,
        {
          headers: this.headerobj
        }
      );
      if (res.result === 1) {
          this.userInfo.avatar = res.data.url;
          this.dataObj= new FormData();
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    handleSuccess() {
      console.log("success");
    },
    handleError(e) {

      console.log("error");
    },

    onBeforeUpload(file) {
      this.dataObj.append("image", file);

      const isIMAGE =
        file.type === "image/jpeg" || "image/gif" || "image/png" || "image/jpg";
      const isLt1M = file.size / 1024 / 1024 < 1;

      if (!isIMAGE) {
        // this.$message.error("上传文件只能是图片格式!");
        Message.error("上传文件只能是图片格式!")
      }
      if (!isLt1M) {
        // this.$message.error("上传文件大小不能超过 1MB!");
        Message.error("上传文件大小不能超过 1MB!")
      }
      return isIMAGE && isLt1M;
    },
    changeDisabled() {
      if (!this.disabled) {
        this.changeInfo();
      }
      this.disabled = !this.disabled;
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      // this.$message.warning(
      //   `当前限制选择 1 个文件，本次选择了 ${
      //     files.length
      //   } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      // );
      Message.warning( `当前限制选择 1 个文件，本次选择了 ${
        files.length
      } 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    async getInfo() {
      let userId = window.localStorage.getItem("userId");

      const { data: res } = await this.$http.get(`user/${userId}`);
      if (res.result === 1) {
        // this.$message({
        //   message: "获取个人信息成功",
        //   type: "success"
        // });
        Message.success("获取个人信息成功");
        this.userInfo = res.data;
        console.log(this.userInfo)
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error");
      }
    },
    async changeInfo() {
      const { data: res } = await this.$http.post("userInfo/", this.userInfo);
      console.log(res);
    }
  },
  mounted() {
    this.getInfo();
  }
};
</script>

<style scoped>
.el-header {
  top: 0;
  width: 100%;
  background-color: #fff;
  position: fixed;
  z-index: 9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  display: flex;
}
.userInfo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 20px;
  height: 82vh;
  width: 60vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.user-avatar {
}
</style>
