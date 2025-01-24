<template>
  <div>

    <div class="filters">
    <h3>Filters</h3>
    <Vueform :endpoint="fetchProperties">
      <TextElement name="searchClass"
        description="Filter by property class" placeholder="Class" :columns="{
          container: 4,
        }" />
      <TextElement name="searchAddress"
        description="Filter by address content" placeholder="Address" :columns="{
          container: 4,
        }" />
      <CheckboxgroupElement name="buildingUse" :items="[
        'Single Family',
        'Multi Family',
      ]" description="Building Use" :columns="{
        container: 4,
      }" />
      <StaticElement name="divider_1" tag="hr" />
      <SliderElement name="resultsLimit" :default="30" description="Number of Results per page" />
      <StaticElement name="divider" tag="hr" />
      <SliderElement name="marketValueRange" :default="[
        300000,
        2000000,
      ]" :min="100000" :max="3000000" :format="{ prefix: '$', thousand: ',', }" description="Estimated Market Value" :columns="{
        container: 6,
      }" />
      <SliderElement name="squareFeetRange" :default="[
        1000,
        5000,
      ]"  :min="0" :max="20000" :format="{ thousand: ',', suffux: 'ft2' }" description="Building Ft2" :columns="{
        container: 6,
      }" />
      <ButtonElement name="submit" button-label="Apply Filter" align="center" :submits="true"/>
    </Vueform>
    </div>

    <PropertyMap v-if="markers.length" :markers="markers" :center="center" />

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
            <td><strong><router-link :to="{ name: 'PropertyDetails', params: { id: prop.id } }" tag="tr">{{ prop.full_address }}</router-link></strong></td>
            <td>{{ prop.class_description }}</td>
            <td>{{ prop.bldg_use }}</td>
            <td>{{ prop.building_sq_ft }}</td>
            <td>{{ prop.estimated_market_value }}</td>
        </tr>
      </tbody>
    </table>

    <h3 v-else>No properties found</h3>
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