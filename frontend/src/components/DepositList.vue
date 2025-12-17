<template>
  <div>
    <h3>금융상품 리스트</h3>
    <DepositListItem 
      v-for="deposit in store.products"
      :key="deposit.id"
      :deposit="deposit"
    />
  </div>
</template>

<script setup>
  import DepositListItem from '@/components/DepositListItem.vue';
  import { useProductStore } from '@/stores/products';

  const store = useProductStore()
</script>

<style scoped>

</style>