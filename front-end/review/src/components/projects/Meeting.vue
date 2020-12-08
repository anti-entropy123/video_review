<template>
  <div>
    <el-header style="position: relative;margin-top:20px">
      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
        <el-tab-pane label="全部会议" name="first">
          <div class="meeting-list">
            <div class="meeting-title">会议列表</div>
            <div class="meeting-divider"></div>

            <el-row
              v-for="meeting in meetingList"
              :key="meeting.meetingId"
              class="meeting-item"
            >
              <el-col :span="2"
                ><el-image
                  class="meeting-icon"
                  src="../../../static/images/meeting-icon.png"
                ></el-image
              ></el-col>
              <el-col :offset="1" :span="8">
                <div>
                  <h3>《{{ meeting.title }}》&ensp;审阅会</h3>
                </div>
                <div class="meeting-owner">
                  创建者: &ensp;{{ meeting.ownerName }}
                </div>
              </el-col>
              <el-col :span="8" class="meeting-time">
                <div style="margin-right:10px">
                  开始时间:{{ meeting.startTime | dateFormat }}
                </div>
                <div>结束时间:{{ meeting.endTime | dateFormat }}</div>
              </el-col>
              <el-col :offset="2" :span="3">
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 0"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >未开始</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 1"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >加入会议</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 2"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >已经结束</el-button
                >
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="历史会议" name="history">
          <div class="meeting-list">
            <div class="meeting-title">历史会议</div>

            <el-row
              v-for="meeting in historyMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
            >
              <el-col :span="2"
                ><el-image
                  class="meeting-icon"
                  src="../../../static/images/meeting-icon.png"
                ></el-image
              ></el-col>
              <el-col :offset="1" :span="8">
                <div>
                  <h3>《{{ meeting.title }}》&ensp;审阅会</h3>
                </div>
                <div class="meeting-owner">
                  创建者: &ensp;{{ meeting.ownerName }}
                </div>
              </el-col>
              <el-col :span="8" class="meeting-time">
                <div style="margin-right:10px">
                  开始时间:{{ meeting.startTime | dateFormat }}
                </div>
                <div>结束时间:{{ meeting.endTime | dateFormat }}</div>
              </el-col>
              <el-col :offset="2" :span="3">
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 0"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >未开始</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 1"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >加入会议</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 2"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >已经结束</el-button
                >
              </el-col>
            </el-row>
          </div></el-tab-pane
        >
        <el-tab-pane label="待办列表" name="todo">
          <div class="meeting-list">
            <div class="meeting-title">代办列表</div>
            <el-divider></el-divider>
            <el-row
              v-for="meeting in todoMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
            >
              <el-col :span="2"
                ><el-image
                  class="meeting-icon"
                  src="../../../static/images/meeting-icon.png"
                ></el-image
              ></el-col>
              <el-col :offset="1" :span="8">
                <div>
                  <h3>《{{ meeting.title }}》&ensp;审阅会</h3>
                </div>
                <div class="meeting-owner">
                  创建者: &ensp;{{ meeting.ownerName }}
                </div>
              </el-col>
              <el-col :span="8" class="meeting-time">
                <div style="margin-right:10px">
                  开始时间:{{ meeting.startTime | dateFormat }}
                </div>
                <div>结束时间:{{ meeting.endTime | dateFormat }}</div>
              </el-col>
              <el-col :offset="2" :span="3">
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 0"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >未开始</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 1"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >加入会议</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 2"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >已经结束</el-button
                >
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="我创建的" name="mine">
          <div class="meeting-list">
            <div class="meeting-title">我创建的</div>
            <div class="meeting-divider"></div>
            <el-row
              v-for="meeting in mineMeetingList"
              :key="meeting.meetingId"
              class="meeting-item"
            >
              <el-col :span="2"
                ><el-image
                  class="meeting-icon"
                  src="../../../static/images/meeting-icon.png"
                ></el-image
              ></el-col>
              <el-col :offset="1" :span="8">
                <div>
                  <h3>《{{ meeting.meetingName }}》&ensp;审阅会</h3>
                </div>
                <div class="meeting-owner">
                  创建者: &ensp;{{ meeting.ownerName }}
                </div>
              </el-col>
              <el-col :span="8" class="meeting-time">
                <div style="margin-right:10px">
                  开始时间:{{ meeting.startTime | dateFormat }}
                </div>
                <div>结束时间:{{ meeting.endTime | dateFormat }}</div>
              </el-col>
              <el-col :offset="2" :span="3">
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 0"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >未开始</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 1"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >加入会议</el-button
                >
                <el-button
                  v-if="showType(meeting.startTime, meeting.endTime) == 2"
                  @click="enterMeeting(meeting.meetingId, meeting.ownerId)"
                  >已经结束</el-button
                >
              </el-col>
            </el-row>
          </div></el-tab-pane
        >
      </el-tabs>

      <el-input
        placeholder="查找会议"
        v-model="meetingInput"
        prefix-icon="el-icon-search"
        class="search-meeting"
      >
        <el-button slot="append" @click="searchMeeting">搜索</el-button>
      </el-input>
      <el-button
        type="text"
        @click="showCreateMeetingVisible = true"
        class="create-meeting"
        >创建会议</el-button
      >
    </el-header>
    <el-dialog
      title="创建会议"
      :visible.sync="showCreateMeetingVisible"
      width="40%"
      @close="CreateMeetingClose"
    >
      <el-form :model="meeting">
        <el-form-item label="title">
          <el-input v-model="meeting.title"></el-input>
        </el-form-item>
        <el-form-item label="belongTo projectId">
          <el-input v-model="meeting.belongTo" disabled></el-input>
        </el-form-item>
        <el-form-item label="startTime">
          <el-input v-model="meeting.startTime"></el-input>
        </el-form-item>
        <el-form-item label="endTime">
          <el-input v-model="meeting.endTime"></el-input>
        </el-form-item>
        <el-form-item label="note">
          <el-input v-model="meeting.note"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="createMeeting">创建会议</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { Message } from "element-ui";

