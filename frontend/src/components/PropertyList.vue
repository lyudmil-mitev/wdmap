<template>
  <div>
    <CollapsibleSection title="Filters">
      <FilterForm :endpoint="fetchProperties"></FilterForm>
    </CollapsibleSection>

    <CollapsibleSection title="Map">
      <PropertyMap v-if="markers.length" :markers="markers" :center="center" />
    </CollapsibleSection>

    <CollapsibleSection title="Property List">
      <table v-if="properties.length" class="property-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Full Address</th>
            <th>Class</th>
            <th>Building use</th>
            <th>Building ft<sup>2</sup></th>
            <th>Market Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prop, index) in properties" :key="prop.id"
            :class="{ 'odd-row': index % 2 === 0, 'even-row': index % 2 !== 0 }">
            <td>{{ prop.id }}</td>
            <td><strong><router-link :to="{ name: 'PropertyDetails', params: { id: prop.id } }" tag="tr">{{
              prop.full_address }}</router-link></strong></td>
            <td>{{ prop.class_description }}</td>
            <td>{{ prop.bldg_use }}</td>
            <td>{{ formatSquareFeet(prop.building_sq_ft) }}</td>
            <td>{{ formatUSD(prop.estimated_market_value) }}</td>
          </tr>
        </tbody>
      </table>

      <h3 v-else>No properties found</h3>
    </CollapsibleSection>
  </div>
</template>

<script>
import { onMounted, computed, ref } from 'vue'
import apiClient from '../api'
import PropertyMap from './PropertyMap.vue';
import { formatSquareFeet, formatUSD } from '../utils';
import FilterForm from './FilterForm.vue';
import CollapsibleSection from './CollapsibleSection.vue';

export default {
  name: 'PropertyList',
  components: {
    FilterForm,
    CollapsibleSection,
    PropertyMap
  },
  setup() {
    const properties = ref([])
    const markers = ref([])

    const fetchProperties = async (formData, form$) => {
      try {
        const response = await apiClient.get('/properties', {
          full_address: form$?.data.searchAddress || '',
          class_description: form$?.data.searchClass || '',
          bldg_use: form$?.data.buildingUse || [],
          estimated_market_value: form$?.data.marketValueRange || [300000, 2000000],
          building_sq_ft: form$?.data.squareFeetRange || [1000, 5000],
          limit: form$?.data.resultsLimit || 20,
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
      fetchProperties,
      formatSquareFeet,
      formatUSD,
      center
    }
  }
}
</script>

<style scoped>
.filters {
  padding: 1rem;
  background-color: #333;
  border-radius: 10px;
  margin: 0 1rem 1rem 1rem;
}

.property-table {
  width: 100%;
  border-collapse: collapse;
}

.property-table th,
.property-table td {
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