<template>
  <div>
    <h3>금융상품 리스트</h3>
    <ProductListItem 
      v-for="product in items"
      :key="product.fin_prdt_cd"
      :product="product"
      :type="type"
    />
  </div>
</template>

<script setup>
  import ProductListItem from '@/components/products/ProductListItem.vue';
  import { useProductStore } from '@/stores/products';

  defineProps({
    items: Array,
    type: String
  })

  const store = useProductStore()
</script>

<style scoped>

</style>