<template>
  <div>
    <h3>좋아요 목록</h3>

    <p v-if="!wishlistStore.wishlist.length">아직 좋아요한 상품이 없어요.</p>

    <div v-else>
      <ProductListItem
        v-for="item in wishlistStore.wishlist"
        :key="item.product_type + '_' + item.fin_prdt_cd"
        :product="item"
        :type="item.product_type"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useWishlistStore } from '@/stores/wishlist'
import ProductListItem from '@/components/ProductListItem.vue'

const wishlistStore = useWishlistStore()

onMounted(() => {
// 좋아요 메뉴 들어오면 내 목록 불러오기
  wishlistStore.getWishlist()
})
</script>
