<template>
  <div class="welcome-container">
    <Header></Header>
    <div id="home" class="glide">
      <div class="glide__track" data-glide-el="track">
        <div class="glide__slides">
          <!-- 轮播图一 -->
          <div class="glide__slide">
            <div class="slide-caption left">
              <h1>云时代音视频生产协助工具</h1>
              <h3>持极速传输的审片协作神器</h3>
              <button class="explore-btn" @click="goHome">探索更多</button>
            </div>
            <div class="backdrop"></div>
            <img src="../../static/images/people-in-couch-1024248.jpg">
          </div>
          <div class="glide__slide">
            <div class="slide-caption left">
              <h1>云时代音视频生产协助工具</h1>
              <h3>支持极速传输的审片协作神器</h3>
              <button class="explore-btn" @click="goHome">探索更多</button>
            </div>
            <div class="backdrop"></div>
            <img src="../../static/images/people-in-couch-1024248.jpg">
            <!-- <video
              src="../../static/videos/working-man.mp4"
              muted
              autoplay
              loop
            ></video> -->
          </div>
        </div>
        <div class="glide__arrows" data-glide-el="controls">
          <button class="glide__arrow glide__arrow--left" data-glide-dir="<">
            <i class="fa fa-angle-left"></i>
          </button>
          <button class="glide__arrow glide__arrow--right" data-glide-dir=">">
            <i class="fa fa-angle-right"></i>
          </button>
          <div class="glide__bullets" data-glide-el="controls[nav]">
            <button class="glide__bullet" data-glide-dir="=0"></button>
            <button class="glide__bullet" data-glide-dir="=1"></button>
          </div>
        </div>
      </div>
    </div>
    <div class="content-wrapper">
      <about-us></about-us>
      <Case></Case>
      <Team></Team>
      <Data></Data>
    </div>
    <Bottom></Bottom>
    <ScrollToTop></ScrollToTop>
  </div>
</template>

<script>
import Header from "../components/welcome/Header";
import Bottom from "../components/welcome/Bottom";
import ScrollToTop from "../components/welcome/ScrollToTop";
import AboutUs from "../components/welcome/AboutUs";
import Team from "../components/welcome/Team";
import Data from "../components/welcome/Data";
import Case from "../components/welcome/Case";
export default {
  name: "Welcome",
  components: {
    Header,
    Bottom,
    ScrollToTop,
    AboutUs,
    Team,
    Data,
    Case
  },

  data() {
    return {};
  },
  mounted() {

  },
  methods: {
    goHome(){
      this.$router.push('/')
    }
  }
};
</script>

<style scoped>

/* 轮播图 */
.glide {
  position: relative;
  top: -80px;
  z-index: 50;
}
.glide__slide img,
.glide__slide video {
  width: 100vw;
  height: 100vh;
  /* 自动等比例缩放 */
  object-fit: cover;
}
.slide-caption {
  position: absolute;
  z-index: 100;

  color: #e7e9ec;
  text-align: center;
  max-width: 60vw;
}

.glide__slide {
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-caption h1 {
  font-size: 54px;
  font-weight: 600;
}

.slide-caption h3 {
  font-size: 24px;
  margin: 48px 0px;
}

.slide-caption.left {
  max-width: 80vw;
  text-align: left;
}

.backdrop {
  background: rgba(42, 42, 42, 0.7);
  z-index: 60;
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  opacity: 0.3;
}
.slide-caption > * {
  opacity: 0;
}
.explore-btn {
  padding: 14px 32px;
  background-color: #ff434f;
  border: 0;
  border-radius: 4px;
  color: #e7e9ec;
  font-size: 18px;
  cursor: pointer;
  outline: none;
}
.content-wrapper {
  /* 一维排版 */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 98.9%;
}

@media (max-width: 992px) {
  .slide-caption h1 {
    font-size: 48px;
  }

  .slide-caption h3 {
    font-size: 18px;
  }
}

@media (max-width: 576px) {
  .slide-caption h1 {
    font-size: 28px;
  }

  .slide-caption h3 {
    font-size: 14px;
  }

  .explore-btn {
    font-size: 14px;
    padding: 8px 18px;
  }
}
</style>
