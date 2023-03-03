package com.example.parking_register_backend.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.example.parking_register_backend.entity.License;
import com.example.parking_register_backend.mapper.LicenseMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@RestController
@CrossOrigin
public class LicenseController {
    @Autowired
    private LicenseMapper licenseMapper;
    @Autowired
    private License_logsController license_logsController;
    @GetMapping("/licenses")
    public List<License> getLicenses() {
        return licenseMapper.selectList(null);
    }

    @GetMapping("/license/{licenseNum}")
    public List getTime(@PathVariable("licenseNum")String licenseNum){
        QueryWrapper<License> wrapper = new QueryWrapper<>();
        wrapper.eq("license_num", licenseNum);
        return licenseMapper.selectList(wrapper);
//        return licenseMapper.selectByLicenseNum(licenseNum);
    }
    @PostMapping("/license/delete/{licenseNum}")
    public String delete(@PathVariable("licenseNum")String licenseNum){
        //记录删除前的有效时间
        QueryWrapper<License> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("licenseNum", licenseNum);
        Date historyTime=licenseMapper.selectOne(queryWrapper).getTime();

        int result=licenseMapper.delete(new QueryWrapper<License>().lambda().eq(License::getLicenseNum, licenseNum));
        if(result==0){
            return "not exist this data";
        }
        else{
            //删除的日志记录
            license_logsController.add_logs(licenseNum,"删除",historyTime,historyTime);
            return "delete "+licenseNum;
        }
    }
    @PostMapping("/license/add_or_update/{licenseNum}/{time}")
    public String add_or_update(@PathVariable("licenseNum") String licenseNum,@PathVariable("time") @DateTimeFormat(pattern = "yyyy-MM-dd") Date time){
        //添加或者更新，没有就添加，已经有就更新
        //查询是否存在这个车牌
        QueryWrapper<License> wrapper = new QueryWrapper<>();
        wrapper.lambda().eq(License::getLicenseNum, licenseNum);
        if(licenseMapper.selectCount(wrapper)!=0){
            //不为空，存在数据，进行更新操作

            //查询更新前该车牌的有效时间，记录日志
            QueryWrapper<License> queryWrapper = new QueryWrapper<>();
            queryWrapper.eq("licenseNum", licenseNum);
            Date historyTime=licenseMapper.selectOne(queryWrapper).getTime();
            license_logsController.add_logs(licenseNum,"更新",time,historyTime);

            UpdateWrapper<License> updateWrapper = new UpdateWrapper<>();
            updateWrapper.lambda().eq(License::getLicenseNum, licenseNum).set(License::getTime, time);
            licenseMapper.update(null,updateWrapper);
            return "update "+licenseNum+",time: "+time;
        }
        else{
            //不存在数据，创建新的数据
            License license=new License();
            license.setTime(time);
            license.setLicenseNum(licenseNum);
            license_logsController.add_logs(licenseNum,"新建",time,time);
            licenseMapper.insert(license);
            return "insert "+licenseNum+",time: "+time;
        }
    }
    @GetMapping("/license/search/{str}")
    public List<License> searchByString(@PathVariable("str")String str){
        QueryWrapper<License> queryWrapper = new QueryWrapper<>();
        queryWrapper.like("licenseNum", "%"+str+"%"); // 查询名字中包含“张”的用户
        List<License> userList = licenseMapper.selectList(queryWrapper); // 返回查询结果
        return userList;
    }

}
