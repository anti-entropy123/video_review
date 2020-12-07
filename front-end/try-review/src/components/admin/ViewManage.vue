<template>
    <el-container class="container">
    <h3 class="title">视图管睆</h3>

    </el-container>
</template>

<script>
    export default {
        name: "ViewManage",
        data(){
          return{
  totalPage:10
          }
        },
        methods:{
           toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleView(index, row) {
      console.log(index, row);
    },

    handleSizeChange(val) {
      console.log(`?? ${val} ?`);
    },
    handleCurrentChange(val) {
      this.getUser();
    },
        }
    }
</script>

<style scoped>
.container{
  display: flex;
  flex-direction: column;
    margin: 10px 0 0 20px;
}
.title{
  background-color: #fff;
  width: 100px;
  height: 36px;
  line-height: 36px;
  border-radius: 5px;
  text-align: center;
  font-size: 18px;
  font-family: Georgia, 'Times New Roman', Times, serif;
}
</style>
