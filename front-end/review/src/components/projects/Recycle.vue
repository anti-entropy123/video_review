<template>
  <div class="recycle-container">
    <div class="no-recycle"  v-if="showList">
      <p>暂无文件</p>
    </div>
    <div v-else class="recycle-list">
      <div
        v-for="(video, index) in recycleList"
        :key="video.videoId"
        class="video-item"
        ref="vv"
        @mousemove="updateXY"
      >
      <div class="video-cover-div"  @mouseover="mousein(video.coverList, index)">
        <el-image
          class="video-cover"
          :src="video.cover"
          fit="cover"
        >

        </el-image>
        </div>
        <div class="video-duration">{{video.duration| timeFormat}}</div>
        <div class="video-description">{{ video.videoName| videoNameFormat }}

        </div>
        <div class="video-time">{{
          video.createDate | dateFormat
          }}</div>
        <template>
          <el-popconfirm
            confirm-button-text='是'
            cancel-button-text='否'
            icon="el-icon-info"
            icon-color="blue"
            title="是否还原该视频？"
          >
            <i class="el-icon-more require-more" slot="reference"></i>
          </el-popconfirm>
        </template>

      </div>
    </div>
  </div>
</template>

<script>

  export default {
    name: "Recycle",
    props: {
      projectName: String
    },
    data(){
      return{
             x: 0,
      coverList: [],
      videoNum: 0,
      left: 0,
      right: 0,
        recycleList:[
          {
            coverList: [
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-0.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-1.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-2.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-3.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-4.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-5.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-6.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-7.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-8.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-9.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-10.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-11.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-12.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-13.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-14.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-15.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-16.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-17.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-18.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-19.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-20.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-21.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-22.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-23.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-24.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-25.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-26.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-27.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-28.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-29.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-30.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-31.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-32.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-33.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-34.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-35.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-36.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-37.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-38.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-39.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-40.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-41.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-42.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-43.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-44.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-45.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-46.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-47.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-48.jpg",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-49.jpg"
            ],
            "createDate": 1605513804.761238,
            "duration": 3600,
            "hasReview": 0,
            "videoId": "5fb23a0fa8601c6b5e3f3c3c",
            "videoName": "\u4e0b\u8f7d.mp4",
            cover:"https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review/cover/kiana-0.jpg"
            },
          {
            coverList: [
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-0.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-1.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-2.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-3.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-4.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-5.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-6.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-7.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-8.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-9.png"
            ],
            "createDate": 1605605163.8294027,
            "duration": 17,
            "hasReview": 0,
            "videoId": "5fb49fb066846c061a54d4c1",
            "videoName": "\u4e0b\u8f7d.mp4"
          },
          {
            coverList: [
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-0.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-1.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-2.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-3.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-4.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-5.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-6.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-7.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-8.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-9.png"
            ],
            "createDate": 1606632378.5890343,
            "duration": 17,
            "hasReview": 0,
            "videoId": "5fc385aa6d206f1f4afc317f",
            "videoName": "\u4e0b\u8f7d.mp4",
            cover:'https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-0.png'
          },
          {
            coverList: [
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-0.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-1.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-2.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-3.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-4.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-5.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-6.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-7.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-8.png",
              "https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-9.png"
            ],
            "createDate": 1606804792.7332563,
            "duration": 17,
            "hasReview": 0,
            "videoId": "5fc60ecf005d6175b95c40b7",
            "videoName": "\u4e0b\u8f7d.mp4",
            cover:'https://hexo-blog-1258787237.cos.ap-beijing.myqcloud.com/video_review//cover/\u4e0b\u8f7d.mp4-0.png'
          }
        ]

      }
    },
    computed:{
      showList() {
        return this.recycleList.length===0
      }
    },
    methods:{
          updateXY: function(event) {
      this.x = event.offsetX;
      let coverNum = Math.floor((this.x / (this.right - this.left)) * 10);
      // recycleList [index] 这一项cover赋值
      let img = new Image();
      img.src = this.coverList[coverNum];
      let that = this;
      img.onload = function() {
        that.recycleList[that.videoNum].cover = that.coverList[coverNum];
      };
    },
    mousein(coverList, index) {
      this.left = this.$refs.vv[index].getBoundingClientRect().left;
      this.right = this.$refs.vv[index].getBoundingClientRect().right;
      this.coverList = coverList;
      console.log(typeof(this.videoNum))
      this.videoNum = index;
       
    },
    }
  }
</script>

<style scoped>
  .recycle-container{
    position: relative;
  }
  .no-recycle{
    position: absolute;
    top:50%;
    left: 50%;
    width: 200px;
    height: 200px;
    transform: translate(-50%,-50%);
    border:2px dashed rgb(134, 161, 236);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .no-recycle p {
    font-size: 24px;
    color: rgb(107, 144, 236);
  }
  .recycle-list{
     width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-row-gap: 20px;
  grid-column-gap: 60px;
  padding:20px 50px;
  grid-template-rows: repeat(2, 200px);
  }

  .video-item {
    position: relative;
    border-radius: 10px;
    border:1px solid #333;
    overflow: hidden;
  }

  .video-item .video-duration{
    position: absolute;
    bottom: 52px;
    right: 0px;
    color: #fff;
    z-index: 9;
    width: 48px;
    text-align: center;
    background-color: #333;
    font-size: 10px;
    opacity: 90%;
  }

.video-item .video-cover-div {
  height: 146px;
  width: 280px;
  overflow: hidden;
}
.video-item .video-description {
  height: 44px;
  margin-top: 2px;
  margin-left: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
  .video-time{
    font-size: 9px;
    color:#333;
    position: absolute;
    bottom: 5px;
    left:5px;
  }
  .video-cover{
    cursor: pointer;
    transition: all 0.5s ease-in-out;
  }
  /* .video-cover:hover{
    transform: scale(1.1);
  } */
  .require-more {
    transform: rotate(90deg);
    position: absolute;
    right: 10px;
    bottom: 10px;
    cursor: pointer;
  }
</style>
