<template>
<div id="meet">
<!--  header-->
  <a-layout-header class="user">
    <div class="title">
      {{videoName}}
    </div>
    <div class="message">
      <div class="selectVideo">
        <a-select :options="videos" placeholder="更换视频" @change="changeSrc" :default-value="videoId">
        </a-select>
      </div>
      <div class="bell">
        <a-dropdown >
          <a class="ant-dropdown-link" @click="e => e.preventDefault()">
            <a-icon type="bell" :style="{ fontSize: '23px', color: '#ffffff' }"/></a>
              <a-menu slot="overlay">
                <a-menu-item key="0">
                  <a target="_blank" rel="noopener noreferrer" href="http://www.alipay.com/">1min 前**同意了你的申请</a>
                </a-menu-item>
                <a-menu-item key="1">
                  <a target="_blank" rel="noopener noreferrer" href="http://www.baidu.com/">15min后**会议召开</a>
                </a-menu-item>
                <a-menu-divider/>
              </a-menu>
        </a-dropdown>
      </div>
      <a-avatar v-bind:src="avatar" size="large"  />
    </div>
  </a-layout-header>
<!--  视频区-->
  <div class="left">
    <div class="videos">
      <video-player class="video"
        width="60%"
        ref="videoPlayer"
        :playsinline="true"
        :options="playerOptions"
        @play="onPlayerPlay($event)"
        @pause="onPlayerPause($event)"
      />
      <Draw class="draw" ref="draw" style="position: absolute"
       v-bind:Size="videoSize" v-if="isDraw==true" v-on:getImg="getImg"> </Draw>
      <div   :style="
        `width:${this.videoSize[0]}px;height:${this.videoSize[1]}px;position: absolute`
      " >
        <img v-cloak v-if="isCheckComment==true" v-bind:src="currentImageUrl"  style="width: 100%;">
      </div>
    </div>
    <!--    评论框-->
    <div class="input">
      <textarea class="text" placeholder="在这写批注" v-on:keyup="isEmpty()"  v-model="commentContent"></textarea>
      <div class="tools">
<!--        <button @click="saveImg">生成图片</button>-->
        <a-icon type="close-circle" theme="twoTone" style="margin-right: 27px;cursor:pointer;font-size:20px" @click="cancelDraw"/>
        <a-icon type="delete" theme="twoTone" style="margin-right: 20px;cursor:pointer;font-size:20px" @click="cleanDraw"/>
        <a-icon type="edit" theme="twoTone" style="margin-right: 10px;cursor:pointer;font-size:20px" @click="draw" />
        <a-button class="submit" type="primary" v-if="textEmpty==false" @click="submitComment()">
          提交
        </a-button>
        <a-button class="submit" type="primary" v-else="textEmpty==true" disabled>
          提交
        </a-button>
      </div>
    </div>
  </div>
<!--  批注区-->
  <div class="commant" >
      <a-menu class="commantHead" v-model="current" mode="horizontal">
        <a-menu-item key="commant"> 批注</a-menu-item>
        <a-menu-item key="fileinfo"> 文件信息</a-menu-item>
      </a-menu>
      <div class="commantCards" v-if="current=='commant'">
        <ul class="discusses" v-for="comment in comments">
          <li>
            <div class="discuss">
              <div id="user">
                <a-avatar class="userHead" style="float: left;" v-bind:src="comment.avatar"/>
                <div style="float: left;line-height: 30px;margin-left: 15px;font-family: -webkit-pictograph;">{{comment.fromName}}</div>
              </div>
              <div class="dicussBody" style="clear:both">
                <div style="cursor:pointer;color:#4189d3" class="discussTime" @click="toPosition(comment.position,comment.imageUrl)">{{comment.time}}</div>
                <div class="discussContent"> {{comment.content}}</div>
<!--                <div v-if="comment.fromName==this.userName" @click="deleteComment(comment.commentId)">删除</div>-->
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="fileInfo" v-if="current=='fileinfo'">
<!--        <div class="discuss">-->
          <div class="info">所属项目：  {{videoInfo.project}}</div>
          <div class="info">视频时长：  {{videoInfo.duration}}</div>
          <div>上传时间：  {{videoInfo.createDate}}</div>
          <div>视频名称：  {{videoInfo.videoName}}</div>
          <div>上传者：  {{videoInfo.uploader}}</div>
          <div>描述：  {{videoInfo.description}}</div>
<!--        </div>-->
      </div>
  </div>
</div>
</template>

