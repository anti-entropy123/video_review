<template>
  <el-container class="container">
      <h3 class="title">项目管理</h3>
    <el-main>
      <el-card class="search">
        搜索
        <br />
        <span>项目名称:</span>
        <el-input v-model="projectName" placeholder="输入项目名称">
          <el-button slot="append" @click="getManageMeeting">搜索</el-button>
        </el-input>
        <span>创建者:</span>
        <el-input v-model="projectOwner" placeholder="项目创建者Name">
          <el-button slot="append" @click="getManageMeeting">搜索</el-button>
        </el-input>
      </el-card>
      <el-card>
        <div class="shadow content">
          <el-row>
            <el-table
              :data="projectTable"
              border
              stripe
              tooltip-effect="dark"
              style="width: 100%"
              @selection-change="handleSelectionChange"
            >
              >
              <el-table-column type="selection" width="40"></el-table-column>
              <el-table-column prop="projectName" label="项目名" align="center" width="120"></el-table-column>
              <el-table-column align="center" prop="owner" label="项目人" width="150"></el-table-column>
              <el-table-column prop="memberNum" label="成员数" align="center" width="80"></el-table-column>

              <el-table-column prop="videoNum" label="视频数" align="center" width="200">
                <template slot-scope="scope">
                  <el-button
                    type="text"
                    size="mini"
                    @click="showVideoDialog(scope.$index, scope.row.userId)"
                  >{{scope.row.videoNum}}</el-button>
                </template>
              </el-table-column>
              <el-table-column prop="meetingNum" label="会议数" align="center" width="200">
                <template slot-scope="scope">
                  <el-button
                    type="text"
                    size="mini"
                    @click="showMeetingDialog(scope.$index, scope.row.userId)"
                  >{{scope.row.meetingNum}}</el-button>
                </template>
              </el-table-column>

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
  name: "ProjectManage",
  data() {
    return {
      projectOwner: "",
      projectName: "",
      projectTable: [],
        totalPage:10,
        page:1,
    };
  },
  methods: {
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
    async getManageProject() {
      const { data: res } = await this.$http.get("admin/projectManage",{
        params:{
          projectName:this.projectName,
          owner:this.projectOwner,
          page:this.page
        }
      });
      if (res.result === 1) {
      
        this.projectTable = res.data.projectList;
               this.totalPage = res.data.totalPage;
      } else {
        Message.error(res.message)
      }
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    showVideoDialog(index, id) {
      // 通过userId获取video列表 展示video列表 每个列表6个 分页展示
      console.log(index, id);
    },
    showMeetingDialog(index, id) {
      // 通过userId获取项目列表 展示video列表 每个列表6个 分页展示
      console.log(index, id);
    }
  },
  mounted() {
    this.getManageProject();
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
