<template>
  <div class="analysis-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
            <line x1="12" y1="22.08" x2="12" y2="12"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">AI 금융 분석</h1>
          <p class="page-subtitle">나에게 맞는 금융상품을 추천받아보세요</p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Step Indicator -->
      <div class="step-indicator">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="step-item"
          :class="{ active: currentStep >= index, completed: currentStep > index }"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <span class="step-label">{{ step }}</span>
        </div>
      </div>

      <div class="analysis-card">
        <!-- Step 1: 목적 선택 -->
        <div v-if="currentStep === 0" class="step-content">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <div>
              <h2 class="card-title">목적을 선택하세요</h2>
              <p class="card-subtitle">어떤 목표를 위해 저축하시나요?</p>
            </div>
          </div>

          <div class="purpose-grid">
            <div 
              v-for="purpose in purposes" 
              :key="purpose.value"
              class="purpose-card"
              :class="{ selected: form.purpose === purpose.value }"
              @click="selectPurpose(purpose.value)"
            >
              <div class="purpose-icon" :style="{ background: purpose.bgColor }">
                <span class="purpose-emoji">{{ purpose.emoji }}</span>
              </div>
              <h3 class="purpose-title">{{ purpose.label }}</h3>
              <p class="purpose-desc">{{ purpose.desc }}</p>
            </div>
          </div>

          <button class="next-btn" :disabled="!form.purpose" @click="nextStep">
            다음 단계
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
        </div>

        <!-- Step 2: 목적별 세부 정보 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </div>
            <div>
              <h2 class="card-title">{{ purposeDetail.title }}</h2>
              <p class="card-subtitle">{{ purposeDetail.subtitle }}</p>
            </div>
          </div>

          <!-- 주택 목적 -->
          <div v-if="form.purpose === 'housing'" class="form-section">
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
                  <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
                주거 유형
              </label>
              <div class="option-grid">
                <div 
                  v-for="type in housingTypes" 
                  :key="type.value"
                  class="option-card"
                  :class="{ selected: form.housing_type === type.value }"
                  @click="form.housing_type = type.value"
                >
                  <span class="option-emoji">{{ type.emoji }}</span>
                  <span class="option-label">{{ type.label }}</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                목표 지역
              </label>
              <input 
                type="text" 
                v-model="form.target_region" 
                class="form-input"
                placeholder="예: 서울 강남구, 경기 성남시"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <path d="M3 9h18M9 21V9"/>
                </svg>
                목표 아파트 (선택)
              </label>
              <input 
                type="text" 
                v-model="form.target_apartment" 
                class="form-input"
                placeholder="예: 래미안, 힐스테이트"
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="1" x2="12" y2="23"/>
                  <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
                </svg>
                예상 가격
              </label>
              <div class="input-wrapper">
                <input 
                  type="number" 
                  v-model.number="displayApartmentPrice" 
                  class="form-input"
                  placeholder="예: 50000"
                />
                <span class="input-suffix">만원</span>
              </div>
              <p class="form-hint">아파트 가격을 입력하면 자동으로 목표 금액이 설정됩니다 ({{ formatCurrency(form.apartment_price) }})</p>
            </div>
          </div>

          <!-- 여행 목적 -->
          <div v-if="form.purpose === 'travel'" class="form-section">
            <!-- 나라 선택 (통화와 연동) -->
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="2" y1="12" x2="22" y2="12"/>
                  <path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/>
                </svg>
                여행 국가 선택
              </label>
              <div class="country-grid">
                <div 
                  v-for="country in travelCountries" 
                  :key="country.code"
                  class="country-card"
                  :class="{ selected: form.travel_country_code === country.code }"
                  @click="selectCountry(country)"
                >
                  <span class="country-flag">{{ country.flag }}</span>
                  <span class="country-name">{{ country.name }}</span>
                  <span class="country-currency">{{ country.currencyName }}</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                세부 여행지 (선택)
              </label>
              <input 
                type="text" 
                v-model="form.travel_destination" 
                class="form-input"
                :placeholder="selectedCountryPlaceholder"
              />
            </div>

            <div class="travel-tip">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              <p>선택한 국가를 기반으로 관련 뉴스와 추천 여행지를 알려드립니다. 적금 완료 후 이자 포함 금액을 현지 통화로 환산해드려요!</p>
            </div>
          </div>

          <!-- 목돈 목적 -->
          <div v-if="form.purpose === 'savings'" class="form-section">
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                세부 목적 (선택)
              </label>
              <div class="option-grid wide">
                <div 
                  v-for="detail in savingsDetails" 
                  :key="detail.value"
                  class="option-card"
                  :class="{ selected: form.savings_purpose_detail === detail.value }"
                  @click="form.savings_purpose_detail = detail.value"
                >
                  <span class="option-emoji">{{ detail.emoji }}</span>
                  <span class="option-label">{{ detail.label }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="btn-group">
            <button class="back-btn" @click="prevStep">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
              이전
            </button>
            <button class="next-btn" @click="nextStep">
              다음 단계
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Step 3: 금액 및 기간 설정 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
            </div>
            <div>
              <h2 class="card-title">금액 및 기간 설정</h2>
              <p class="card-subtitle">목표 달성을 위한 상세 정보를 입력하세요</p>
            </div>
          </div>

          <div class="form-section">
            <!-- 현재 보유 금액 -->
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="4" width="20" height="16" rx="2"/>
                  <path d="M2 10h20"/>
                </svg>
                현재 보유 금액
              </label>
              <div class="input-wrapper">
                <input 
                  type="number" 
                  v-model.number="displayCurrentSavings" 
                  class="form-input"
                  placeholder="예: 500"
                />
                <span class="input-suffix">만원</span>
              </div>
              <p class="form-hint">예금에 활용할 수 있는 금액을 입력하세요 ({{ formatCurrency(form.current_savings) }})</p>
            </div>

            <!-- 목표 금액 -->
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
                목표 금액
              </label>
              <div class="input-wrapper">
                <input 
                  type="number" 
                  v-model.number="displayTargetAmount" 
                  class="form-input"
                  placeholder="예: 1000"
                />
                <span class="input-suffix">만원</span>
              </div>
              <p class="form-hint">{{ formatCurrency(form.target_amount) }}</p>
            </div>

            <!-- 월 납입액 -->
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                월 납입액
              </label>
              <div class="input-wrapper">
                <input 
                  type="number" 
                  v-model.number="displayMonthlyAmount" 
                  class="form-input"
                  placeholder="예: 50"
                />
                <span class="input-suffix">만원</span>
              </div>
              <p class="form-hint">{{ formatCurrency(form.monthly_amount) }}</p>
            </div>

            <!-- 기간 -->
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                기간
              </label>
              <div class="period-selector">
                <div 
                  v-for="period in periodOptions" 
                  :key="period.value"
                  class="period-option"
                  :class="{ selected: form.period_months === period.value }"
                  @click="form.period_months = period.value"
                >
                  {{ period.label }}
                </div>
                <div class="period-custom">
                  <input 
                    type="number" 
                    v-model.number="form.period_months" 
                    class="form-input small"
                    placeholder="직접 입력"
                  />
                  <span class="input-suffix">개월</span>
                </div>
              </div>
            </div>

            <!-- 예상 계산 결과 미리보기 -->
            <div class="preview-card" v-if="previewCalculation">
              <h4 class="preview-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
                예상 결과 미리보기
              </h4>
              <div class="preview-stats">
                <div class="preview-stat">
                  <span class="stat-label">예상 총 납입액</span>
                  <span class="stat-value">{{ formatCurrency(previewCalculation.totalSavings) }}</span>
                </div>
                <div class="preview-stat">
                  <span class="stat-label">보유금 포함 총액</span>
                  <span class="stat-value highlight">{{ formatCurrency(previewCalculation.totalWithCurrent) }}</span>
                </div>
                <div class="preview-stat" :class="{ success: previewCalculation.achievable, warning: !previewCalculation.achievable }">
                  <span class="stat-label">목표 달성 여부</span>
                  <span class="stat-value">{{ previewCalculation.achievable ? '✅ 달성 가능' : '⚠️ 부족' }}</span>
                </div>
                <div v-if="!previewCalculation.achievable" class="preview-stat warning">
                  <span class="stat-label">부족 금액</span>
                  <span class="stat-value">{{ formatCurrency(previewCalculation.shortfall) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="btn-group">
            <button class="back-btn" @click="prevStep">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
              이전
            </button>
            <button class="submit-btn" :disabled="analysisStore.loading || !isFormValid" @click="submit">
              <template v-if="analysisStore.loading">
                <div class="loading-spinner"></div>
                분석 중...
              </template>
              <template v-else>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
                </svg>
                AI 분석하기
              </template>
            </button>
          </div>
        </div>
      </div>

      <!-- Info Cards -->
      <div class="info-cards">
        <div class="info-card">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </div>
          <h4 class="info-title">GPT 기반 분석</h4>
          <p class="info-text">AI가 수백 개의 금융상품 중 최적의 상품을 추천합니다</p>
        </div>
        
        <div class="info-card">
          <div class="info-icon purple">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <h4 class="info-title">예금+적금 조합</h4>
          <p class="info-text">보유금과 월 납입을 최적으로 조합해 추천합니다</p>
        </div>
        
        <div class="info-card">
          <div class="info-icon amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <h4 class="info-title">목적별 맞춤 분석</h4>
          <p class="info-text">주택, 여행, 목돈 등 목적에 맞는 조언을 제공합니다</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAnalysisStore } from '@/stores/analysis'

const router = useRouter()
const analysisStore = useAnalysisStore()

const currentStep = ref(0)
const steps = ['목적 선택', '상세 정보', '금액 설정']

const form = reactive({
  purpose: '',
  period_months: 12,
  monthly_amount: 500000,
  target_amount: 10000000,
  current_savings: 0,
  // 주택
  housing_type: '',
  target_region: '',
  target_apartment: '',
  apartment_price: null,
  // 여행
  travel_destination: '',
  travel_country_code: '',
  // 목돈
  savings_purpose_detail: '',
})

const purposes = [
  { 
    value: 'housing', 
    label: '주택', 
    emoji: '🏠', 
    desc: '내 집 마련, 전월세 자금',
    bgColor: '#dbeafe'
  },
  { 
    value: 'savings', 
    label: '목돈 마련', 
    emoji: '💰', 
    desc: '결혼, 자동차, 창업 등',
    bgColor: '#fef3c7'
  },
  { 
    value: 'travel', 
    label: '여행', 
    emoji: '✈️', 
    desc: '국내외 여행 자금',
    bgColor: '#f3e8ff'
  },
]

const housingTypes = [
  { value: 'purchase', label: '매매', emoji: '🏢' },
  { value: 'jeonse', label: '전세', emoji: '🔑' },
  { value: 'wolse_deposit', label: '월세 보증금', emoji: '💵' },
  { value: 'wolse', label: '월세', emoji: '📅' },
]

const savingsDetails = [
  { value: '결혼', label: '결혼 자금', emoji: '💒' },
  { value: '자동차', label: '자동차 구매', emoji: '🚗' },
  { value: '창업', label: '창업 자금', emoji: '🚀' },
  { value: '교육', label: '교육/학자금', emoji: '📚' },
  { value: '비상금', label: '비상금', emoji: '🛡️' },
  { value: '기타', label: '기타', emoji: '📦' },
]

// 여행 국가 목록 (나라 선택 시 통화 자동 설정) - exchange/views.py의 currencies와 동기화
// 실제 환율 API에서 제공하는 통화만 포함 (VND, TWD 제외)
const travelCountries = [
  { code: 'JPY', name: '일본', flag: '🇯🇵', currencyName: '엔 (JPY)', placeholder: '예: 도쿄, 오사카, 후쿠오카' },
  { code: 'USD', name: '미국', flag: '🇺🇸', currencyName: '달러 (USD)', placeholder: '예: 뉴욕, LA, 하와이' },
  { code: 'EUR', name: '유럽', flag: '🇪🇺', currencyName: '유로 (EUR)', placeholder: '예: 파리, 로마, 바르셀로나' },
  { code: 'CNH', name: '중국', flag: '🇨🇳', currencyName: '위안 (CNH)', placeholder: '예: 상하이, 베이징' },
  { code: 'THB', name: '태국', flag: '🇹🇭', currencyName: '바트 (THB)', placeholder: '예: 방콕, 치앙마이, 푸켓' },
  { code: 'SGD', name: '싱가포르', flag: '🇸🇬', currencyName: '싱가포르 달러 (SGD)', placeholder: '예: 마리나베이, 센토사' },
  { code: 'GBP', name: '영국', flag: '🇬🇧', currencyName: '파운드 (GBP)', placeholder: '예: 런던, 에든버러, 맨체스터' },
  { code: 'HKD', name: '홍콩', flag: '🇭🇰', currencyName: '홍콩 달러 (HKD)', placeholder: '예: 빅토리아 피크, 란타우' },
]

const periodOptions = [
  { value: 6, label: '6개월' },
  { value: 12, label: '12개월' },
  { value: 24, label: '24개월' },
  { value: 36, label: '36개월' },
]

// 만원 단위 입력을 위한 computed (양방향 바인딩)
const displayCurrentSavings = computed({
  get: () => form.current_savings ? form.current_savings / 10000 : null,
  set: (val) => { form.current_savings = val ? val * 10000 : 0 }
})

const displayTargetAmount = computed({
  get: () => form.target_amount ? form.target_amount / 10000 : null,
  set: (val) => { form.target_amount = val ? val * 10000 : 0 }
})

const displayMonthlyAmount = computed({
  get: () => form.monthly_amount ? form.monthly_amount / 10000 : null,
  set: (val) => { form.monthly_amount = val ? val * 10000 : 0 }
})

const displayApartmentPrice = computed({
  get: () => form.apartment_price ? form.apartment_price / 10000 : null,
  set: (val) => { form.apartment_price = val ? val * 10000 : 0 }
})

// 선택된 국가에 따른 placeholder
const selectedCountryPlaceholder = computed(() => {
  const country = travelCountries.find(c => c.code === form.travel_country_code)
  return country ? country.placeholder : '먼저 여행 국가를 선택하세요'
})

// 선택된 국가 정보
const selectedCountry = computed(() => {
  return travelCountries.find(c => c.code === form.travel_country_code)
})

// 국가 선택 함수
const selectCountry = (country) => {
  form.travel_country_code = country.code
  // 여행지에 국가명 자동 설정 (비어있을 경우)
  if (!form.travel_destination) {
    form.travel_destination = country.name
  }
}

const purposeDetail = computed(() => {
  switch (form.purpose) {
    case 'housing':
      return { title: '주택 정보 입력', subtitle: '목표 주거지 정보를 입력하세요' }
    case 'travel':
      return { title: '여행 정보 입력', subtitle: '여행할 국가를 선택하세요' }
    case 'savings':
      return { title: '저축 목적 선택', subtitle: '세부 저축 목적을 선택하세요' }
    default:
      return { title: '상세 정보', subtitle: '' }
  }
})

const previewCalculation = computed(() => {
  if (!form.monthly_amount || !form.period_months || !form.target_amount) {
    return null
  }
  
  const totalSavings = form.monthly_amount * form.period_months
  const totalWithCurrent = totalSavings + (form.current_savings || 0)
  const achievable = totalWithCurrent >= form.target_amount
  const shortfall = Math.max(0, form.target_amount - totalWithCurrent)
  
  return {
    totalSavings,
    totalWithCurrent,
    achievable,
    shortfall,
  }
})

const isFormValid = computed(() => {
  return form.purpose && 
         form.period_months > 0 && 
         form.monthly_amount > 0 && 
         form.target_amount > 0
})

// 아파트 가격 입력 시 목표 금액 자동 설정
watch(() => form.apartment_price, (newPrice) => {
  if (newPrice && form.purpose === 'housing') {
    form.target_amount = newPrice
  }
})

const selectPurpose = (value) => {
  form.purpose = value
}

const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount)
}

