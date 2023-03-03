<template>
    <div>
        <!-- 打开 Dialog 的按钮 -->
        <el-button type="primary" @click="dialogVisible = true">添加或者更新车牌</el-button>

        <!-- Dialog 组件 -->
        <!-- 使用 v-model 双向绑定 Dialog 的显示状态 -->
        <!-- 使用 :visible.sync 将 visible 属性双向绑定到 dialogVisible 变量上 -->
        <!-- 使用 :width 动态绑定 Dialog 的宽度 -->
        <el-dialog v-model="dialogVisible" title="添加或者更新车牌" :visible.sync="dialogVisible" width="90%">

            <el-input v-model="inputValue" placeholder="请填入车牌" style="width: 50%;" />
            <p />
            <el-form :model="form" :rules="rules" ref="form" style="margin-bottom: 5%;">
                <el-select v-model="form.range" placeholder="请选择日期范围" clearable >
                    <el-option v-for="option in options" :key="option.value" :label="option.label" :value="option.value">
                        <span style="float: left">{{ option.label }}</span>
                        <span style=" float: right; color: var(--el-text-color-secondary);font-size: 13px;">
                            {{ option.value }}
                        </span>
                    </el-option>
                </el-select>
            </el-form>
            <p />
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitForm('form')">确认</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
import axios from 'axios';
import * as func from '../../static/function.js'	//引入自己写的js功能
export default {
    data() {
        const currentYear = new Date().getFullYear();
        const nextYear = currentYear + 1;
        const afterYear = currentYear + 2;
        const tenYear = currentYear + 10;
        return {
            dialogVisible: false,
            inputValue: '',
            results: [],
            form: {
                range: '',
            },
            options: [
                { label: `${currentYear}上半年`, value: `${currentYear}-7-1` },
                { label: `${currentYear}下半年`, value: `${nextYear}-1-1` },
                { label: `${nextYear}上半年`, value: `${nextYear}-7-1` },
                { label: `${nextYear}下半年`, value: `${afterYear}-1-1` },
                { label: `十年至尊会员`, value: `${tenYear}-12-31` },
            ],
            rules: {
                range: [
                    // { required: true, message: '请选择日期范围', trigger: 'change' }
                ],
            }
        };
    },
    methods: {
        validateRange(rule, value, callback) {
            if (!value) {
                callback(new Error('请选择日期范围'));
            } else {
                callback();
            }
        },
        submitForm(formName) {
            const form = this.$refs[formName];
            form.validate((valid) => {
                if (valid) {
                    console.log('表单验证成功');
                    console.log('有效时间：', this.form.range);
                    this.inputValue = this.inputValue.replace(/\s+/g, "")
                    this.inputValue = this.inputValue.toUpperCase()
                    axios.post('/license/add_or_update/' + this.inputValue + '/' + this.form.range, { range: this.form.range })
                        .then(() => {
                            this.dialogVisible = false;
                            alert('提交成功');
                            location.reload();
                        })
                        .catch(() => {
                            alert('提交失败');
                        });
                } else {
                    console.log('表单验证失败');
                    return false;
                }
            });
        },
    },
};
</script>
  