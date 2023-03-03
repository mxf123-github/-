package com.example.parking_register_backend.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.parking_register_backend.entity.License_logs;
import com.example.parking_register_backend.mapper.License_logsMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.List;

@RestController
@CrossOrigin
public class License_logsController {
    @Autowired
    License_logsMapper license_logsMapper;

    @PostMapping("/license_logs/{licenseNum}/{modifyType}/{modifyTime}/{historyTime}")
    //分别是车牌号，修改类型，修改后有效时间，修改前有效时间
    public void add_logs(@PathVariable("licenseNum") String licenseNum, //车牌号
                     @PathVariable("modifyType")String modifyType,    //修改类型
                     @PathVariable("modifyTime") @DateTimeFormat(pattern = "yyyy-MM-dd") Date modifyTime,   //修改后有效时间
                     @PathVariable("historyTime") @DateTimeFormat(pattern = "yyyy-MM-dd") Date historyTime  //修改前有效时间
    ) {
        // 获取当前时间
        LocalDateTime now = LocalDateTime.now();
        // 创建格式化器
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        // 格式化当前时间为字符串
        String nowStr = now.format(formatter);
        // 转换字符串为Timestamp对象
        Timestamp ts = Timestamp.valueOf(nowStr);
        Date nowTime=ts;   //发生修改的时间
        License_logs license_logs =new License_logs();
        license_logs.setLicenseNum(licenseNum);
        license_logs.setModifyTime(modifyTime);
        license_logs.setHistoryTime(historyTime);
        license_logs.setNowTime(nowTime);
        license_logs.setModifyType(modifyType);
        license_logsMapper.insert(license_logs);
    }
    @GetMapping("/license_logs_all")
    public List getLicense_logs(){
        List list = license_logsMapper.selectList(null);
        System.out.println(list);
        return list;
    }
    @GetMapping("/license_logs_type/{modifyType}")
    public List getLicense_logs_type(@PathVariable("modifyType")String modifyType){
        QueryWrapper queryWrapper = new QueryWrapper();
        queryWrapper.eq("modifyType",modifyType);
        List list = license_logsMapper.selectList(queryWrapper);
        return list;
    }
}
