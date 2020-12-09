<template>
  <el-container class="container">
      <h3 class="title">视频管理</h3>
    <el-main>
      <el-card class="search">
        搜索
        <br />
        <span>项目名称:</span>
        <el-input v-model="projectName" placeholder="输入项目名称">
          <el-button slot="append" @click="getManageVideo">搜索</el-button>
        </el-input>
        <span>上传用户:</span>
        <el-input v-model="videoOwner" placeholder="上传用户">
          <el-button slot="append" @click="getManageVideo">搜索</el-button>
        </el-input>
        <span>视频名称:</span>
        <el-input v-model="videoName" placeholder="上传用户">
          <el-button slot="append" @click="getManageVideo">搜索</el-button>
        </el-input>
      </el-card>
      <el-card>
        <div class="shadow content">
          <el-row>
            <el-table
              :data="videoTable"
              border
              stripe
              tooltip-effect="dark"
              style="width: 100%"
              @selection-change="handleSelectionChange"
            >
              >
              <el-table-column type="selection" width="40"></el-table-column>
              <el-table-column prop="videoName" label="视频名称" align="center" width="120"></el-table-column>
              <el-table-column align="center" prop="owner" label="项目人" width="150"></el-table-column>
              <el-table-column prop="belongTo" label="belongTo" align="center" width="150"></el-table-column>

              <el-table-column prop="videoUrl" label="videoUrl" align="center" width="200">
                      <template slot-scope="scope">
                        <el-image :src="scope.row.cover" style="width:200px" fit="cover" ></el-image>
                        </template>
              </el-table-column>
              <el-table-column prop="
comment" label="comment" align="center" width="200">true</el-table-column>

              <el-table-column label="操作" align="center" width="150">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="block" style="margin-left:20%">
              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page.sync="currentPage"
                :page-size="8"
                layout="prev, pager, next, jumper"
                :total="totalPage"
              ></el-pagination>
            </div>
          </el-row>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "VideoManage",
  data() {
    return {
      projectName: "",
      videoName: "",
      videoOwner: "",
      videoTable: [],
      currentPage: 1,
      totalPage: 1,
      username:''
    };
  },
  methods: {
    async getManageVideo() {
      const { data: res } = await this.$http.get("admin/videoManage",{
        params:{
          username:this.username,
          projectName:this.projectName,
          page: this.currentPage
        }

      });
      if (res.result === 1) {
        this.videoTable = res.data.videoList;
        this.totalPage = parseInt( res.data.totalPage);
      } else {
        Message.error(res.message)
      }
    },
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
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      this.getUser();
    },
  },
  mounted() {
    this.getManageVideo();
  }
};
</script>

<style scoped>
.container{
  display: flex;
  flex-direction: column;
    margin: 10px 0 0 20px;
}
.title {
  background-color: #fff;
  width: 100px;
  height: 36px;
  line-height: 36px;
  border-radius: 5px;
  text-align: center;
  font-size: 18px;
  font-family: Georgia, "Times New Roman", Times, serif;
}
.search {
  width: 100%;
  height: 120px;
  margin-right: 20px;
  margin-bottom: 20px;
}
.search .el-input {
  width: 240px;
}
</style>
