<template>
  <div class="detail-view" v-if="property">
    <div class="header">
      <div class="left-column">
        <button @click="goBack" class="back-button">← Back</button>
      </div>

      <div class="right-column">
        <h1>{{ property.full_address }}</h1>
        <h2>{{ property.class_description }}</h2>
      </div>
    </div>
    <CollapsibleSection title="Map">
      <PropertyMap :markers="[{ lat: property.latitude, lng: property.longitude, id: property.id }]"
        :center="{ lat: property.latitude, lng: property.longitude }" />
    </CollapsibleSection>

    <CollapsibleSection title="Details">
      <ul class="property-details">
        <li><strong>ID:</strong> {{ property.id }}</li>
        <li><strong>Class Description:</strong> {{ property.class_description }}</li>
        <li><strong>Prior Land Value:</strong> {{ property.pprior_land }}</li>
        <li><strong>Tax Code:</strong> {{ property.tax_code }}</li>
        <li><strong>City:</strong> {{ property.city }}</li>
        <li><strong>Attic Description:</strong> {{ property.attic_desc }}</li>
        <li><strong>Total Units:</strong> {{ property.units_tot }}</li>
        <li><strong>Appeal Result:</strong> {{ property.appeal_a_result }}</li>
        <li><strong>Current Land Value:</strong> {{ property.current_land }}</li>
        <li><strong>Prior Building Value:</strong> {{ property.pprior_building }}</li>
        <li><strong>Neighborhood:</strong> {{ property.neighborhood }}</li>
        <li><strong>Residential Type:</strong> {{ property.res_type }}</li>
        <li><strong>Air Conditioning:</strong> {{ property.ac }}</li>
        <li><strong>Multi Sale:</strong> {{ property.multi_sale }}</li>
        <li><strong>Latitude:</strong> {{ property.latitude }}</li>
        <li><strong>Longitude:</strong> {{ property.longitude }}</li>
        <!-- Add other properties here -->
      </ul>
    </CollapsibleSection>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../api'
import PropertyMap from '../components/PropertyMap.vue';
import CollapsibleSection from '../components/CollapsibleSection.vue';

export default {
  name: 'DetailView',
  props: {
    property: Object
  },
  components: {
    PropertyMap,
    CollapsibleSection
  },
  setup() {
    const property = ref(null)
    const route = useRoute()
    const router = useRouter()

    function goBack() {
      console.log("GO BACK")
      router.go(-1)
    }

    onMounted(async () => {
      if (property.value === null) {
        const id = route.params.id
        const response = await apiClient.get(`/properties/${id}`)
        property.value = response
      }
    })

    return {
      property,
      goBack
    }
  }

}

</script>

<style scoped>

.header {
  display: flex;
  align-items: center;
  margin: 1rem 0;
}

h1 {
  margin: 0;
}

h2 {
  margin-top: 0;
  color: #AAA;
  font-size: 100%;
}

.left-column {
  flex: 0 0 auto;
  padding-left: 3rem;
}
.right-column {
  flex: 1 1 auto;
  padding-left: 1rem;
  text-align: left;
}
.back-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #07bf9b;
}

.detail-view {
  padding: 20px;
}

.property-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  list-style-type: none;
  padding: 0;
}

.property-details li {
  display: flex;
  justify-content: space-between;
  padding: 0.25rem;
  border-bottom: 1px solid #ccc;
}

.property-details li:nth-child(odd) {
  background-color: #333;
}

.property-details li strong {
  margin-right: 10px;
}
</style>