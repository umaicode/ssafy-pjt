<template>
  <div class="my-product-section">
    <div class="section-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18"/>
          <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
        </svg>
      </div>
      <div class="header-text">
        <h2 class="section-title">금융상품 그래프</h2>
        <p class="section-description">AI 분석에서 선택한 상품들의 적립 시뮬레이션을 확인하세요</p>
      </div>
    </div>

    <!-- 선택된 상품이 없는 경우 -->
    <div v-if="!selectedProducts.length" class="chart-placeholder">
      <div class="placeholder-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M3 9h18"/>
          <path d="M9 21V9"/>
          <circle cx="15" cy="15" r="2"/>
        </svg>
      </div>
      <h3 class="placeholder-title">선택된 상품이 없습니다</h3>
      <p class="placeholder-text">
        AI 금융 분석에서 상품을 선택하면<br>
        이곳에서 월별 적립 시뮬레이션을 확인할 수 있어요.
      </p>
      <button class="go-analysis-btn" @click="goToAnalysis">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        AI 분석 하러가기
      </button>
    </div>

    <!-- 선택된 상품 목록 -->
    <div v-else class="products-container">
      <!-- 선택된 상품 카드 목록 -->
      <div class="selected-products">
        <div 
          v-for="product in selectedProducts" 
          :key="product.fin_prdt_cd"
          class="product-mini-card"
          :class="{ active: activeProduct?.fin_prdt_cd === product.fin_prdt_cd }"
          @click="setActiveProduct(product)"
        >
          <div class="mini-card-header">
            <span class="product-type-badge" :class="product.product_type">
              {{ product.product_type === 'deposit' ? '예금' : '적금' }}
            </span>
            <button class="remove-btn" @click.stop="removeProduct(product)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <h4 class="mini-card-name">{{ product.name }}</h4>
          <p class="mini-card-bank">{{ product.bank }}</p>
          <div class="mini-card-rate">
            <span class="rate-label">최고금리</span>
            <span class="rate-value">{{ product.intr_rate2 }}%</span>
          </div>
        </div>
      </div>

      <!-- 활성 상품 상세 시뮬레이션 -->
      <div v-if="activeProduct" class="simulation-section">
        <div class="simulation-header">
          <div class="sim-title-area">
            <h3 class="sim-title">{{ activeProduct.name }}</h3>
            <span class="sim-subtitle">{{ activeProduct.bank }} · {{ activeProduct.save_trm }}개월</span>
          </div>
          <div class="sim-rate-badge">
            연 {{ activeProduct.intr_rate2 }}%
          </div>
        </div>

        <!-- 월 납입액 입력 (적금인 경우) -->
        <div v-if="activeProduct.product_type === 'saving'" class="monthly-input-section">
          <label class="input-label">월 납입액 설정</label>
          <div class="input-wrapper">
            <input 
              type="number" 
              v-model.number="monthlyAmount"
              placeholder="300000"
              min="10000"
              step="10000"
            />
            <span class="input-suffix">원</span>
          </div>
        </div>

        <!-- 시뮬레이션 요약 -->
        <div class="simulation-summary">
          <div class="summary-item">
            <span class="summary-label">총 납입액</span>
            <span class="summary-value">{{ formatCurrency(simulationData.principal) }}</span>
          </div>
          <div class="summary-item highlight">
            <span class="summary-label">예상 이자 (세전)</span>
            <span class="summary-value">+{{ formatCurrency(simulationData.interest) }}</span>
          </div>
          <div class="summary-item total">
            <span class="summary-label">만기 수령액</span>
            <span class="summary-value">{{ formatCurrency(simulationData.total) }}</span>
          </div>
        </div>

        <!-- Chart.js 그래프 영역 -->
        <div class="chart-container" v-if="activeProduct.product_type === 'saving'">
          <div class="chart-header">
            <h4 class="chart-title">월별 누적 금액</h4>
          </div>
          <div class="chart-wrapper">
            <Line :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <!-- 예금인 경우 (목돈 예치) -->
        <div v-if="activeProduct.product_type === 'deposit'" class="deposit-notice">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <p>예금 상품은 목돈을 한번에 예치하는 방식입니다. 월별 적립 그래프 대신 만기 수익을 확인해주세요.</p>
        </div>
      </div>

      <!-- 전체 초기화 버튼 -->
      <button class="clear-all-btn" @click="clearAll">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
        </svg>
        전체 선택 초기화
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAnalysisStore } from '@/stores/analysis'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Chart.js 컴포넌트 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const router = useRouter()
const analysisStore = useAnalysisStore()

const selectedProducts = computed(() => analysisStore.selectedProducts)
const activeProduct = ref(null)
const monthlyAmount = ref(300000)

// 첫 번째 상품을 기본 활성화
watch(selectedProducts, (products) => {
  if (products.length > 0 && !activeProduct.value) {
    activeProduct.value = products[0]
    if (products[0].simulation?.monthlyDeposit) {
      monthlyAmount.value = products[0].simulation.monthlyDeposit
    }
  }
}, { immediate: true })

