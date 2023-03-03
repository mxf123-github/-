<template>
    <div>
        <input class="uni-input" focus placeholder="请输入您的车牌号(不区分大小写)" v-model="licenseNumInput" />
        <button :type="buttontype" @click="login()">登录</button>
    </div>
</template>

<script lang="js">
import store from '../store/index.js';//需要引入store
import * as func from '../static/function.js'	//引入自己写的js功能
import axios from 'axios';
export default {
    data() {
        return {
            licenseNumInput: "",
            buttontype: "primary",
        }
    },
    methods: {
        login() {
            var date;	//数据库存储的到期时间
            var day = 0;	//剩余存车天数
            this.licenseNumInput = this.licenseNumInput.replace(/\s+/g, "")
            this.licenseNumInput = this.licenseNumInput.toUpperCase()
            var licenseNum = this.licenseNumInput
            store.commit('setLicenseNum', licenseNum)
            //将修改后的车牌信息放入全局存储


            axios.get( '/license/getTime/' + licenseNum, {
            })
                .then(res => {
                    // console.log(res);
                    date = res.data[0];	//获取数据库到期时间
                    if (date != undefined) {
                        var UTC_DBTime = Date.parse(date.time);
                        // console.log("数据库存储时间毫秒数:"+UTC_DBTime);
                        // console.log("当前毫秒数:"+Date.parse(new Date));
                        var second = (UTC_DBTime - Date.parse(new Date)) / 1000;
                        var Precise_timing = func.secondFormatV2(second);
                        //参数为秒，输出具体剩余时间
                        // this.time=Precise_timing;
                        store.commit('setTime', Precise_timing)
                        //打印出精准时间
                        if (second / 60 / 60 / 24 >= 3) {
                            // this.timeColor='green';
                            store.commit('setTimeColor', 'green')
                        }
                        else {
                            // this.timeColor='red';
                            store.commit('setTimeColor', 'red')
                        }
                    }
                    if (this.licenseNumInput == 730119) {
                        // alert("欢迎管理员");
                        store.commit('setTime', "");
                        uni.navigateTo({
                            url: 'Admin/admin_page',
                        });
                    }
                    else if (date == undefined) {
                        alert("此车牌还未在车库停车");
                        store.commit('setTime', "");
                    }
                })
                .catch(error => {
                    console.error(error)
                })
        }
    },
}
</script>