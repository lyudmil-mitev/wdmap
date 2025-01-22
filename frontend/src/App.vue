<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { routeLocationKey } from 'vue-router';
import PropertyList from './components/PropertyList.vue'
import router from './router';
import PropertyMap from './components/PropertyMap.vue';

export default {
  name: 'App',
  components: {
    PropertyList,
    PropertyMap
  }
}
</script>

<style>
/* Add your styles here */
</style>