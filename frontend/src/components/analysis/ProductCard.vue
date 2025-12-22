<template>
  <div class="product-card">
    <!-- Card Header -->
    <div class="card-header">
      <div class="bank-info">
        <div class="bank-logo">{{ d.bank?.charAt(0) || 'B' }}</div>
        <div class="bank-text">
          <span class="bank-name">{{ d.bank }}</span>
          <h4 class="product-name">{{ d.name }}</h4>
        </div>
      </div>
      <div class="fit-score" :class="scoreClass">
        {{ (item.fit_score * 100).toFixed(0) }}%
      </div>
    </div>

    <!-- Rate Info -->
    <div class="rate-section">
      <div class="rate-item">
        <span class="rate-label">기본금리</span>
        <span class="rate-value">{{ d.intr_rate }}%</span>
      </div>
      <div class="rate-divider"></div>
      <div class="rate-item">
        <span class="rate-label">최고금리</span>
        <span class="rate-value highlight">{{ d.intr_rate2 }}%</span>
      </div>
    </div>

    <!-- Product Details -->
    <div class="details-section">
      <div class="detail-row">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
        </svg>
        <span>기간: {{ d.save_trm }}개월</span>
      </div>
      <div v-if="d.max_limit" class="detail-row">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="1" x2="12" y2="23"/>
          <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
        </svg>
        <span>한도: {{ d.max_limit.toLocaleString() }}원</span>
      </div>
    </div>

    <!-- Join Way Tags -->
    <div v-if="joinWayTags.length" class="tags-section">
      <span class="tag" v-for="tag in joinWayTags" :key="tag">
        {{ tag }}
      </span>
    </div>

    <!-- Plan Box -->
    <div v-if="plan" class="plan-box">
      <!-- 적금: 월납 -->
      <template v-if="plan.type === 'monthly'">
        <div class="plan-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span class="plan-title">{{ plan.term_months }}개월 기준 목표 달성 계획</span>
        </div>
        <div class="plan-content">
          <p class="plan-item">
            목표 달성 월납입액: <strong>{{ plan.required_monthly_amount?.toLocaleString() }}원</strong>
          </p>
          <p v-if="plan.extra_needed_per_month > 0" class="plan-item warning">
            현재보다 추가로: <strong>+{{ plan.extra_needed_per_month.toLocaleString() }}원/월</strong>
          </p>
          <p class="plan-note">
            현재 계획 유지 시 {{ plan.term_months }}개월 후 
            {{ plan.planned_total_amount.toLocaleString() }}원 → 
            부족 {{ plan.shortfall_amount.toLocaleString() }}원
          </p>
        </div>
      </template>

      <!-- 예금: 일시납 -->
      <template v-else-if="plan.type === 'lump_sum'">
        <div class="plan-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="1" x2="12" y2="23"/>
            <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
          </svg>
          <span class="plan-title">예금(일시납) 안내</span>
        </div>
        <div class="plan-content">
          <p class="plan-item">
            목표 달성 필요 금액: <strong>{{ plan.required_lump_sum?.toLocaleString() }}원</strong>
          </p>
          <p class="plan-note">{{ plan.message }}</p>
        </div>
      </template>
    </div>

    <!-- Special Conditions -->
    <details class="conditions-section">
      <summary class="conditions-summary">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
        우대 조건 보기
      </summary>
      <p class="conditions-text">{{ d.spcl_cnd || '우대 조건 정보가 없습니다.' }}</p>
    </details>

    <!-- AI Reason -->
    <div class="reason-section">
      <div class="reason-header">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <span>AI 추천 이유</span>
      </div>
      <p class="reason-text">{{ item.reason }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const d = props.item.detail
const plan = props.item.plan

const joinWayTags = computed(() =>
  d?.join_way?.split(',').map(v => v.trim()) || []
)

const scoreClass = computed(() => {
  const score = props.item.fit_score * 100
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  return 'normal'
})
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.bank-info {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.bank-logo {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.bank-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bank-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #71717a;
}

.product-name {
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
  line-height: 1.3;
}

.fit-score {
  padding: 6px 12px;
  font-size: 0.875rem;
  font-weight: 700;
  border-radius: 20px;
}

.fit-score.excellent {
  background: #dcfce7;
  color: #16a34a;
}

.fit-score.good {
  background: #fef3c7;
  color: #d97706;
}

.fit-score.normal {
  background: #f4f4f5;
  color: #71717a;
}

/* Rate Section */
.rate-section {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #faf5ff;
  border-radius: 14px;
}

.rate-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.rate-label {
  font-size: 0.75rem;
  color: #71717a;
}

.rate-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #18181b;
}

.rate-value.highlight {
  color: #9333ea;
}

.rate-divider {
  width: 1px;
  height: 36px;
  background: #e4e4e7;
}

/* Details Section */
.details-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.875rem;
  color: #52525b;
}

.detail-row svg {
  width: 16px;
  height: 16px;
  color: #a1a1aa;
}

/* Tags Section */
.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 6px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #3b82f6;
  background: #dbeafe;
  border-radius: 6px;
}

/* Plan Box */
.plan-box {
  padding: 16px;
  background: #f0fdf4;
  border-left: 4px solid #16a34a;
  border-radius: 12px;
}

.plan-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.plan-header svg {
  width: 18px;
  height: 18px;
  color: #16a34a;
}

.plan-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #166534;
}

.plan-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.plan-item {
  font-size: 0.875rem;
  color: #166534;
  margin: 0;
}

.plan-item strong {
  font-weight: 700;
}

.plan-item.warning {
  color: #dc2626;
}

.plan-note {
  font-size: 0.75rem;
  color: #52525b;
  margin: 4px 0 0;
}

/* Conditions Section */
.conditions-section {
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  overflow: hidden;
}

.conditions-summary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  background: #fafafa;
  cursor: pointer;
  list-style: none;
}

.conditions-summary::-webkit-details-marker {
  display: none;
}

.conditions-summary svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s;
}

.conditions-section[open] .conditions-summary svg {
  transform: rotate(90deg);
}

.conditions-text {
  padding: 16px;
  font-size: 0.875rem;
  color: #52525b;
  line-height: 1.6;
  margin: 0;
  border-top: 1px solid #e4e4e7;
}

/* Reason Section */
.reason-section {
  padding: 16px;
  background: #fef3c7;
  border-radius: 12px;
}

.reason-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.reason-header svg {
  width: 18px;
  height: 18px;
  color: #d97706;
}

.reason-header span {
  font-size: 0.8125rem;
  font-weight: 700;
  color: #92400e;
}

.reason-text {
  font-size: 0.875rem;
  color: #78350f;
  line-height: 1.6;
  margin: 0;
  font-style: italic;
}
</style>
