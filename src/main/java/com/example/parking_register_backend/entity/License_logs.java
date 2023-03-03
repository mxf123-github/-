package com.example.parking_register_backend.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.util.Date;
@TableName("license_logs")
public class License_logs {
    @TableId("licenseNum")
    private String licenseNum;

    private Date historyTime;//修改前时间
    private Date nowTime;//发生修改的时间
    private Date modifyTime;//修改后时间
    private String modifyType;//修改类型

    @Override
    public String toString() {
        return "License_logs{" +
                "licenseNum='" + licenseNum + '\'' +
                ", historyTime=" + historyTime +
                ", nowTime=" + nowTime +
                ", modifyTime=" + modifyTime +
                ", modifyType='" + modifyType + '\'' +
                '}';
    }

    public String getLicenseNum() {
        return licenseNum;
    }

    public void setLicenseNum(String licenseNum) {
        this.licenseNum = licenseNum;
    }

    public Date getHistoryTime() {
        return historyTime;
    }

    public void setHistoryTime(Date historyTime) {
        this.historyTime = historyTime;
    }

    public Date getNowTime() {
        return nowTime;
    }

    public void setNowTime(Date nowTime) {
        this.nowTime = nowTime;
    }

    public Date getModifyTime() {
        return modifyTime;
    }

    public void setModifyTime(Date modifyTime) {
        this.modifyTime = modifyTime;
    }

    public String getModifyType() {
        return modifyType;
    }

    public void setModifyType(String modifyType) {
        this.modifyType = modifyType;
    }
}
