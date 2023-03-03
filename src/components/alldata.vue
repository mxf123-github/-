<template>
    <div>
        <el-table :data="tableData" stripe height="250">
            <el-table-column prop="licenseNum" label="车牌" width=100></el-table-column>
            <el-table-column prop="time" label="有效时间" width=150></el-table-column>
            <el-table-column label="操作">
                <template #default="{ row }">
                    <Delete @click="handleDeleteClick(row)"
                        style="color:#B22222 ;width: 1em; height: 1em; margin-right: 10px" />
                    <Edit @click="handleModifyClick(row)" style="width: 1em; height: 1em; margin-right: 10px" />
                </template>
            </el-table-column>
        </el-table>
        <el-dialog v-model="deleteDialogVisible" title="删除车牌">
            <el-form :model="form">
                <el-form-item label="车牌" prop="licenseNum">
                    <el-input v-model="form.licenseNum"></el-input>
                </el-form-item>
            </el-form>

            <!-- 底部按钮 -->
            <template #footer="{}">
                <!-- 取消按钮 -->
                <el-button @click="handleCancelClick">取消</el-button>

                <!-- 确定按钮 -->
                <el-button @click="handleConfirmClick">确定</el-button>
            </template>
        </el-dialog>
        <p />
        <logs />
        <p />
        <add ref="add" />
    </div>

    <!-- 搜索模块，点击数字按钮立即搜索 -->
    <div>
        <p />
        <el-row>
            <el-input @input="db()" placeholder="搜索车牌"
                style="width:115px;margin-left:5px;margin-right:5px;margin-bottom: 5px;height:45px;" v-model="input">
            </el-input>
            <el-button type="info" plain class="num_button" @click="clear()">C</el-button>
        </el-row>
        <el-row>
            <el-button type="info" plain class="num_button" @click="get(1)">1</el-button>
            <el-button type="info" plain class="num_button" @click="get(2)">2</el-button>
            <el-button type="info" plain class="num_button" @click="get(3)">3</el-button>
        </el-row>
        <el-row>
            <el-button type="info" plain class="num_button" @click="get(4)">4</el-button>
            <el-button type="info" plain class="num_button" @click="get(5)">5</el-button>
            <el-button type="info" plain class="num_button" @click="get(6)">6</el-button>
        </el-row>
        <el-row>
            <el-button type="info" plain class="num_button" @click="get(7)">7</el-button>
            <el-button type="info" plain class="num_button" @click="get(8)">8</el-button>
            <el-button type="info" plain class="num_button" @click="get(9)">9</el-button>
        </el-row>
        <el-row>
            <el-button type="info" plain class="num_button" @click="get(0)">0</el-button>
            <el-button type="info" plain class="num_button" @click="del()" style="width:110px">←</el-button>
        </el-row>
    </div>
</template>
<style scoped>
div {
    font-size: 20px
}

.num_button {
    height: 45px;
    width: 50px;
    font-size: large;
    margin-left: 5px;
    margin-bottom: 5px;
}

el-table {
    height: 300px;
    /* 设置容器高度 */
    overflow: auto;
    /* 创建滚动条 */
}
</style>
<script>
import { ref } from 'vue'
import axios from 'axios'
import * as func from '../static/function.js'	//引入自己写的js功能
import add from './alldata_components/add2.vue'
import logs from './alldata_components/logs.vue'
export default {
    data() {
        return {
            tableData: [], // 表格数据
            deleteDialogVisible: false, // 删除对话框是否可见
            form: {}, // 表单数据
            input: ref(''),
        }
    },
    components: {
        add,
        logs,
    },
    provide() {
        return {
            showAdd: this.showAdd,
        };
    },
    mounted() {
        this.getAllLicenses()
    },
    methods: {
        showAdd(licenseNum) {
            // 调用子组件的方法
            this.$refs.add.dialogVisible = true;
            this.$refs.add.inputValue = licenseNum;
        },
        getAllLicenses() {
            axios.get('/licenses')
                .then(response => {
                    this.tableData = response.data
                    var i
                    for (i = 0; i < this.tableData.length; i++)
                        this.tableData[i].time = func.getTime(response.data[i].time)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        handleDeleteClick(row) {
            this.form = row; // 将点击的行数据赋值给表单数据
            this.deleteDialogVisible = true; // 显示删除对话框
        },
        handleCancelClick() {
            this.deleteDialogVisible = false; // 隐藏删除对话框
        },
        handleConfirmClick() {
            this.deleteLicense(this.form.licenseNum); // 调用删除方法并传入车牌号
        },
        handleModifyClick(row) {
            this.form = row;
            this.showAdd(this.form.licenseNum);
        },
        deleteLicense(licenseNum) {
            axios.post('/license/delete/' + licenseNum)
                .then(() => {
                    this.dialogVisible = false;
                    console.log('提交成功');
                    location.reload();
                })
                .catch(() => {
                    console.log('提交失败');
                });
        },
        get(buttonNumber) {
            this.input += buttonNumber
            this.db()
        },
        del() {
            this.input = this.input.substring(0, this.input.length - 1)
            this.db()
        },
        clear() {
            this.input = ''
            this.db()
        },
        db() {
            if (this.input != '') {
                this.input = this.input.toUpperCase();
                this.input = this.input.replace(/\s+/g, "");
                const response = axios.get('/license/search/' + this.input).then(response => {
                    this.tableData = response.data;
                    var i
                    for (i = 0; i < this.tableData.length; i++)
                        this.tableData[i].time = func.getTime(response.data[i].time)
                }).catch(error => {
                    console.error(error);
                })
            }
            else {
                this.getAllLicenses()
            }
        }
    }
}
</script>