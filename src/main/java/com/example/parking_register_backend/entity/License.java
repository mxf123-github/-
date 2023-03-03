package com.example.parking_register_backend.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.util.Date;

@TableName("license")
public class License {
    @TableId("licenseNum")
    private String licenseNum;
    private Date time;

    public String getLicenseNum() {
        return licenseNum;
    }

    public void setLicenseNum(String licenseNum) {
        this.licenseNum = licenseNum;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    @Override
    public String toString() {
        return "License{" +
                "licenseNum='" + licenseNum + '\'' +
                ", time=" + time +
                '}';
    }
}
