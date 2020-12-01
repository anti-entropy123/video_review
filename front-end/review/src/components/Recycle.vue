<template>
  <div class="recycle-container">
    <div class="no-recycle"  v-if="showList">
      暂无文件
    </div>
    <div v-else class="recycle-list">
      <el-card v-for="(video,index) in list" :key="index" class="recycle-item" >
        {{video}}
      </el-card>
    </div>
  </div>
</template>

<script>
    export default {
        name: "Recycle",
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
.recycle-container{
  position: relative;
  height: 100%;
}
  .no-recycle{
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
  .recycle-list{
    display: grid;
    grid-template-columns: repeat(4,25%);
    grid-template-rows: repeat(auto-fill,150px);
  }
  .recycle-item{
    margin: 10px;
  }
</style>
