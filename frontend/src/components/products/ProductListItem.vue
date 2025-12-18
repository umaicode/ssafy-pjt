<template>
  <div>
    <h5>{{ product.kor_co_nm}} - {{ product.fin_prdt_nm }}</h5>
    <RouterLink :to="{name: 'ProductDetailView', params: {type, fin_prdt_cd: product.fin_prdt_cd}}">
      [DETAIL]
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
  defineProps({
    product: Object,
    type: String,
  })
</script>

<style scoped>

</style>