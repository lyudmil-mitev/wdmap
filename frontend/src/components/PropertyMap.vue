<script setup>
import { GoogleMap, AdvancedMarker, InfoWindow, MarkerCluster } from 'vue3-google-map'
import { defineProps, onMounted, ref } from 'vue'
import apiClient from '../api';

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

/* TODO: Fetch markers from the currently visible area
const inactiveMarkers = ref([]);
onMounted(async () => {
  try {
    const response = await apiClient.getAll();
    inactiveMarkers.value = response.map(prop => ({ lat: prop.latitude, lng: prop.longitude, id: prop.id }));
  } catch (error) {
    console.error('Error fetching properties:', error)
  }
});
*/

</script>

<template>
  <GoogleMap :api-key="apiKey" style="width: 100%; height: 500px" :center="props.center" :zoom="15" mapId="DEMO_MAP_ID">
    <MarkerCluster>
      <AdvancedMarker v-for="(marker, index) in props.markers" :key="index"
        :options="{ position: marker, title: `Property id: ${marker.id}` }">
        <InfoWindow>
          <span style="color: black">Property id: {{ marker.id }}</span>
          <div style="color: black;">
            <router-link :to="{ name: 'PropertyDetails', params: { id: marker.id } }">
              Open detail page
            </router-link>
          </div>
        </InfoWindow>
      </AdvancedMarker>
    </MarkerCluster>
    <!-- TODO: show clusters below active markers
    <MarkerCluster>
      <AdvancedMarker v-for="(marker, index) in inactiveMarkers" :key="index"
        :options="{ position: marker, title: `Property id: ${marker.id}` }" :pin-options="{ background: 'gray' }">
        <InfoWindow>
          <span style="color: black">Property id: {{ marker.id }}</span>
        </InfoWindow>
      </AdvancedMarker>
    </MarkerCluster>
  -->
  </GoogleMap>
</template>