<script>
  import Header from "./Header";
  import Draw from "./Draw"
  import axios from "axios";
    export default {
      components: {Draw, Header},
      name: "Meet",
      data() {
        return {
          // videoName:'项目名称',
          current: ['commant'],
          textEmpty: true,
          playerOptions: {
            playbackRates: [0.5, 1.0, 1.5, 2.0], //播放速度
            autoplay: false, // 如果true,浏览器准备好时开始回放。
            muted: false, // 默认情况下将会消除任何音频。
            loop: false, // 导致视频一结束就重新开始。
            preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
            language: 'zh-CN',
            aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
            fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
            sources: [
              {
                type: 'video/mp4', // 这里的种类支持很多种：基本视频格式、直播、流媒体等，具体可以参看git网址项目
                src: '"https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/初音未来.mp4"' // url地址
              }
            ],
            hls: true,
            poster: 'http://pic33.nipic.com/20131007/13639685_123501617185_2.jpg', // 你的封面地址
            width: 400, // 播放器宽度
            notSupportedMessage: '此视频暂无法播放，请稍后再试', // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
            controlBar: {
              timeDivider: true,
              durationDisplay: true,
              remainingTimeDisplay: false,
              fullscreenToggle: true // 全屏按钮
            }
          },
          userId: "5fcb46a9872ad7704cb534c1",
          userName: 'yjn',
          meetingId: "5fcb98682fd62669086c8dad",
          projectId: "5fcb46f7872ad7704cb534c2",
          videos:[{
            value: '5fbe93d6077dd49c9e0955ac',
            label: '初音未来.mp4',
          },{
            value: '5fcb4716872ad7704cb534c3',
            label: '八重樱.mp4',
          },],
          videoId: "5fcb4716872ad7704cb534c3",
          videoName: "",
          videoInfo:[],
          videoSize:[{
            videoWidth:"",
            videoHeight:""
          }],
          memberNum: 1,
          comments: [],
          avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
          commentContent: '',
          isDraw:false,
          imgFile:new FormData(),
          imgUrl:'',
          currentImageUrl:'',
          isCheckComment:false,
          headerobj: {
            Authorization: "Bearer " + window.sessionStorage.getItem("token"),
            "Content-Type": "multipart/form-data"
          },
        };
      },
      methods: {
        isEmpty() {
          if (this.commentContent !== '') {
            this.textEmpty = false;
          } else {
            this.textEmpty = true;
          }
        },
        // 监听 socketio 事件 'onPlayerPlay'
        onPlayerPlay: function () {
          if (!this.player.paused()) {
            this.changeVideo(3);
          }
        },
        // 监听 socketio 事件 'onPlayerPause'
        onPlayerPause: function () {
          if (this.player.paused()) {
            this.changeVideo(0);
          }
        },
        // 视频进度条鼠标左键抬起事件(mouseup)监听回调
        // 即拖动进度条.
        onPlayerTimeupdate: function (e) {
          this.changeVideo(2);
          e.stopPropagation();
        },
        // 触发 socketio 事件 'changeVideo', 通知服务器做出操作.
        changeVideo: function (type) {
          if(type===3){
            this.isCheckComment=false;
            this.currentImageUrl='';
          }
          this.$socket.emit("changeProcess", {
            type: type,
            position: this.player.currentTime(),
            videoId: this.videoId,
          });
        },
        changeSrc:function(value){
          console.log(value)
          this.videoId=value
          this.changeVideo(5)
        },
        toPosition:function (position,imageUrl) {
          this.player.currentTime(position)
          let myPlayer = this.$refs.videoPlayer.player;
          myPlayer.pause();
          this.changeVideo(2);
          this.isCheckComment = true;
          this.currentImageUrl = imageUrl;
          console.log(this.isCheckComment);
          console.log(this.currentImageUrl);
        },
        submitComment(){
          if(this.isDraw){
            this.saveImg();
            console.log(this.imgUrl)
            this.cleanDraw();
          }
          let _this = this;
          // 提交批注
          setTimeout(function(){
            console.log(_this.imgUrl)
            _this.$socket.emit('addComment', {
              meetingId: _this.meetingId,
              content: _this.commentContent,
              imageUrl: _this.imgUrl,
              position: _this.player.currentTime(),
              fromName: _this.userId
            });
            _this.commentContent = '';
            _this.commentPosition = '';
            _this.imgUrl = '';
          },1000)
        },
        //删除批注
        deleteComment(commentId){
          this.$sockets.emit('removeComment',{
            commentId:commentId
          });
        },
        formatSecond(second) {
          // const days = Math.floor(second / 86400);
          const hours = Math.floor((second % 86400) / 3600);
          const minutes = Math.floor(((second % 86400) % 3600) / 60);
          const seconds = Math.floor(((second % 86400) % 3600) % 60);
          let forMatDate = '';
          (hours<10)?(forMatDate += '0'+ hours.toString()+':'):(forMatDate += hours.toString() +':');
          (minutes<10)?(forMatDate += '0'+ minutes.toString()+':'):(forMatDate +=minutes.toString()+':');
          (seconds<10)?(forMatDate += '0'+ seconds.toString()):(forMatDate +=seconds.toString());
          // console.log(forMatDate)
          return forMatDate;
        },
        formatTimestamp(second){
          let temp = parseInt(second);
          var timestamp = new Date(temp*1000);
          var timestamp1 = timestamp.toLocaleDateString().replace(/\//g, "-") + " " + timestamp.toTimeString().substr(0, 8);
          return timestamp1;
        },
        //请求头像
        async getHead(userId) {
          const {data: res} = await this.$http.get(
            `/user/${userId}`
          ).catch(function (error) {
              console.log(error);
            }
          );
          if (res.result == 1) {
            // this.$message({
            //   message: "获取用户信息",
            //   type: "success"
            // });
            this.avatar = res.data.avatar;
          }
        },
        //根据id请求用户信息
        async getUser(userId){
          const {data: res} =await this.$http.get(
            `/user/${userId}`
          ).catch(function (error) {
              console.log(error);
            }
          );
          if (res.result == 1) {
            // console.log(res.data.username)
            this.videoInfo.uploader = res.data.username;
          }
        },
        draw:function () {
          this.changeVideo(1);
          this.isDraw = true;
          console.log(this.isDraw);
        },
        cancelDraw:function () {
          this.isDraw = false;
        },
        cleanDraw:function(){
          this.$refs.draw.clearPalette();
        },
        saveImg:function(){
          this.$refs.draw.savePalette('png');
        },
        dataURLtoFile: function(dataurl, filename) {
          var arr = dataurl.split(','),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);
          while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
          }
          return new File([u8arr], filename, { type: mime });
        },
        getImg:function(lastBase64){
          this.imgFile.append("image",this.dataURLtoFile(lastBase64,'img'));
          this.request();
        },
        async request(){
          var self = this;
          const{data:res}=await axios.post(
            "http://188.131.227.20:1314/api/uploadImg/",
            this.imgFile,
            {
              headers:self.headerobj
            }
          ).catch(function (error) {
              console.log(error);
            }
          );
          if (res.result == 1) {
            this.imgFile=new FormData();
              this.imgUrl = res.data.url;
            console.log(this.imgUrl)
          }
        },
        getVideoSize(){
          // this.videoSize.videoWidth = this.$refs.videoPlayer.$el.clientWidth;
          this.$set(this.videoSize,0,this.$refs.videoPlayer.$el.clientWidth);
          // this.videoSize.videoHeight = this.$refs.videoPlayer.$el.clientHeight;
          this.$set(this.videoSize,1,this.$refs.videoPlayer.$el.clientHeight);
          console.log(this.videoSize)//高度
        },
        //获取项目中所有视频
        async getVideo(projectId){
          const {data: res} =await this.$http.get(
            `/project/${projectId}/userAndVideo/`
          ).catch(function (error) {
              console.log(error);
            }
          );
          console.log('++++++++++++++=')
          console.log(projectId)
          console.log(res)
          if (res.result == 1) {
            console.log('++++++++++++++=')
            console.log(res.data)
          }
        }
      },
      mounted() {
        this.avatar = this.getHead(this.userId);
        this.getVideo(this.projectId);
        this.getVideoSize();
        let that = this;
        window.onresize = () => {
           that.getVideoSize();
        }
      },
      destroyed(){
        window.onresize = null;
      },
      computed: {
          player() {
            return this.$refs.videoPlayer.player//自定义播放
          }
        },
      sockets: {
          connect() {
            this.id = this.$socket.id;
            this.$socket.emit("init", {
              userId: this.userId,
              meetingId: this.meetingId,
            });
          },
          sycnVideoState(data) {
            this.url = data.data.url;
            this.duration = data.data.duration;
            this.videoName = data.data.videoName;
            // 设置封面
            this.player.poster(data.data.cover);
            // 检查是否切换了视频源
            if (this.player.src() != data.data.url) {
              this.player.src(data.data.url);
              this.videoInfo = data.data.videoInfo;
              this.getUser(data.data.videoInfo.uploader);
              this.videoInfo.duration = this.formatSecond(data.data.videoInfo.duration);
              this.videoInfo.createDate = this.formatTimestamp(data.data.videoInfo.createDate);
              console.log(data.data)
            }
            // 弹出通知气泡
            this.$Notice.open({
              title: data.data.userName + "进行了操作" + data.data.reason.toString()
            });
            // 检查是否需要切换播放状态
            if (data.data.isPlay) {
              this.player.play();
            } else {
              this.player.pause();
            }
            if (Math.abs(data.data.position - this.player.currentTime()) > 1) {
              this.player.currentTime(data.data.position);
            }
            let element = document.getElementsByClassName('vjs-progress-control vjs-control')[0];
            element.addEventListener(
              'mouseup',
              this.onPlayerTimeupdate);
          },
          sycnMember(data) {
            this.memberNum = data.data.memberNum;
          },
          updateComment(data) {
            this.comments = data.data;
            console.log(this.comments)
            for (var comment of data.data){
              comment.time = this.formatSecond(comment.position)
            }
          },
          errorHandle(data) {
            this.$Notice.open({
              title: data.message
            });
          }
        },
      watch:{
        videoSize: {
          handler(newValue, oldValue) {
            // for (let i = 0; i < newValue.length; i++) {
            //   if (oldValue[i] != newValue[i]) {
            //     console.log(newValue)
            //   }
            // }
          },
          deep: true,
          immediate:true,
        }
      }
    }
