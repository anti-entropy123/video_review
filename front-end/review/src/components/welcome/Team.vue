<template>
  <div>
    <section id="team-intro" class="team-intro section-bg">
      <h2 class="title-team">团队介绍</h2>
      <div class="team-members">
        <div class="team-member">
          <div class="profile-image">
            <img
              src="../../../static/images/yjn.jpg"
              alt=""
            />
          </div>
          <h4 class="name">尤嘉宁</h4>
          <p class="position">全栈工程师</p>
          <ul class="social-links">
            <li>
              <el-popover
                placement="top"
                width="400"
                trigger="hover">
                <el-image src="../../../static/images/code.jpg"></el-image>

                <el-button type="text" slot="reference">
                  <a href=""><i class="fab fa-weixin"></i></a></el-button>
              </el-popover>

            </li>
            <li>
              <el-popover
                placement="top"
                width="400"
                trigger="hover">
                <el-image src="../../../static/images/code.jpg"></el-image>

                <el-button type="text" slot="reference">
                  <a href=""><i class="fab fa-weibo"></i></a></el-button>
              </el-popover>

            </li>
            <li>
              <el-popover
                placement="top"
                width="400"
                trigger="hover">
                <el-image src="../../../static/images/code.jpg"></el-image>

                <el-button type="text" slot="reference">
                  <a href=""><i class="fab fa-github"></i></a></el-button>
              </el-popover>

            </li>
            <li>
              <el-popover
                placement="top"
                width="400"
                trigger="hover">
                <el-image src="../../../static/images/code.jpg"></el-image>

                <el-button type="text" slot="reference">
                  <a href=""><i class="fab fa-linkedin"></i></a></el-button>
              </el-popover>
            </li>
          </ul>
        </div>
        <div class="team-member">
          <div class="profile-image">
            <img
              src="../../../static/images/rlj.jpg"
              alt=""
            />
          </div>
          <h4 class="name">任林杰</h4>
          <p class="position">前端攻城狮</p>
          <ul class="social-links">
            <li>
              <a href="#"><i class="fab fa-weixin"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-weibo"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-github"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-linkedin"></i></a>
            </li>
          </ul>
        </div>
        <div class="team-member">
          <div class="profile-image">
            <img
              src="../../../static/images/selective-focus-photograph-of-man-wearing-gray-suit-jacket-1138903.jpg"
              alt=""
            />
          </div>
          <h4 class="name">鲍子龙</h4>
          <p class="position">前端攻城狮</p>
          <ul class="social-links">
            <li>
              <a href="#"><i class="fab fa-weixin"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-weibo"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-github"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-linkedin"></i></a>
            </li>
          </ul>
        </div>
        <div class="team-member">
          <div class="profile-image">
            <img
              src="../../../static/images/smiling-woman-wearing-black-sweater-1587009.jpg"
              alt=""
            />
          </div>
          <h4 class="name">满显凡</h4>
          <p class="position">架构师</p>
          <ul class="social-links">
            <li>
              <a href="#"><i class="fab fa-weixin"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-weibo"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-github"></i></a>
            </li>
            <li>
              <a href="#"><i class="fab fa-linkedin"></i></a>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    name: "Team"
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

  .title-team {
    font-size: 34px;
    color: #2e2e2e;
  }

  .title-team::after {
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
  /* 团队介绍 */
  .team-intro {
    margin-top: 48px;
    padding-top: 62px;
    padding-bottom: 52px;
  }

  .team-members {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    column-gap: 24px;
    margin-top: 86px;
  }

  .team-member {
    background-color: white;
    box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.2);
    text-align: center;
    padding-bottom: 28px;
    transition: 0.4s;
    display: grid;
    justify-items: center;
  }

  .profile-image {
    overflow: hidden;
  }

  .profile-image img {
    width: 100%;
    height: 264px;
    object-fit: cover;
    object-position: top center;
  }

  .team-member .name {
    margin-top: 18px;
    font-size: 18px;
    font-weight: 500;
    color: #494949;
  }

  .team-member .position {
    color: #727272;
    margin-top: 20px;
    margin-bottom: 18px;
  }

  .social-links {
    width: 100%;
    max-width: 200px;
    display: flex;
    justify-content: space-between;
    padding: 0 42px;
  }

  .social-links li {
    list-style: none;
  }

  .social-links li a {
    color: #8b8b8b;
    text-decoration: none;
  }

  .team-member:hover {
    transform: translateY(-20px) scale(1.05);
    box-shadow: 0px 0px 36px rgba(0, 0, 0, 0.1);
  }
  @media (max-width: 1100px) {
    .team-members {
      grid-template-columns: repeat(2, 1fr);
      row-gap: 36px;
      column-gap: 6vw;
    }
  }

  @media (max-width: 768px) {
    section {
      padding: 0 40px;
    }
    .team-members {
      grid-template-columns: minmax(200px, 400px);
    }
  }
</style>
