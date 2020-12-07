<template>
  <div>
    <div v-show="this.show" class="scroll-to-top">
      <a href="#">↑</a>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ScrollToTop",
    data() {
      return {
        show: false
      };
    },
    created() {
      window.addEventListener("scroll", () => {
        // 获取
        let scrollToTop = document.getElementsByClassName("toTop");

        if (window.pageYOffset > window.screen.height) {
          this.show = true;
        } else {
          this.show = false;
        }
      });
    },
    methods: {}
  };
</script>

<style scoped>
  .scroll-to-top {
    z-index: 300;
  }
  .scroll-to-top a {
    z-index: 150;
    width: 50px;
    height: 50px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffafb9;
    text-decoration: none;
    position: fixed;
    bottom: 45px;
    right: 30px;
    opacity: 80%;
  }
</style>