const submit = () => {
  const payload = {
    purpose: form.purpose,
    period_months: form.period_months,
    monthly_amount: form.monthly_amount,
    target_amount: form.target_amount,
    current_savings: form.current_savings || 0,
  }
  
  // 목적별 추가 필드
  if (form.purpose === 'housing') {
    payload.housing_type = form.housing_type
    payload.target_region = form.target_region
    payload.target_apartment = form.target_apartment
    payload.apartment_price = form.apartment_price
  } else if (form.purpose === 'travel') {
    payload.travel_destination = form.travel_destination
    payload.travel_country_code = form.travel_country_code
  } else if (form.purpose === 'savings') {
    payload.savings_purpose_detail = form.savings_purpose_detail
  }
  
  analysisStore.createAnalysis(payload)
}
</script>

<style scoped>
.analysis-page {
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
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 24px 60px;
}

/* Step Indicator */
.step-indicator {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
  margin-top: -20px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.5;
  transition: all 0.3s;
}

.step-item.active {
  opacity: 1;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  color: #9333ea;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.step-item.active .step-number {
  background: #9333ea;
  color: white;
}

.step-item.completed .step-number {
  background: #22c55e;
  color: white;
}

.step-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
}

/* Analysis Card */
.analysis-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  position: relative;
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f4f4f5;
}

