<template>
    <el-row  class="message-container">
      <el-col class="message-list" :span="6">
        <div v-for="message in messageList" :key="message.messageId" @click="showDetail(message.messageId);message.hasRead=1">
          <el-card class="message-item" >
            <i class="el-icon-close message-close" @click.stop="deleteMessage(message)"></i>
            <el-badge :is-dot="message.hasRead===0" class="dot-item"></el-badge>
            <span class="message-time">{{message.date | dateFormat}}</span>
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
          <p v-if="messageDetail.type===0||messageDetail.type===1">{{messageDetail.videoName}}</p>
          <p v-if="messageDetail.type===1">{{messageDetail.reviewResult}}</p>
          <p v-if="messageDetail.type===2">{{messageDetail.meetingId}}</p>
          <div>{{messageDetail.type|messageType}}
            <el-popover
              placement="top"
              width="160"
              v-model="visible">
              <p>是否同意加入项目"{{messageDetail.projectName}}？"</p>
              <div style="text-align: right; margin: 0">
                <el-button size="mini" type="text" @click="pocessVisit(0)">不同意</el-button>
                <el-button type="primary" size="mini" @click="pocessVisit(1)">同意</el-button>
              </div>
              <el-button slot="reference" type="text" v-if="messageDetail.type===3" @click="visible = true" :disable="messageDetail.hasProcess">{{messageDetail.projectName}}</el-button>

            </el-popover>

          </div>
          <span class="detail-time">{{messageDetail.date|dateFormat}}</span>
        </div>
        <div v-else class="no-detail " >
          点击公告查看详情
        </div>
      </el-col>

    </el-row>

</template>

<script>
  import { Message } from "element-ui";

  export default {
    name: "Message",
    data() {
      return {
        noDetail:true,
        imgSrc: require("./../../assets/logo.png"),
        messageList:[

        ],
        visible:false,
        messageDetail:{
        },
        currentMessageId:'',
      };
    },
    methods:{
      showDetail(v){
        if(this.noDetail){
          this.noDetail = false
        }
        this.getMessageDetail(v)

      },
      deleteMessage(msg){
        this.messageList = this.messageList.filter(message =>{
          return message!=msg
        })
      },
      async getMessageList(){
        const { data: res } = await this.$http.get('messages/');
        if(res.result === 1){

          // Message.success("获取通知成功")
          this.messageList = res.data
          console.log(res)
        } else {
          Message.error(res.message)
        }
      },
      async getMessageDetail(i){
        this.currentMessageId = i
        const { data: res } = await this.$http.get(`message/${i}`);
        if(res.result === 1){

          // Message.success("获取详情成功")
          this.messageDetail =res.data
        } else {
          Message.error(res.message);
        }

      },
      async pocessVisit(n){
        let isAgree = n===1
        console.log(isAgree)
        const { data: res } = await this.$http.post(`project/${this.messageDetail.projectId}/join/`,{
          isAgree,
          messageId:this.currentMessageId
        });
        if(res.result === 1){
          // Message.success("处理成功");
          this.messageDetail =res.data
          console.log(res)
        } else {
          Message.error(res.message)
        }
        this.visible = false

      }
    },
    mounted() {
      this.getMessageList()
    },

  }
</script>

<style scoped>
  .message-container{
    margin-top: 65px;
    height: 82vh;
    padding: 2px;
    width: 100%;
    background-color: #fafafa;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }
  .message-list{
    padding: 0 10px 0 10px;
    height: 80vh;
    overflow: auto;
  }
  .message-item {
    margin-top: 5px;
    position: relative;
    display: flex;
    cursor: pointer;
  }
  .message-close{
    position: absolute;
    top:2px;
    right: 2px;
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
    background-color: #fff;
    height: 82vh;
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
    font-size: 28px;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
