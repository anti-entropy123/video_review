<template>
  <el-container class="container">
    <h3 class="title">用户管理</h3>
    <el-main >
      <el-card class="shadow">
        
        <el-row :gutter="10" style="margin-top: 5px;margin-bottom:5px">
          
          <el-col :span="2">
            <div class="search_tag">userName:</div>
          </el-col>
          <el-col :span="4">
            <el-input
              placeholder="请输入内容"
              v-model="search_input_nickname"
              @keyup.enter.native="getSearch()"
              clearable
            >
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="getSearch()"
              ></el-button>
            </el-input>
          </el-col>

          <el-col :offset="1" :span="2">
            <div class="search_tag">手机号:</div>
          </el-col>
          <el-col :span="4">
            <el-input
              placeholder="请输入内容"
              v-model="search_input_mobileNumber"
              @keyup.enter.native="getSearch()"
              clearable
            >
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="getSearch()"
              ></el-button>
            </el-input>
          </el-col>
        </el-row>
      </el-card>
      <div class="shadow content">
        <el-row>
          <el-col :span="4" class="inner-title">用户信息</el-col>
        </el-row>
        <el-row>
          <el-table
            :data="userTable"
            border
            stripe
            tooltip-effect="dark"
            style="width: 100%"
            @selection-change="handleSelectionChange"
            size="mini"
          >
            >
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column
              prop="userId"
              label="userId"
              align="center"
              width="200"
              :show-overflow-tooltip="true"
            ></el-table-column>
            <el-table-column
              align="center"
              prop="avatar"
              label="头像"
              width="80"
            >
              <template slot-scope="scope">
                <el-avatar :src="scope.row.avatar"></el-avatar>
              </template>
            </el-table-column>
            <el-table-column
              prop="username"
              label="用户"
              align="center"
              width="150"
              :show-overflow-tooltip="true"
            ></el-table-column>

            <el-table-column
              prop="mobileNum"
              label="手机号"
              align="center"
              width="200"
            ></el-table-column>
            <el-table-column
              prop="uploadNum"
              label="上传视频数"
              align="center"
              width="120"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  @click="showVideoDialog(scope.$index, scope.row.userId)"
                  >{{ scope.row.uploadNum }}</el-button
                >
              </template>
            </el-table-column>
            <el-table-column
              prop="projectNum"
              label="参与项目数"
              align="center"
              width="120"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  @click="showProjectDialog(scope.$index, scope.row.userId)"
                  >{{ scope.row.projectNum }}</el-button
                >
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center" width="150">
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  @click="handleDelete(scope.$index, scope.row)"
                  >删除</el-button
                >
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
    </el-main>
    <el-dialog
      title="项目"
      :visible.sync="showProjectVisible"
      width="30%"
      @close="showProjectClose"
    >
      <!-- <el-table>

    </el-table> -->
    </el-dialog>
    <el-dialog
      title="会议"
      :visible.sync="showVideoVisible"
      width="30%"
      @close="showVideoClose"
    >
      <!-- <el-table>

    </el-table> -->
    </el-dialog>
  </el-container>
</template>

<script>
export default {
  name: "UserManage",
  mounted() {
    this.getUser();
  },
  data() {
    return {
      search_input_nickname: "",
      search_input_userId: "",
      search_input_mobileNumber: "",
      currentPage: 1,
      totalPage: 2,
      userTable: [],
      multipleSelection: [],
      showProject: {
        projectName: ""
      },
      showMeeting: {
        projectName: ""
      },
      showProjectVisible: false,
      showVideoVisible: false
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
    getSearch() {
      this.getUser();
    },
    async getUser() {
      const { data: res } = await this.$http.get(`/admin/userManage`, {
        params: {
          username: this.search_input_nickname,
          mobileNum: this.search_input_mobileNumber,
          page: this.currentPage
        }
      });
      if (res.result === 1) {
        this.userTable = res.data.userList;
       
        this.totalPage = parseInt(res.data.totalPage);
         
      } else {
        Message.error(res.message);
      }
      this.search_input_nickname = "";
      this.search_input_userId = "";
      this.search_input_mobileNumber = "";
    },
    showVideoDialog(index, id) {
      // 通过userId获取video列表 展示video列表 每个列表6个 分页展示
      console.log(index, id);
      this.showVideoVisible = true;
    },
    showProjectDialog(index, id) {
      // 通过userId获取项目列表 展示video列表 每个列表6个 分页展示
      console.log(index, id);
      this.showProjectVisible = true;
    },
    showProjectClose() {},
    showMeetingClose() {},
    showVideoClose(){

    }
  },
  computed: {}
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  margin: 10px 0 0 20px;
}
.title {
  background-color: #fff;
  width: 100px;
  height: 28px;
  line-height: 28px;
  border-radius: 5px;
  text-align: center;
  font-size: 18px;
  font-family: Georgia, "Times New Roman", Times, serif;
}
.shadow {
  box-shadow: 5px 5px 5px #c0c0c0;
  border-radius: 10px;
}

.content {
  margin-top: 10px;
  background-color: #fff;
  height: 620px;
  padding-top: 10px;
}
.inner-title {
  font-size: larger;
  margin-bottom: 10px;
  margin-left: 30px;
}
.search_btn {
  height: 32px;
  line-height: 32px;
  cursor: pointer;
  background-color: #f0f0f0;
  border-radius: 6px;
  display: inline-block;
  padding-right: 10px;
  padding-left: 10px;
}
.search_tag {
  height: 32px;
  line-height: 32px;
  text-align: center;
}
</style>
