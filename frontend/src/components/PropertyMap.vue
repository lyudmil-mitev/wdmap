<script setup>
import { GoogleMap, AdvancedMarker } from 'vue3-google-map'
import { defineProps } from 'vue'

const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY

const props = defineProps({
  markers: {
    type: Array,
    required: true,
    default: () => []
  },
  center: {
    type: Object,
    required: true,
    default: () => ({ lat: 0, lng: 0 })
  }
})
</script>

<template>
  <GoogleMap
    :api-key="apiKey"
    style="width: 100%; height: 500px"
    :center="props.center"
    :zoom="15"
    mapId="DEMO_MAP_ID"
  >
    <AdvancedMarker v-for="(marker, index) in props.markers" :key="index" :options="{ position: marker }" />
  </GoogleMap>
</template>