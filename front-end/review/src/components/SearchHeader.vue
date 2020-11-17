<template>
    <div class="search-header">
      <span class="project-name">projectName</span>

      <span>3项,73.84MB</span>
      <el-input
        prefix-icon="el-icon-search"
        class="project-search"
      >
      </el-input>
      <el-select v-model="value" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <div>
        <i class="el-icon-s-operation"></i>
      </div>
    </div>
</template>

<script>
    export default {
      name: "SearchHeader",
      data(){
        return{
          options: [{
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
          value: ''
        }
      }
    }
</script>

<style scoped>
.search-header{
  display: flex;
}
  .project-search{
    width: 150px;
  }
  .project-name{
    flex: 1;
  }
</style>
