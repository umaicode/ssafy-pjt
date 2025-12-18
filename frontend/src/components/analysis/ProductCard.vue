<template>
  <div class="card">
    <h3>{{ d.bank }} · {{ d.name }}</h3>

    <p>기간: {{ d.save_trm }}개월</p>
    <p>금리: {{ d.intr_rate }}% (최대 {{ d.intr_rate2 }}%)</p>
    <p v-if="d.max_limit">한도: {{ d.max_limit.toLocaleString() }}원</p>

    <!-- 가입 채널 태그 -->
    <div class="tags">
      <span
        v-for="tag in joinWayTags"
        :key="tag"
        class="tag"
      >
        {{ tag }}
      </span>
    </div>

    <!-- 우대 조건 -->
    <details>
      <summary>우대 조건</summary>
      <p>{{ d.spcl_cnd }}</p>
    </details>

    <!-- ✅ 목표 달성 계획 (핵심 UX) -->
    <div v-if="plan" class="plan-box">
      <!-- 적금: 월납 -->
      <template v-if="plan.type === 'monthly'">
        <p class="plan-title">
          🎯 {{ plan.term_months }}개월 기준 목표 달성 계획
        </p>
        <p>
          · 목표 달성 월납입액:
          <b>{{ plan.required_monthly_amount?.toLocaleString() }}원</b>
        </p>
        <p v-if="plan.extra_needed_per_month > 0" class="warn">
          · 현재보다 추가로:
          <b>+{{ plan.extra_needed_per_month.toLocaleString() }}원/월</b>
        </p>
        <p class="sub">
          (현재 계획 유지 시 {{ plan.term_months }}개월 후
          {{ plan.planned_total_amount.toLocaleString() }}원 →
          부족 {{ plan.shortfall_amount.toLocaleString() }}원)
        </p>
      </template>

      <!-- 예금: 일시납 -->
      <template v-else-if="plan.type === 'lump_sum'">
        <p class="plan-title">
          💰 예금(일시납) 안내
        </p>
        <p>
          · 목표 달성을 위해
          <b>{{ plan.required_lump_sum?.toLocaleString() }}원</b>
          수준의 목돈 예치가 필요합니다.
        </p>
        <p class="sub">
          {{ plan.message }}
        </p>
      </template>
    </div>

    <!-- GPT 추천 이유 -->
    <p class="reason">🤖 {{ item.reason }}</p>

    <!-- 적합도 -->
    <p class="score">적합도: {{ (item.fit_score * 100).toFixed(0) }}%</p>
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
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.tags {
  margin: 8px 0;
}
.tag {
  background: #eef;
  padding: 4px 8px;
  margin-right: 6px;
  border-radius: 6px;
  font-size: 12px;
}

.plan-box {
  margin-top: 12px;
  padding: 12px;
  background: #f9fafc;
  border-left: 4px solid #4f7cff;
  border-radius: 6px;
  font-size: 14px;
}
.plan-title {
  font-weight: bold;
  margin-bottom: 6px;
}
.warn {
  color: #d9534f;
  font-weight: 600;
}
.sub {
  color: #666;
  font-size: 12px;
  margin-top: 4px;
}

.reason {
  margin-top: 12px;
  font-style: italic;
}
.score {
  font-weight: bold;
  margin-top: 6px;
}
</style>
