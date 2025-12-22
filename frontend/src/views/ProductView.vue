<template>
  <div class="products-page">
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">금융상품</h1>
        <p class="page-description">다양한 예금·적금 상품을 비교하고 나에게 맞는 상품을 찾아보세요</p>
      </div>

      <!-- Tab Navigation -->
      <div class="tabs-container">
        <div class="tabs tabs-pill">
          <button 
            :class="['tab', { active: active === 'deposits' }]"
            @click="active = 'deposits'"
          >
            <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M3 9h18"/>
              <path d="M9 21V9"/>
            </svg>
            예금
          </button>
          <button 
            :class="['tab', { active: active === 'savings' }]"
            @click="active = 'savings'"
          >
            <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 5c-1.5 0-2.8 1.4-3 2-3.5-1.5-11-.3-11 5 0 1.8 0 3 2 4.5V20h4v-2h3v2h4v-4c1-.5 1.5-1 2-2h2v-4h-2c0-1-.5-1.5-1-2h0V5z"/>
              <path d="M2 9v1c0 1.1.9 2 2 2h1"/>
              <circle cx="16" cy="11" r="1"/>
            </svg>
            적금
          </button>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="filter-section">
        <div class="filter-card">
          <div class="filter-grid">
            <!-- Bank Filter -->
            <div class="filter-group">
              <label class="filter-label">
                <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 21h18"/>
                  <path d="M3 10h18"/>
                  <path d="M5 6l7-3 7 3"/>
                  <path d="M4 10v11"/>
                  <path d="M20 10v11"/>
                  <path d="M8 14v3"/>
                  <path d="M12 14v3"/>
                  <path d="M16 14v3"/>
                </svg>
                은행
              </label>
              <select v-model="selectedBank" class="filter-select">
                <option value="">전체 은행</option>
                <option v-for="bank in bankOptions" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>

            <!-- Term Filter -->
            <div class="filter-group">
              <label class="filter-label">
                <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                기간
              </label>
              <select v-model.number="selectedTerm" class="filter-select">
                <option :value="0">전체 기간</option>
                <option v-for="term in termOptions" :key="term" :value="term">
                  {{ term }}개월
                </option>
              </select>
            </div>

            <!-- Search -->
            <div class="filter-group filter-group-search">
              <label class="filter-label">
                <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                검색
              </label>
              <div class="search-input-wrapper">
                <input 
                  v-model.trim="keyword" 
                  type="text" 
                  class="filter-input"
                  placeholder="은행명, 상품명으로 검색" 
                />
                <button v-if="keyword" @click="keyword = ''" class="search-clear">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Reset Button -->
            <div class="filter-group filter-group-reset">
              <button @click="resetFilter" class="btn btn-secondary">
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 4v6h6"/>
                  <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
                </svg>
                초기화
              </button>
            </div>
          </div>

          <!-- Active Filters -->
          <div v-if="hasActiveFilters" class="active-filters">
            <span class="active-filters-label">적용된 필터:</span>
            <span v-if="selectedBank" class="filter-tag">
              {{ selectedBank }}
              <button @click="selectedBank = ''" class="filter-tag-remove">×</button>
            </span>
            <span v-if="selectedTerm !== 0" class="filter-tag">
              {{ selectedTerm }}개월
              <button @click="selectedTerm = 0" class="filter-tag-remove">×</button>
            </span>
            <span v-if="keyword" class="filter-tag">
              "{{ keyword }}"
              <button @click="keyword = ''" class="filter-tag-remove">×</button>
            </span>
          </div>
        </div>
      </div>

      <!-- Results Info -->
      <div class="results-info">
        <span class="results-count">
          총 <strong>{{ filteredItems.length }}</strong>개 상품
        </span>
      </div>

      <!-- Product List -->
      <ProductList 
        v-if="active === 'deposits'" 
        :items="filteredItems" 
        type="deposit" 
      />
      <ProductList 
        v-else 
        :items="filteredItems" 
        type="saving" 
      />

      <!-- Empty State -->
      <div v-if="filteredItems.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <h3 class="empty-title">검색 결과가 없습니다</h3>
        <p class="empty-description">다른 조건으로 검색해 보세요</p>
        <button @click="resetFilter" class="btn btn-primary">필터 초기화</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useProductStore } from '@/stores/products'
import ProductList from '@/components/products/ProductList.vue'

const store = useProductStore()
const active = ref('deposits')

// 필터 상태
const selectedBank = ref('')
const selectedTerm = ref(0)
const keyword = ref('')

onMounted(() => {
  store.getDeposits()
  store.getSavings()
})

