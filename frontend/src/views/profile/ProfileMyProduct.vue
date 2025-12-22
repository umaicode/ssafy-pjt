<template>
  <div class="my-product-section">
    <div class="section-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18"/>
          <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
        </svg>
      </div>
      <div class="header-text">
        <h2 class="section-title">금융상품 그래프</h2>
        <p class="section-description">관심 상품들의 금리 비교 및 분석 차트를 확인하세요</p>
      </div>
    </div>

    <div class="chart-placeholder">
      <div class="placeholder-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M3 9h18"/>
          <path d="M9 21V9"/>
          <circle cx="15" cy="15" r="2"/>
        </svg>
      </div>
      <h3 class="placeholder-title">준비 중입니다</h3>
      <p class="placeholder-text">
        금융상품 비교 차트 기능이 곧 추가될 예정이에요.<br>
        조금만 기다려주세요!
      </p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.my-product-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
}

.section-description {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: #fafafa;
  border: 2px dashed #e4e4e7;
  border-radius: 20px;
  text-align: center;
}

.placeholder-icon {
  width: 80px;
  height: 80px;
  background: #f3e8ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.placeholder-icon svg {
  width: 40px;
  height: 40px;
  color: #9333ea;
}

.placeholder-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 8px;
}

.placeholder-text {
  font-size: 0.9375rem;
  color: #71717a;
  line-height: 1.6;
  margin: 0;
}
</style>