//输入毫秒，转换为具体的天、小时、分钟、秒
export function secondFormatV2(v) {
    v = Number(v)
    let str = ''
    if (v > 0) {
        if (v < 60) {
            str = v + '秒'
        }
        else {
            let day = parseInt(v / 86400);
            let hour = parseInt((v % 86400) / 3600)
            let miniue = parseInt((v % 86400 % 3600) / 60)
            let second = parseInt(v % 86400 % 3600 % 60)
            str = `${day}天${hour}小时${miniue}分钟${second}秒`
        }
    }
    else {
        str = '0秒'
    }
    return str;
}

// 转换时间格式
export function getTime(time) {
    var date = new Date(time)
    var y = date.getFullYear()
    var m = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
    var d = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate())
    return y + '-' + m + '-' + d
}

/*判断是否是内网IP*/
export function isInnerIPFn() {
    // 获取当前页面url
    // //	#ifdef MP-WEIXIN
    // 	return false;
    // //	#endif
    var curPageUrl = window.location.href;
    // console.log('curPageUrl-0  '+curPageUrl);
    var reg1 = /(http|ftp|https|www):\/\//g;//去掉前缀
    curPageUrl = curPageUrl.replace(reg1, '');
    // console.log('curPageUrl-1  '+curPageUrl);
    var reg2 = /\:+/g;//替换冒号为一点
    curPageUrl = curPageUrl.replace(reg2, '.');
    // console.log('curPageUrl-2  '+curPageUrl);
    if (curPageUrl.substring(0, 9) == 'localhost') {
        console.log('是否是内网:' + true);
        return true;
    }
    curPageUrl = curPageUrl.split('.');//通过一点来划分数组
    var ipAddress = curPageUrl[0] + '.' + curPageUrl[1] + '.' + curPageUrl[2] + '.' + curPageUrl[3];
    var isInnerIp = false;//默认给定IP不是内网IP      
    var ipNum = getIpNum(ipAddress);
    /** 
     * 私有IP：A类  10.0.0.0    -10.255.255.255 
     *       B类  172.16.0.0  -172.31.255.255    
     *       C类  192.168.0.0 -192.168.255.255   
     *       D类   127.0.0.0   -127.255.255.255(环回地址)  
     **/
    var aBegin = getIpNum("10.0.0.0");
    var aEnd = getIpNum("10.255.255.255");
    var bBegin = getIpNum("172.16.0.0");
    var bEnd = getIpNum("172.31.255.255");
    var cBegin = getIpNum("192.168.0.0");
    var cEnd = getIpNum("192.168.255.255");
    var dBegin = getIpNum("127.0.0.0");
    var dEnd = getIpNum("127.255.255.255");
    isInnerIp = isInner(ipNum, aBegin, aEnd) || isInner(ipNum, bBegin, bEnd) || isInner(ipNum, cBegin, cEnd) || isInner(ipNum, dBegin, dEnd);
    console.log('是否是内网:' + isInnerIp);
    return isInnerIp;
}
/*获取IP数*/
function getIpNum(ipAddress) {
    var ip = ipAddress.split(".");
    var a = parseInt(ip[0]);
    var b = parseInt(ip[1]);
    var c = parseInt(ip[2]);
    var d = parseInt(ip[3]);
    var ipNum = a * 256 * 256 * 256 + b * 256 * 256 + c * 256 + d;
    return ipNum;
}

function isInner(userIp, begin, end) {
    return (userIp >= begin) && (userIp <= end);
}

