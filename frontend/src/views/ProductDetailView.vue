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
            <span class="product-type-badge" :class="route.params.type === 'deposit' ? 'deposit' : 'saving'">
              {{ route.params.type === 'deposit' ? '예금' : '적금' }}
            </span>
            <span class="product-join-badge" :class="joinDenyClass">
              {{ joinDenyText }}
            </span>
          </div>
          
          <div class="product-bank-info">
            <div class="bank-logo-large">
              <img
                v-if="bankLogoSrc"
                :src="bankLogoSrc"
                :alt="product.kor_co_nm"
                class="bank-logo-img-large"
                loading="lazy"
              />
            </div>
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


/* ✅ banks 폴더 png 전체 import */
const bankLogos = import.meta.glob('@/assets/banks/*.png', {
  eager: true,
  import: 'default',
})

/* ✅ 은행명 → 파일명 매핑 */
const BANK_FILE_MAP = {
  국민은행: "국민은행.png",
  신한은행: "신한은행.png",
  우리은행: "우리은행.png",
  농협은행주식회사: "농협은행.png",
  중소기업은행: "기업은행.png",
  한국산업은행: "산업은행.png",
  '주식회사 하나은행': "하나은행.png",
  씨티뱅크: "씨티뱅크.png",
  한국씨티은행: "citi.png",

  // 인터넷은행
  '주식회사 카카오뱅크': "카카오뱅크.png",
  '주식회사 케이뱅크': "케이뱅크.png",
  '토스뱅크 주식회사': "토스뱅크.png",

  // 지방은행
  부산은행: "부산은행.png",
  경남은행: "경남은행.png",
  아이엠뱅크: "아이엠뱅크.png",
  광주은행: "광주은행.png",
  제주은행: "제주은행.png",
  전북은행: "전북은행.png",
  수협은행: "수협은행.png",
  한국스탠다드차타드은행: "sc제일은행.png",
}

/* ✅ 상세페이지용 은행 로고 src */
const bankLogoSrc = computed(() => {
  if (!product.value?.kor_co_nm) return null

  const name = product.value.kor_co_nm.trim()

  let fileName = BANK_FILE_MAP[name]

  if (!fileName) {
    const normalized = name
      .replace(/^BNK/, '')
      .replace(/^IBK/, '')
      .replace(/^KEB/, '')
      .replace(/^NH/, '')
      .trim()
    fileName = BANK_FILE_MAP[normalized]
  }

  if (!fileName) return null

  return (
    bankLogos[`/src/assets/banks/${fileName}`] ||
    bankLogos[`@/assets/banks/${fileName}`] ||
    null
  )
})


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
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
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
  color: #7469B6;
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
  border-radius: 20px;
}

.product-type-badge.deposit {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
}

.product-type-badge.saving {
  color: #16a34a;
  background: rgba(22, 163, 74, 0.1);
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
  width: 130px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
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
  font-size: 1.55rem;
  font-weight: 600;
  color: #18181b;
  line-height: 1.3;
  margin-bottom: 70px;
  margin-top: 50px;
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
  color: #7469B6;
  border: 2px solid #E1AFD1;
}

.like-btn:hover {
  background: rgba(116, 105, 182, 0.05);
  border-color: #7469B6;
}

.like-btn.liked {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
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
  background: rgba(116, 105, 182, 0.1);
  color: #7469B6;
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
  color: #7469B6;
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
  color: #7469B6;
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
  border: 4px solid rgba(116, 105, 182, 0.1);
  border-top-color: #7469B6;
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

/* .bank-logo-img-large {
  width: 80px;
  height: 80px;
  object-fit: contain;
} */

/* Dark Mode */
[data-theme="dark"] .product-detail-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 50%, #0a0a0a 100%);
}

[data-theme="dark"] .back-link {
  color: #a1a1aa;
}

[data-theme="dark"] .back-link:hover {
  color: #c9b8c6;
}

[data-theme="dark"] .product-header-card,
[data-theme="dark"] .options-card,
[data-theme="dark"] .details-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .product-type-badge.deposit {
  background: rgba(37, 99, 235, 0.2);
  color: #93c5fd;
}

[data-theme="dark"] .product-type-badge.saving {
  background: rgba(22, 163, 74, 0.2);
  color: #86efac;
}

[data-theme="dark"] .badge-success {
  background: rgba(5, 150, 105, 0.2);
  color: #34d399;
}

[data-theme="dark"] .badge-warning {
  background: rgba(217, 119, 6, 0.2);
  color: #fbbf24;
}

[data-theme="dark"] .badge-info {
  background: rgba(2, 132, 199, 0.2);
  color: #38bdf8;
}

[data-theme="dark"] .product-title {
  color: #e4e4e7;
}

[data-theme="dark"] .like-btn {
  background: #27272a;
  border-color: rgba(116, 105, 182, 0.3);
  color: #c9b8c6;
}

[data-theme="dark"] .like-btn:hover {
  background: #3f3f46;
  border-color: #7469B6;
}

[data-theme="dark"] .like-btn.liked {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
}

[data-theme="dark"] .like-btn:not(.liked) .like-count {
  background: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .card-title {
  color: #e4e4e7;
}

[data-theme="dark"] .options-table th {
  background: #27272a;
  color: #a1a1aa;
  border-bottom-color: #3f3f46;
}

[data-theme="dark"] .options-table td {
  color: #a1a1aa;
  border-bottom-color: #27272a;
}

[data-theme="dark"] .term-value {
  color: #e4e4e7;
}

[data-theme="dark"] .rate-max {
  color: #d4b8d0;
}

[data-theme="dark"] .detail-label {
  color: #71717a;
}

[data-theme="dark"] .detail-value {
  color: #e4e4e7;
}

[data-theme="dark"] .loading-state p {
  color: #a1a1aa;
}
</style>
