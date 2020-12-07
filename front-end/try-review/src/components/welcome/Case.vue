<template>
  <div>
    <section id="showcases" class="showcases section-bg">
      <h2 class="title-success">成功案例</h2>
      <div class="filter-btns">

      </div>
      <div class="cases">
        <div class="case-item web science">
          <img
            src="../../../static/images/gray-laptop-computer-showing-html-codes-in-shallow-focus-160107.jpg"
            alt=""
          />
        </div>
        <div class="case-item web science">
          <img
            src="../../../static/images/photo-of-imac-near-macbook-1029757.jpg"
            alt=""
          />
        </div>
        <div class="case-item web">
          <img
            src="../../../static/images/apple-laptop-notebook-office-39284.jpg"
            alt=""
          />
        </div>
        <div class="case-item web">
          <img
            src="../../../static/images/apple-apple-device-design-desk-285814.jpg"
            alt=""
          />
        </div>
        <div class="case-item mobile">
          <img
            src="../../../static/images/person-using-black-and-white-smartphone-and-holding-blue-230544.jpg"
            alt=""
          />
        </div>
        <div class="case-item science">
          <img
            src="../../../static/images/person-holding-a-smartphone-892757.jpg"
            alt=""
          />
        </div>
        <div class="case-item mobile web science">
          <img
            src="../../../static/images/blur-close-up-code-computer-546819.jpg"
            alt=""
          />
        </div>
        <div class="case-item mobile">
          <img
            src="../../../static/images/bokeh-photography-of-person-holding-turned-on-iphone-1440727.jpg"
            alt=""
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script>

  export default {
    name: "Case",
    created() {},
    mounted() {

  },
    data() {
      return {};
    },
    methods: {
      handleClick(data) {
        console.log(data);
      }
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
  .section-bg {
    position: relative;
  }
  .section-bg::before {
    content: "";
    display: block;
    position: absolute;
    background-color: #f9fbfb;
    width: 100vw;
    height: 100%;
    z-index: -1;
  }
  .title-success {
    font-size: 34px;
    color: #2e2e2e;
  }

  .title-success::after {
    content: "";
    display: block;
    width: 80%;
    height: 4px;
    background-color: #ff434f;
    margin-top: 14px;
    transform: translateX(10%);
  }
  /* 成功案例 */
  .showcases {
    max-width: unset;
    padding: 72px 0px 0px 0px;
  }

  .filter-btns {
    margin-top: 54px;
    margin-bottom: 38px;
  }

  .filter-btn {
    margin: 0 7px;
    background-color: #e3e3e3;
    border: 0;
    color: #727272;
    padding: 0 18px;
    height: 36px;
    line-height: 36px;
    line-height: 36px;
    border-radius: 4px;
    cursor: pointer;
    transition: 0.4s;
  }

  .filter-btn:focus,
  .filter-btn:active {
    outline: none;
  }

  .filter-btn.active,
  .filter-btn:hover {
    background-color: #ff434f;
    color: white;
  }

  .showcases .cases {
    width: 100vw;
    display: grid;

    grid-template-columns:repeat(4,1fr) ;
  }

  .showcases .case-item {
    width: 25vw;
    height: 20vw;
    overflow: hidden;
  }

  .case-item img {
    height: 100%;
    object-fit: cover;
  }

  @media (max-width: 992px) {
    .showcases .case-item {
      width: calc(100vw / 3);
    }
  }

  @media (max-width: 768px) {
    .showcases .case-item {
      width: calc(100vw / 2);
      height: 30vw;
    }
  }

  @media (max-width: 576px) {
    .showcases .case-item {
      width: 100vw;
      height: 60vw;
    }
  }
</style>
