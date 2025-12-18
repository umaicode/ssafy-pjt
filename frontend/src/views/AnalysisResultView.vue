<template>
  <div>
    <h1>추천 결과</h1>

    <p v-if="analysisStore.loading">로딩 중...</p>
    <p v-if="analysisStore.error">에러가 발생했습니다.</p>

    <p v-if="analysisStore.result?.summary" class="summary">
      {{ analysisStore.result.summary }}
    </p>

    <div class="cards">
      <ProductCard
        v-for="item in analysisStore.result?.items"
        :key="item.option_id"
        :item="item"
      />
    </div>

    <button @click="goBack">다시 분석하기</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAnalysisStore } from '@/stores/analysis'
import ProductCard from '@/components/analysis/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const analysisStore = useAnalysisStore()
const token = localStorage.getItem('token')

onMounted(() => {
  analysisStore.fetchResult(route.params.id, token)
})

const goBack = () => {
  analysisStore.resetResult()
  router.push('/analysis')
}
</script>

<style scoped>
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}
.summary {
  font-weight: bold;
  margin-bottom: 16px;
}
</style>