.card-icon {
  width: 48px;
  height: 48px;
  background: #f3e8ff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon svg {
  width: 24px;
  height: 24px;
  color: #9333ea;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 4px;
}

.card-subtitle {
  font-size: 0.875rem;
  color: #71717a;
  margin: 0;
}

/* Purpose Grid */
.purpose-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.purpose-card {
  padding: 24px 16px;
  border: 2px solid #e4e4e7;
  border-radius: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.purpose-card:hover {
  border-color: #9333ea;
  transform: translateY(-2px);
}

.purpose-card.selected {
  border-color: #9333ea;
  background: #faf5ff;
}

.purpose-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}

.purpose-emoji {
  font-size: 2rem;
}

.purpose-title {
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 4px;
}

.purpose-desc {
  font-size: 0.8125rem;
  color: #71717a;
  margin: 0;
}

/* Option Grid */
.option-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.option-grid.wide {
  grid-template-columns: repeat(3, 1fr);
}

.option-card {
  padding: 16px 12px;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.option-card:hover {
  border-color: #9333ea;
}

.option-card.selected {
  border-color: #9333ea;
  background: #faf5ff;
}

.option-emoji {
  display: block;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.option-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #3f3f46;
}

/* Form */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #3f3f46;
}

.form-label svg {
  width: 18px;
  height: 18px;
  color: #9333ea;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 14px 60px 14px 16px;
  font-size: 1rem;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  background: white;
  transition: all 0.2s;
}

