<template>
  <div>
    <section id="about-us" class="about-us">
      <h2 class="title-us">关于我们</h2>
      <div class="intro">
        <p>
          励志做一个超越分秒帧的视频审阅软件
        </p>
      </div>
      <div class="features">
        <div class="feature">
          <i class="fas fa-lightbulb"></i>
          <h4 class="feature-title">帧秒分</h4>
          <p class="feature-content">
            影音协作 从此无界
          </p>
        </div>
        <div class="feature">
          <i class="fas fa-chart-line"></i>
          <h4 class="feature-title">访问权限控制</h4>
          <p class="feature-content">
            项目权限管理,带密码的审阅链接
          </p>
        </div>
        <div class="feature">
          <i class="fas fa-shopping-cart"></i>
          <h4 class="feature-title">同步分享</h4>
          <p class="feature-content">
            用画笔在画面上标记问题点，精确到帧，团队成员可实时在线查看，并一键导出修改清单。还可以上传参考文件更清晰地表达想法。
          </p>
        </div>
        <div class="feature">
          <i class="fas fa-desktop"></i>
          <h4 class="feature-title">随时随地审片协作</h4>
          <p class="feature-content">
            无论在办公室还是移动状态，可随时通过小程序预览高清视频，进行审片协作。
          </p>
        </div>
        <div class="feature">
          <i class="fas fa-tachometer-alt"></i>
          <h4 class="feature-title">多版本管理</h4>
          <p class="feature-content">
            修改意见可记录可追溯，多版本便捷切换比对，方便审阅者和客户快速浏览确认，进度一目了然。
          </p>
        </div>
        <div class="feature">
          <i class="fas fa-server"></i>
          <h4 class="feature-title">极速传输</h4>
          <p class="feature-content">
            支持各种格式的行业常用文件，不仅提供项目团队共享的云端存储空间，也提供私人独享的云存储空间。
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    name: "AboutUs",
    mounted() {
      // 通用滑动出现动画配置项
          const staggeringOption = {
            delay: 300,
            distance: "50px",
            duration: 500,
            easing: "ease-in-out",
            origin: "bottom",
          };

      // interval设置等待时间
          ScrollReveal().reveal(".feature", { ...staggeringOption, interval: 350 });
    }
  };
</script>

<style scoped>
  section {
    /* 二维 */
    display: grid;
    /* 每个列的对齐方式 */
    justify-items: center;
    max-width: 1280px;
    padding: 0 80px;
  }
  /* 关于我们 */
  .about-us {
    padding-bottom: 32px;
  }

  .features {
    display: grid;
    /* 重复几次，重复的值  1fr：容器宽度的1/3*/
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 126px 126px;
    column-gap: 5vw;
  }

  .feature {
    display: grid;
    grid-template-areas:
      "icon title"
      "icon content";
    grid-template-columns: 60px 1fr;
    grid-template-rows: 1fr 3fr;
  }

  .feature i.fas {
    grid-area: icon;
    font-size: 34px;
    color: #ff434f;
  }

  .feature-title {
    grid-area: title;
    font-size: 18px;
    color: #2e2e2e;
  }

  .feature-content {
    grid-area: content;
    color: #8b8b8b;
    margin-top: 8px;
  }
  .title-us {
    font-size: 34px;
    color: #2e2e2e;
  }

  .title-us::after {
    content: "";
    display: block;
    width: 80%;
    height: 4px;
    background-color: #ff434f;
    margin-top: 14px;
    transform: translateX(10%);
  }
  .intro {
    margin: 28px 0 60px 0;
    /* text-indent: 2em; */
    font-size: 18px;
    color: #727272;
  }

  @media (max-width: 992px) {
    .features {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: unset;
    }
  }

  @media (max-width: 768px) {
    section {
      padding: 0 40px;
    }

    .features {
      grid-template-columns: 1fr;
    }
  }
</style>
