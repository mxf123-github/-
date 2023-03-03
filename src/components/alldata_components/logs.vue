<template>
    <el-button type="primary" @click="dialogVisible = true, serachlogs()">最近删除和修改记录</el-button>
    <el-dialog v-model="dialogVisible" title="最近删除和修改记录" :visible.sync="dialogVisible" width="90%">
        <el-button-group class="ml-4">
            <el-button @click="serach_type_logs('新建')">新建</el-button>
            <el-button @click="serach_type_logs('更新')">更新</el-button>
            <el-button @click="serach_type_logs('删除')">删除</el-button>
            <el-button @click="serachlogs">全部</el-button>
        </el-button-group>
        <p />
        <el-table :data="logsData" stripe height="280">
            <el-table-column prop="licenseNum" label="车牌" width="70%"></el-table-column>
            <el-table-column prop="modifyType" label="修改类型" width="60%"></el-table-column>
            <el-table-column prop="historyTime" label="修改前有效时间" width="110%"></el-table-column>
            <el-table-column prop="modifyTime" label="修改后有效时间" width="110%"></el-table-column>
            <el-table-column prop="nowTime" label="发生修改的时间" width="110%"></el-table-column>
        </el-table>
    </el-dialog>
</template>
<script>
import axios from 'axios';
import * as func from '../../static/function.js'	//引入自己写的js功能
export default {
    data() {
        return {
            dialogVisible: false,
            logsData: [], // 表格数据
        }
    },
    mounted() {

    },
    methods: {
        serachlogs() {
            axios.get('/license_logs_all')
                .then(response => {
                    this.logsData = response.data
                    var i
                    for (i = 0; i < this.logsData.length; i++) {
                        this.logsData[i].historyTime = func.getTime(response.data[i].historyTime)
                        this.logsData[i].modifyTime = func.getTime(response.data[i].modifyTime)
                        this.logsData[i].nowTime = func.getTime(response.data[i].nowTime)
                    }
                    this.logsData.reverse();
                })
                .catch(error => {
                    console.log(error)
                })
        },
        serach_type_logs(type) {
            axios.get('/license_logs_type/' + type)
                .then(response => {
                    this.logsData = response.data
                    var i
                    for (i = 0; i < this.logsData.length; i++) {
                        this.logsData[i].historyTime = func.getTime(response.data[i].historyTime)
                        this.logsData[i].modifyTime = func.getTime(response.data[i].modifyTime)
                        this.logsData[i].nowTime = func.getTime(response.data[i].nowTime)
                    }
                    this.logsData.reverse();
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>