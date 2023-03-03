<template>
  <div id="app">
    <!-- <Info /> -->
    <!-- <TabBar /> -->
    <router-view />
  </div>
</template>

<script>
// import TabBar from './components/tabbar.vue'
// import Info from './components/info.vue'
export default {
  name: 'App',
  components: {
    // TabBar,
    // Info
  },
}
</script>

<style>
#app {
  height: 100%;
}
</style>
