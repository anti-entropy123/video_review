<template>
  <div class="meeting-container">
    <el-header style="position: relative">

      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
 <el-tab-pane label="我的会议" name="mine">
          <div class="meeting-list">
            <div class="meeting-title">我的会议</div>
            <el-divider></el-divider>
            <div
              v-for="meeting in mineMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
              @click="enterMeeting(meeting.meetingId)"
            >
              <h3 class="meeting-name">{{meeting.meetingName}}</h3>
              <div class="meeting-long">会议时长:{{meeting.duration |dataFilter2}}</div>
              <div class="meeting-owner">发起人:{{meeting.userName}}</div>
              <div class="meeting-time">
                <div>开始时间:{{meeting.time|dateFormat}}</div>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="历史会议" name="history">
          <div class="meeting-list">
            <div class="meeting-title">历史会议</div>
            <el-divider></el-divider>
            <div
              v-for="meeting in historyMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
              @click="enterMeeting(meeting.meetingId)"
            >
              <h3 class="meeting-name">{{meeting.title}}</h3>
              <div class="meeting-long">会议时长:{{meeting.endTime-meeting.startTime |dataFilter2}}</div>
              <div class="meeting-owner">发起人:{{meeting.ownerName}}</div>
              <div class="meeting-time">
                <div style="margin-right:10px">开始时间:{{meeting.startTime|dateFormat}}</div>
                <div>结束时间:{{meeting.endTime|dateFormat}}</div>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="待办列表" name="todo">
          <div class="meeting-list">
            <div class="meeting-title">待办列表</div>
            <el-divider></el-divider>
            <div
              v-for="meeting in todoMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
              @click="enterMeeting(meeting.meetingId)"
            >
              <h3 class="meeting-name">{{meeting.title}}</h3>
              <div class="meeting-long">会议时长:{{meeting.endTime-meeting.startTime |dataFilter2}}</div>
              <div class="meeting-owner">发起人:{{meeting.userName}}</div>
              <div class="meeting-time">
                <div style="margin-right:10px">开始时间:{{meeting.startTime|dateFormat}}</div>
                <div>结束时间:{{meeting.endTime|dateFormat}}</div>
              </div>
            </div>
          </div>
        </el-tab-pane>

      </el-tabs>

      <el-input
        placeholder="查找会议"
        v-model="meetingInput"
        prefix-icon="el-icon-search"
        class="search-meeting"
      >
        <el-button slot="append" @click="searchMeeting">搜索</el-button>
      </el-input>

    </el-header>
  </div>
</template>

<script>
  import { Message } from "element-ui";

  export default {
  name: "MyMeeting",
  data() {
    return {
      todoMeetingList: [],
      meetingList: [],
      historyMeetingList: [],
      mineMeetingList: [],
      activeName: "mine",
      meetingInput: "",
      projectId: "",
      showCreateMeetingVisible: false,
      meeting: {
        title: "前端代码整合",
        belongTo: "",
        startTime: "",
        endTime: "",
        note: "太难了"
      }
    };
  },
  methods: {

    async searchMeeting() {
      const { data: res } = await this.$http
        .post(`meeting/search/`, {
          linkNum: this.meetingInput
        })
        .catch(function(error) {
          console.log(error);
        });

      if (res.result == 1) {
        this.meetingList = res.data.meetingList;
        console.log(res);
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async getMeetingByName(name) {
      switch (name) {
        case "todo":
          this.getTodoMeeting();
          break;
        case "mine":
          this.getMineMeeting();
          break;
        case "history":
          this.getHistoryMeeting();
          break;
      }
    },
    async getTodoMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/todo`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.todoMeetingList = res.data.meetingList;
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async getHistoryMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/history`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.histroyMeetingList = res.data;
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async getMineMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/mine`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.mineMeetingList = res.data.meetingList;
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async enterMeeting(id) {
      //路由跳转
    },
    handleClick(tab, event) {
      this.getMeetingByName(tab.name);
    },
  },
  mounted() {
    this.token = window.localStorage.getItem("token");
     this.getMeetingByName(this.activeName);
  }
};
</script>

<style scoped>
.meeting-container{
  margin-top:80px;
}
.meeting-list {
  width: 80%;
  display: flex;
  flex-direction: column;
  margin-left: 10%;
}
.meeting-title {
  background-color: rgba(34, 103, 253, 0.39);
  height: 42px;
  margin-bottom: -10px;
  line-height: 42px;
  font-size: 18px;
  padding-left: 10px;
  border-radius: 6px;
}
.meeting-item {
  width: 100%;
  position: relative;
  height: 80px;
  padding: 10px;
  background-color: rgba(0, 59, 252, 0.062);
  margin-bottom: 10px;
  border-radius: 6px;
}
.meeting-name {
  position: absolute;
  top: 10px;
  left: 25px;
  font-size: 16px;
}
.meeting-owner {
  position: absolute;
  bottom: 16px;
  left: 50px;
}
.meeting-long {
  position: absolute;
  top: 10px;
  right: 20px;
}
.meeting-time {
  display: flex;
  position: absolute;
  bottom: 10px;
  right: 20px;
}
.search-meeting {
  width: 300px;
  position: absolute;
  top: 2px;
  left: 450px;
}
.create-meeting {
  position: absolute;
  left: 780px;
  top: 2px;
}
</style>
