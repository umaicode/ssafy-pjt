<template>
  <div class="stock-detail">
    <!-- Stock Header -->
    <div class="detail-header">
      <div class="stock-main-info">
        <h2 class="stock-name">{{ stock.name }}</h2>
        <div class="stock-meta">
          <span class="stock-symbol">{{ stock.symbol }}</span>
          <span v-if="stock.exchange" class="stock-exchange">{{ stock.exchange }}</span>
          <span v-if="stock.sector" class="stock-sector">{{ stock.sector }}</span>
        </div>
      </div>

      <div class="price-info">
        <span class="current-price">{{ formatPrice(stock.current_price, stock.currency) }}</span>
        <div v-if="stock.change !== null" :class="['price-change', changeClass]">
          <svg v-if="stock.change > 0" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7 14l5-5 5 5H7z"/>
          </svg>
          <svg v-else-if="stock.change < 0" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7 10l5 5 5-5H7z"/>
          </svg>
          <span>{{ formatChange(stock.change) }} ({{ formatPercent(stock.change_percent) }})</span>
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="chart-header">
        <h3>가격 차트</h3>
        <div class="period-buttons">
          <button 
            v-for="period in periods" 
            :key="period.value"
            :class="['period-btn', { active: currentPeriod === period.value }]"
            @click="$emit('change-period', period.value)"
          >
            {{ period.label }}
          </button>
        </div>
      </div>

      <div v-if="chartLoading" class="chart-loading">
        <div class="loading-spinner"></div>
      </div>

      <div v-else-if="chartData && chartData.data?.length > 0" class="chart-container">
        <StockChart :data="chartData.data" :currency="stock.currency" />
      </div>

      <div v-else class="chart-empty">
        <p>차트 데이터가 없습니다.</p>
      </div>
    </div>

    <!-- Stock Stats -->
    <div class="stats-section">
      <h3>주요 지표</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">시가</span>
          <span class="stat-value">{{ formatPrice(stock.open_price, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">전일 종가</span>
          <span class="stat-value">{{ formatPrice(stock.previous_close, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">고가</span>
          <span class="stat-value">{{ formatPrice(stock.day_high, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">저가</span>
          <span class="stat-value">{{ formatPrice(stock.day_low, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">52주 최고</span>
          <span class="stat-value">{{ formatPrice(stock.fifty_two_week_high, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">52주 최저</span>
          <span class="stat-value">{{ formatPrice(stock.fifty_two_week_low, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">거래량</span>
          <span class="stat-value">{{ formatNumber(stock.volume) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">평균 거래량</span>
          <span class="stat-value">{{ formatNumber(stock.avg_volume) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">시가총액</span>
          <span class="stat-value">{{ formatMarketCap(stock.market_cap, stock.currency) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">PER</span>
          <span class="stat-value">{{ stock.pe_ratio ? stock.pe_ratio.toFixed(2) : '-' }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">EPS</span>
          <span class="stat-value">{{ stock.eps ? stock.eps.toFixed(2) : '-' }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">배당수익률</span>
          <span class="stat-value">{{ stock.dividend_yield ? (stock.dividend_yield * 100).toFixed(2) + '%' : '-' }}</span>
        </div>
      </div>
    </div>

    <!-- Company Description -->
    <div v-if="stock.description" class="description-section">
      <h3>기업 소개</h3>
      <p class="description-text">{{ stock.description }}</p>
      <a v-if="stock.website" :href="stock.website" target="_blank" class="website-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
          <polyline points="15 3 21 3 21 9"/>
          <line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
        공식 웹사이트 방문
      </a>
    </div>

    <!-- News Section -->
    <div v-if="news && news.length > 0" class="news-section">
      <h3>관련 뉴스</h3>
      <div class="news-list">
        <a 
          v-for="item in news" 
          :key="item.link"
          :href="item.link"
          target="_blank"
          class="news-item"
        >
          <div class="news-content">
            <h4 class="news-title">{{ item.title }}</h4>
            <div class="news-meta">
              <span v-if="item.publisher" class="news-publisher">{{ item.publisher }}</span>
            </div>
          </div>
          <svg class="news-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import StockChart from './StockChart.vue'

const props = defineProps({
  stock: {
    type: Object,
    required: true
  },
  chartData: {
    type: Object,
    default: null
  },
  chartLoading: {
    type: Boolean,
    default: false
  },
  news: {
    type: Array,
    default: () => []
  }
})

defineEmits(['change-period'])

const periods = [
  { label: '1일', value: '1d' },
  { label: '5일', value: '5d' },
  { label: '1개월', value: '1mo' },
  { label: '3개월', value: '3mo' },
  { label: '6개월', value: '6mo' },
  { label: '1년', value: '1y' },
]

const currentPeriod = computed(() => props.chartData?.period || '1mo')

const changeClass = computed(() => {
  if (props.stock.change > 0) return 'positive'
  if (props.stock.change < 0) return 'negative'
  return 'neutral'
})

const formatPrice = (price, currency) => {
  if (price === null || price === undefined) return '-'
  
  const currencyCode = currency || 'USD'
  
  if (currencyCode === 'KRW') {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0
    }).format(price)
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currencyCode,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(price)
}

const formatChange = (change) => {
  if (change === null || change === undefined) return '-'
  const prefix = change > 0 ? '+' : ''
  return `${prefix}${change.toFixed(2)}`
}

const formatPercent = (percent) => {
  if (percent === null || percent === undefined) return '-'
  const prefix = percent > 0 ? '+' : ''
  return `${prefix}${percent.toFixed(2)}%`
}

const formatNumber = (num) => {
  if (num === null || num === undefined) return '-'
  return new Intl.NumberFormat().format(num)
}

const formatMarketCap = (cap, currency) => {
  if (cap === null || cap === undefined) return '-'
  
  const trillion = 1000000000000
  const billion = 1000000000
  const million = 1000000
  
  let value, suffix
  
  if (cap >= trillion) {
    value = cap / trillion
    suffix = '조'
  } else if (cap >= billion) {
    value = cap / billion
    suffix = currency === 'KRW' ? '억' : 'B'
  } else if (cap >= million) {
    value = cap / million
    suffix = currency === 'KRW' ? '백만' : 'M'
  } else {
    return formatNumber(cap)
  }
  
  return `${value.toFixed(2)}${suffix}`
}
</script>

<style scoped>
.stock-detail {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

/* Detail Header */
.detail-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 28px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 20px;
}

.stock-main-info {
  color: white;
}

.stock-name {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.stock-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.stock-symbol,
.stock-exchange,
.stock-sector {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  backdrop-filter: blur(10px);
}

.price-info {
  text-align: right;
  color: white;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  display: block;
  margin-bottom: 8px;
}

.price-change {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  font-size: 16px;
  font-weight: 500;
}

.price-change svg {
  width: 20px;
  height: 20px;
}

.price-change.positive {
  color: #86efac;
}

.price-change.negative {
  color: #fca5a5;
}

.price-change.neutral {
  color: rgba(255, 255, 255, 0.7);
}

/* Chart Section */
.chart-section {
  padding: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.chart-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.period-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.period-btn {
  padding: 6px 14px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.period-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.chart-loading {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-container {
  height: 350px;
}

.chart-empty {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

/* Stats Section */
.stats-section {
  padding: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.stats-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.stat-item {
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

/* Description Section */
.description-section {
  padding: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.description-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.description-text {
  color: #4b5563;
  line-height: 1.7;
  font-size: 14px;
  margin: 0 0 16px 0;
}

.website-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.website-link svg {
  width: 16px;
  height: 16px;
}

.website-link:hover {
  text-decoration: underline;
}

/* News Section */
.news-section {
  padding: 24px;
}

.news-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 20px 0;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.news-item:hover {
  background: #f3f4f6;
  transform: translateX(4px);
}

.news-content {
  flex: 1;
  min-width: 0;
}

.news-title {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin: 0 0 6px 0;
  line-height: 1.4;
}

.news-meta {
  display: flex;
  gap: 12px;
}

.news-publisher {
  font-size: 12px;
  color: #6b7280;
}

.news-arrow {
  width: 20px;
  height: 20px;
  color: #9ca3af;
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .detail-header {
    padding: 20px;
  }

  .stock-name {
    font-size: 22px;
  }

  .current-price {
    font-size: 26px;
  }

  .price-info {
    text-align: left;
  }

  .price-change {
    justify-content: flex-start;
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
