<template>
    <nav class="tab-bar">
      <router-link to="/Payment_page" class="tab-item" >
        <i class="icon"></i>
        <span>支付</span>
      </router-link>
      <router-link to="/" class="tab-item">
        <i class="icon"></i>
        <span>车库管理</span>
      </router-link>
    </nav>
  </template>
  
  
<script>
import { useRoute } from 'vue-router';
export default {
  name: 'TabBar',
  setup() {
    const route = useRoute();
    return {
      currentPath: route.path
    }
  }
}
</script>
  
<style>
.tab-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 50px;
    background-color: #fff;
    box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.2);
}

.tab-item {
  display: inline-block;
  padding: 10px 20px;
  font-size: 30px;
  text-align: center;
  color: #333;
  text-decoration: none;
}


</style>