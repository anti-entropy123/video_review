<template>
  <header class="review-header">
    <div class="header-title fl">
      <span>{{ videoName }}</span>
    </div>
    <div class="fr">
      <div class="select-video">
        <el-select v-model="video" placeholder="更换视频">
          <el-option
            v-for="item in videos"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            @change="changeVideo"
          >
          </el-option>
        </el-select>
        <div v-if = "isOnline">
            <el-button>
                会议成员
            </el-button>
            <el-button>
                退出会议
            </el-button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
    name:'ReviewHeader',
  data() {
    return {
         videos: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        video: '选项1',
      videoName: "rlj",

    };
  },
  methods: {},
  mounted() {}
};
</script>

<style scoped>
.review-header{
     height: 60px;
     line-height: 60px;
     background-color: #333;
}
    </style>
