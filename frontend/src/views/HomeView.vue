<template>
  <div class="home-container">
    <!-- 환율 정보 표시 -->
    <div v-if="accountStore.isLogin && currentRate" class="exchange-banner">
      <div class="exchange-content">
        <div class="exchange-icon">💱</div>
        <div class="exchange-info">
          <p class="currency-name">{{ currentRate.cur_nm }}</p>
          <p class="exchange-rate">
            <span class="rate-value">{{ formatRate(currentRate.deal_bas_r) }}</span>
            <span class="currency-unit">원 ({{ currentRate.cur_unit }})</span>
          </p>
        </div>
        <div class="exchange-label">매매기준율</div>
      </div>
    </div>

    <!-- 메뉴 -->
    <nav>
      <RouterLink :to="{name:'ProductView'}">금융상품</RouterLink> | 
      <RouterLink :to="{name: 'AnalysisView'}">분석하기</RouterLink> | 
      <RouterLink :to="{name:'ProfileView'}">마이페이지</RouterLink> |
      <RouterLink :to="{name:'KakaoMapView'}">은행찾기</RouterLink> |
      <RouterLink :to="{name:'NewsView'}">뉴스</RouterLink> |
      <RouterLink :to="{ name: 'YoutubeLayoutView' }">YouTube</RouterLink> |
      <RouterLink :to="{ name: 'MetalView' }">현물상품</RouterLink> |
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useExchangeStore } from '@/stores/exchange'
import { useAccountStore } from '@/stores/accounts'

const exchangeStore = useExchangeStore()
const accountStore = useAccountStore()

const currentIndex = ref(0)
let intervalId = null

// 현재 표시할 환율 정보
const currentRate = computed(() => {
  if (!exchangeStore.rates || exchangeStore.rates.length === 0) {
    return null
  }
  return exchangeStore.rates[currentIndex.value]
})

// 환율 포맷팅 (천단위 콤마)
const formatRate = (rate) => {
  if (!rate) return '-'
  const numRate = parseFloat(rate.replace(/,/g, ''))
  return numRate.toLocaleString('ko-KR', { 
    minimumFractionDigits: 2, 
    maximumFractionDigits: 2 
  })
}

// 3초마다 통화 변경
const startRotation = () => {
  if (exchangeStore.rates.length === 0) return
  
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % exchangeStore.rates.length
  }, 3000)
}

const stopRotation = () => {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

// 환율 데이터 변경 감시
watch(() => exchangeStore.rates.length, (newLen) => {
  if (newLen > 0 && accountStore.isLogin) {
    stopRotation()
    startRotation()
  }
})

onMounted(async () => {
  // 디버깅
  console.log('isLogin:', accountStore.isLogin)
  console.log('rates:', exchangeStore.rates)
  console.log('rates.length:', exchangeStore.rates.length)
  
  // 로그인 상태인데 환율 데이터가 없으면 DB에서 조회
  if (accountStore.isLogin && exchangeStore.rates.length === 0) {
    try {
      await exchangeStore.getExchangeRates()
      console.log('DB에서 환율 조회 완료:', exchangeStore.rates)
    } catch (err) {
      console.error('환율 조회 실패:', err)
    }
  }
  
  // 로그인 상태이고 환율 데이터가 있으면 회전 시작
  if (accountStore.isLogin && exchangeStore.rates.length > 0) {
    startRotation()
  }
})

onUnmounted(() => {
  stopRotation()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.exchange-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.exchange-content {
  display: flex;
  align-items: center;
  gap: 16px;
  color: white;
}

.exchange-icon {
  font-size: 40px;
}

.exchange-info {
  flex: 1;
}

.currency-name {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
  font-weight: 500;
}

.exchange-rate {
  margin: 4px 0 0 0;
  font-size: 28px;
  font-weight: bold;
}

.rate-value {
  margin-right: 8px;
}

.currency-unit {
  font-size: 16px;
  opacity: 0.9;
  font-weight: 500;
}

.exchange-label {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.main-nav {
  padding: 20px;
  text-align: center;
  font-size: 16px;
}

.main-nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.2s;
}

.main-nav a:hover {
  color: #667eea;
}

.main-nav a.router-link-active {
  color: #667eea;
  font-weight: 700;
}
</style>