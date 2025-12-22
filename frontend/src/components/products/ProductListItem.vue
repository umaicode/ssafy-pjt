<template>
  <article class="product-card">
    <div class="product-card-header">
      <div class="product-type-badge">
        {{ type === 'deposit' ? '예금' : '적금' }}
      </div>
      <div class="product-bank">
        <div class="bank-logo">
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
        <span class="bank-name">{{ product.kor_co_nm }}</span>
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
          <path d="M5 12h14"/>
          <path d="M12 5l7 7-7 7"/>
        </svg>
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: Object,
  type: String,
})

const getMaxBasicRate = computed(() => {
  if (!props.product.options || props.product.options.length === 0) return '-'
  const rates = props.product.options.map(opt => Number(opt.intr_rate) || 0)
  return Math.max(...rates).toFixed(2)
})

const getMaxPreferRate = computed(() => {
  if (!props.product.options || props.product.options.length === 0) return '-'
  const rates = props.product.options.map(opt => Number(opt.intr_rate2) || 0)
  return Math.max(...rates).toFixed(2)
})

const uniqueTerms = computed(() => {
  if (!props.product.options) return []
  const terms = props.product.options.map(opt => Number(opt.save_trm)).filter(t => !isNaN(t))
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
  box-shadow: 0 12px 40px rgba(147, 51, 234, 0.15);
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
  color: #9333ea;
  background: #f3e8ff;
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
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
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
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
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
  color: #9333ea;
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
  color: #9333ea;
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
</style>