<template>
  <div>
    <h5>{{ product.kor_co_nm}} - {{ product.fin_prdt_nm }}</h5>
  </div>
</template>

<script setup>
  defineProps({
    product: Object
  })
</script>

<style scoped>

</style>