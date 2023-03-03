<template>
    <view>
        <text>车牌号：{{ $store.state.licenseNum }}</text>
        <p></p>
        <text>您的可用时长：</text>
        <text :style="{ 'color': $store.state.timeColor }">{{ $store.state.time }}</text>
        <p></p>
        <text style="position:absolute;bottom:50px;right:10px">版本：{{ $store.state.version }}</text>
    </view>
</template>
<script>
import store from '../store/index.js';//需要引入store
export default {
    name: 'Info',
    props: {
    }
}
</script>