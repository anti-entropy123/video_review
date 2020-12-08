<template>
  <div class="footer">
    <div class="footer-menus">
      <div class="contact-us">
        <p class="menu-title">联系我们</p>
        <p>地址：天津市津南区海河教育园区<br />雅观路135号天津大学北洋园校区</p>
        <p>电话：18722648040</p>
        <p>传真：022-69518735</p>
        <p>电子邮件：rlj1999@163.com</p>
      </div>
      <div class="service-menu footer-menu">
        <p class="menu-title">产品</p>
        <ul class="menu-items">
          <li><a href="#">产品介绍</a></li>
          <li><a href="#">小程序版</a></li>
          <li><a href="#">网页版</a></li>
        </ul>
      </div>
      <div class="service-menu footer-menu">
        <p class="menu-title">支持</p>
        <ul class="menu-items">
          <li><a href="#">预约演示</a></li>
        </ul>
      </div>
      <div class="service-menu footer-menu">
        <p class="menu-title">关于</p>
        <ul class="menu-items">
          <li><a href="#">关于我们</a></li>
          <li><a href="#">加入我们</a></li>

        </ul>
      </div>
      <div class="service-menu footer-menu">
        <p class="menu-title">帮助与支持</p>
        <ul class="menu-items">
          <li><a href="#">帮助中心</a></li>
          <li><a href="#">联系客服</a></li>
          <li><a href="#">文档资源</a></li>
        </ul>
      </div>
      <p class="icp-info">津ICP备5201314号</p>
      <p class="rights">&copy; 2020 MBRY</p>
      <div class="scroll-to-top">
        <a href="#"><i class="fas fa-chevron-up"></i></a>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Bottom"
  };
</script>

<style scoped>
  /* 底部信息 */
  .footer {
    margin-top: 0px;
    background-color: #181818;
    display: grid;
    justify-items: center;
    padding-top: 36px;
    padding-bottom: 24px;
  }
  .footer-menus {
    width: 100%;
    max-width: 1280px;
    display: grid;
    grid-template-columns: 2fr repeat(4, 1fr);
    padding: 0 80px;
    position: relative;
  }

  .menu-title {
    font-size: 16px;
    color: white;
    font-weight: 500;
    margin-bottom: 20px;
  }

  .contact-us {
    justify-self: start;
    color: #e7e9ec;
  }

  .contact-us p:not(:first-child) {
    padding-bottom: 16px;
  }

  .menu-items li {
    list-style: none;
    padding-bottom: 8px;
  }

  .menu-items li a {
    text-decoration: none;
    font-weight: 300;
    color: #fff;
  }

  .icp-info {
    margin-top: 24px;
    margin-bottom: 16px;
  }

  .icp-info,
  .rights {
    grid-column: 1 / -1;
    justify-self: center;
    color: white;
  }

  .scroll-to-top {
    display: none;
    position: relative;
    z-index: 300;
  }
  .scroll-to-top a {
    width: 32px;
    height: 32px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ff434f;
    color: #fff;
    text-decoration: none;
    position: fixed;
    bottom: 60px;
    right: 30px;
  }

  @media (max-width: 768px) {
    .footer-menus {
      padding: 0 40px;
    }

    .footer-menus {
      grid-template-columns: 2fr repeat(2, 1fr);
      row-gap: 24px;
    }

    .contact-us {
      grid-row: 1 / 3;
    }

    .footer-menus {
      text-align: right;
    }
  }

  @media (max-width: 576px) {
    .footer-menus {
      grid-template-columns: 1fr;
    }

    .footer-menus {
      justify-self: start;
      text-align: left;
    }
  }
</style>
