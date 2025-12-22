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
      <div class="analysis-card">
        <div class="card-header">
          <div class="card-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/>
            </svg>
          </div>
          <div>
            <h2 class="card-title">사용자 분석 정보 입력</h2>
            <p class="card-subtitle">금융 목표에 맞는 상품을 찾아드립니다</p>
          </div>
        </div>

        <form class="analysis-form" @submit.prevent="submit">
          <!-- Purpose -->
          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
              목적
            </label>
            <div class="select-wrapper">
              <select v-model="form.purpose" class="form-select">
                <option value="목돈">목돈 마련</option>
                <option value="주택">주택 구매</option>
                <option value="여행">여행 자금</option>
              </select>
              <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>
          
          <!-- Period -->
          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              기간 (개월)
            </label>
            <div class="input-wrapper">
              <input 
                type="number" 
                v-model.number="form.period_months" 
                class="form-input"
                placeholder="예: 12"
              />
              <span class="input-suffix">개월</span>
            </div>
          </div>

          <!-- Monthly Amount -->
          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
              월 납입액
            </label>
            <div class="input-wrapper">
              <input 
                type="number" 
                v-model.number="form.monthly_amount" 
                class="form-input"
                placeholder="예: 500000"
              />
              <span class="input-suffix">원</span>
            </div>
          </div>

          <!-- Target Amount -->
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
                v-model.number="form.target_amount" 
                class="form-input"
                placeholder="예: 6000000"
              />
              <span class="input-suffix">원</span>
            </div>
          </div>

          <button class="submit-btn" :disabled="analysisStore.loading">
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
        </form>
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
          <h4 class="info-title">목표 달성 계획</h4>
          <p class="info-text">목표 금액 달성을 위한 구체적인 계획을 제시합니다</p>
        </div>
        
        <div class="info-card">
          <div class="info-icon amber">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <h4 class="info-title">안전한 투자</h4>
          <p class="info-text">예금자보호 대상 상품 위주로 추천드립니다</p>
        </div>
      </div>
    </main>
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

/* Analysis Card */
.analysis-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  margin-top: -40px;
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

/* Form */
.analysis-form {
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

/* Submit Button */
.submit-btn {
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
  margin-top: 8px;
  transition: all 0.2s;
}

.submit-btn svg {
  width: 20px;
  height: 20px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(147, 51, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
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

  .info-cards {
    grid-template-columns: 1fr;
  }
}
</style>