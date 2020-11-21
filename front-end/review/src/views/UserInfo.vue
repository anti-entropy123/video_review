<template>
  <div  >
    <!-- <el-header>帧秒分</el-header> -->
    <el-card class="userInfo-container">

      <el-form ref="UserForm" :model="userInfo" label-width="80px">
        <el-form-item label="头像" size="medium">
          <el-avatar
            class="user-avatar"
            :src="userInfo.avatar"
          ></el-avatar>
        </el-form-item>
        <el-form-item label="上传头像">
          <el-upload
            class="upload-demo"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="userInfo.username" :disabled="disabled"></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input
            v-model="userInfo.mobileNum"
            clearable
            :disabled="disabled"
          ></el-input>
        </el-form-item>
        <el-form-item label="公司">
          <el-input
            v-model="userInfo.company"
            clearable
            :disabled="disabled"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button type="info" @click="changeDisabled">
        {{ this.disabled ? "修改个人信息" : "确定" }}</el-button
      >
    </el-card>
  </div>

</template>

<script>
    export default {
        name: "UserInfo",
      data() {
        return {
          userInfo: {},
          disabled: true,
          fileList: [
            {
              name: "food.jpeg",
              url:"https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100"
            }
          ]
        };
      },
      methods: {
        changeDisabled() {
          if(!this.disabled){
            this.changeInfo()
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
          this.$message.warning(
            `当前限制选择 1 个文件，本次选择了 ${
              files.length
            } 个文件，共选择了 ${files.length + fileList.length} 个文件`
          );
        },
        beforeRemove(file, fileList) {
          return this.$confirm(`确定移除 ${file.name}？`);
        },
        async getInfo() {
          let userId = window.sessionStorage.getItem("userId");
          console.log(userId)
          const { data: res } = await this.$http.get(`user/${userId}`);
          if (res.result === 1) {
            this.$message({
              message: "获取个人信息成功",
              type: "success"
            });
            this.userInfo = res.data;
          } else {
            this.$message({
              message: res.message,
              type: "error"
            });
          }
        },
        async changeInfo(){
          const { data: res } = await this.$http.post("userInfo/",this.userInfo);
          console.log(res)
        }
      },
      mounted() {
        this.getInfo();
      }
    }
</script>

<style scoped>
  .el-header{
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
    height: 500px;
    width: 380px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
  }
  .user-avatar {
    height: 100%;
    width: 100%;
  }
</style>
