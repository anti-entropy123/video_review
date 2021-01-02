<template>
  <div class="login-container">
    <el-card class="login-box" v-if="loginOrRegister">
      <!-- 头像 -->
      <div class="avatar-box">
        <img :src="logo" alt="" />
      </div>
      <!-- 表单 -->
      <el-form
        ref="LoginFormRef"
        :model="loginForm"
        label-width="0"
        :rules="LoginFormRules"
        class="login-form"
      >
        <el-tabs
          v-model="activeIndex"
          :before-leave="beforeTabLeave"
          :tab-position="'top'"
          @tab-click="tabClicked"
          class="login-tabs"
        >
          <el-tab-pane label="账号密码登陆" name="0">
            <el-form-item prop="mobileNum">
              <el-input
                v-model="loginForm.mobileNum"
                prefix-icon="el-icon-phone"
                @blur="getUserAvatar"
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
              <el-button type="info" @click="resetLoginForm">重置</el-button>
              <el-button type="info" @click="goRegister">注册</el-button>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="手机号登陆" name="1">
            <el-form-item prop="mobileNum">
              <el-input
                v-model="loginForm.mobileNum"
                prefix-icon="el-icon-phone"
                @blur="getUserAvatar"
              ></el-input>
            </el-form-item>
            <el-form-item prop="checkcode">
              <el-input
                v-model="loginForm.checkcode"
                prefix-icon="el-icon-lock"
              >
                <el-button slot="append" @click="getCheckcode('login')">
                  获取验证码</el-button
                ></el-input
              >
            </el-form-item>
            <el-form-item class="btns">
              <el-button type="primary" @click="login">登录</el-button>
              <el-button type="info" @click="resetLoginForm">重置</el-button>
              <el-button type="info" @click="goRegister">注册</el-button>
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
    <el-card class="register-box" v-else>
      <div
        style="
cursor:pointer;"
        @click="goLogin"
      >
        <i class="el-icon-arrow-left"></i>登陆
      </div>
      <!-- <div class="avatar-box">
        <img :src="logo" alt="" />
      </div> -->
      <el-form
        ref="RegisterFormRef"
        :model="registerForm"
        status-icon
        label-width="100px"
        :rules="RegisterFormRules"
        class="login-form"
      >
        <el-form-item label="账号" prop="username">
          <el-input
            v-model="registerForm.username"
            prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            prefix-icon="el-icon-lock"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPassword">
          <el-input
            v-model="registerForm.checkPassword"
            prefix-icon="el-icon-lock"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="mobileNum">
          <el-input
            v-model="registerForm.mobileNum"
            prefix-icon="el-icon-phone"
          ></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="checkCode">
          <el-input v-model="registerForm.checkCode" prefix-icon="el-icon-lock">
            <el-button slot="append" @click="getRegistercheckcode('register')"
              >获取验证码</el-button
            >
          </el-input>
        </el-form-item>
        <el-form-item class="register-btn">
          <el-button type="primary" @click="register">注册</el-button>
          <el-button type="info" @click="resetRegisterForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { requestLogin } from "../api/api";
import { Message } from "element-ui";

