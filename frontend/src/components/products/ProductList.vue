<template>
  <div class="product-list">
    <div class="product-grid">
      <ProductListItem 
        v-for="product in items"
        :key="product.fin_prdt_cd"
        :product="product"
        :type="type"
      />
    </div>
  </div>
</template>

<script setup>
import ProductListItem from '@/components/products/ProductListItem.vue'

defineProps({
  items: Array,
  type: String
})
</script>

<style scoped>
.product-list {
  margin-bottom: 40px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}

/* Dark Mode */
[data-theme="dark"] .product-list {
  background: transparent;
}
</style>