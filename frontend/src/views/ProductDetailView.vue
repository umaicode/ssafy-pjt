<template>
  <div class="product-detail-page">
    <div class="container">
      <!-- Back Button -->
      <RouterLink :to="{ name: 'ProductView' }" class="back-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5"/>
          <path d="M12 19l-7-7 7-7"/>
        </svg>
        상품 목록으로
      </RouterLink>

      <div v-if="product" class="product-detail-container">
        <!-- Header Card -->
        <div class="product-header-card">
          <div class="product-badge-row">
            <span class="product-type-badge">
              {{ route.params.type === 'deposit' ? '예금' : '적금' }}
            </span>
            <span class="product-join-badge" :class="joinDenyClass">
              {{ joinDenyText }}
            </span>
          </div>
          
          <div class="product-bank-info">
            <div class="bank-logo-large">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 21h18"/>
                <path d="M3 10h18"/>
                <path d="M5 6l7-3 7 3"/>
                <path d="M4 10v11"/>
                <path d="M20 10v11"/>
                <path d="M8 14v3"/>
                <path d="M12 14v3"/>
                <path d="M16 14v3"/>
              </svg>
            </div>
            <span class="bank-name-large">{{ product.kor_co_nm }}</span>
          </div>
          
          <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button
              @click="toggleLike"
              class="like-btn"
              :class="{ liked: likeStore.liked }"
              type="button"
            >
              <svg v-if="!likeStore.liked" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <span>{{ likeStore.liked ? '관심상품' : '관심등록' }}</span>
              <span class="like-count">{{ likeStore.likesCount ?? 0 }}</span>
            </button>

            <button
              v-if="likeStore.liked && product"
              @click="toggleMap"
              class="map-btn"
              type="button"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              {{ showMap ? '지도 닫기' : '은행 위치 찾기' }}
            </button>
          </div>
        </div>

        <!-- Map Section -->
        <ProductBankMap
          v-if="showMap && product"
          :bank-name="product.kor_co_nm"
          @close="showMap = false"
        />

        <!-- Rate Options Card -->
        <div v-if="options.length" class="options-card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M16 8l-4 4-4-4"/>
              <path d="M8 16l4-4 4 4"/>
            </svg>
            금리 옵션
          </h2>
          
          <div class="options-table-wrapper">
            <table class="options-table">
              <thead>
                <tr>
                  <th>가입기간</th>
                  <th>금리유형</th>
                  <th>기본금리</th>
                  <th>최고금리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="option in options" :key="option.id">
                  <td>
                    <span class="term-value">{{ option.save_trm }}</span>
                    <span class="term-unit">개월</span>
                  </td>
                  <td>{{ option.intr_rate_type_nm }}</td>
                  <td class="rate-cell">{{ option.intr_rate }}%</td>
                  <td class="rate-cell rate-max">{{ option.intr_rate2 }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Details Card -->
        <div class="details-card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
              <path d="M14 2v6h6"/>
              <path d="M16 13H8"/>
              <path d="M16 17H8"/>
              <path d="M10 9H8"/>
            </svg>
            상품 상세정보
          </h2>
          
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">가입 대상</span>
              <span class="detail-value">{{ product.join_member || '-' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">가입 방법</span>
              <span class="detail-value">{{ product.join_way || '-' }}</span>
            </div>
            <div class="detail-item detail-full">
              <span class="detail-label">우대조건</span>
              <span class="detail-value">{{ product.spcl_cnd || '-' }}</span>
            </div>
            <div class="detail-item detail-full">
              <span class="detail-label">기타 사항</span>
              <span class="detail-value">{{ product.etc_note || '-' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else class="loading-state">
        <div class="loading-spinner"></div>
        <p>상품 정보를 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useLikeStore } from '@/stores/like'
import { useAccountStore } from '@/stores/accounts'
import ProductBankMap from '@/components/products/ProductBankMap.vue'

const store = useProductStore()
const likeStore = useLikeStore()
const accountStore = useAccountStore()
const route = useRoute()

const product = ref(null)
const options = ref([])
const showMap = ref(false)

const joinDenyText = computed(() => {
  if (!product.value) return ''
  const map = { 1: '제한 없음', 2: '서민 전용', 3: '일부 제한' }
  return map[product.value.join_deny]
})

const joinDenyClass = computed(() => {
  if (!product.value) return ''
  const classMap = { 1: 'badge-success', 2: 'badge-warning', 3: 'badge-info' }
  return classMap[product.value.join_deny]
})

const toggleLike = function () {
  const payload = {
    fin_prdt_cd: route.params.fin_prdt_cd,
    product_type: route.params.type,
  }

  likeStore.toggleLike(payload)
    .then(() => {})
    .catch((err) => {
      console.log(err)
      alert('좋아요 처리에 실패했습니다.')
    })
}

const toggleMap = () => {
  showMap.value = !showMap.value
}

watch(() => likeStore.liked, (newVal) => {
  if (!newVal) showMap.value = false
})

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/products/${route.params.type}/${route.params.fin_prdt_cd}/`,
    headers: accountStore.token ? { Authorization: `Token ${accountStore.token}` } : {},
  })
    .then((res) => {
      product.value = res.data
      options.value = res.data.options
      likeStore.liked = res.data.is_liked ?? res.data.liked ?? false
      likeStore.likesCount = res.data.likes_count ?? 0
    })
    .catch((err) => console.log(err))
})
</script>

<style scoped>
.product-detail-page {
  min-height: calc(100vh - 72px);
  padding: 48px 24px;
  background: linear-gradient(180deg, #faf5ff 0%, #f5f3ff 50%, #fafafa 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* Back Link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #71717a;
  text-decoration: none;
  margin-bottom: 24px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #9333ea;
}

.back-link svg {
  width: 18px;
  height: 18px;
}

/* Header Card */
.product-header-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.product-badge-row {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.product-type-badge {
  padding: 6px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #9333ea;
  background: #f3e8ff;
  border-radius: 20px;
}

.product-join-badge {
  padding: 6px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 20px;
}

.badge-success {
  color: #059669;
  background: #d1fae5;
}

.badge-warning {
  color: #d97706;
  background: #fef3c7;
}

.badge-info {
  color: #0284c7;
  background: #e0f2fe;
}

.product-bank-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.bank-logo-large {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bank-logo-large svg {
  width: 24px;
  height: 24px;
  color: white;
}

.bank-name-large {
  font-size: 1.125rem;
  font-weight: 600;
  color: #52525b;
}

.product-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #18181b;
  line-height: 1.3;
  margin-bottom: 24px;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.like-btn,
.map-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.9375rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-btn {
  background: white;
  color: #9333ea;
  border: 2px solid #e9d5ff;
}

.like-btn:hover {
  background: #faf5ff;
  border-color: #9333ea;
}

.like-btn.liked {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  color: white;
  border-color: transparent;
}

.like-btn svg {
  width: 18px;
  height: 18px;
}

.like-count {
  padding: 2px 8px;
  font-size: 0.75rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.like-btn:not(.liked) .like-count {
  background: #f3e8ff;
  color: #9333ea;
}

.map-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
}

.map-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.map-btn svg {
  width: 18px;
  height: 18px;
}

/* Options Card */
.options-card,
.details-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 24px;
}

.card-title svg {
  width: 24px;
  height: 24px;
  color: #9333ea;
}

.options-table-wrapper {
  overflow-x: auto;
}

.options-table {
  width: 100%;
  border-collapse: collapse;
}

.options-table th {
  padding: 14px 16px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
  text-align: left;
  background: #fafafa;
  border-bottom: 2px solid #e4e4e7;
}

.options-table th:first-child {
  border-radius: 12px 0 0 0;
}

.options-table th:last-child {
  border-radius: 0 12px 0 0;
}

.options-table td {
  padding: 16px;
  font-size: 0.9375rem;
  color: #3f3f46;
  border-bottom: 1px solid #f4f4f5;
}

.options-table tr:last-child td {
  border-bottom: none;
}

.term-value {
  font-weight: 700;
  color: #18181b;
  font-size: 1rem;
}

.term-unit {
  color: #71717a;
  font-size: 0.875rem;
}

.rate-cell {
  font-weight: 600;
}

.rate-max {
  color: #9333ea;
  font-size: 1rem;
}

/* Detail Grid */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-full {
  grid-column: span 2;
}

.detail-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
}

.detail-value {
  font-size: 0.9375rem;
  color: #18181b;
  line-height: 1.6;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 80px 24px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  border: 4px solid #f3e8ff;
  border-top-color: #9333ea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .product-detail-page {
    padding: 32px 16px;
  }

  .product-header-card,
  .options-card,
  .details-card {
    padding: 24px;
  }

  .product-title {
    font-size: 1.5rem;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .detail-full {
    grid-column: span 1;
  }

  .action-buttons {
    flex-direction: column;
  }

  .like-btn,
  .map-btn {
    justify-content: center;
  }
}
</style>