const setActiveProduct = (product) => {
  activeProduct.value = product
  if (product.simulation?.monthlyDeposit) {
    monthlyAmount.value = product.simulation.monthlyDeposit
  }
}

const removeProduct = (product) => {
  analysisStore.removeSelectedProduct(product.fin_prdt_cd, product.product_type)
  if (activeProduct.value?.fin_prdt_cd === product.fin_prdt_cd) {
    activeProduct.value = selectedProducts.value[0] || null
  }
}

const clearAll = () => {
  if (confirm('선택한 모든 상품을 초기화하시겠습니까?')) {
    analysisStore.clearSelectedProducts()
    activeProduct.value = null
  }
}

const goToAnalysis = () => {
  router.push('/analysis')
}

// 시뮬레이션 데이터 계산
const simulationData = computed(() => {
  if (!activeProduct.value) return { principal: 0, interest: 0, total: 0 }
  
  const product = activeProduct.value
  const months = parseInt(product.save_trm) || 12
  const rate = parseFloat(product.intr_rate2) / 100
  
  if (product.product_type === 'saving') {
    const monthly = monthlyAmount.value || 300000
    const principal = monthly * months
    const interest = Math.round(monthly * (months * (months + 1) / 2) * (rate / 12))
    return { principal, interest, total: principal + interest }
  } else {
    // 예금: 목돈 예치
    const principal = monthlyAmount.value || 10000000
    const interest = Math.round(principal * rate * (months / 12))
    return { principal, interest, total: principal + interest }
  }
})

// 월별 데이터 계산
const monthlyData = computed(() => {
  if (!activeProduct.value || activeProduct.value.product_type !== 'saving') return []
  
  const months = parseInt(activeProduct.value.save_trm) || 12
  const rate = parseFloat(activeProduct.value.intr_rate2) / 100
  const monthly = monthlyAmount.value || 300000
  
  const data = []
  for (let month = 1; month <= months; month++) {
    const principal = monthly * month
    const interest = Math.round(monthly * (month * (month + 1) / 2) * (rate / 12))
    data.push({
      month,
      principal,
      interest,
      total: principal + interest
    })
  }
  return data
})

// Chart.js 데이터
const chartData = computed(() => {
  const labels = monthlyData.value.map(d => `${d.month}개월`)
  const principalData = monthlyData.value.map(d => d.principal)
  const totalData = monthlyData.value.map(d => d.total)
  
  return {
    labels,
    datasets: [
      {
        label: '이자 포함 총액',
        data: totalData,
        borderColor: '#7469B6',
        backgroundColor: 'rgba(116, 105, 182, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#7469B6',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
      {
        label: '납입 원금',
        data: principalData,
        borderColor: '#E1AFD1',
        backgroundColor: 'rgba(225, 175, 209, 0.2)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#E1AFD1',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ]
  }
})

// Chart.js 옵션
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: 'index',
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12,
          weight: '600',
        }
      }
    },
    tooltip: {
      backgroundColor: '#18181b',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      cornerRadius: 8,
      titleFont: {
        size: 13,
        weight: '600',
      },
      bodyFont: {
        size: 12,
      },
      callbacks: {
        label: function(context) {
          const value = context.raw
          return `${context.dataset.label}: ${value.toLocaleString()}원`
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        font: {
          size: 11,
        },
        color: '#71717a',
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: '#f4f4f5',
      },
      ticks: {
        font: {
          size: 11,
        },
        color: '#71717a',
        callback: function(value) {
          if (value >= 10000000) {
            return (value / 10000000).toFixed(1) + '천만'
          } else if (value >= 10000) {
            return (value / 10000).toFixed(0) + '만'
          }
          return value
        }
      }
    }
  }
}))

const formatCurrency = (value) => {
  if (!value) return '0원'
  return value.toLocaleString() + '원'
}
</script>

<style scoped>
.my-product-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
}

.section-description {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

/* Placeholder */
.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: #fafafa;
  border: 2px dashed #e4e4e7;
  border-radius: 20px;
  text-align: center;
}

.placeholder-icon {
  width: 80px;
  height: 80px;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.placeholder-icon svg {
  width: 40px;
  height: 40px;
  color: #7469B6;
}

.placeholder-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 8px;
}

.placeholder-text {
  font-size: 0.9375rem;
  color: #71717a;
  line-height: 1.6;
  margin: 0 0 24px;
}

.go-analysis-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.go-analysis-btn svg {
  width: 18px;
  height: 18px;
}

.go-analysis-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

