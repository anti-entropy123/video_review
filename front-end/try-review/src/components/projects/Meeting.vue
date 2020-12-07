<template>
  <div>
    <el-header style="position: relative">
      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
        <el-tab-pane label="全部会议" name="first">

          <div class="meeting-list">
                  <div>会议列表</div>
          <el-divider></el-divider>
            <div
              v-for="meeting in meetingList"
              :key="meeting.meetingId"
              class="meeting-item"
            >
              <el-card style="height:100%">
                <div style="display:flex">
                    <div><h3>{{meeting.title}}</h3></div>
                  <a href="">会议号:{{meeting.meetingUrl}}</a>
                </div>

                <div class="meeting-owner">{{meeting.ownerName}}</div>
                <div class="meeting-time">
               <div style="margin-right:10px">开始时间:{{meeting.startTime}}</div>
                        <div>结束时间:{{meeting.endTime}}</div>
                </div>

              </el-card>
            </div>
          </div>
        </el-tab-pane>
         <el-tab-pane label="历史会议" name="history">
              <div class="meeting-list">
                 <div
          v-for="meeting in historyMeetingList"
          :key="meeting.meetingId"
          class="meeting-item"
        >
          <el-card>
            <el-form :model="meeting">
              <el-form-item label="title">
                <span>{{ meeting.title }}</span>
              </el-form-item>
              <el-form-item label="ownerName">
                <span>{{ meeting.ownerName }}</span>
              </el-form-item>
              <el-form-item label="startTime">
                <span>{{ meeting.startTime }}</span>
              </el-form-item>
              <el-form-item label="endTime">
                <span>{{ meeting.endTime }}</span>
              </el-form-item>
              <el-form-item label="note">
                <span>{{ meeting.note }}</span>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
        </div></el-tab-pane>
    <el-tab-pane label="待办列表" name="todo">
      <div class="meeting-list">
<div
          v-for="meeting in todoMeetingList"
          :key="meeting.meetingId"
          class="meeting-item"
        >
          <el-card>
            <el-form :model="meeting">
              <el-form-item label="title">
                <span>{{ meeting.title }}</span>
              </el-form-item>
              <el-form-item label="ownerName">
                <span>{{ meeting.ownerName }}</span>
              </el-form-item>
              <el-form-item label="startTime">
                <span>{{ meeting.startTime }}</span>
              </el-form-item>
              <el-form-item label="endTime">
                <span>{{ meeting.endTime }}</span>
              </el-form-item>
              <el-form-item label="note">
                <span>{{ meeting.note }}</span>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
       </el-tab-pane>
        <el-tab-pane label="我创建的" name="mine">
             <div class="meeting-list">
          <div
          v-for="meeting in mineMeetingList"
          :key="meeting.meetingId"
          class="meeting-item"
        >
          <el-card>
            <el-form :model="meeting">
              <el-form-item label="title">
                <span>{{ meeting.title }}</span>
              </el-form-item>
              <el-form-item label="ownerName">
                <span>{{ meeting.ownerName }}</span>
              </el-form-item>
              <el-form-item label="startTime">
                <span>{{ meeting.startTime }}</span>
              </el-form-item>
              <el-form-item label="endTime">
                <span>{{ meeting.endTime }}</span>
              </el-form-item>
              <el-form-item label="note">
                <span>{{ meeting.note }}</span>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
             </div></el-tab-pane>

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
      meetingList:[],
      historyMeetingList:[],
      mineMeetingList:[],
      activeName: "first",
      meetingInput: "",
      projectId:'',
      showCreateMeetingVisible: false,
      meeting: {
        title:'',
        belongTo: '',
        startTime:'',
        endTime:'',
        note:''
      },

    };
  },
  methods: {
    CreateMeetingClose() {
      this.meeting.title = '';
      this.meeting.startTime='';
      this.meeting.endTime='';
      this.meeting.note = '';
    },
    async createMeeting() {
      const { data: res } = await this.$http.post("meeting/", this.meeting);
      if (res.result === 1) {
        // this.$message({
        //   message: "成功创建会议",
        //   type: "success"
        // });
        Message.success("成功创建会议");
        this.getMeeting(this.projectId)
         this.activeName='first'
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error");
      }
      this.showCreateMeetingVisible = false;
    },
    async searchMeeting() {
      const { data: res } = await this.$http
        .post(`meeting/search/`, {
          linkNum: this.meetingInput
        })
        .catch(function(error) {
          console.log(error);
        });

      if (res.result == 1) {
        this.meetingList=res.data.meetingList
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
        switch(name){
          case 'first':this.getMeeting(this.projectId); break;
          case 'todo': this.getTodoMeeting(); break;
          case 'mine': this.getMineMeeting(); break;
          case 'history':this.getHistoryMeeting();break;
        }
    },
    async getTodoMeeting(){
      const { data: res } = await this.$http
        .get(`meeting/todo`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.todoMeetingList=res.data.meetingList
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async getHistoryMeeting(){
      const { data: res } = await this.$http
        .get(`meeting/history`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.histroyMeetingList=res.data
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    },
    async getMineMeeting(){
      const { data: res } = await this.$http
        .get(`meeting/mine`)
        .catch(error => console.log(error));
      if (res.result == 1) {
        this.mineMeetingList=res.data.meetingList
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
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
        // this.$message({
        //   message: "获取会议列表",
        //   type: "success"
        // });
        Message.success("获取会议列表")
        this.meetingList = res.data;
      } else {
        // this.$message({
        //   message: res.message,
        //   type: "error"
        // });
        Message.error("error")
      }
    }
  },
  mounted() {
    this.token = window.sessionStorage.getItem("token");
    this.projectId = this.$route.params.id;
    this.meeting.belongTo = this.$route.params.id
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
  margin-left:10%;
}
.meeting-item{
  width: 100%;
  position: relative;
  height: 100px;
}
.meeting-owner{
  position: absolute;
  bottom: 10px;
  left: 30px;

}
.meeting-time{
  display: flex;
  position: absolute;
  bottom: 10px;
  right: 30px;
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
