<template>
  <div class="page">
    <h2>금 · 은 가격 추이</h2>

    <MetalFilterBar />

    <div v-if="store.loading">로딩 중...</div>

    <MetalEmptyState
      v-else-if="store.errorMessage || store.isEmpty"
      :message="store.errorMessage"
    />

    <MetalChart
      v-else
      :labels="store.labels"
      :prices="store.priceValues"
      :metal="store.metal"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMetalsStore } from '@/stores/metals'

import MetalFilterBar from '@/components/metals/MetalFilterBar.vue'
import MetalChart from '@/components/metals/MetalChart.vue'
import MetalEmptyState from '@/components/metals/MetalEmptyState.vue'

const store = useMetalsStore()

onMounted(() => {
  store.loadPrices()   // 최초 전체 조회
})
</script>

<style scoped>
.page {
  max-width: 900px;
  margin: 0 auto;
}
</style>