/* Products Container */
.products-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Selected Products */
.selected-products {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.product-mini-card {
  min-width: 200px;
  padding: 16px;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.product-mini-card:hover {
  border-color: #E1AFD1;
}

.product-mini-card.active {
  border-color: #7469B6;
  background: rgba(116, 105, 182, 0.05);
}

.mini-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.product-type-badge {
  padding: 4px 8px;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
}

.product-type-badge.deposit {
  background: #dbeafe;
  color: #2563eb;
}

.product-type-badge.saving {
  background: #dcfce7;
  color: #16a34a;
}

.remove-btn {
  width: 24px;
  height: 24px;
  background: #fee2e2;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn svg {
  width: 14px;
  height: 14px;
  color: #dc2626;
}

.remove-btn:hover {
  background: #fecaca;
}

.mini-card-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mini-card-bank {
  font-size: 0.8125rem;
  color: #71717a;
  margin: 0 0 12px;
}

.mini-card-rate {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e4e4e7;
}

.rate-label {
  font-size: 0.75rem;
  color: #71717a;
}

.rate-value {
  font-size: 1rem;
  font-weight: 800;
  color: #7469B6;
}

/* Simulation Section */
.simulation-section {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.simulation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.sim-title-area {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sim-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.sim-subtitle {
  font-size: 0.875rem;
  color: #71717a;
}

.sim-rate-badge {
  padding: 8px 16px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 12px;
}

/* Monthly Input */
.monthly-input-section {
  margin-bottom: 24px;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  margin-bottom: 8px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-wrapper input {
  flex: 1;
  max-width: 200px;
  padding: 12px 16px;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #7469B6;
}

.input-suffix {
  font-size: 1rem;
  font-weight: 600;
  color: #52525b;
}

/* Simulation Summary */
.simulation-summary {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(116, 105, 182, 0.05);
  border-radius: 16px;
  margin-bottom: 24px;
}

.summary-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-label {
  font-size: 0.8125rem;
  color: #71717a;
}

.summary-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
}

.summary-item.highlight .summary-value {
  color: #16a34a;
}

.summary-item.total .summary-value {
  font-size: 1.25rem;
  color: #7469B6;
}

/* Chart Container */
.chart-container {
  border: 1px solid #e4e4e7;
  border-radius: 16px;
  padding: 20px;
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.chart-wrapper {
  height: 300px;
}

/* Deposit Notice */
.deposit-notice {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #fef3c7;
  border-radius: 12px;
}

.deposit-notice svg {
  width: 20px;
  height: 20px;
  color: #d97706;
  flex-shrink: 0;
  margin-top: 2px;
}

.deposit-notice p {
  font-size: 0.875rem;
  color: #92400e;
  line-height: 1.5;
  margin: 0;
}

/* Clear All Button */
.clear-all-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  align-self: center;
}

.clear-all-btn svg {
  width: 18px;
  height: 18px;
}

.clear-all-btn:hover {
  background: #fecaca;
}

/* Dark Mode */
[data-theme="dark"] .section-title {
  color: #e4e4e7;
}

[data-theme="dark"] .section-description {
  color: #71717a;
}

[data-theme="dark"] .chart-placeholder {
  background: #18181b;
}

[data-theme="dark"] .placeholder-icon {
  background: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .placeholder-title {
  color: #e4e4e7;
}

[data-theme="dark"] .placeholder-text {
  color: #71717a;
}

[data-theme="dark"] .product-mini-card {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme="dark"] .product-mini-card:hover {
  border-color: #AD88C6;
}

[data-theme="dark"] .product-mini-card.active {
  background: rgba(116, 105, 182, 0.1);
  border-color: #7469B6;
}

[data-theme="dark"] .mini-card-name {
  color: #e4e4e7;
}

[data-theme="dark"] .mini-card-bank {
  color: #71717a;
}

[data-theme="dark"] .mini-card-rate {
  border-top-color: #3f3f46;
}

[data-theme="dark"] .rate-value {
  color: #E1AFD1;
}

[data-theme="dark"] .simulation-section {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .sim-title {
  color: #e4e4e7;
}

[data-theme="dark"] .sim-subtitle {
  color: #71717a;
}

[data-theme="dark"] .input-label {
  color: #a1a1aa;
}

[data-theme="dark"] .input-wrapper input {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .input-wrapper input:focus {
  border-color: #7469B6;
}

[data-theme="dark"] .input-suffix {
  color: #a1a1aa;
}

[data-theme="dark"] .simulation-summary {
  background: rgba(116, 105, 182, 0.1);
}

[data-theme="dark"] .summary-value {
  color: #e4e4e7;
}

[data-theme="dark"] .summary-item.total .summary-value {
  color: #E1AFD1;
}

[data-theme="dark"] .chart-container {
  border-color: #3f3f46;
}

[data-theme="dark"] .chart-title {
  color: #e4e4e7;
}

[data-theme="dark"] .deposit-notice {
  background: rgba(217, 119, 6, 0.1);
}

[data-theme="dark"] .deposit-notice p {
  color: #fbbf24;
}

[data-theme="dark"] .clear-all-btn {
  background: rgba(220, 38, 38, 0.1);
}

[data-theme="dark"] .clear-all-btn:hover {
  background: rgba(220, 38, 38, 0.2);
}
</style>
