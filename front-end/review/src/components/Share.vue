<template>
<div class="share-container">
  <div class="no-share"  v-if="showList">
    暂无分享过的链接
  </div>
  <div v-else class="share-list">
    <el-card v-for="(share,index) in list" :key="index" class="share-item" >
      {{share}}
    </el-card>
  </div>
</div>
</template>

<script>
    export default {
        name: "Share",
      props:{
        list:Array
      },
      data(){
        return{

        }
      },
      computed:{
        showList() {
          return this.list.length===0
        }
      }
    }
</script>

<style scoped>
.share-container{
  position: relative;
  height: 100%;
}
  .no-share{
    position: absolute;
    top:50%;
    left: 50%;
    width: 200px;
    height: 200px;
    transform: translate(-50%,-50%);
    border: 1px dashed #8c939d;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .share-list{
    display: grid;
    grid-template-columns: repeat(4,25%);
    grid-template-rows: repeat(auto-fill,150px);
  }
  .share-item{
    margin: 10px;
  }
</style>
