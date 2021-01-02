<template>
  <div class="review-offline clearfix">
    <!-- 头部 -->
    <el-header class="review-header">
      <div class="header-title fl">
        <span>{{ video }}</span>
      </div>
      <div class="fr user-box">
        <el-avatar size="medium" :src="circleUrl"></el-avatar>
        <span>任林杰</span>
      </div>
      <div class="select-video fr">
        <el-select v-model="video" placeholder="更换视频"  @change="handleChange">
          <el-option
            v-for="video in videoList"
            :key="video.videoId"
            :label="video.videoName"
            :value="{videoId:video.videoId,videoName:video.videoName}"
          >
          </el-option>
        </el-select>
      </div>
    </el-header>
    <!-- 内容 -->
    <div class="offline-container">
      <div class="left">
        <div class="videos">
          <video-player
            class="video-player vjs-custom-skin"
            ref="videoPlayer"
            :playsinline="true"
            :options="playerOptions"
            @play="onPlayerPlay($event)"
            @pause="onPlayerPause($event)"
            @ended="onPlayerEnded($event)"
            @waiting="onPlayerWaiting($event)"
            @playing="onPlayerPlaying($event)"
            @loadeddata="onPlayerLoadeddata($event)"
            @timeupdate="onPlayerTimeupdate($event)"
            @canplay="onPlayerCanplay($event)"
            @canplaythrough="onPlayerCanplaythrough($event)"
            @statechanged="playerStateChanged($event)"
            @ready="playerReadied"
          >
          </video-player>
          <Draw
            class="draw"
            ref="draw"
            style="position: absolute"
            v-bind:Size="videoSize"
            v-if="isDraw == true"
            v-on:getImg="getImg"
          >
          </Draw>
          <div
            :style="
              `width:${this.videoSize[0]}px;height:${this.videoSize[1]}px;position: absolute`
            "
          >
            <img
              v-cloak
              v-if="isCheckComment == true"
              v-bind:src="currentImageUrl"
              style="width: 100%;"
            />
          </div>
                  <div
          class="mask"
          v-if="canControl == false"
          :style="
            `width:${this.videoSize[0]}px;height:${this.videoSize[1]}px;position: absolute`
          "
        ></div>
        </div>
        <!-- 评论框 -->
        <div class="comment-box">
          <el-input
            class="comment-input"
            type="textarea"
            placeholder="在这写批注"
            v-model="textarea"
            rows="4"
          >
          </el-input>
          <div class="operate-btns">
            <i class="el-icon-close operate-btn" @click="cancelDraw"></i>
            <i class="el-icon-delete operate-btn" @click="cleanDraw"></i>
            <i class="el-icon-edit operate-btn" @click="draw"></i>
            <el-button class="operate-btn" @click="submitComment"
              >提交</el-button
            >
          </div>
        </div>
      </div>
      <!-- 批注区 -->
      <div class="notation-box">
        <div class="notation-menus">
          <div class="pointer" @click="changeMenu(1)">批注</div>
          <div class="pointer" @click="changeMenu(2)">文件信息</div>
        </div>
        <div v-if="currentMenu === 1" class="notation-content">
          <div class="notation-list">
            <div
              class="notation-item"
              v-for="comment in comments"
              :key="comment.commentId"
              @click="toViewComment(comment.imageUrl, index)"
            >
              <div class="notation-content">
                <div class="notation-user">
                  <el-avatar :src="comment.avatar"></el-avatar>
                  <div>{{ comment.fromName }}</div>
                  <div>{{ comment.date }}</div>
                </div>
                <div class="notation-time"></div>
                <div class="notation-content">
                  {{ comment.content }}
                </div>
                <div class="notation-operate">
                  <el-button type="text" @click="submitComment">删除</el-button>
                  <el-button type="text">回复</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="currentMenu === 2" class="video-into">
          <el-form ref="VideoInfoRef" :model="videoInfo" label-width="80px">
            <el-form-item label="所属项目"
              ><span>{{ videoInfo.project }}</span></el-form-item
            >
            <el-form-item label="视频时长"
              ><span>{{ videoInfo.duration }}</span></el-form-item
            >
            <el-form-item label="上传时间"
              ><span>{{ videoInfo.createDate }}</span></el-form-item
            >
            <el-form-item label="视频名称"
              ><span>{{ videoInfo.videoName }}</span></el-form-item
            >
            <el-form-item label="上传者"
              ><span>{{ videoInfo.uploader }}</span></el-form-item
            >
            <el-form-item label="描述"
              ><span>{{ videoInfo.description }}</span></el-form-item
            >
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Draw from "./Draw";
export default {
  components: { Draw },
  data() {
    return {
      isCheckComment:false,
      isDraw: false,
      videoSize: [],
      videoInfo: {
        project: "222",
        duration: "111",
        createData: "创建时间",
        videoName: "视频名称",
        uploader: "上传者",
        description: "描述"
      },
      projectId: "",
      userId: "",
      videoId: "",
      textarea: "",
      comments: [],
      currentMenu: 1,
      videoList: [
        
      ],
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0], //播放速度
        autoplay: false, // 如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 导致视频一结束就重新开始。
        preload: "auto", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: "zh-CN",
        aspectRatio: "16:9", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [
          {
            type: "video/mp4", // 这里的种类支持很多种：基本视频格式、直播、流媒体等，具体可以参看git网址项目
            src:"https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/初音未来.mp4" // url地址
          }
        ],
        hls: true,
        poster: "http://pic33.nipic.com/20131007/13639685_123501617185_2.jpg", // 你的封面地址
        width: 400, // 播放器宽度
        notSupportedMessage: "此视频暂无法播放，请稍后再试", // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true // 全屏按钮
        }
      },
      headerobj: {
        Authorization: "Bearer " + window.sessionStorage.getItem("token"),
        "Content-Type": "multipart/form-data"
      },
      video: "",
      videoName: "rlj",
      circleUrl:
        "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
      currentImageUrl: "",
      imgUrl: "",
      imgFile: new FormData(),
      //不知道是什么
      url: "",
      duration: "",
      videoName: "",
      canControl:true,
    };
  },
  methods: {
    getImg: function(lastBase64) {
      this.imgFile.append("image", this.dataURLtoFile(lastBase64, "img"));
      this.request();
    },
    async request() {
      var self = this;
      const { data: res } = await axios
        .post(
          "https://api.video-review.top:1314/api/uploadImg/",
          this.imgFile,
          {
            headers: self.headerobj
          }
        )
        .catch(function(error) {
          // console.log(error);
        });
      if (res.result == 1) {
        this.imgFile = new FormData();
        this.imgUrl = res.data.url;
        // console.log(this.imgUrl)
      }
    },
    //跳转到视频相应位置
    toViewComment(position, imageUrl, index) {
      this.currentImageUrl = "";
      this.player.currentTime(position);
      let myPlayer = this.$refs.videoPlayer.player;
      myPlayer.pause();
      this.changeVideo(6, index);
      // this.changeVideo(2);
      this.isCheckComment = true;
      this.currentImageUrl = imageUrl;
    },
    //删除视频批注
    async deleteComment(commentId) {
      const { data: res } = await this.$http
        .get(`video/${this.videoId}/comment`, {
          params: {
            commentId: commentId
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.getComments(this.videoId);
    },
    // 获取项目视频批注
    async getComments(videoId) {
      const { data: res } = await this.$http
        .get(`video/${videoId}/comments`)
        .catch(err => {
          console.log(err);
        });
      this.comments = res.data;
    },
    //获取项目中所有视频
    async getVideo(projectId) {
      var that = this;
      const { data: res } = await this.$http
        .get(`project/${projectId}/userAndVideo`)
        .catch(function(error) {
          console.log(error);
        });
      console.log(res);
      if (res.result == 1) {
        that.userList = res.data.userList;
        that.videoList = res.data.videoList;
        console.log(this.videoList);
        for (video in this.videoList) {
          if(video.videoId === this.videoId){
            this.video = video.videoName
            console.log(this.video)
          }   
        }     
      }
    },
    // 获取视频信息
    async getVideoInfo() {
      const { data: res } = await this.$http
        .get(`video/${this.videoId}/info`)
        .catch(function(error) {
          console.log(error);
        });
      this.videoInfo = res.data;
    },
    // 更换视频
         handleChange(params){
            const { videoId, videoName } = params;
            this.videoId = videoId,
            this.video = videoName
            console.log(this.video,this.videoId)
       },
    // 播放回调
    onPlayerPlay(player) {
      console.log("player play!", player);
    },

    // 暂停回调
    onPlayerPause(player) {
      console.log("player pause!", player);
    },

    // 视频播完回调
    onPlayerEnded($event) {
      console.log(player);
    },

    // DOM元素上的readyState更改导致播放停止
    onPlayerWaiting($event) {
      console.log(player);
    },

    // 已开始播放回调
    onPlayerPlaying($event) {
      console.log(player);
    },

    // 当播放器在当前播放位置下载数据时触发
    onPlayerLoadeddata($event) {
      console.log(player);
    },

    // 当前播放位置发生变化时触发。
    onPlayerTimeupdate($event) {
      console.log(player);
    },

    //媒体的readyState为HAVE_FUTURE_DATA或更高
    onPlayerCanplay(player) {
      // console.log('player Canplay!', player)
    },

    //媒体的readyState为HAVE_ENOUGH_DATA或更高。这意味着可以在不缓冲的情况下播放整个媒体文件。
    onPlayerCanplaythrough(player) {
      // console.log('player Canplaythrough!', player)
    },

    //播放状态改变回调
    playerStateChanged(playerCurrentState) {
      console.log("player current update state", playerCurrentState);
    },

    //将侦听器绑定到组件的就绪状态。与事件监听器的不同之处在于，如果ready事件已经发生，它将立即触发该函数。。
    playerReadied(player) {
      console.log("example player 1 readied", player);
    },
    changeMenu(value) {
      if (value == 2) {
        this.getVideoInfo();
      }
      this.currentMenu = value;
    },
    changeVideo(type) {
      if (type === 3) {
        this.isCheckComment = false;
        this.currentImageUrl = "";
      }
    },
    getVideoSize() {
      // this.videoSize.videoWidth = this.$refs.videoPlayer.$el.clientWidth;
      this.$set(this.videoSize, 0, this.$refs.videoPlayer.$el.clientWidth);
      // this.videoSize.videoHeight = this.$refs.videoPlayer.$el.clientHeight;
      this.$set(this.videoSize, 1, this.$refs.videoPlayer.$el.clientHeight);
      console.log(this.videoSize); //高度
    },
    //提交批注
    async submitComment() {
      if (this.isDraw) {
        this.saveImg();
        // console.log(this.imgUrl)
        this.cleanDraw();
        this.isDraw = false;
        const { data: res } = await this.$http
          .post(`/api/video/${this.videoId}/comment/`)
          .then(res => {
            this.commentContent = "";
            this.commentPosition = "";
            this.imgUrl = "";
          })
          .catch(err => {
            console.log;
          });
        console.log(res);
      }
    },
    saveImg: function() {
      this.$refs.draw.savePalette("png");
    },
    draw: function() {
      this.changeVideo(1);
      this.isDraw = true;
      // console.log(this.isDraw);
    },
    cancelDraw: function() {
      this.isDraw = false;
    },
    cleanDraw: function() {
      this.$refs.draw.clearPalette();
    },
    //删除批注
    deleteComment(commentId) {
      this.$socket.emit("removeComment", {
        commentId: commentId
      });
    },
        // 视频进度条鼠标左键抬起事件(mouseup)监听回调
    // 即拖动进度条.
    onPlayerTimeupdate: function(e) {
      this.isCheckComment = false;
      this.currentImageUrl = "";
      this.changeVideo(2);
      e.stopPropagation();
    },
    init() {
      this.getComments(this.videoId);
      let element = document.getElementsByClassName(
        "vjs-progress-control vjs-control"
      )[0];
      element.addEventListener("mouseup", this.onPlayerTimeupdate);
      this.getVideo(this.projectId);
      this.getVideoSize()
       let that = this;
     window.onresize = () => {
      that.getVideoSize();
    };
      // this.url = data.data.url;
      // this.duration = data.data.duration;
      // this.videoName = data.data.videoName;
      //  this.videoId = data.data.videoInfo.videoId;
      // 设置封面
      // this.player.poster(data.data.cover);
      console.log(this.player);
      // this.player.play()
    }
  },
  computed: {
    player() {
      return this.$refs.videoPlayer.player; //自定义播放
    }
  },
  watch: {
    videoSize: {
      handler(newValue, oldValue) {},
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.videoId = this.$route.query.videoId;
    this.projectId = this.$route.query.projectId;
    this.userId = window.localStorage.getItem("userId");
    this.init();
  }
};
</script>
<style scoped>
.revidew-offline {
  width: 100%;
  height: 100%;
  background: #dcdee2;
}
.review-header {
  height: 60px;
  line-height: 60px;
  background-color: #c0c0c0;
}
.user-box {
  margin-left: 20px;
  display: flex;
  align-items: center;
  height: 60px;
}
.offline-container {
  height: 100%;
  display: flex;
}
.left {
  height: 90.5%;
  width: 1000px;
  margin: 10px 80px;
  padding: 20px;
}
.videos {
  width: 100%;
  /*height:66%;*/
  display: flex;
  justify-content: center;
  margin-top: 14px;
}
.video-player {
  height: 100%;
  width: 70%;
  padding: 0 20px;
}
.comment-box {
  display: flex;
  justify-content: center;
  height: 160px;
  margin-top: 14px;
  position: relative;
}
.comment-input {
  margin: 10px 20px;
}
.operate-btns {
  position: absolute;
  bottom: 10px;
  right: 20px;
}
.operate-btn {
  margin-right: 27px;
  cursor: pointer;
  font-size: 20px;
}
.notation-box {
  margin-top: 10px;
  height: 90vh;
  width: 240px;
  background-color: #fafafa;
}
.notation-menus {
  background-color: red;
  height: 28px;
  line-height: 28px;
  display: flex;
  border-bottom: 1px solid black;
}
.notation-menus div {
  flex: 1;
  text-align: center;
}
.notation-menus div:first-child {
  border-right: 1px solid black;
}
.notation-content {
  height: 100%;
}
.notation-list {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.notation-item {
  margin-bottom: 2px;
  border-bottom: 1px solid #333;
}
.notation-user {
  display: flex;
}
.notation-content {
  min-height: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}
/*  */
[v-cloak] {
  display: none;
}
.mask {
  z-index: 101;
}
</style>
