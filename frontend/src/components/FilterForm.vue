<template>
    <Vueform :endpoint="endpoint">
        <TextElement name="searchClass" description="Filter by property class" placeholder="Class" :columns="{
            container: 4,
        }" />
        <TextElement name="searchAddress" description="Filter by address content" placeholder="Address" :columns="{
            container: 4,
        }" />
        <CheckboxgroupElement name="buildingUse" :items="[
            'Single Family',
            'Multi Family',
        ]" description="Building Use" :columns="{
        container: 4,
    }" />
        <StaticElement name="divider_1" tag="hr" />
        <SliderElement name="resultsLimit" :default="30" description="Numbe
r of Results per page" />
        <StaticElement name="divider" tag="hr" />
        <SliderElement name="marketValueRange" :default="[
            300000,
            2000000,
        ]" :min="100000" :max="3000000" :format="{ prefix: '$', thousand: ',', }" description="Estimated Market Value"
            :columns="{
                container: 6,
            }" />
        <SliderElement name="squareFeetRange" :default="[
            1000,
            5000,
        ]" :min="0" :max="20000" :format="{ thousand: ',', suffux: 'ft2' }" description="Building Ft2" :columns="{
        container: 6,
    }" />
        <ButtonElement name="submit" button-label="Apply Filter" align="center" :submits="true" />
    </Vueform>
</template>

<script>
export default {
    props: {
        endpoint: {
            type: Function,
            required: true
        }
    }
}
</script>