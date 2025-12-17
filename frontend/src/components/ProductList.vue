<template>
  <div>
    <h3>금융상품 리스트</h3>
    <ProductListItem 
      v-for="product in items"
      :key="product.id"
      :product="product"
    />
  </div>
</template>

<script setup>
  import ProductListItem from '@/components/ProductListItem.vue';
  import { useProductStore } from '@/stores/products';

  defineProps({
    items: Array
  })
  
  const store = useProductStore()
</script>

<style scoped>

</style>