export default {
  name: "Login",
  data() {
    var validateCheckPassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registerForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    var checkPhone = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("手机号不能为空"));
      } else {
        const reg = /^1[3|4|5|7|8][0-9]\d{8}$/;
        console.log(reg.test(value));
        if (reg.test(value)) {
          callback();
        } else {
          return callback(new Error("请输入正确的手机号"));
        }
      }
    };
    return {
      loginOrRegister: true,
      activeIndex: "1",
      //18502616338 123
      loginForm: {
        mobileNum: "",
        password: "",
        checkcode: "",
      },
      registerForm: {
        username: "",
        password: "",
        checkPassword: "",
        mobileNum: "",
        checkCode: ""
      },
      RegisterFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { min: 3, max: 10, message: "长度在3 到 10 个字符", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "密码长度在6 到 15 个字符",
            trigger: "blur"
          }
        ],
        checkPassword: [
          { required: true, validator: validateCheckPassword, trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "密码长度在6 到 15 个字符",
            trigger: "blur"
          }
        ],
        mobileNum: [{ required: true, validator: checkPhone, trigger: "blur" }],
        checkCode: [{ required: true, trigger: "blur" }]
      },
      LoginFormRules: {
        mobileNum: [{ required: true, validator: checkPhone, trigger: "blur" }]
        // password: [
        //   { required: true, message: "请输入密码", trigger: "blur" },
        //   {
        //     min: 3,
        //     max: 15,
        //     message: "密码长度在6 到 15 个字符",
        //     trigger: "blur"
        //   }
        // ]
      },
      logo: ""
    };
  },
  methods: {
    async getUserAvatar() {
      const { data: res } = await this.$http.get(`userAvatar`, {
        params: {
          mobileNum: this.loginForm.mobileNum
        }
      });
      if (res.result === 1) {
        this.logo = res.data.avatarUrl;
      } else {
        Message.error(res.message);
      }
    },
    resetRegisterForm() {
      this.$refs.RegisterFormRef.resetFields();
    },
    resetLoginForm() {
      // 通过ref获取表单, resetFields重置表单
      this.$refs.LoginFormRef.resetFields();
    },
    async login() {
      // 通过调用validate 对表单进行校验
      // requestLogin( this.loginForm).then(data =>{
      //   console.log(data)
      // })

      this.$refs["LoginFormRef"].validate(async valid => {
        if (valid) {
    
          const { data: res } = await this.$http.post("login/", this.loginForm);
          console.log(res);
          this.resetLoginForm();
          if (res.result === 1) {
            // this.$message({
            //   message: "登录成功",
            //   type: "success"
            // });
            Message.success("登录成功");
            // 将登录成功之后的toen,保存到客户端的sessionStorage 中
            window.localStorage.setItem("token", res.token);
            window.localStorage.setItem("userId", res.userId);
            window.localStorage.setItem("mobileNum", this.loginForm.mobileNum);
            this.$router.push("/");
          } else {
            // this.$message({
            //   message: res.message,
            //   type: "error"
            // });
            Message.error("error");
          }
        } else {
          return false;
        }
      });
    },
    register() {
      this.$refs["RegisterFormRef"].validate(async valid => {
        if (valid) {
          const { data: res } = await this.$http.post(
            "register/",
            this.registerForm
          );
          this.resetRegisterForm();
          console.log(res);
          if (res.result === 1) {
            // this.$message({
            //   message: "注册成功",
            //   type: "success"
            // });
            Message.success("注册成功");
            this.loginOrRegister = true;
            this.loginForm.mobileNum = this.registerForm.mobileNum;
          } else {
            // this.$message({
            //   message: res.message,
            //   type: "error"
            // });
            Message.error("error");
          }
        } else {
          return false;
        }
      });
    },
    goRegister() {
      this.loginOrRegister = false;
    },
    tabClicked() {
      if (this.activeIndex ==='1'){
        this.loginForm.password=''
      }
    },
    beforeTabLeave(activeName, oldActiveName) {
      console.log(activeName, oldActiveName);
    },
    getCheckcode(operation) {
      let params = {
        mobileNum:this.loginForm.mobileNum,
        operation:operation
      }
        
      const { data: res } = this.$http.get("checkCode", {
        params: parmas
      });
    },
    getRegistercheckcode(operation) {
      let parmas = {
        mobileNum:this.registerForm.mobileNum,
        operation:operation
      };
      const { data: res } = this.$http.get("checkCode", {
        params: parmas
      });
    },
    goLogin() {
      this.loginOrRegister = true;
    }
  },
  mounted() {
    this.getUserAvatar();
  }
};
</script>

<style scoped>
.login-container {
  background-color: #e1e8fa;
  height: 100vh;
}
.el-card {
  overflow: unset;
}
.el-form-item {
  margin-right: 45px;
}
.login-box {
  width: 450px;
  height: 320px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.register-box {
  width: 450px;
  height: 450px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.avatar-box {
  width: 110px;
  height: 110px;
  border: 1px solid #eee;
  border-radius: 50%;
  padding: 10px;
  box-shadow: 0 0 10px #ddd;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
}
.avatar-box img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #eee;
}
.login-form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
</style>
