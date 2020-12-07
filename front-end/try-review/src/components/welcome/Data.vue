<template>
  <div>
    <section class="data-section">
      <div class="data-piece">
        <i class="fas fa-code"></i>
        <div class="num">9999</div>
        <div class="data-desc">行代码</div>
      </div>
      <div class="data-piece">
        <i class="fas fa-code"></i>
        <div class="num">288</div>
        <div class="data-desc">个奖项</div>
      </div>
      <div class="data-piece">
        <i class="fas fa-code"></i>
        <div class="num">156</div>
        <div class="data-desc">位客户</div>
      </div>
      <div class="data-piece">
        <i class="fas fa-code"></i>
        <div class="num">156</div>
        <div class="data-desc">个项目</div>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    name: "Data",
    mounted() {
      //   const dataSectionEl = document.querySelector(".data-section");
      //
      //   ScrollReveal().reveal(".data-section", {
      //     beforeReveal: () => {
      //       anime({
      //         targets: ".data-piece .num",
      //         innerHTML: (el) => {
      //           return [0, el.innerHTML];
      //         },
      //         duration: 1500,
      //         round: 1,
      //         easinge: "easeInExpo",
      //       });
      //       dataSectionEl.style.backgroundPosition =
      //         "center calc(50% - ${dataSectionEl.getBoundingClientRect().bottom/5}px)";
      //     },
      //   });
      // //判断是否在可见区域
      //   window.addEventListener("scroll", () => {
      //
      //     const bottom = dataSectionEl.getBoundingClientRect().bottom;
      //     const top = dataSectionEl.getBoundingClientRect.top;
      //     //判断是否在可见区域
      //     if (bottom >= 0 && top <= window.innerHeight) {
      //       dataSectionEl.style.backgroundPosition = "center calc(50% - ${bottom/5}px)";
      //     }
      //   });
    }
  };
</script>

<style scoped>
  /* 数据部分 */
  .data-section {
    max-width: unset;
    width: 100vw;
    height: 255px;
    background-image: url(../../../static/images/adult-business-computer-contemporary-380769.jpg);
    background-size: cover;
    background-position: center;
    display: grid;
    grid-template-columns: repeat(4, minmax(auto, 220px));
    justify-content: center;
    align-items: center;
    /* 子元素绝对定位时需要有相对的父级元素 */
    position: relative;
    z-index: 20;
  }

  .data-section::before {
    content: "";
    display: block;
    position: absolute;
    background-color: rgba(42, 42, 42, 0.7);
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .data-piece {
    width: 250px;
    display: grid;
    grid-template-rows: repeat(3, 1fr);
    justify-items: center;
    color: white;
    position: relative;
    z-index: 40;
  }

  .data-piece i.fas {
    font-size: 44px;
  }

  .data-piece .num {
    margin-top: 7px;
    font-size: 41px;
    font-weight: 600;
  }

  .data-piece .data-desc {
    font-size: 18px;
    font-weight: 500;
  }

  @media (max-width: 992px) {
    .data-section {
      grid-template-columns: repeat(2, minmax(200px, auto));
      padding: 24px 0;
      height: auto;
      row-gap: 24px;
      background-size: 200%;
    }
  }

  @media (max-width: 768px) {
    section {
      padding: 0 40px;
    }
    .data-section {
      grid-template-columns: 1fr;
      background-size: 300%;
    }
  }
</style>