.form-input.small {
  width: 120px;
  padding: 10px 40px 10px 12px;
}

.form-input::placeholder {
  color: #a1a1aa;
}

.form-input:focus {
  outline: none;
  border-color: #9333ea;
  box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.1);
}

.input-suffix {
  position: absolute;
  right: 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #71717a;
}

.form-hint {
  font-size: 0.8125rem;
  color: #71717a;
  margin: 4px 0 0;
}

/* Select */
.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 14px 44px 14px 16px;
  font-size: 1rem;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  background: white;
  cursor: pointer;
  appearance: none;
  transition: all 0.2s;
}

.form-select:focus {
  outline: none;
  border-color: #9333ea;
  box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.1);
}

.select-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #71717a;
  pointer-events: none;
}

/* Period Selector */
.period-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.period-option {
  padding: 12px 20px;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #3f3f46;
  cursor: pointer;
  transition: all 0.2s;
}

.period-option:hover {
  border-color: #9333ea;
}

.period-option.selected {
  border-color: #9333ea;
  background: #9333ea;
  color: white;
}

.period-custom {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.period-custom .input-suffix {
  position: static;
}

/* Preview Card */
.preview-card {
  background: #f8f8f8;
  border-radius: 16px;
  padding: 20px;
  margin-top: 8px;
}

.preview-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 16px;
}

