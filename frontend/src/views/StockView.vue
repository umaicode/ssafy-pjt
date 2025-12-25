<template>
  <div class="stock-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-title">
          <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
            <polyline points="16 7 22 7 22 13"/>
          </svg>
          <span>주식</span>
        </div>
      </div>
    </header>

    <main class="stock-container">
      <div class="stock-layout">
        <!-- Left Sidebar - Stock List -->
        <aside class="stock-sidebar">

      <!-- Search Box -->
      <div class="sidebar-search">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="종목명, 심볼 검색"
            @input="handleSearch"
            @focus="showSearchResults = true"
          />
        </div>
        <!-- Search Results Dropdown -->
        <div v-if="showSearchResults && searchResults.length > 0" class="search-dropdown">
          <div 
            v-for="result in searchResults" 
            :key="result.symbol"
            class="search-result"
            @click="selectStock(result.symbol)"
          >
            <span class="result-symbol">{{ result.symbol }}</span>
            <span class="result-name">{{ result.name }}</span>
          </div>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="filter-tabs">
        <button 
          :class="['filter-tab', { active: store.selectedMarket === 'BOOKMARK' }]"
          @click="store.setMarket('BOOKMARK')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
          북마크
        </button>
        <button 
          :class="['filter-tab', { active: store.selectedMarket === 'KR' }]"
          @click="store.setMarket('KR')"
        >
          국내
        </button>
        <button 
          :class="['filter-tab', { active: store.selectedMarket === 'US' }]"
          @click="store.setMarket('US')"
        >
          해외
        </button>
      </div>

      <!-- Refresh Bar -->
      <div class="refresh-bar">
        <span class="update-info">
          <template v-if="store.selectedMarket === 'BOOKMARK'">
            {{ store.bookmarkRefreshTime ? formatLastUpdated(store.bookmarkRefreshTime) : '갱신하여 최신 가격 확인' }}
          </template>
          <template v-else>
            {{ formatLastUpdated(store.updateStatus[store.selectedMarket]?.last_updated) }}
          </template>
        </span>
        <button 
          class="refresh-btn"
          :disabled="store.refreshLoading || store.bookmarkRefreshLoading"
          @click="store.selectedMarket === 'BOOKMARK' ? handleBookmarkRefresh() : handleRefresh()"
        >
          <svg v-if="store.refreshLoading || store.bookmarkRefreshLoading" class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
          </svg>
          {{ (store.refreshLoading || store.bookmarkRefreshLoading) ? '갱신 중...' : '갱신' }}
        </button>
      </div>

      <!-- Stock List -->
      <div class="stock-list">
        <div v-if="store.listLoading" class="list-loading">
          <div class="spinner"></div>
        </div>

        <div 
          v-else
          v-for="(stock, index) in store.filteredStocks"
          :key="stock.symbol"
          :class="['stock-item', { active: selectedSymbol === stock.symbol }]"
          @click="selectStock(stock.symbol)"
        >
          <div class="stock-rank">{{ (store.currentPage - 1) * store.perPage + index + 1 }}</div>
          <div class="stock-info">
            <span class="stock-name">{{ stock.name }}</span>
            <span class="stock-symbol">{{ stock.code || stock.symbol.replace('.KS', '').replace('.KQ', '') }}</span>
          </div>
          <div class="stock-price-info">
            <span class="stock-price">{{ formatListPrice(stock.current_price, stock.market) }}</span>
            <span :class="['stock-change', getChangeClass(stock.change_percent)]">
              {{ formatChangePercent(stock.change_percent) }}
            </span>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="store.totalPages > 1" class="pagination">
          <button 
            :disabled="store.currentPage <= 1"
            class="page-btn"
            @click="changePage(store.currentPage - 1)"
          >
            ‹
          </button>
          <span class="page-info">{{ store.currentPage }} / {{ store.totalPages }}</span>
          <button 
            :disabled="store.currentPage >= store.totalPages"
            class="page-btn"
            @click="changePage(store.currentPage + 1)"
          >
            ›
          </button>
        </div>
      </div>
    </aside>

        <!-- Main Content -->
        <section class="stock-main">
      <!-- No Stock Selected -->
      <div v-if="!store.hasSelectedStock && !store.loading" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
            <polyline points="16 7 22 7 22 13"/>
          </svg>
        </div>
        <h2>종목을 선택해주세요</h2>
        <p>왼쪽 목록에서 종목을 선택하면<br/>상세 정보를 확인할 수 있어요</p>
      </div>

      <!-- Stock Detail -->
      <div v-else-if="store.hasSelectedStock" class="stock-detail">
        <!-- Header -->
        <header class="detail-header">
          <div class="header-left">
            <div class="header-title-row">
              <h1 class="detail-name">{{ store.selectedStock.name }}</h1>
              <!-- 북마크 버튼 -->
              <button 
                v-if="isLoggedIn"
                class="bookmark-btn"
                :class="{ active: isCurrentStockBookmarked }"
                :disabled="bookmarkLoading"
                @click="toggleBookmark"
              >
                <svg v-if="bookmarkLoading" class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"/>
                </svg>
                <svg v-else-if="isCurrentStockBookmarked" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </button>
            </div>
            <div class="detail-meta">
              <span class="detail-symbol">{{ store.selectedStock.symbol }}</span>
              <span v-if="store.selectedStock.exchange" class="detail-exchange">{{ store.selectedStock.exchange }}</span>
            </div>
          </div>
          <div class="header-right">
            <div class="detail-price">{{ formatDetailPrice(store.selectedStock.current_price, store.selectedStock.currency) }}</div>
            <div :class="['detail-change', getChangeClass(store.selectedStock.change)]">
              {{ formatChange(store.selectedStock.change) }}
              ({{ formatChangePercent(store.selectedStock.change_percent) }})
            </div>
          </div>
        </header>

        <!-- Chart Section -->
        <section class="chart-section">
          <div class="chart-tabs">
            <button 
              v-for="period in periods" 
              :key="period.value"
              :class="['chart-tab', { active: store.chartPeriod === period.value }]"
              @click="changePeriod(period.value)"
            >
              {{ period.label }}
            </button>
          </div>

          <div v-if="store.chartLoading" class="chart-loading">
            <div class="spinner"></div>
          </div>
          
          <div v-else-if="store.hasChartData" class="chart-container">
            <StockChart :data="store.chartData.data" :currency="store.selectedStock.currency" />
          </div>

          <div v-else class="chart-empty">
            차트 데이터가 없습니다
          </div>
        </section>

        <!-- Stats Grid -->
        <section class="stats-section">
          <h3 class="section-title">종목 정보</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-label">시가</span>
              <span class="stat-value">{{ formatDetailPrice(store.selectedStock.open_price, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">고가</span>
              <span class="stat-value up">{{ formatDetailPrice(store.selectedStock.day_high, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">저가</span>
              <span class="stat-value down">{{ formatDetailPrice(store.selectedStock.day_low, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">전일 종가</span>
              <span class="stat-value">{{ formatDetailPrice(store.selectedStock.previous_close, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">거래량</span>
              <span class="stat-value">{{ formatVolume(store.selectedStock.volume) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">시가총액</span>
              <span class="stat-value">{{ formatMarketCap(store.selectedStock.market_cap) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">52주 최고</span>
              <span class="stat-value up">{{ formatDetailPrice(store.selectedStock.fifty_two_week_high, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">52주 최저</span>
              <span class="stat-value down">{{ formatDetailPrice(store.selectedStock.fifty_two_week_low, store.selectedStock.currency) }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">PER</span>
              <span class="stat-value">{{ store.selectedStock.pe_ratio?.toFixed(2) || '-' }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">EPS</span>
              <span class="stat-value">{{ store.selectedStock.eps?.toFixed(2) || '-' }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">배당수익률</span>
              <span class="stat-value">{{ store.selectedStock.dividend_yield ? (store.selectedStock.dividend_yield * 100).toFixed(2) + '%' : '-' }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">베타</span>
              <span class="stat-value">{{ store.selectedStock.beta?.toFixed(2) || '-' }}</span>
            </div>
          </div>
        </section>

        <!-- Company Info -->
        <section v-if="store.selectedStock.description" class="info-section">
          <div class="section-header">
            <h3 class="section-title">기업 소개</h3>
            <button 
              v-if="!store.translatedDescription && !store.translating"
              class="translate-btn"
              @click="handleTranslate"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 8l4 4-4 4"/>
                <path d="M12 4h7a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-7"/>
                <path d="M3 12h12"/>
              </svg>
              한글로 번역
            </button>
            <span v-if="store.translating" class="translating-text">
              <div class="spinner small"></div>
              번역 중...
            </span>
          </div>
          <p class="company-desc">{{ store.translatedDescription || store.selectedStock.description }}</p>
          <div class="company-meta">
            <span v-if="store.selectedStock.sector" class="meta-tag">{{ store.selectedStock.sector }}</span>
            <span v-if="store.selectedStock.industry" class="meta-tag">{{ store.selectedStock.industry }}</span>
          </div>
        </section>

        <!-- News -->
        <section class="news-section">
          <h3 class="section-title">관련 뉴스</h3>
          <div v-if="store.stockNews.length > 0" class="news-list">
            <a 
              v-for="(news, idx) in store.stockNews" 
              :key="idx"
              :href="news.link"
              target="_blank"
              class="news-item"
            >
              <div class="news-content">
                <span class="news-title">{{ news.title }}</span>
                <span v-if="news.description" class="news-desc">{{ news.description }}</span>
              </div>
              <div class="news-meta">
                <span v-if="news.publisher" class="news-publisher">{{ news.publisher }}</span>
                <span v-if="news.published_date" class="news-date">{{ formatNewsDate(news.published_date) }}</span>
              </div>
            </a>
          </div>
          <div v-else class="news-empty">
            관련 뉴스가 없습니다
          </div>
        </section>
      </div>

      <!-- Loading -->
      <div v-else class="loading-state">
        <div class="spinner large"></div>
      </div>
    </section>

    <!-- Right Sidebar - Market Info -->
    <aside class="market-sidebar">
      <h3 class="sidebar-title">주요 지표</h3>
      
      <!-- Market Indices -->
      <div class="market-section">
        <div v-if="store.indicesLoading" class="market-loading">
          <div class="spinner small"></div>
        </div>
        <div v-else-if="store.marketIndices.length > 0" class="indices-list">
          <div 
            v-for="index in store.marketIndices" 
            :key="index.symbol"
            class="index-card"
          >
            <div class="index-header">
              <span class="index-name">{{ index.name }}</span>
              <span :class="['index-change', getChangeClass(index.change)]">
                {{ formatChangePercent(index.change_percent) }}
              </span>
            </div>
            <div class="index-price">{{ formatIndexPrice(index.current_price, index.name) }}</div>
            <!-- Mini Chart -->
            <div v-if="index.chart_data?.length > 0" class="mini-chart">
              <svg viewBox="0 0 100 30" preserveAspectRatio="none">
                <polyline
                  :points="getMiniChartPoints(index.chart_data)"
                  fill="none"
                  :stroke="index.change >= 0 ? '#e55b5b' : '#4a90d9'"
                  stroke-width="1.5"
                />
              </svg>
            </div>
          </div>
        </div>
        <div v-else class="market-empty">
          데이터를 불러오는 중...
        </div>
      </div>
    </aside>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useStocksStore } from '@/stores/stocks'
import { useExchangeStore } from '@/stores/exchange'
import { useAccountStore } from '@/stores/accounts'
import StockChart from '@/components/stocks/StockChart.vue'

const store = useStocksStore()
const exchangeStore = useExchangeStore()
const accountStore = useAccountStore()

const searchQuery = ref('')
const showSearchResults = ref(false)
const searchTimeout = ref(null)
const selectedSymbol = ref(null)
const bookmarkLoading = ref(false)
const isCurrentStockBookmarked = ref(false)

const searchResults = computed(() => store.searchResults)
const isLoggedIn = computed(() => !!accountStore.token)

const periods = [
  { label: '1일', value: '1d' },
  { label: '1주', value: '5d' },
  { label: '1개월', value: '1mo' },
  { label: '3개월', value: '3mo' },
  { label: '1년', value: '1y' },
]

onMounted(async () => {
  // 갱신 상태 조회
  await store.fetchUpdateStatus()
  
  // 현재 마켓에 따라 데이터 로드 (페이지네이션 정보 포함)
  if (store.selectedMarket === 'KR') {
    await store.fetchKrStocks(1, store.perPage)
  } else if (store.selectedMarket === 'US') {
    await store.fetchUsStocks(1, store.perPage)
  } else if (store.selectedMarket === 'BOOKMARK') {
    await store.fetchBookmarkedStocks()
  }
  
  store.fetchMarketIndices()  // 주요 지표 로드
  if (exchangeStore.rates.length === 0) {
    exchangeStore.getExchangeRates()
  }
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 종목 변경 시 번역 초기화 및 북마크 상태 확인
watch(() => store.selectedStock?.symbol, async (newSymbol) => {
  store.translatedDescription = null
  if (newSymbol && isLoggedIn.value) {
    isCurrentStockBookmarked.value = await store.checkBookmark(newSymbol)
  } else {
    isCurrentStockBookmarked.value = false
  }
})

const handleSearch = () => {
  if (searchTimeout.value) clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(() => {
    if (searchQuery.value.trim()) {
      store.searchStocks(searchQuery.value)
      showSearchResults.value = true
    } else {
      store.clearSearchResults()
      showSearchResults.value = false
    }
  }, 300)
}

const selectStock = (symbol) => {
  selectedSymbol.value = symbol
  store.fetchStockDetail(symbol)
  showSearchResults.value = false
  searchQuery.value = ''
  store.clearSearchResults()
}

const changePeriod = (period) => {
  store.setChartPeriod(period)
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.sidebar-search')) {
    showSearchResults.value = false
  }
}

const handleTranslate = () => {
  if (store.selectedStock?.description) {
    store.translateDescription(store.selectedStock.description)
  }
}

const changePage = (page) => {
  store.changePage(page)
}

// 북마크 토글 핸들러
const toggleBookmark = async () => {
  if (!store.selectedStock || bookmarkLoading.value) return
  
  bookmarkLoading.value = true
  try {
    if (isCurrentStockBookmarked.value) {
      const success = await store.removeBookmark(store.selectedStock.symbol)
      if (success) {
        isCurrentStockBookmarked.value = false
      }
    } else {
      const success = await store.addBookmark(
        store.selectedStock.symbol,
        store.selectedStock.name
      )
      if (success) {
        isCurrentStockBookmarked.value = true
      }
    }
  } finally {
    bookmarkLoading.value = false
  }
}

// 데이터 갱신 핸들러
const handleRefresh = async () => {
  const result = await store.refreshStocks(store.selectedMarket)
  if (result.success) {
    alert(result.message)
  } else {
    alert(result.message)
  }
}

// 북마크 갱신 핸들러
const handleBookmarkRefresh = async () => {
  const result = await store.refreshBookmarkedStocks()
  if (result.success) {
    alert(result.message)
  } else {
    alert(result.message || '북마크 갱신에 실패했습니다.')
  }
}

// 마지막 갱신 시간 포맷
const formatLastUpdated = (dateStr) => {
  if (!dateStr) return '갱신 필요'
  
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date
    const minutes = Math.floor(diff / (1000 * 60))
    
    if (minutes < 1) return '방금 갱신'
    if (minutes < 60) return `${minutes}분 전 갱신`
    
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}시간 전 갱신`
    
    return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' }) + ' 갱신'
  } catch {
    return '갱신 필요'
  }
}

// 마켓 변경 감지 (setMarket에서 이미 데이터를 로드하므로 여기서는 불필요)
// watch(() => store.selectedMarket, (newMarket) => {
//   // setMarket 내부에서 이미 데이터를 로드함
// })

const getChangeClass = (change) => {
  if (change > 0) return 'up'
  if (change < 0) return 'down'
  return ''
}

const formatListPrice = (price, market) => {
  if (!price) return '-'
  const numPrice = Number(price)
  if (market === 'US') {
    return '$' + new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(numPrice)
  }
  return new Intl.NumberFormat('ko-KR').format(numPrice) + '원'
}

const formatPrice = (price, market) => {
  if (!price) return '-'
  if (market === 'KR') {
    return new Intl.NumberFormat('ko-KR').format(price) + '원'
  }
  return '$' + new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(price)
}

const formatDetailPrice = (price, currency) => {
  if (!price) return '-'
  if (currency === 'KRW') {
    return new Intl.NumberFormat('ko-KR').format(price) + '원'
  }
  return '$' + new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(price)
}

const formatChange = (change) => {
  if (!change) return '-'
  const prefix = change > 0 ? '+' : ''
  return prefix + change.toFixed(2)
}

const formatChangePercent = (percent) => {
  if (percent === null || percent === undefined) return '-'
  const numPercent = Number(percent)
  const prefix = numPercent > 0 ? '+' : ''
  return prefix + numPercent.toFixed(2) + '%'
}

const formatVolume = (volume) => {
  if (!volume) return '-'
  if (volume >= 100000000) return (volume / 100000000).toFixed(1) + '억'
  if (volume >= 10000) return (volume / 10000).toFixed(1) + '만'
  return new Intl.NumberFormat().format(volume)
}

const formatMarketCap = (cap) => {
  if (!cap) return '-'
  if (cap >= 1000000000000) return (cap / 1000000000000).toFixed(1) + '조'
  if (cap >= 100000000) return (cap / 100000000).toFixed(1) + '억'
  if (cap >= 1000000) return (cap / 1000000).toFixed(1) + 'M'
  return new Intl.NumberFormat().format(cap)
}

const formatRate = (rate) => {
  if (!rate) return '-'
  return parseFloat(rate.replace(/,/g, '')).toLocaleString('ko-KR', { maximumFractionDigits: 2 })
}

// 지표별 가격 포맷
const formatIndexPrice = (price, name) => {
  if (!price) return '-'
  // 환율인 경우
  if (name.includes('환율') || name.includes('USD') || name.includes('EUR') || name.includes('JPY')) {
    return new Intl.NumberFormat('ko-KR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(price) + '원'
  }
  // 주가 지수
  return new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(price)
}

// 미니 차트 포인트 계산
const getMiniChartPoints = (chartData) => {
  if (!chartData || chartData.length === 0) return ''
  
  // 숫자 배열이거나 객체 배열인 경우 모두 처리
  const prices = chartData.map(d => {
    if (typeof d === 'number') return d
    return d.close || d.price || 0
  })
  const min = Math.min(...prices)
  const max = Math.max(...prices)
  const range = max - min || 1
  
  return prices.map((price, i) => {
    const x = (i / (prices.length - 1)) * 100
    const y = 30 - ((price - min) / range) * 28  // 반전: 낮은 값이 아래
    return `${x},${y}`
  }).join(' ')
}

const formatNewsDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date
    const hours = Math.floor(diff / (1000 * 60 * 60))
    
    if (hours < 1) return '방금 전'
    if (hours < 24) return `${hours}시간 전`
    
    const days = Math.floor(hours / 24)
    if (days < 7) return `${days}일 전`
    
    return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })
  } catch {
    return dateStr
  }
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   Page Layout
   ═══════════════════════════════════════════════════════════════ */
.stock-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

/* ═══════════════════════════════════════════════════════════════
   Page Header - NewsHeader Style
   ═══════════════════════════════════════════════════════════════ */
.page-header {
  background: linear-gradient(135deg, #5b5b6d 0%, #6d698f 100%);
  padding: 20px 24px;
  margin-bottom: 0px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.title-icon {
  width: 24px;
  height: 24px;
  color: #E1AFD1;
}

.filter-tabs {
  display: flex;
  gap: 6px;
  padding: 12px 14px;
  background: #f9fafb;
  border-bottom: 1px solid #f0f0f0;
}

.filter-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  flex: 1;
  padding: 10px 12px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #666;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab svg {
  width: 14px;
  height: 14px;
}

.filter-tab:hover {
  color: #7469B6;
  border-color: #7469B6;
}

.filter-tab.active {
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(116, 105, 182, 0.3);
}

/* ═══════════════════════════════════════════════════════════════
   Main Container
   ═══════════════════════════════════════════════════════════════ */
.stock-container {
  padding: 24px;
}

.stock-layout {
  display: grid;
  grid-template-columns: 340px 1fr 280px;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* ═══════════════════════════════════════════════════════════════
   Left Sidebar - Stock List
   ═══════════════════════════════════════════════════════════════ */
.stock-sidebar {
  background: white;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  position: sticky;
  top: 96px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

/* Sidebar Search */
.sidebar-search {
  position: relative;
  padding: 14px;
  background: white;
  border-bottom: 1px solid #f0f0f0;
}

.sidebar-search .search-box {
  display: flex;
  align-items: center;
  gap: 0;
  background: #f5f6f8;
  border-radius: 12px;
  padding: 4px;
  border: 1px solid #e5e5e5;
  transition: all 0.2s;
}

.sidebar-search .search-box:focus-within {
  background: white;
  border-color: #7469B6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.1);
}

.sidebar-search .search-icon {
  width: 18px;
  height: 18px;
  color: #999;
  margin-left: 12px;
}

.sidebar-search .search-box input {
  flex: 1;
  padding: 10px 12px;
  font-size: 0.875rem;
  background: transparent;
  border: none;
  outline: none;
  color: #1a1a1a;
}

.sidebar-search .search-box input::placeholder {
  color: #999;
}

.sidebar-search .search-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 14px;
  right: 14px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  z-index: 100;
  max-height: 280px;
  overflow-y: auto;
}

.search-result {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-bottom: 1px solid #f5f5f5;
  transition: background 0.15s;
}

.search-result:last-child {
  border-bottom: none;
}

.search-result:hover {
  background: #f9f9fb;
}

.result-symbol {
  font-weight: 600;
  color: #7469B6;
  font-size: 13px;
}

.result-name {
  color: #666;
  font-size: 12px;
}

/* Refresh Bar */
.refresh-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f9fafb;
  border-bottom: 1px solid #f0f0f0;
}

.update-info {
  font-size: 11px;
  color: #888;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  border-color: #7469B6;
  color: #7469B6;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 14px;
  height: 14px;
}

.refresh-btn svg.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Stock List */
.stock-list {
  flex: 1;
  overflow-y: auto;
}

.list-loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.stock-item {
  display: flex;
  align-items: center;
  padding: 12px 14px;
  gap: 10px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  transition: all 0.15s;
}

.stock-item:hover {
  background: #fafbfc;
}

.stock-item.active {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.08) 0%, rgba(225, 175, 209, 0.05) 100%);
  border-left: 3px solid #7469B6;
}

.stock-rank {
  width: 24px;
  height: 24px;
  background: #f0f0f0;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #888;
  flex-shrink: 0;
}

.stock-item.active .stock-rank {
  background: #7469B6;
  color: white;
}

.stock-info {
  flex: 1;
  min-width: 0;
}

.stock-name {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a1a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 1px;
}

.stock-symbol {
  font-size: 11px;
  color: #999;
}

.stock-price-info {
  text-align: right;
  flex-shrink: 0;
}

.stock-price {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 1px;
}

.stock-change {
  font-size: 11px;
  font-weight: 600;
}

.stock-change.up { color: #e55b5b; }
.stock-change.down { color: #4a90d9; }

/* Market Badge */
.stock-market-badge {
  flex-shrink: 0;
}

.market-badge {
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
}

.market-badge.kospi {
  background: rgba(116, 105, 182, 0.1);
  color: #7469B6;
}

.market-badge.kosdaq {
  background: rgba(225, 175, 209, 0.2);
  color: #AD88C6;
}

.market-badge.us {
  background: rgba(74, 144, 217, 0.1);
  color: #4a90d9;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  border-top: 1px solid #f0f0f0;
  background: white;
  position: sticky;
  bottom: 0;
}

.page-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.page-btn:hover:not(:disabled) {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: #666;
  min-width: 60px;
  text-align: center;
}

/* ═══════════════════════════════════════════════════════════════
   Main Content
   ═══════════════════════════════════════════════════════════════ */
.stock-main {
  overflow-y: auto;
  background: transparent;
  min-height: calc(100vh - 200px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #888;
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.empty-icon {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.12) 0%, rgba(225, 175, 209, 0.08) 100%);
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon svg {
  width: 48px;
  height: 48px;
  color: #7469B6;
}

.empty-state h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 10px;
}

.empty-state p {
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
  color: #888;
}

/* Stock Detail */
.stock-detail {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.detail-name {
  font-size: 26px;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0;
  letter-spacing: -0.02em;
}

/* Bookmark Button */
.bookmark-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.bookmark-btn svg {
  width: 16px;
  height: 18px;
  color: #888;
}

.bookmark-btn:hover:not(:disabled) {
  border-color: #7469B6;
  background: rgba(116, 105, 182, 0.05);
}

.bookmark-btn:hover:not(:disabled) svg {
  color: #7469B6;
}

.bookmark-btn.active {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

.bookmark-btn.active svg {
  color: white;
}

.bookmark-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.bookmark-btn svg.spin {
  animation: spin 1s linear infinite;
}

.detail-meta {
  display: flex;
  gap: 6px;
  margin-top: 8px;
}

.detail-symbol,
.detail-exchange {
  padding: 5px 12px;
  background: #f5f6f8;
  border-radius: 8px;
  font-size: 12px;
  color: #666;
}

.detail-symbol {
  color: #7469B6;
  font-weight: 700;
}

.header-right {
  text-align: right;
}

.detail-price {
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  letter-spacing: -0.02em;
}

.detail-change {
  font-size: 16px;
  font-weight: 600;
  margin-top: 6px;
}

.detail-change.up { color: #e55b5b; }
.detail-change.down { color: #4a90d9; }

/* Chart Section */
.chart-section {
  background: #f9fafb;
  border-radius: 20px;
  padding: 24px;
  margin-top: 24px;
}

.chart-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 20px;
}

.chart-tab {
  padding: 10px 18px;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
}

.chart-tab:hover {
  background: white;
  color: #666;
}

.chart-tab.active {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

.chart-container {
  height: 320px;
}

.chart-loading,
.chart-empty {
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 14px;
}

/* Stats Section */
.stats-section {
  background: #f9fafb;
  border-radius: 20px;
  padding: 24px;
  margin-top: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-card {
  background: white;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #888;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-value.up { color: #e55b5b; }
.stat-value.down { color: #4a90d9; }

/* Info Section */
.info-section {
  background: #f9fafb;
  border-radius: 20px;
  padding: 24px;
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header .section-title {
  margin: 0;
}

.translate-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.translate-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

.translate-btn svg {
  width: 16px;
  height: 16px;
}

.translating-text {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #7469B6;
}

.company-desc {
  font-size: 15px;
  line-height: 1.9;
  color: #444;
  margin: 0 0 18px;
  background: white;
  padding: 20px;
  border-radius: 14px;
}

.company-meta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.meta-tag {
  padding: 8px 14px;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #7469B6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* News Section */
.news-section {
  background: #f9fafb;
  border-radius: 20px;
  padding: 24px;
  margin-top: 20px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: white;
  border-radius: 14px;
  text-decoration: none;
  transition: all 0.15s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.news-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.news-item:hover .news-title {
  color: #7469B6;
}

.news-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.news-title {
  font-size: 15px;
  color: #1a1a1a;
  line-height: 1.5;
  font-weight: 600;
  transition: color 0.15s;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 4px;
}

.news-publisher {
  font-size: 13px;
  color: #7469B6;
  font-weight: 500;
}

.news-date {
  font-size: 12px;
  color: #999;
}

.news-empty {
  padding: 48px;
  text-align: center;
  color: #888;
  font-size: 15px;
  background: white;
  border-radius: 14px;
}

/* ═══════════════════════════════════════════════════════════════
   Right Sidebar
   ═══════════════════════════════════════════════════════════════ */
.market-sidebar {
  background: white;
  border-radius: 20px;
  padding: 24px 20px;
  height: calc(100vh - 200px);
  position: sticky;
  top: 96px;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.sidebar-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 20px;
}

.market-section {
  margin-bottom: 24px;
}

.market-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #888;
  margin: 0 0 14px;
}

.market-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.market-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  background: #f9fafb;
  border-radius: 12px;
  transition: all 0.15s;
}

.market-item:hover {
  background: #f0f2f5;
}

.market-item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.market-flag {
  font-size: 18px;
}

.market-name {
  font-size: 13px;
  font-weight: 600;
  color: #444;
}

.market-value {
  font-size: 13px;
  font-weight: 700;
  color: #1a1a1a;
}

.market-empty {
  display: flex;
  justify-content: center;
  padding: 24px;
  color: #888;
  font-size: 13px;
}

.market-loading {
  display: flex;
  justify-content: center;
  padding: 24px;
}

/* Indices Cards */
.indices-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.index-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 12px 14px;
  transition: all 0.15s;
}

.index-card:hover {
  background: #f0f2f5;
}

.index-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.index-name {
  font-size: 12px;
  font-weight: 600;
  color: #444;
}

.index-change {
  font-size: 12px;
  font-weight: 700;
}

.index-change.up {
  color: #e55b5b;
}

.index-change.down {
  color: #4a90d9;
}

.index-price {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.mini-chart {
  height: 30px;
  overflow: hidden;
}

.mini-chart svg {
  width: 100%;
  height: 100%;
}

/* ═══════════════════════════════════════════════════════════════
   Spinner
   ═══════════════════════════════════════════════════════════════ */
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #f0f0f0;
  border-top-color: #7469B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner.large {
  width: 36px;
  height: 36px;
  border-width: 4px;
}

.spinner.small {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ═══════════════════════════════════════════════════════════════
   Responsive
   ═══════════════════════════════════════════════════════════════ */
@media (max-width: 1200px) {
  .stock-layout {
    grid-template-columns: 320px 1fr;
  }

  .market-sidebar {
    display: none;
  }
}

@media (max-width: 900px) {
  .stock-layout {
    grid-template-columns: 1fr;
  }

  .stock-sidebar {
    position: relative;
    top: 0;
    height: auto;
    max-height: 350px;
  }

  .stock-main {
    min-height: auto;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box input {
    width: 100%;
  }

  .filter-tabs {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .stock-container {
    padding: 16px;
  }

  .stock-sidebar {
    max-height: 300px;
  }

  .stock-item {
    padding: 10px 12px;
  }

  .stock-detail {
    padding: 16px;
  }

  .detail-name {
    font-size: 20px;
  }

  .detail-price {
    font-size: 26px;
  }

  .chart-section,
  .stats-section,
  .info-section,
  .news-section {
    border-radius: 14px;
    padding: 16px;
  }
}

/* ═══════════════════════════════════════════════════════════════
   Dark Mode
   ═══════════════════════════════════════════════════════════════ */
[data-theme="dark"] .stock-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #18181b 50%, #0f0f0f 100%);
}

[data-theme="dark"] .page-header {
  background: linear-gradient(135deg, #1a1a1f 0%, #2a2a35 100%);
}

[data-theme="dark"] .search-dropdown {
  background: #1f1f23;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

[data-theme="dark"] .search-result {
  border-bottom-color: #2a2a2f;
}

[data-theme="dark"] .search-result:hover {
  background: #2a2a30;
}

[data-theme="dark"] .result-name {
  color: #a1a1aa;
}

[data-theme="dark"] .stock-sidebar {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .sidebar-search {
  background: #18181b;
  border-bottom-color: #27272a;
}

[data-theme="dark"] .sidebar-search .search-box {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme="dark"] .sidebar-search .search-box:focus-within {
  background: #1f1f23;
  border-color: #7469B6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .sidebar-search .search-icon {
  color: #71717a;
}

[data-theme="dark"] .sidebar-search .search-box input {
  color: #e4e4e7;
}

[data-theme="dark"] .sidebar-search .search-box input::placeholder {
  color: #71717a;
}

[data-theme="dark"] .sidebar-search .search-dropdown {
  background: #1f1f23;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

[data-theme="dark"] .search-result {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .search-result:hover {
  background: #27272a;
}

[data-theme="dark"] .result-name {
  color: #a1a1aa;
}

[data-theme="dark"] .filter-tabs {
  background: #1f1f23;
  border-bottom-color: #27272a;
}

[data-theme="dark"] .filter-tab {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .filter-tab:hover {
  color: #AD88C6;
  border-color: #7469B6;
}

[data-theme="dark"] .filter-tab.active {
  color: white;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
}

[data-theme="dark"] .refresh-bar {
  background: #1f1f23;
  border-bottom-color: #27272a;
}

[data-theme="dark"] .update-info {
  color: #71717a;
}

[data-theme="dark"] .refresh-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .refresh-btn:hover:not(:disabled) {
  border-color: #7469B6;
  color: #7469B6;
  background: #2a2a35;
}

[data-theme="dark"] .stock-item {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .stock-item:hover {
  background: #1f1f23;
}

[data-theme="dark"] .stock-item.active {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.15) 0%, rgba(225, 175, 209, 0.08) 100%);
}

[data-theme="dark"] .stock-rank {
  background: #27272a;
  color: #71717a;
}

[data-theme="dark"] .stock-item.active .stock-rank {
  background: #7469B6;
  color: white;
}

[data-theme="dark"] .stock-name {
  color: #e4e4e7;
}

[data-theme="dark"] .stock-symbol {
  color: #71717a;
}

[data-theme="dark"] .stock-price {
  color: #e4e4e7;
}

[data-theme="dark"] .pagination {
  background: #18181b;
  border-top-color: #27272a;
}

[data-theme="dark"] .page-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .page-btn:hover:not(:disabled) {
  background: #7469B6;
  border-color: #7469B6;
  color: white;
}

[data-theme="dark"] .page-info {
  color: #a1a1aa;
}

[data-theme="dark"] .empty-state {
  background: #18181b;
}

[data-theme="dark"] .empty-state h2 {
  color: #e4e4e7;
}

[data-theme="dark"] .empty-state p {
  color: #71717a;
}

[data-theme="dark"] .empty-icon {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.2) 0%, rgba(225, 175, 209, 0.12) 100%);
}

[data-theme="dark"] .stock-detail {
  background: #18181b;
}

[data-theme="dark"] .detail-header {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .detail-name {
  color: #e4e4e7;
}

[data-theme="dark"] .detail-symbol,
[data-theme="dark"] .detail-exchange {
  background: #27272a;
  color: #a1a1aa;
}

[data-theme="dark"] .detail-symbol {
  color: #AD88C6;
}

[data-theme="dark"] .detail-price {
  color: #e4e4e7;
}

[data-theme="dark"] .bookmark-btn {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme="dark"] .bookmark-btn svg {
  color: #71717a;
}

[data-theme="dark"] .bookmark-btn:hover:not(:disabled) {
  border-color: #7469B6;
  background: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .bookmark-btn:hover:not(:disabled) svg {
  color: #AD88C6;
}

[data-theme="dark"] .chart-section,
[data-theme="dark"] .stats-section,
[data-theme="dark"] .info-section,
[data-theme="dark"] .news-section {
  background: #1f1f23;
}

[data-theme="dark"] .section-title {
  color: #e4e4e7;
}

[data-theme="dark"] .chart-tab {
  color: #71717a;
}

[data-theme="dark"] .chart-tab:hover {
  background: #27272a;
  color: #a1a1aa;
}

[data-theme="dark"] .stat-card {
  background: #27272a;
  box-shadow: none;
}

[data-theme="dark"] .stat-label {
  color: #71717a;
}

[data-theme="dark"] .stat-value {
  color: #e4e4e7;
}

[data-theme="dark"] .company-desc {
  background: #27272a;
  color: #d4d4d8;
}

[data-theme="dark"] .meta-tag {
  background: #27272a;
  color: #AD88C6;
}

[data-theme="dark"] .news-item {
  background: #27272a;
  box-shadow: none;
}

[data-theme="dark"] .news-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .news-title {
  color: #e4e4e7;
}

[data-theme="dark"] .news-desc {
  color: #a1a1aa;
}

[data-theme="dark"] .news-date {
  color: #71717a;
}

[data-theme="dark"] .news-empty {
  background: #27272a;
  color: #71717a;
}

[data-theme="dark"] .market-sidebar {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .sidebar-title {
  color: #e4e4e7;
}

[data-theme="dark"] .index-card {
  background: #1f1f23;
}

[data-theme="dark"] .index-card:hover {
  background: #27272a;
}

[data-theme="dark"] .index-name {
  color: #a1a1aa;
}

[data-theme="dark"] .index-price {
  color: #e4e4e7;
}

[data-theme="dark"] .market-empty {
  color: #71717a;
}

[data-theme="dark"] .spinner {
  border-color: #27272a;
  border-top-color: #7469B6;
}
</style>
