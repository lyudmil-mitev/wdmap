<template>
  <div>
    <h1>W &amp; D Property Browser</h1>
    <PropertyList />
  </div>
</template>

<script>
import PropertyList from '../components/PropertyList.vue';
import PropertyMap from '../components/PropertyMap.vue';

export default {
  name: 'HomeView',
  components: {
    PropertyList,
    PropertyMap
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>