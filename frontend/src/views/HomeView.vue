<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-orb hero-orb-1"></div>
        <div class="hero-orb hero-orb-2"></div>
        <div class="hero-orb hero-orb-3"></div>
      </div>
      
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-icon">✨</span>
          AI 기반 금융 플랫폼
        </div>
        
        <h1 class="hero-title">
          당신의 금융을<br>
          <span class="text-gradient">더 스마트하게</span>
        </h1>
        
        <p class="hero-description">
          F!NK와 함께 예금, 적금 상품을 비교하고 AI 추천을 받아보세요.<br>
          실시간 뉴스와 커뮤니티로 금융 정보를 한눈에 확인하세요.
        </p>
        
        <div class="hero-actions">
          <RouterLink :to="{ name: 'AnalysisView' }" class="btn btn-primary btn-lg">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            AI 분석 시작하기
          </RouterLink>
          <RouterLink :to="{ name: 'ProductView' }" class="btn btn-glass btn-lg">
            상품 둘러보기
          </RouterLink>
        </div>
        
        <!-- Stats -->
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-value">500+</span>
            <span class="stat-label">금융 상품</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat">
            <span class="stat-value">24개</span>
            <span class="stat-label">제휴 은행</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat">
            <span class="stat-value">실시간</span>
            <span class="stat-label">AI 분석</span>
          </div>
        </div>
      </div>
      
      <!-- Hero Visual -->
      <div class="hero-visual">
        <div class="hero-card hero-card-1">
          <div class="mini-card-icon">💰</div>
          <div class="mini-card-content">
            <span class="mini-card-title">예금 추천</span>
            <span class="mini-card-value">연 4.5%</span>
          </div>
        </div>
        <div class="hero-card hero-card-2">
          <div class="mini-card-icon">📈</div>
          <div class="mini-card-content">
            <span class="mini-card-title">적금 상품</span>
            <span class="mini-card-value">연 5.2%</span>
          </div>
        </div>
        <div class="hero-card hero-card-3">
          <div class="mini-card-icon">🤖</div>
          <div class="mini-card-content">
            <span class="mini-card-title">AI 분석 완료</span>
            <span class="mini-card-value">맞춤 추천</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="section-header">
        <h2 class="section-title">F!NK와 함께하는 금융 생활</h2>
        <p class="section-subtitle">복잡한 금융, 이제 쉽고 스마트하게 관리하세요</p>
      </div>
      
      <div class="features-grid">
        <RouterLink :to="{ name: 'ProductView' }" class="feature-card">
          <div class="feature-icon feature-icon-purple">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h3 class="feature-title">금융상품 비교</h3>
          <p class="feature-description">
            500개 이상의 예금·적금 상품을 한눈에 비교하고 나에게 맞는 상품을 찾아보세요.
          </p>
          <span class="feature-link">
            상품 보기 <span class="arrow">→</span>
          </span>
        </RouterLink>

        <RouterLink :to="{ name: 'AnalysisView' }" class="feature-card">
          <div class="feature-icon feature-icon-pink">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <h3 class="feature-title">AI 맞춤 추천</h3>
          <p class="feature-description">
            AI가 나의 재정 상황과 목표를 분석해 최적의 금융 상품을 추천해드려요.
          </p>
          <span class="feature-link">
            분석 시작 <span class="arrow">→</span>
          </span>
        </RouterLink>

        <RouterLink :to="{ name: 'NewsView' }" class="feature-card">
          <div class="feature-icon feature-icon-blue">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
            </svg>
          </div>
          <h3 class="feature-title">실시간 뉴스</h3>
          <p class="feature-description">
            금융 시장의 최신 뉴스를 실시간으로 확인하고 중요한 정보를 북마크하세요.
          </p>
          <span class="feature-link">
            뉴스 보기 <span class="arrow">→</span>
          </span>
        </RouterLink>

        <RouterLink :to="{ name: 'MetalView' }" class="feature-card">
          <div class="feature-icon feature-icon-gold">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
          </div>
          <h3 class="feature-title">현물 시세</h3>
          <p class="feature-description">
            금, 은 등 현물 상품의 실시간 시세를 차트로 확인하고 투자 타이밍을 잡으세요.
          </p>
          <span class="feature-link">
            시세 확인 <span class="arrow">→</span>
          </span>
        </RouterLink>

        <RouterLink :to="{ name: 'KakaoMapView' }" class="feature-card">
          <div class="feature-icon feature-icon-teal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <h3 class="feature-title">주변 은행 찾기</h3>
          <p class="feature-description">
            현재 위치에서 가장 가까운 은행과 ATM을 지도에서 바로 찾아보세요.
          </p>
          <span class="feature-link">
            은행 찾기 <span class="arrow">→</span>
          </span>
        </RouterLink>

        <RouterLink :to="{ name: 'CommunityView' }" class="feature-card">
          <div class="feature-icon feature-icon-orange">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
            </svg>
          </div>
          <h3 class="feature-title">커뮤니티</h3>
          <p class="feature-description">
            다른 사용자들과 금융 정보를 공유하고 투자 전략을 함께 이야기해보세요.
          </p>
          <span class="feature-link">
            참여하기 <span class="arrow">→</span>
          </span>
        </RouterLink>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-card">
        <div class="cta-content">
          <h2 class="cta-title">
            지금 바로 시작하세요
          </h2>
          <p class="cta-description">
            회원가입하고 AI가 분석하는 나만의 맞춤 금융 상품을 추천받으세요.
          </p>
          <div class="cta-actions">
            <RouterLink 
              v-if="!accountStore.isLogin" 
              :to="{ name: 'SignUpView' }" 
              class="btn btn-primary btn-lg"
            >
              무료로 시작하기
            </RouterLink>
            <RouterLink 
              v-else 
              :to="{ name: 'AnalysisView' }" 
              class="btn btn-primary btn-lg"
            >
              AI 분석 받기
            </RouterLink>
          </div>
        </div>
        <div class="cta-decoration">
          <div class="cta-circle cta-circle-1"></div>
          <div class="cta-circle cta-circle-2"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
