<template>
    <el-row  class="message-container">
      <el-col class="message-list" :span="6">
        <div v-for="message in messageList" :key="message.messageId" @click="showDetail(message.messageId)">
        <el-card class="message-item" >
          <el-badge :is-dot="message.hasRead" class="dot-item"></el-badge>
          <span class="message-time">{{message.date | dateFilters}}</span>
          <el-image :src="imgSrc" class="user-avatar">
            <div slot="placeholder" class="image-slot">
              加载中
              <span class="dot">...</span>
            </div>
          </el-image>
          <div class="message-user">
            <div>{{message.fromName}}:</div>
            <div>{{message.projectName}}</div>
          </div>
        </el-card>
        </div>
      </el-col>
      <el-col :span="18" class="message-detail-box" >
        <div class="message-detail" v-if="!noDetail">
          <h2>{{messageDetail.projectName}}</h2>
          <p>
            {{messageDetail.word}}
          </p>
          <span class="detail-time">{{messageDetail.date}}</span>
        </div>
        <div v-else class="no-detail " >
            点击公告查看详情
        </div>
      </el-col>

    </el-row>

</template>

<script>
    export default {
        name: "Message",
      data() {
        return {
          noDetail:true,
          imgSrc: require("../assets/logo.png"),
          messageList:[
            {
              messageId:'001',
              fromId:'002',
              fromName:'yjn',
              date:'2020/10/20',
              projectId:'p1',
              projectName:'yjn网恋日记',
              hasRead:false,
              hasProcess:false,
              type:0
            },
            {
              messageId:'002',
              fromId:'002',
              fromName:'yjn',
              date:'2020/10/20',
              projectId:'p1',
              projectName:'yjn网恋日记',
              hasRead:true,
              hasProcess:false,
              type:0
            },
            {
              messageId:'003',
              fromId:'002',
              fromName:'yjn',
              date:'2020/10/20',
              projectId:'p1',
              projectName:'yjn网恋日记',
              hasRead:true,
              hasProcess:false,
              type:0
            }
          ],
          messageDetail:{
            fromId: "HVgu",
            fromName: "Q4uD^Y",
            date: "2014-10-05",
            projectId: "T$3M",
            projectName: "][32",
            type: "tNFr1M",
            videoName: "BJvU",
            reviewResult: "T#[[h0",
            meetingId: "CRt^",
            word: "gHf&",
            inviteResult: false
          }
        };
      },
      methods:{
        showDetail(v){

            if(this.noDetail){
              this.noDetail = false
            }
            this.getMessageDetail(v)
            // this.getMessageList()
        },
        async getMessageList(){
          const { data: res } = await this.$http.get('messages/');
          if(res.result === 1){
            this.$message({
              message: "获取通知成功",
              type: "success"
            });
            // this.messageList = res.data
          } else {
            this.$message({
              message: res.message,
              type: "error"
            });
          }
        },
        async getMessageDetail(i){
          const { data: res } = await this.$http.get(`message/${i}`);
          if(res.result === 1){
            this.$message({
              message: "获取详情成功",
              type: "success"
            });
            // this.messageDetail =res.data
          } else {
            this.$message({
              message: res.message,
              type: "error"
            });
          }

        }

      },
      mounted() {
          this.getMessageList()
      },
      filters:{
          dateFilters (value){
             return value
          }
      }
    }
</script>

<style scoped>


.message-container{
  margin-top: 20px;
  height: 90%;
  padding: 2px;
  width: 100%
}
.message-list{
  padding: 0 10px 0 10px;
  border: 1px solid #ccc;
  min-height: 80vh;
}
.message-item {
  margin-top: 5px;
  position: relative;
  display: flex;
}
.user-avatar {
  width: 50px;
  height: 50px;
  float: left;
  clear: both;
}
.message-user {
  padding-left: 75px;
}
.dot-item {
  position: absolute;
  top: 5px;
  right: 5px;
}
.message-time {
  position: absolute;
  bottom: 5px;
  right: 5px;
}
.message-detail-box{
  height: 100%;
}
.message-detail {
  position: relative;
  min-height: 80vh;
  padding: 10px;
  border: 1px solid #ccc;
  margin-left: 3px;
}
.detail-time {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
.no-detail{
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