// 현재 탭 원본 목록
const currentItems = computed(() => {
  return active.value === 'deposits' ? store.deposits : store.savings
})

/** 옵션에서 기간 뽑기 */
const getTerm = (opt) => {
  const n = Number(opt?.save_trm)
  return Number.isNaN(n) ? null : n
}

// 은행 옵션(중복 제거)
const bankOptions = computed(() => {
  const banks = currentItems.value.map(item => item.kor_co_nm).filter(Boolean)
  return [...new Set(banks)]
})

// 기간 옵션(중복 제거)
const termOptions = computed(() => {
  const terms = currentItems.value
    .flatMap(item => (item.options ?? []).map(getTerm))
    .filter(n => n !== null)
  return [...new Set(terms)].sort((a, b) => a - b)
})

// 필터링 결과
const filteredItems = computed(() => {
  let result = currentItems.value

  if (selectedBank.value) {
    result = result.filter(item => item.kor_co_nm === selectedBank.value)
  }

  if (selectedTerm.value !== 0) {
    result = result.filter(item =>
      (item.options ?? []).some(opt => getTerm(opt) === selectedTerm.value)
    )
  }

  if (keyword.value) {
    const k = keyword.value.toLowerCase()
    result = result.filter(item => {
      const productName = (item.fin_prdt_nm || '').toLowerCase()
      const companyName = (item.kor_co_nm || '').toLowerCase()
      return productName.includes(k) || companyName.includes(k)
    })
  }

  return result
})

const hasActiveFilters = computed(() => {
  return selectedBank.value || selectedTerm.value !== 0 || keyword.value
})

const resetFilter = () => {
  selectedBank.value = ''
  selectedTerm.value = 0
  keyword.value = ''
}
</script>

<style scoped>
.products-page {
  min-height: calc(100vh - 72px);
  padding: 48px 24px;
  background: linear-gradient(180deg, #faf5ff 0%, #f5f3ff 50%, #fafafa 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #18181b;
  margin-bottom: 12px;
}

.page-description {
  font-size: 1.0625rem;
  color: #71717a;
  max-width: 500px;
  margin: 0 auto;
}

/* Tabs */
.tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.tabs-pill {
  background: white;
  padding: 6px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  display: inline-flex;
  gap: 4px;
}

.tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #71717a;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab:hover {
  color: #9333ea;
}

.tab.active {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
}

.tab-icon {
  width: 18px;
  height: 18px;
}

/* Filter Section */
.filter-section {
  margin-bottom: 24px;
}

.filter-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.filter-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr auto;
  gap: 16px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #52525b;
}

.filter-icon {
  width: 14px;
  height: 14px;
  color: #9333ea;
}

.filter-select,
.filter-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 0.9375rem;
  background: #fafafa;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s ease;
}

.filter-select:focus,
.filter-input:focus {
  border-color: #9333ea;
  background: white;
  box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.1);
}

.search-input-wrapper {
  position: relative;
}

.search-clear {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  padding: 0;
  background: #e4e4e7;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-clear svg {
  width: 12px;
  height: 12px;
  color: #71717a;
}

.filter-group-reset {
  justify-content: flex-end;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* Active Filters */
.active-filters {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f4f4f5;
  flex-wrap: wrap;
}

.active-filters-label {
  font-size: 0.8125rem;
  color: #71717a;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #9333ea;
  background: #f3e8ff;
  border-radius: 20px;
}

.filter-tag-remove {
  width: 16px;
  height: 16px;
  padding: 0;
  background: transparent;
  border: none;
  color: #9333ea;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.filter-tag-remove:hover {
  opacity: 1;
}

/* Results Info */
.results-info {
  margin-bottom: 20px;
}

.results-count {
  font-size: 0.9375rem;
  color: #71717a;
}

.results-count strong {
  color: #9333ea;
  font-weight: 700;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 24px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: #f4f4f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #a1a1aa;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 8px;
}

.empty-description {
  color: #71717a;
  margin-bottom: 24px;
}

/* Responsive */
@media (max-width: 900px) {
  .filter-grid {
    grid-template-columns: 1fr 1fr;
  }

  .filter-group-search {
    grid-column: span 2;
  }

  .filter-group-reset {
    grid-column: span 2;
    justify-content: center;
  }
}

@media (max-width: 600px) {
  .products-page {
    padding: 32px 16px;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .filter-group-search,
  .filter-group-reset {
    grid-column: span 1;
  }

  .tab {
    padding: 10px 20px;
    font-size: 0.875rem;
  }
}
</style>
