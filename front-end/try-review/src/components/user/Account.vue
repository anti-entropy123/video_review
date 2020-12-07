<template>
  <div style="display: flex;flex-direction: column; align-items: center;margin-top: 100px">
    <el-card style="width: 640px">
      <div>账号安全</div>
      <el-form
        ref="accountFormRef"
        :model="accountForm"
        label-width="80px"
        style="margin-left: 100px; width: 400px"
        label-suffix=":"
      >
        <el-form-item label="手机号">
          <el-input v-model="accountForm.mobileNum" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="登陆密码">
          <el-input v-model="accountForm.password" :disabled="pwddisable"
          show-password
          >
            <el-button slot="append" @click="changePasswordVisible=true">修改</el-button>
          </el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="accountForm.mail" :disabled="true"></el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog title="修改密码" :visible.sync="changePasswordVisible" width="40%">
      <el-form-item label="手机号">
          <el-input v-model="password.mobileNum" :disabled="true"></el-input>
        </el-form-item>
      <el-form :model="password">
        <el-form-item label="验证码">
          <el-input v-model="password.checkcode">
            <el-button slot="append" @click="getCode">获取验证码</el-button>
          </el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password.password"></el-input>
        </el-form-item>
        <el-form-item label="密码确认">
          <el-input v-model="password.checkPassword"></el-input>
        </el-form-item>
        <el-button type="primary" @click="changePassword">确定</el-button>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import { Message } from "element-ui";

  export default {
  name: "Account",
  data() {
    return {
      accountForm: {
        mobileNum: "",
        password: "123456",
        mail: "1535045887@qq.com"
      },
      password: {
        mobileNum: "",
        password: "",
        checkPassword: "",
        checkcode:''
      },
      pwddisable: true,
      changePasswordVisible: false
    };
  },
  methods: {
    changePassword() {
         const { data: res } = this.$http.post("user/resetPassword/", {
          params: this.password
        });
        if(res.result===1){
          this.accountForm.password=res.data
        }
        else{
             // this.$message({
             //    message: res.message,
             //    type: "error"
             //  });
            Message.error("error");
        }
    },
    getCode() {

        const { data: res } = this.$http.get("checkCode", {
          params: this.accountForm
        });
    }
  },
  mounted() {
    this.accountForm.mobileNum = window.localStorage.getItem('mobileNum')
    this.accountForm.mobileNum = window.localStorage.getItem('mobileNum')
  }
};
</script>

<style scoped>
</style>
