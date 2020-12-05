<template>
<el-row class="adm-container">
  <el-col :span="17">
    <el-image :src="imgSrc" ></el-image>
  </el-col>
  <el-col :span="7" class="login-box">
    <div>帧秒分后台</div>
          <el-form
        ref="LoginFormRef"
        :model="loginForm"
        label-width="0"
        :rules="LoginFormRules"
        class="login-form"
      >
            <el-form-item prop="mobileNum">
              <el-input
                v-model="loginForm.mobileNum"
                prefix-icon="el-icon-phone"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                prefix-icon="el-icon-lock"
                type="password"
              ></el-input>
            </el-form-item>
            <el-form-item class="btns">
              <el-button type="primary" @click="login">登录</el-button>
            </el-form-item>


      </el-form>
  </el-col>
</el-row>
</template>

<script>
    export default {
        name: "AdminLogin",
      data(){
          return {
            imgSrc:"../../../static/images/people-in-couch-1024248.jpg",
                loginForm: {
          mobileNum: "18502616338",
          password: "123",
        },
                  LoginFormRules: {
          mobileNum: [
            { required: true, message: "请输入用户名", trigger: "blur" }
          ],
          password: [
            { required: true, message: "请输入密码", trigger: "blur" },
            {
              min: 3,
              max: 15,
              message: "密码长度在6 到 15 个字符",
              trigger: "blur"
            }
          ]
        }
          }
      },
      methods:{
        async login() {
          // 通过调用validate 对表单进行校验
          // requestLogin( this.loginForm).then(data =>{
          //   console.log(data)
          // })

          this.$refs["LoginFormRef"].validate(async valid => {

            if (valid) {
              const { data: res } = await this.$http.post("/admin/login/", this.loginForm);
              console.log(res);
              if (res.result === 1) {
                this.$message({
                  message: "登录成功",
                  type: "success"
                });
                // 将登录成功之后的toen,保存到客户端的sessionStorage 中
                window.sessionStorage.setItem("adm-token", res.token);

                this.$router.push("/admin");
              } else {
                this.$message({
                  message: res.message,
                  type: "error"
                });
              }
            } else {
              return false;
            }
          });
        },
      }
    }
</script>

<style scoped>
.adm-container{
  width:100vw;
  height:100vh;
  overflow: hidden;
}
.el-image{
  height:100%;
}
.login-box{
  height: 100%;
  display:flex;
  flex-direction: column;
  align-items: center;
  margin-top:15%
}
</style>
