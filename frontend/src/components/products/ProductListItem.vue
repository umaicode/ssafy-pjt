<template>
  <article class="product-card">
    <div class="product-card-header">
      <div class="product-type-badge">
        {{ type === "deposit" ? "예금" : "적금" }}
      </div>

      <div class="product-bank">
        <!-- ✅ 로고 있으면 은행 CI (로컬 assets/banks/*.png) -->
        <img
          v-if="bankLogoSrc"
          :src="bankLogoSrc"
          :alt="product.kor_co_nm"
          class="bank-logo-img"
          loading="lazy"
        />

        <!-- ✅ 없으면 기본 아이콘 -->
        <div v-else class="bank-logo" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 21h18" />
            <path d="M3 10h18" />
            <path d="M5 6l7-3 7 3" />
            <path d="M4 10v11" />
            <path d="M20 10v11" />
            <path d="M8 14v3" />
            <path d="M12 14v3" />
            <path d="M16 14v3" />
          </svg>
        </div>

        <!-- <span class="bank-name">{{ product.kor_co_nm }}</span> -->
      </div>
    </div>

    <div class="product-card-body">
      <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>

      <div v-if="product.options && product.options.length > 0" class="product-rates">
        <div class="rate-item">
          <span class="rate-label">기본금리</span>
          <span class="rate-value">{{ getMaxBasicRate }}%</span>
        </div>
        <div class="rate-item rate-max">
          <span class="rate-label">최고금리</span>
          <span class="rate-value">{{ getMaxPreferRate }}%</span>
        </div>
      </div>

      <div class="product-terms">
        <span v-for="term in uniqueTerms.slice(0, 4)" :key="term" class="term-badge">
          {{ term }}개월
        </span>
        <span v-if="uniqueTerms.length > 4" class="term-badge term-more">
          +{{ uniqueTerms.length - 4 }}
        </span>
      </div>
    </div>

    <div class="product-card-footer">
      <RouterLink
        :to="{ name: 'ProductDetailView', params: { type, fin_prdt_cd: product.fin_prdt_cd } }"
        class="detail-link"
      >
        상세정보
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14" />
          <path d="M12 5l7 7-7 7" />
        </svg>
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue"

/**
 * ✅ 폴더 전체를 "한 번에 import" 하는 Vite 방식
 * - src/assets/banks/ 폴더에 있는 png들을 자동으로 가져옴
 * - key는 "/src/assets/banks/파일명.png" 형태로 만들어짐
 */
const bankLogos = import.meta.glob("@/assets/banks/*.png", {
  eager: true,
  import: "default",
})

const props = defineProps({
  product: Object,
  type: String,
})

/**
 * ✅ 은행명(kor_co_nm) -> 로고 파일명 매핑
 * - 여기 파일명은 src/assets/banks/ 안의 실제 파일명과 동일해야 함
 * - 예: src/assets/banks/kb.png
 */
const BANK_FILE_MAP = {
  // 시중은행
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

/**
 * ✅ 현재 상품 은행명으로 로고 src 찾기
 * - 로고 없으면 null -> 기본 아이콘 노출
 */
const bankLogoSrc = computed(() => {
  const name = (props.product?.kor_co_nm || "").trim()
  if (!name) return null

  // 1) 정확 매칭
  let fileName = BANK_FILE_MAP[name]

  // 2) 접두어 제거 후 재시도 (BNK/IBK/KEB/NH)
  if (!fileName) {
    const normalized = name
      .replace(/^BNK/, "")
      .replace(/^IBK/, "")
      .replace(/^KEB/, "")
      .replace(/^NH/, "")
      .trim()
    fileName = BANK_FILE_MAP[normalized]
  }

  if (!fileName) return null

  // Vite glob 키는 보통 "/src/assets/..." 형태가 됨
  // 어떤 환경에선 "@/assets/..."가 아닐 수 있어 아래처럼 둘 다 시도
  return (
    bankLogos[`/src/assets/banks/${fileName}`] ||
    bankLogos[`@/assets/banks/${fileName}`] ||
    null
  )
})

const getMaxBasicRate = computed(() => {
  if (!props.product.options || props.product.options.length === 0) return "-"
  const rates = props.product.options.map((opt) => Number(opt.intr_rate) || 0)
  return Math.max(...rates).toFixed(2)
})

const getMaxPreferRate = computed(() => {
  if (!props.product.options || props.product.options.length === 0) return "-"
  const rates = props.product.options.map((opt) => Number(opt.intr_rate2) || 0)
  return Math.max(...rates).toFixed(2)
})

const uniqueTerms = computed(() => {
  if (!props.product.options) return []
  const terms = props.product.options.map((opt) => Number(opt.save_trm)).filter((t) => !isNaN(t))
  return [...new Set(terms)].sort((a, b) => a - b)
})
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(116, 105, 182, 0.15);
}

.product-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f4f4f5;
}

.product-type-badge {
  padding: 6px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  border-radius: 20px;
}

.product-bank {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bank-logo {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bank-logo svg {
  width: 18px;
  height: 18px;
  color: white;
}

.bank-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3f3f46;
}

.product-card-body {
  padding: 24px;
  flex: 1;
}

.product-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 20px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-rates {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.rate-item {
  flex: 1;
  padding: 16px;
  background: #fafafa;
  border-radius: 12px;
  text-align: center;
}

.rate-item.rate-max {
  background: linear-gradient(135deg, #FFE6E6 0%, rgba(116, 105, 182, 0.1) 100%);
}

.rate-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 500;
  color: #71717a;
  margin-bottom: 4px;
}

.rate-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #18181b;
}

.rate-max .rate-value {
  color: #7469B6;
}

.product-terms {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.term-badge {
  padding: 6px 10px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #52525b;
  background: #f4f4f5;
  border-radius: 6px;
}

.term-more {
  color: #71717a;
}

.product-card-footer {
  padding: 16px 24px;
  border-top: 1px solid #f4f4f5;
}

.detail-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #7469B6;
  text-decoration: none;
  transition: gap 0.2s ease;
}

.detail-link:hover {
  gap: 12px;
}

.detail-link svg {
  width: 16px;
  height: 16px;
}

.bank-logo-img {
  width: 80px;
  height: 32px;
  object-fit: contain;
}

/* Dark Mode */
[data-theme="dark"] .product-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .product-card:hover {
  box-shadow: 0 12px 40px rgba(116, 105, 182, 0.25);
}

[data-theme="dark"] .product-card-header {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .product-type-badge {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .bank-name {
  color: #a1a1aa;
}

[data-theme="dark"] .product-name {
  color: #e4e4e7;
}

[data-theme="dark"] .rate-item {
  background: #27272a;
}

[data-theme="dark"] .rate-item.rate-max {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.2) 0%, rgba(225, 175, 209, 0.15) 100%);
}

[data-theme="dark"] .rate-label {
  color: #a1a1aa;
}

[data-theme="dark"] .rate-value {
  color: #e4e4e7;
}

[data-theme="dark"] .rate-max .rate-value {
  color: #E1AFD1;
}

[data-theme="dark"] .term-badge {
  background: #27272a;
  color: #a1a1aa;
}

[data-theme="dark"] .product-card-footer {
  border-top-color: #27272a;
}

[data-theme="dark"] .detail-link {
  color: #E1AFD1;
}
</style>