</script>

<style scoped>
/* Hero Section */
.hero {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  padding: 80px 0;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: -1;
}

.hero-gradient {
  position: absolute;
  top: -50%;
  left: -20%;
  width: 80%;
  height: 150%;
  background: radial-gradient(circle, rgba(147, 51, 234, 0.08) 0%, transparent 70%);
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.6;
}

.hero-orb-1 {
  top: 10%;
  right: 20%;
  width: 300px;
  height: 300px;
  background: rgba(147, 51, 234, 0.15);
  animation: float 8s ease-in-out infinite;
}

.hero-orb-2 {
  bottom: 20%;
  left: 10%;
  width: 200px;
  height: 200px;
  background: rgba(236, 72, 153, 0.12);
  animation: float 6s ease-in-out infinite reverse;
}

.hero-orb-3 {
  top: 40%;
  right: 30%;
  width: 150px;
  height: 150px;
  background: rgba(59, 130, 246, 0.1);
  animation: float 10s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(147, 51, 234, 0.1);
  border: 1px solid rgba(147, 51, 234, 0.2);
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #9333ea;
  margin-bottom: 24px;
}

.badge-icon {
  font-size: 1rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  color: #18181b;
  margin-bottom: 24px;
  letter-spacing: -0.03em;
}

.text-gradient {
  background: linear-gradient(135deg, #9333ea 0%, #c084fc 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #52525b;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 32px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #18181b;
}

.stat-label {
  font-size: 0.875rem;
  color: #71717a;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #e4e4e7;
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 400px;
}

.hero-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  animation: float 6s ease-in-out infinite;
}

.hero-card-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.hero-card-2 {
  top: 40%;
  right: 5%;
  animation-delay: -2s;
}

.hero-card-3 {
  bottom: 10%;
  left: 20%;
  animation-delay: -4s;
}

.mini-card-icon {
  font-size: 2rem;
}

.mini-card-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mini-card-title {
  font-size: 0.8125rem;
  color: #71717a;
}

.mini-card-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
}

/* Features Section */
.features-section {
  margin-bottom: 80px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 12px;
}

.section-subtitle {
  font-size: 1.0625rem;
  color: #71717a;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  position: relative;
  padding: 32px;
  background: white;
  border-radius: 24px;
  border: 1px solid #f4f4f5;
  text-decoration: none;
  transition: all 0.3s ease;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 2px;
  background: linear-gradient(135deg, transparent 50%, rgba(147, 51, 234, 0.1) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -15px rgba(147, 51, 234, 0.15);
  border-color: rgba(147, 51, 234, 0.2);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.feature-icon svg {
  width: 28px;
  height: 28px;
}

.feature-icon-purple {
  background: rgba(147, 51, 234, 0.1);
  color: #9333ea;
}

.feature-icon-pink {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.feature-icon-blue {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.feature-icon-gold {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.feature-icon-teal {
  background: rgba(20, 184, 166, 0.1);
  color: #14b8a6;
}

.feature-icon-orange {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin-bottom: 12px;
}

.feature-description {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: #71717a;
  margin-bottom: 20px;
}

.feature-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #9333ea;
}

.feature-link .arrow {
  transition: transform 0.2s ease;
}

.feature-card:hover .feature-link .arrow {
  transform: translateX(4px);
}

/* CTA Section */
.cta-section {
  margin-bottom: 40px;
}

.cta-card {
  position: relative;
  padding: 64px;
  background: linear-gradient(135deg, #1a1625 0%, #2d1f47 50%, #1a1625 100%);
  border-radius: 32px;
  overflow: hidden;
}

.cta-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: white;
  margin-bottom: 16px;
}

.cta-description {
  font-size: 1.0625rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 32px;
}

.cta-actions {
  display: flex;
  justify-content: center;
}

.cta-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.cta-circle {
  position: absolute;
  border-radius: 50%;
}

.cta-circle-1 {
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(147, 51, 234, 0.3) 0%, transparent 70%);
}

.cta-circle-2 {
  bottom: -150px;
  left: -50px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.2) 0%, transparent 70%);
}

/* Responsive */
@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 40px;
    padding: 40px 0;
  }

  .hero-visual {
    display: none;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-description {
    font-size: 1rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .hero-stats {
    flex-wrap: wrap;
    gap: 24px;
  }

  .stat-divider {
    display: none;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .cta-card {
    padding: 40px 24px;
  }

  .cta-title {
    font-size: 1.75rem;
  }

  .exchange-body {
    flex-wrap: wrap;
  }

  .rate-value {
    font-size: 2rem;
  }
}
</style>