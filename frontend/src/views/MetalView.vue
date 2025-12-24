<template>
  <div class="metal-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">금 · 은 가격 추이 차트</h1>
          <p class="page-subtitle">귀금속 시세를 한눈에 확인하세요</p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <MetalFilterBar />

      <!-- Loading State -->
      <div v-if="store.loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>데이터를 불러오는 중...</p>
      </div>

      <!-- Error / Empty State -->
      <MetalEmptyState
        v-else-if="store.errorMessage || store.isEmpty"
        :message="store.errorMessage"
      />

      <!-- Chart -->
      <div v-else class="chart-wrapper">
        <MetalChart
          :labels="store.labels"
          :prices="store.priceValues"
          :metal="store.metal"
        />
      </div>
    </main>
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
.metal-page {
  min-height: calc(100vh - 200px);
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 50%, #7469B6 100%);
  padding: 32px 24px;
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
  text-align: left;
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 60px;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  color: #71717a;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e4e4e7;
  border-top-color: #7469B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Chart Wrapper */
.chart-wrapper {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-top: 24px;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 32px 16px;
  }

  .main-content {
    padding: 24px 16px 40px;
  }

  .chart-wrapper {
    padding: 16px;
    border-radius: 16px;
  }
}

/* Dark Mode */
[data-theme="dark"] .metal-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #18181b 50%, #0f0f0f 100%);
}

[data-theme="dark"] .loading-state {
  color: #a1a1aa;
}

[data-theme="dark"] .loading-spinner {
  border-color: #3f3f46;
  border-top-color: #AD88C6;
}

[data-theme="dark"] .chart-wrapper {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
</style>
