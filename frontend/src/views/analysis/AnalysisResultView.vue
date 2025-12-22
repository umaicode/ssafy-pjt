<template>
  <div class="result-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">추천 결과</h1>
          <p class="page-subtitle">AI가 분석한 맞춤 금융상품입니다</p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Loading State -->
      <div v-if="analysisStore.loading" class="loading-state">
        <div class="loading-card">
          <div class="loading-spinner"></div>
          <p class="loading-title">분석 결과를 불러오는 중...</p>
          <span class="loading-text">잠시만 기다려주세요</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="analysisStore.error" class="error-state">
        <div class="error-card">
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <p class="error-title">오류가 발생했습니다</p>
          <span class="error-text">다시 시도해주세요</span>
          <button class="retry-btn" @click="goBack">다시 분석하기</button>
        </div>
      </div>

      <!-- Result Content -->
      <template v-else>
        <!-- Summary Card -->
        <div v-if="analysisStore.result?.summary" class="summary-card">
          <div class="summary-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <div class="summary-content">
            <h3 class="summary-title">AI 분석 요약</h3>
            <p class="summary-text">{{ analysisStore.result.summary }}</p>
          </div>
        </div>

        <!-- Results Count -->
        <div class="results-header">
          <h3 class="results-title">추천 상품</h3>
          <span class="results-count">{{ analysisStore.result?.items?.length || 0 }}개의 상품</span>
        </div>

        <!-- Product Cards -->
        <div class="product-grid">
          <ProductCard
            v-for="item in analysisStore.result?.items"
            :key="item.option_id"
            :item="item"
          />
        </div>

        <!-- Back Button -->
        <div class="action-area">
          <button class="back-btn" @click="goBack">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            다시 분석하기
          </button>
        </div>
      </template>
    </main>
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
.result-page {
  min-height: calc(100vh - 200px);
  background: linear-gradient(180deg, #faf5ff 0%, #f5f3ff 50%, #fafafa 100%);
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  padding: 40px 24px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.header-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}

/* Main Content */
.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 24px 60px;
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.loading-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e4e4e7;
  border-top-color: #9333ea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-title {
  font-size: 1rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 6px;
}

.loading-text {
  font-size: 0.875rem;
  color: #71717a;
}

/* Error State */
.error-state {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.error-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.error-icon {
  width: 64px;
  height: 64px;
  background: #fef2f2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.error-icon svg {
  width: 32px;
  height: 32px;
  color: #dc2626;
}

.error-title {
  font-size: 1rem;
  font-weight: 600;
  color: #18181b;
  margin: 0 0 6px;
}

.error-text {
  font-size: 0.875rem;
  color: #71717a;
  margin-bottom: 20px;
}

.retry-btn {
  padding: 12px 24px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(147, 51, 234, 0.35);
}

/* Summary Card */
.summary-card {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
  border-radius: 20px;
  margin-bottom: 32px;
  margin-top: -40px;
  position: relative;
}

.summary-icon {
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.summary-icon svg {
  width: 24px;
  height: 24px;
  color: #9333ea;
}

.summary-content {
  flex: 1;
}

.summary-title {
  font-size: 1rem;
  font-weight: 700;
  color: #7c3aed;
  margin: 0 0 8px;
}

.summary-text {
  font-size: 0.9375rem;
  color: #581c87;
  line-height: 1.6;
  margin: 0;
}

/* Results Header */
.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.results-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.results-count {
  font-size: 0.875rem;
  color: #71717a;
}

/* Product Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* Action Area */
.action-area {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #9333ea;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn svg {
  width: 20px;
  height: 20px;
}

.back-btn:hover {
  border-color: #9333ea;
  background: #faf5ff;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 32px 16px;
  }

  .main-content {
    padding: 24px 16px 40px;
  }

  .summary-card {
    flex-direction: column;
    gap: 16px;
  }

  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