.preview-title svg {
  width: 18px;
  height: 18px;
  color: #9333ea;
}

.preview-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.preview-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.8125rem;
  color: #71717a;
}

.stat-value {
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
}

.stat-value.highlight {
  color: #9333ea;
}

.preview-stat.success .stat-value {
  color: #22c55e;
}

.preview-stat.warning .stat-value {
  color: #f59e0b;
}

/* Country Grid for Travel */
.country-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.country-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px 12px;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.country-card:hover {
  border-color: #9333ea;
  transform: translateY(-2px);
}

.country-card.selected {
  border-color: #9333ea;
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
}

.country-flag {
  font-size: 2rem;
}

.country-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #18181b;
}

.country-currency {
  font-size: 0.75rem;
  color: #71717a;
}

/* Travel Tip */
.travel-tip {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #fef3c7;
  border-radius: 12px;
  margin-top: 8px;
}

.travel-tip svg {
  width: 20px;
  height: 20px;
  color: #f59e0b;
  flex-shrink: 0;
  margin-top: 2px;
}

.travel-tip p {
  margin: 0;
  font-size: 0.875rem;
  color: #92400e;
  line-height: 1.5;
}

/* Buttons */
.btn-group {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.next-btn, .submit-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 32px;
  font-size: 1rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.next-btn svg, .submit-btn svg {
  width: 20px;
  height: 20px;
}

.next-btn:hover:not(:disabled), .submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(147, 51, 234, 0.4);
}

.next-btn:disabled, .submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  font-size: 1rem;
  font-weight: 600;
  color: #71717a;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

.back-btn:hover {
  border-color: #9333ea;
  color: #9333ea;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 32px;
}

.info-card {
  background: white;
  border-radius: 16px;
  padding: 24px 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.info-icon {
  width: 48px;
  height: 48px;
  background: #dbeafe;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
}

.info-icon svg {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.info-icon.purple {
  background: #f3e8ff;
}

.info-icon.purple svg {
  color: #9333ea;
}

.info-icon.amber {
  background: #fef3c7;
}

.info-icon.amber svg {
  color: #f59e0b;
}

.info-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 6px;
}

.info-text {
  font-size: 0.8125rem;
  color: #71717a;
  line-height: 1.5;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 32px 16px;
  }

  .main-content {
    padding: 24px 16px 40px;
  }

  .analysis-card {
    padding: 24px;
    border-radius: 20px;
  }

  .purpose-grid {
    grid-template-columns: 1fr;
  }

  .option-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .option-grid.wide {
    grid-template-columns: repeat(2, 1fr);
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .step-indicator {
    gap: 12px;
  }

  .step-label {
    display: none;
  }

  .preview-stats {
    grid-template-columns: 1fr;
  }
}
</style>