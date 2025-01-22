<template>
  <div>
    <PropertyMap v-if="markers.length" :markers="markers" :center="center" />
    <table v-if="properties.length" class="property-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Full Address<br />
            <input v-model="searchAddress" placeholder="filter address" @keyup.enter="fetchProperties" />
          </th>
          <th>Class<br />
            <input v-model="searchClass" placeholder="filter class" @keyup.enter="fetchProperties" />
          </th>
          <th>Building use</th>
          <th>Building ft<sup>2</sup></th>
          <th>Market Value</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(prop, index) in properties" :key="prop.id" :class="{'odd-row': index % 2 === 0, 'even-row': index % 2 !== 0}">
          <td>{{ prop.id }}</td>
          <td><strong>{{ prop.full_address }}</strong></td>
          <td>{{ prop.class_description }}</td>
          <td>{{ prop.bldg_use }}</td>
          <td>{{ prop.building_sq_ft }}</td>
          <td>{{ prop.estimated_market_value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { onMounted, computed, ref } from 'vue'
import apiClient from '../api'
import PropertyMap from './PropertyMap.vue';

export default {
  name: 'PropertyList',
  components: {
    PropertyMap
  },
  setup() {
    const properties = ref([])
    const markers = ref([])
    const searchAddress = ref('')
    const searchClass = ref('')

    const fetchProperties = async () => {
      try {
        const response = await apiClient.get('/properties', {
          full_address: searchAddress.value,
          class_description: searchClass.value,
          limit: 20,
          offset: 0
        })
        properties.value = response
        markers.value = response.map(prop => ({ lat: prop.latitude, lng: prop.longitude, id: prop.id }))
      } catch (error) {
        console.error('Error fetching properties:', error)
      }
    }

    const calculateCenter = (markers) => {
      if (markers.length === 0) {
        return { lat: 0, lng: 0 }
      }
      const total = markers.reduce((acc, marker) => {
        acc.lat += marker.lat
        acc.lng += marker.lng
        return acc
      }, { lat: 0, lng: 0 })
      return {
        lat: total.lat / markers.length,
        lng: total.lng / markers.length
      }
    }

    const center = computed(() => calculateCenter(markers.value))

    onMounted(() => {
      fetchProperties()
    })

    return {
      properties,
      markers,
      searchAddress,
      searchClass,
      fetchProperties,
      center
    }
  }
}
</script>

<style scoped>
.property-table {
  width: 100%;
  border-collapse: collapse;
}

.property-table th, .property-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.property-table th {
  background-color: #555;
  text-align: left;
}

.property-table .odd-row {
  background-color: #333;
}

.property-table .even-row {
  background-color: #000;
}
</style>