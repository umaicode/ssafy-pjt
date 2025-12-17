<template>
  <div>
    <h5>{{ deposit.kor_co_nm}} - {{ deposit.fin_prdt_nm }}</h5>
  </div>
</template>

<script setup>
  defineProps({
    deposit: Object
  })
</script>

<style scoped>

</style>