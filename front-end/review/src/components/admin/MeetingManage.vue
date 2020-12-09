<template>
  <el-container class="container">
   <h3 class="title">会议管理</h3>
    <el-main>
      <el-card class="search">
        搜索
        <br />
        <span>项目名称:</span>
        <el-input v-model="projectSearch" placeholder="输入项目名称">
          <el-button slot="append" @click="getManageMeeting">搜索</el-button>
        </el-input>
      </el-card>
      <el-card>
        <div class="shadow content">
          <el-row>
            <el-table
              :data="meetingTable"
              border
              stripe
              tooltip-effect="dark"
              style="width: 100%"
              @selection-change="handleSelectionChange"
            >
              >
              <el-table-column type="selection" width="40"></el-table-column>
              <el-table-column
                prop="onlineNum"
                label="会议号"
                align="center"
                width="120"
                :show-overflow-tooltip="true"
              ></el-table-column>
              <el-table-column align="center" prop="title" label="会议名" width="150"></el-table-column>
              <el-table-column prop="belongTo" label="属于" align="center" width="200"></el-table-column>

              <el-table-column prop="onlineNum" label="当前视频" align="center" width="200"></el-table-column>
              <el-table-column prop label="是否正在开会" align="center" width="200">true</el-table-column>

              <el-table-column prop="startTime" label="开始时间" align="center" width="150"></el-table-column>
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
import {Message} from 'element-ui';
export default {
  name: "MeetingManage",
  data() {
    return {
      meetingSearch: "",
      meetingTable: [],
        totalPage:10
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
    async getManageMeeting() {
      const { data: res } = await this.$http.get("admin/meetingManage");
      if (res.result === 1) {
       
        this.meetingTable = res.data.meetingList;
               this.totalPage = res.data.totalPage;
      } else {
        Message.error(res.message)
        
      }
    }
  },
  mounted() {
    this.getManageMeeting();
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