</script>

<style scoped>
  #meet{
    width: 100%;
    height: 100%;
    background: #dcdee2;
  }
  .user{
    background: #136abb;
    color: #fff;
    align-items: center;
  }
  .title{
    float: left;
    color: white;
    font-size: 17px;
  }
  .message{
    margin-right: 14px;
    align-items: center;
    float: right;
  }
  .bell{
    margin-right: 20px;
    float: left;
    margin-top: 4px;
  }
  .selectVideo{
    margin-right: 20px;
    float: left;
    margin-top: 4px;
  }
  .left{
    background: #dcdee2;
    height: 90.5%;
    width: 75%;
    float: left;
    /*text-align: center;*/
  }
  .input{
    float: top;
    display: flex;
    justify-content: center;
    height: 28%;
    margin-top: 14px;
    position: relative;
  }
  .tools{
    position: absolute;
    bottom: 9%;
    right: 16%;
  }
  .text{
    width: 70%;
    height: 95%;
    border-radius: 20px;
    font-family: none;
    font-size: 16px;
    outline:none;resize:none;
    border: 0;
  }
  .text:focus{
    /*border: #658bad solid 2px;*/
    /*box-shadow: #888888;*/
    box-shadow: 2px 2px 7px 1px #888888;
  }
  .commant{
    margin-top: -0.26%;
    background: #dcdee2;
    float: right;
    float: top;
    width: 25%;
    height: 90.5%;
    /*overflow:auto;*/
  }
  .videos{
    width:100%;
    /*height:66%;*/
    display: flex;
    justify-content: center;
    margin-top: 0px;
  }
  .video{
    width: 70%;
    height: 100%;
  }
  .draw{

  }
  .commantHead{
    background: #dcdee2;
    color: black;
    font-size: 10px;
  }
  .commantCards{
    /*text-align: center;*/
    height: 90.5%;
    margin-top: 3px;
    overflow:auto;
  }
  .discusses{
    /*text-align: center;*/
    list-style:none;
    /*margin: auto;*/
  }
  .discuss{
    background: #cfd3d694;
    height: 115px;
    float: bottom;
    color: black;
    padding: 18px;
  }
  .dicussBody{
    float: top;
    padding: 3px;
    font-size: 13px;
    color: #041466;
    font-family: -webkit-pictograph;
  }
  #user{
    float: left;
    /*margin-top: 11px;*/
    /*margin-left: 12px;*/
  }
  ul{
    margin-bottom: 0.1em;
  }

  .info{
    width: 100%;
  }
  .fileInfo{
    background: #cfd3d694;
    height: max-content;
    float: bottom;
    color: black;
    padding: 18px;
    font-size: 14px;
    font-family: fangsong;
    color:#0b034d;
  }
  [v-cloak] {
    display: none;
  }

</style>
