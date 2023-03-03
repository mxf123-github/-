<template>
    <div>
        <button @click="pay">微信支付</button>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            appId: '',  // 微信公众号AppId
            timeStamp: '',  // 时间戳，自1970年以来的秒数
            nonceStr: '',  // 随机字符串
            packageStr: '',  // 统一下单接口返回的 prepay_id 参数值，格式为：prepay_id=***
            signType: 'MD5',  // 签名算法类型，默认为MD5
            paySign: '',  // 签名
            orderId: '',  // 订单ID
            amount: '1',  // 支付金额
        }
    },
    methods: {
        async pay() {
            // 向后端请求支付信息
            const { data } = await axios.get('/api/pay', { params: { orderId: this.orderId, amount: this.amount } });
            const { appId, timeStamp, nonceStr, packageStr,prepayId, signType, paySign } = data;

            // 调用微信JSAPI支付接口
            window.WeixinJSBridge.invoke('getBrandWCPayRequest', {
                "appId": appId, // 公众号名称，由商户传入
                "timeStamp": timeStamp, // 时间戳，自1970年以来的秒数
                "nonceStr": nonceStr, // 随机串
                // "package": packageStr,
                "package": 'prepay_id=' + prepayId,
                "signType": signType, // 微信签名方式
                "paySign": paySign // 微信签名
            }, function (res) {
                if (res.err_msg == "get_brand_wcpay_request:ok") {
                    // 支付成功，跳转到成功页面
                    window.location.href = '/success';
                } else if (res.err_msg == "get_brand_wcpay_request:cancel") {
                    // 用户取消支付，提示用户
                    alert("用户取消支付");
                } else {
                    // 支付失败，提示用户
                    alert("支付失败，请稍后再试");
                }
            });
        }
    }
}
</script>
  