export default {
  name: "Meeting",
  data() {
    return {
      todoMeetingList: [],
      meetingList: [],
      historyMeetingList: [],
      mineMeetingList: [],
      activeName: "first",
      meetingInput: "",
      projectId: "",
      showCreateMeetingVisible: false,
      meeting: {
        title: "",
        belongTo: "",
        startTime: "",
        endTime: "",
        note: ""
      }
    };
  },
  methods: {
    CreateMeetingClose() {
      this.meeting.title = "";
      this.meeting.startTime = "";
      this.meeting.endTime = "";
      this.meeting.note = "";
    },
    async createMeeting() {
      const { data: res } = await this.$http.post("meeting/", this.meeting);
      if (res.result === 1) {
        this.getMeeting(this.projectId);
        this.activeName = "first";
      } else {
        Message.error(res.message);
      }
      this.showCreateMeetingVisible = false;
    },
    async searchMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/search`, {
          linkNum: this.meetingInput
        })
        .catch(function(error) {
          console.log(error);
        });

      if (res.result == 1) {
        this.meetingList = res.data.meetingList;
        console.log(res);
      } else {
        Message.error(res.message);
      }
    },
    async getMeetingByName(name) {
      switch (name) {
        case "first":
          this.getMeeting(this.projectId);
          break;
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
        Message.error(res.message);
      }
    },
    async getHistoryMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/history`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.histroyMeetingList = res.data;
      } else {
        Message.error(res.message);
      }
    },
    async getMineMeeting() {
      const { data: res } = await this.$http
        .get(`meeting/mine`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.mineMeetingList = res.data.meetingList;
      } else {
        Message.error(res.message);
      }
    },
    handleClick(tab, event) {
      this.getMeetingByName(tab.name);
    },
    async getMeeting(project) {
      const { data: res } = await this.$http
        .get(`project/${project}/getMeeting`)
        .catch(function(error) {
          console.log(error);
        });
      if (res.result == 1) {
        // Message.success("获取会议列表");
        this.meetingList = res.data;
      } else {
        Message.error(res.message);
      }
    },
    enterMeeting(meetingId, ownerId) {

      let isAdmin =
        window.localStorage.getItem("userId") === ownerId ? true : false;
      this.$router.push({
        path: "/review",
        query: { meetingId: meetingId, isAdmin: isAdmin }
      });
    },
    showType(start, end) {
      var now = new Date().getTime();
      if (start > now) {
        return 0;
      } else if (now < end) {
        return 1;
      } else {
        return 2;
      }
    }
  },
  mounted() {
    this.token = window.sessionStorage.getItem("token");
    this.projectId = this.$route.params.id;
    this.meeting.belongTo = this.$route.params.id;
    console.log(this.projectId);
    this.getMeeting(this.projectId);
  }
};
</script>

<style scoped>
.meeting-list {
  width: 80%;
  display: flex;
  flex-direction: column;
  margin-left: 10%;
  padding: 10px 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
.meeting-divider {
  margin-left: 20px;
  width: 98%;
  height: 1px;
  background-color: #ccc;
  margin: 4px 0;
}
.meeting-title {
  height: 18px;
  line-height: 18px;
  font-size: 16px;
  margin: 4px 0 4px 30px;
}
.meeting-item {
  width: 100%;
  position: relative;
  height: 80px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ccc;
}
.meeting-icon {
  height: 60px;
  margin-top: 10px;
  margin-left: 15px;
}
.meeting-time {
  display: flex;
  flex-direction: column;
  justify-content: end;
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
