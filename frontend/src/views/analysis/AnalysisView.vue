<template>
  <div>
    <h1>사용자 분석</h1>

    <form @submit.prevent="submit">
      <div>
        <label>목적</label>
        <select v-model="form.purpose">
          <option value="목돈">목돈</option>
          <option value="주택">주택</option>
          <option value="여행">여행</option>
        </select>
      </div>
      
      <div>
        <label>기간(개월)</label>
        <input type="number" v-model.number="form.period_months" />
      </div>

      <div>
        <label>월 납입액</label>
        <input type="number" v-model.number="form.monthly_amount" />
      </div>

      <div>
        <label>목표 금액</label>
        <input type="number" v-model.number="form.target_amount" />
      </div>

      <button :disabled="analysisStore.loading">
        {{ analysisStore.loading ? '분석 중...' : '분석하기' }}
      </button>

    </form>
  </div>
</template>

<script setup>
  import { reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAnalysisStore } from '@/stores/analysis'

  const router = useRouter()
  const analysisStore = useAnalysisStore()

  const form = reactive({
    purpose: '목돈',
    period_months: 12,
    monthly_amount: 500000,
    target_amount: 6000000,
  })

  const submit = () => {
    analysisStore.createAnalysis(form)
  }
</script>

<style scoped>

</style>