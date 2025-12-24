<template>
  <div class="home">
    <!-- Hero Section - 제주은행 스타일 풀스크린 히어로 -->
    <section class="hero-section">
      <!-- Animated Background -->
      <div class="hero-bg">
        <div class="hero-gradient-mesh"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="orb orb-4"></div>
        <div class="particles">
          <span v-for="n in 20" :key="n" class="particle"></span>
        </div>
      </div>
      
      <div class="hero-container">
        <div class="hero-content">
          <!-- AI Badge -->
          <div class="ai-chip">
            <span class="ai-chip-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <span class="ai-chip-text">AI 기반 자산관리 플랫폼</span>
            <span class="ai-chip-dot"></span>
          </div>
          
          <!-- Main Title -->
          <h1 class="hero-title">
            <span class="title-line">
              <span class="title-word">당신의</span>
              <span class="title-word">금융을</span>
            </span>
            <span class="title-line title-highlight">
              <span class="title-gradient">더 스마트하게</span>
            </span>
          </h1>
          
          <!-- Description -->
          <p class="hero-description">
            F!NK의 AI가 당신의 재정 상황을 분석하고<br>
            <strong>최적의 금융 상품</strong>을 추천해 드립니다.
          </p>
          
          <!-- CTA Buttons -->
          <div class="hero-cta">
            <RouterLink :to="{ name: 'AnalysisView' }" class="btn-hero-primary">
              <span class="btn-content">
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                AI 분석 시작하기
              </span>
              <span class="btn-shine"></span>
            </RouterLink>
            <RouterLink :to="{ name: 'ProductView' }" class="btn-hero-secondary">
              상품 둘러보기
              <svg class="btn-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </RouterLink>
          </div>

          <!-- Stats -->
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">50<span class="stat-plus">+</span></span>
              <span class="stat-label">금융 상품</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">24<span class="stat-unit">개</span></span>
              <span class="stat-label">제휴 은행</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">실시간</span>
              <span class="stat-label">AI 분석</span>
            </div>
          </div>
        </div>
        
        <!-- Hero Visual - Floating Cards -->
        <div class="hero-visual">
          <div class="visual-container">
            <!-- Main Card -->
            <div class="floating-card main-card">
              <div class="card-header">
                <div class="card-icon ai">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="currentColor" stroke-width="1.5"/>
                  </svg>
                </div>
                <span class="card-badge">AI 분석 완료</span>
              </div>
              <div class="card-body">
                <p class="card-title">맞춤 추천 상품</p>
                <p class="card-value">3<span class="card-unit">건</span></p>
              </div>
              <div class="card-footer">
                <div class="card-progress">
                  <div class="progress-bar"></div>
                </div>
                <span class="card-status">분석 정확도 98%</span>
              </div>
            </div>
            
            <!-- Deposit Card -->
            <div class="floating-card deposit-card">
              <div class="card-mini-icon">💰</div>
              <div class="card-mini-content">
                <span class="mini-label">예금 추천</span>
                <span class="mini-value">연 4.5%</span>
              </div>
            </div>
            
            <!-- Savings Card -->
            <div class="floating-card savings-card">
              <div class="card-mini-icon">📈</div>
              <div class="card-mini-content">
                <span class="mini-label">적금 상품</span>
                <span class="mini-value">연 5.2%</span>
              </div>
            </div>

            <!-- Notification Card -->
            <div class="floating-card notification-card">
              <div class="notif-dot"></div>
              <span class="notif-text">새로운 상품이 추천되었습니다</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="scroll-indicator">
        <span class="scroll-text">스크롤하여 더 알아보기</span>
        <div class="scroll-mouse">
          <div class="scroll-wheel"></div>
        </div>
      </div>
    </section>

    <!-- AI Feature Section -->
    <section class="ai-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">핵심 기능</span>
          <h2 class="section-title">
            <span class="title-gradient-reverse">AI</span>가 당신의 자산을<br>분석합니다
          </h2>
          <p class="section-subtitle">
            복잡한 금융 상품 비교, 이제 AI에게 맡기세요
          </p>
        </div>

        <div class="ai-features">
          <div class="ai-feature-card main-feature">
            <div class="feature-visual">
              <div class="ai-brain">
                <svg viewBox="0 0 80 80" fill="none">
                  <circle cx="40" cy="40" r="35" stroke="url(#gradient1)" stroke-width="2" opacity="0.3"/>
                  <circle cx="40" cy="40" r="25" stroke="url(#gradient1)" stroke-width="2" opacity="0.5"/>
                  <circle cx="40" cy="40" r="15" stroke="url(#gradient1)" stroke-width="2"/>
                  <circle cx="40" cy="40" r="5" fill="url(#gradient1)"/>
                  <defs>
                    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#FFE6E6"/>
                      <stop offset="50%" style="stop-color:#AD88C6"/>
                      <stop offset="100%" style="stop-color:#7469B6"/>
                    </linearGradient>
                  </defs>
                </svg>
                <div class="pulse-ring"></div>
                <div class="pulse-ring delay-1"></div>
                <div class="pulse-ring delay-2"></div>
              </div>
            </div>
            <div class="feature-content">
              <h3 class="feature-title">
                <span class="highlight">맞춤형</span> AI 자산 분석
              </h3>
              <p class="feature-description">
                당신의 재정 상황, 목표, 위험 성향을 종합 분석하여<br>
                가장 적합한 금융 상품을 추천해 드립니다.
              </p>
              <RouterLink :to="{ name: 'AnalysisView' }" class="feature-link">
                지금 분석 시작하기
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2"/>
                </svg>
              </RouterLink>
            </div>
          </div>

          <div class="ai-feature-grid">
            <div class="ai-mini-feature">
              <div class="mini-feature-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h4>실시간 분석</h4>
              <p>최신 금융 데이터를 실시간으로 분석</p>
            </div>
            <div class="ai-mini-feature">
              <div class="mini-feature-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h4>안전한 데이터</h4>
              <p>개인정보 암호화 및 보안 처리</p>
            </div>
            <div class="ai-mini-feature">
              <div class="mini-feature-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h4>최적화 추천</h4>
              <p>수익률 극대화를 위한 맞춤 제안</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">서비스</span>
          <h2 class="section-title">F!NK와 함께하는<br>스마트 금융 생활</h2>
          <p class="section-subtitle">
            모든 금융 서비스를 한 곳에서 관리하세요
          </p>
        </div>

        <div class="services-grid">
          <RouterLink :to="{ name: 'ProductView' }" class="service-card">
            <div class="service-icon purple">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>금융상품 비교</h3>
              <p>50개 이상의 예금·적금 상품을 한눈에 비교하세요</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>

          <RouterLink :to="{ name: 'AnalysisView' }" class="service-card featured">
            <div class="service-badge">AI 추천</div>
            <div class="service-icon pink">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>AI 맞춤 추천</h3>
              <p>AI가 분석하는 나만의 최적 금융 솔루션</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>

          <RouterLink :to="{ name: 'NewsView' }" class="service-card">
            <div class="service-icon blue">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>실시간 뉴스</h3>
              <p>금융 시장 최신 뉴스와 트렌드를 확인하세요</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>

          <RouterLink :to="{ name: 'MetalView' }" class="service-card">
            <div class="service-icon gold">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>현물 시세</h3>
              <p>금, 은 등 현물 상품의 실시간 시세를 확인하세요</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>

          <RouterLink :to="{ name: 'KakaoMapView' }" class="service-card">
            <div class="service-icon teal">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="2"/>
                <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>주변 은행 찾기</h3>
              <p>가까운 은행과 ATM을 지도에서 찾아보세요</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>

          <RouterLink :to="{ name: 'CommunityView' }" class="service-card">
            <div class="service-icon orange">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="service-content">
              <h3>커뮤니티</h3>
              <p>다른 사용자들과 금융 정보를 공유하세요</p>
            </div>
            <span class="service-arrow">→</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Partner Banks Section -->
    <section class="partners-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">제휴 은행</span>
          <h2 class="section-title">24개 금융기관과<br>함께합니다</h2>
        </div>

        <div class="partners-marquee">
          <div class="marquee-track">
            <div class="partner-logo" v-for="bank in banks" :key="bank">
              <img :src="getBankLogo(bank)" :alt="bank" class="bank-img" />
            </div>
            <div class="partner-logo" v-for="bank in banks" :key="bank + '-dup'">
              <img :src="getBankLogo(bank)" :alt="bank" class="bank-img" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <div class="cta-bg">
          <div class="cta-orb cta-orb-1"></div>
          <div class="cta-orb cta-orb-2"></div>
        </div>
        <div class="cta-content">
          <h2 class="cta-title">
            지금 바로<br>
            <span class="cta-gradient">AI 분석</span>을 시작하세요
          </h2>
          <p class="cta-description">
            회원가입하고 나만의 맞춤 금융 상품을 추천받으세요
          </p>
          <div class="cta-buttons">
            <RouterLink 
              v-if="!accountStore.isLogin" 
              :to="{ name: 'SignUpView' }" 
              class="btn-cta-primary"
            >
              무료로 시작하기
            </RouterLink>
            <RouterLink 
              v-else 
              :to="{ name: 'AnalysisView' }" 
              class="btn-cta-primary"
            >
              AI 분석 받기
            </RouterLink>
          </div>
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

// 은행 목록
const banks = [
  '국민은행', '신한은행', '하나은행', '우리은행', '농협은행',
  '기업은행', '카카오뱅크', '토스뱅크', '케이뱅크', '부산은행',
  '경남은행', '광주은행', '전북은행', '제주은행', '아이엠뱅크'
]

// 은행 로고 가져오기
const getBankLogo = (bankName) => {
  const logoMap = {
    '국민은행': '국민은행.png',
    '신한은행': '신한은행.png',
    '하나은행': '하나은행.png',
    '우리은행': '우리은행.png',
    '농협은행': '농협은행.jpg',
    '기업은행': '기업은행.png',
    '카카오뱅크': '카카오뱅크.png',
    '토스뱅크': '토스뱅크.png',
    '케이뱅크': '케이뱅크.png',
    '부산은행': '부산은행.png',
    '경남은행': '경남은행.png',
    '광주은행': '광주은행.png',
    '전북은행': '전북은행.png',
    '제주은행': '제주은행.png',
    '아이엠뱅크': '아이엠뱅크.png'
  }
  return new URL(`../assets/banks/${logoMap[bankName]}`, import.meta.url).href
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════════════════
   Hero Section - 풀스크린 모션 UI
   ═══════════════════════════════════════════════════════════════════════════ */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 100%);
}

/* Animated Background */
.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
}

.hero-gradient-mesh {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(ellipse 60% 40% at 10% 20%, rgba(225, 175, 209, 0.25) 0%, transparent 50%),
    radial-gradient(ellipse 50% 50% at 90% 10%, rgba(173, 136, 198, 0.2) 0%, transparent 50%),
    radial-gradient(ellipse 40% 60% at 80% 80%, rgba(116, 105, 182, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 20% 90%, rgba(255, 230, 230, 0.3) 0%, transparent 50%);
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.6;
  animation: orbFloat 20s ease-in-out infinite;
}

.orb-1 {
  top: 10%;
  left: 15%;
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, rgba(255, 230, 230, 0.6), rgba(225, 175, 209, 0.4));
  animation-delay: 0s;
}

.orb-2 {
  top: 50%;
  right: 10%;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(173, 136, 198, 0.5), rgba(116, 105, 182, 0.3));
  animation-delay: -5s;
}

.orb-3 {
  bottom: 10%;
  left: 30%;
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.4), rgba(173, 136, 198, 0.3));
  animation-delay: -10s;
}

.orb-4 {
  top: 30%;
  right: 30%;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, rgba(225, 175, 209, 0.5), rgba(255, 230, 230, 0.4));
  animation-delay: -15s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -40px) scale(1.05); }
  50% { transform: translate(-20px, -60px) scale(0.95); }
  75% { transform: translate(-40px, -20px) scale(1.02); }
}

/* Particles */
.particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: linear-gradient(135deg, #E1AFD1, #7469B6);
  border-radius: 50%;
  opacity: 0.4;
  animation: particleFloat 15s ease-in-out infinite;
}

.particle:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { top: 30%; left: 20%; animation-delay: -1s; }
.particle:nth-child(3) { top: 40%; left: 30%; animation-delay: -2s; }
.particle:nth-child(4) { top: 50%; left: 40%; animation-delay: -3s; }
.particle:nth-child(5) { top: 60%; left: 50%; animation-delay: -4s; }
.particle:nth-child(6) { top: 70%; left: 60%; animation-delay: -5s; }
.particle:nth-child(7) { top: 80%; left: 70%; animation-delay: -6s; }
.particle:nth-child(8) { top: 15%; left: 80%; animation-delay: -7s; }
.particle:nth-child(9) { top: 25%; left: 90%; animation-delay: -8s; }
.particle:nth-child(10) { top: 35%; left: 5%; animation-delay: -9s; }
.particle:nth-child(11) { top: 45%; left: 15%; animation-delay: -10s; }
.particle:nth-child(12) { top: 55%; left: 25%; animation-delay: -11s; }
.particle:nth-child(13) { top: 65%; left: 35%; animation-delay: -12s; }
.particle:nth-child(14) { top: 75%; left: 45%; animation-delay: -13s; }
.particle:nth-child(15) { top: 85%; left: 55%; animation-delay: -14s; }
.particle:nth-child(16) { top: 10%; left: 65%; animation-delay: -15s; }
.particle:nth-child(17) { top: 20%; left: 75%; animation-delay: -16s; }
.particle:nth-child(18) { top: 30%; left: 85%; animation-delay: -17s; }
.particle:nth-child(19) { top: 40%; left: 95%; animation-delay: -18s; }
.particle:nth-child(20) { top: 90%; left: 85%; animation-delay: -19s; }

@keyframes particleFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.4; }
  50% { transform: translateY(-100px) rotate(180deg); opacity: 0.8; }
}

/* Hero Container */
.hero-container {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 120px 24px 80px;
}

/* Hero Content */
.hero-content {
  animation: fadeInUp 1s ease forwards;
}

/* 애니메이션 클래스 - 제주은행 스타일 */
.animate-fade-in {
  animation: fadeInUp 0.8s ease forwards;
  opacity: 0;
}

.animate-slide-left {
  animation: slideInLeft 0.8s ease forwards;
  opacity: 0;
}

.animate-slide-right {
  animation: slideInRight 0.8s ease forwards;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn 0.6s ease forwards;
  opacity: 0;
}

.animate-bounce-in {
  animation: bounceIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
  opacity: 0;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-60px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(60px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@keyframes float-gentle {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-10px) rotate(1deg);
  }
  50% {
    transform: translateY(-20px) rotate(0deg);
  }
  75% {
    transform: translateY(-10px) rotate(-1deg);
  }
}

@keyframes glow-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(116, 105, 182, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(116, 105, 182, 0.6), 0 0 60px rgba(225, 175, 209, 0.3);
  }
}

.ai-chip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(116, 105, 182, 0.15);
  border-radius: 50px;
  margin-bottom: 28px;
  animation: fadeInUp 0.8s ease forwards, glow-pulse 3s ease-in-out infinite;
  animation-delay: 0.2s;
  opacity: 0;
  position: relative;
  overflow: hidden;
}

.ai-chip::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  background-size: 200% 100%;
  animation: shimmer 3s infinite;
}

.ai-chip-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #E1AFD1, #7469B6);
  border-radius: 8px;
  color: white;
}

.ai-chip-icon svg {
  width: 14px;
  height: 14px;
}

.ai-chip-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #7469B6;
  letter-spacing: -0.01em;
}

.ai-chip-dot {
  width: 8px;
  height: 8px;
  background: #34c759;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.hero-title {
  font-size: clamp(3rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.05;
  color: #1d1d1f;
  margin-bottom: 24px;
  letter-spacing: -0.04em;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.3s;
  opacity: 0;
}

.title-line {
  display: block;
  overflow: hidden;
}

.title-word {
  display: inline-block;
  margin-right: 12px;
  animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

.title-word:nth-child(1) {
  animation-delay: 0.4s;
}

.title-word:nth-child(2) {
  animation-delay: 0.5s;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.title-gradient {
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 30%, #AD88C6 60%, #7469B6 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease infinite, slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 0.6s;
  opacity: 0;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.hero-description {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #6e6e73;
  margin-bottom: 36px;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.4s;
  opacity: 0;
}

.hero-description strong {
  color: #1d1d1f;
  font-weight: 600;
}

/* CTA Buttons */
.hero-cta {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.5s;
  opacity: 0;
}

.btn-hero-primary {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 18px 36px;
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  background-size: 200% 200%;
  color: white;
  font-size: 1.0625rem;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  overflow: hidden;
  transition: all 0.4s ease;
  box-shadow: 0 20px 50px -15px rgba(116, 105, 182, 0.4);
  animation: gradientShift 3s ease infinite, glow-pulse 2s ease-in-out infinite;
}

.btn-hero-primary:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 25px 60px -15px rgba(116, 105, 182, 0.5);
}

.btn-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-icon {
  width: 22px;
  height: 22px;
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.btn-hero-primary:hover {
  transform: scale(1.03) translateY(-3px);
  box-shadow: 0 30px 60px -15px rgba(116, 105, 182, 0.5);
}

.btn-hero-primary:hover .btn-shine {
  left: 100%;
}

.btn-hero-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 18px 32px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  border: 1.5px solid rgba(116, 105, 182, 0.2);
  color: #7469B6;
  font-size: 1.0625rem;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.4s ease;
}

.btn-hero-secondary:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: #AD88C6;
  transform: translateY(-3px);
}

.btn-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.btn-hero-secondary:hover .btn-arrow {
  transform: translateX(4px);
}

/* Stats */
.hero-stats {
  display: flex;
  align-items: center;
  gap: 36px;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.6s;
  opacity: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1d1d1f;
  letter-spacing: -0.03em;
}

.stat-plus, .stat-unit {
  font-size: 1.25rem;
  color: #7469B6;
}

.stat-label {
  font-size: 0.875rem;
  color: #86868b;
}

.stat-divider {
  width: 1px;
  height: 48px;
  background: linear-gradient(180deg, transparent, #d2d2d7, transparent);
}

/* Hero Visual - Floating Cards */
.hero-visual {
  position: relative;
  height: 500px;
  animation: fadeIn 1s ease forwards;
  animation-delay: 0.4s;
  opacity: 0;
}

.visual-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  box-shadow: 0 20px 60px -20px rgba(116, 105, 182, 0.2);
  animation: float 6s ease-in-out infinite, fadeInScale 0.8s ease forwards;
  opacity: 0;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

.main-card {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 280px;
  padding: 28px;
  animation-delay: 0.8s;
  transition: all 0.4s ease;
}

.main-card:hover {
  transform: translate(-50%, -50%) scale(1.05);
  box-shadow: 0 30px 80px -20px rgba(116, 105, 182, 0.35);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
}

.card-icon.ai {
  background: linear-gradient(135deg, #FFE6E6, #E1AFD1);
  color: #7469B6;
}

.card-icon svg {
  width: 24px;
  height: 24px;
}

.card-badge {
  padding: 6px 12px;
  background: linear-gradient(135deg, #E1AFD1, #7469B6);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 20px;
  animation: pulse 2s ease-in-out infinite;
  position: relative;
  overflow: hidden;
}

.card-badge::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

.card-body {
  margin-bottom: 20px;
}

.card-title {
  font-size: 0.875rem;
  color: #86868b;
  margin-bottom: 8px;
}

.card-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1d1d1f;
  letter-spacing: -0.03em;
}

.card-unit {
  font-size: 1.5rem;
  color: #86868b;
  margin-left: 4px;
}

.card-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-progress {
  height: 6px;
  background: #f0f0f3;
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, #FFE6E6, #E1AFD1, #AD88C6, #7469B6);
  background-size: 200% 100%;
  border-radius: 3px;
  animation: progressGrow 1.5s ease forwards 1.5s, progressShimmer 2s linear infinite;
}

@keyframes progressGrow {
  0% {
    width: 0;
  }
  100% {
    width: 80%;
  }
}

@keyframes progressShimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.card-status {
  font-size: 0.8125rem;
  color: #34c759;
  font-weight: 500;
  animation: fadeIn 0.5s ease forwards 2s;
  opacity: 0;
}

/* Mini Cards */
.deposit-card {
  top: 15%;
  left: 5%;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 24px;
  animation: floatSmall 6s ease-in-out infinite, miniCardFadeIn 0.6s ease forwards 1s;
  opacity: 0;
  transition: all 0.3s ease;
}

.deposit-card:hover {
  transform: translateY(-20px) scale(1.05);
  box-shadow: 0 25px 50px -15px rgba(116, 105, 182, 0.3);
}

.savings-card {
  top: 25%;
  right: 0%;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 24px;
  animation: floatSmall 6s ease-in-out infinite 1s, miniCardFadeIn 0.6s ease forwards 1.2s;
  opacity: 0;
  transition: all 0.3s ease;
}

.savings-card:hover {
  transform: translateY(-20px) scale(1.05);
  box-shadow: 0 25px 50px -15px rgba(116, 105, 182, 0.3);
}

.notification-card {
  bottom: 15%;
  left: 10%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  animation: floatSmall 6s ease-in-out infinite 2s, miniCardFadeIn 0.6s ease forwards 1.4s;
  opacity: 0;
  transition: all 0.3s ease;
}

.notification-card:hover {
  transform: translateY(-20px) scale(1.05);
}

@keyframes miniCardFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-mini-icon {
  font-size: 1.75rem;
}

.card-mini-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mini-label {
  font-size: 0.75rem;
  color: #86868b;
}

.mini-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1d1d1f;
}

.notif-dot {
  width: 8px;
  height: 8px;
  background: #ff3b30;
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

.notif-text {
  font-size: 0.8125rem;
  color: #1d1d1f;
  font-weight: 500;
}

@keyframes float {
  0%, 100% { transform: translate(-50%, -50%) translateY(0); }
  50% { transform: translate(-50%, -50%) translateY(-20px); }
}

@keyframes floatSmall {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-8px) rotate(0.5deg); }
  50% { transform: translateY(-15px) rotate(0deg); }
  75% { transform: translateY(-8px) rotate(-0.5deg); }
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  animation: fadeIn 1s ease forwards;
  animation-delay: 1.5s;
  opacity: 0;
}

.scroll-text {
  font-size: 0.75rem;
  color: #86868b;
  letter-spacing: 0.05em;
}

.scroll-mouse {
  width: 24px;
  height: 40px;
  border: 2px solid #d2d2d7;
  border-radius: 12px;
  position: relative;
}

.scroll-wheel {
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 8px;
  background: #AD88C6;
  border-radius: 2px;
  animation: scrollWheel 2s ease-in-out infinite;
}

@keyframes scrollWheel {
  0%, 100% { top: 8px; opacity: 1; }
  50% { top: 20px; opacity: 0.3; }
}

/* ═══════════════════════════════════════════════════════════════════════════
   AI Section
   ═══════════════════════════════════════════════════════════════════════════ */
.ai-section {
  padding: 120px 0;
  background: white;
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 64px;
}

.section-badge {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(225, 175, 209, 0.2), rgba(116, 105, 182, 0.2));
  color: #7469B6;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 20px;
  margin-bottom: 20px;
}

.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  color: #1d1d1f;
  line-height: 1.15;
  margin-bottom: 16px;
  letter-spacing: -0.03em;
}

.title-gradient-reverse {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 50%, #E1AFD1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #86868b;
  max-width: 500px;
  margin: 0 auto;
}

.ai-features {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.ai-feature-card.main-feature {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  padding: 60px;
  background: linear-gradient(135deg, #FFF5F8 0%, #FDFBFD 100%);
  border-radius: 32px;
  border: 1px solid rgba(225, 175, 209, 0.2);
}

.feature-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-brain {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-brain svg {
  width: 100%;
  height: 100%;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pulse-ring {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(116, 105, 182, 0.3);
  border-radius: 50%;
  animation: pulseRing 3s ease-out infinite;
}

.pulse-ring.delay-1 { animation-delay: 1s; }
.pulse-ring.delay-2 { animation-delay: 2s; }

@keyframes pulseRing {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.5); opacity: 0; }
}

.feature-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1d1d1f;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.feature-title .highlight {
  color: #7469B6;
}

.feature-description {
  font-size: 1.125rem;
  color: #6e6e73;
  line-height: 1.6;
}

.feature-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #7469B6;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: gap 0.3s ease;
}

.feature-link:hover {
  gap: 14px;
}

.feature-link svg {
  width: 18px;
  height: 18px;
}

/* Mini Features Grid */
.ai-feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.ai-mini-feature {
  padding: 32px;
  background: white;
  border-radius: 24px;
  border: 1px solid #f0f0f3;
  text-align: center;
  transition: all 0.4s ease;
}

.ai-mini-feature:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px -20px rgba(116, 105, 182, 0.2);
  border-color: rgba(225, 175, 209, 0.3);
}

.mini-feature-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 230, 230, 0.5), rgba(225, 175, 209, 0.3));
  border-radius: 16px;
  color: #7469B6;
}

.mini-feature-icon svg {
  width: 28px;
  height: 28px;
}

.ai-mini-feature h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.ai-mini-feature p {
  font-size: 0.9375rem;
  color: #86868b;
}

/* ═══════════════════════════════════════════════════════════════════════════
   Services Section
   ═══════════════════════════════════════════════════════════════════════════ */
.services-section {
  padding: 120px 0;
  background: #f5f5f7;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.service-card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 32px;
  background: white;
  border-radius: 24px;
  text-decoration: none;
  transition: all 0.4s ease;
  overflow: hidden;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 60px -20px rgba(116, 105, 182, 0.2);
}

.service-card.featured {
  background: linear-gradient(135deg, #FFF5F8 0%, white 100%);
  border: 1px solid rgba(225, 175, 209, 0.3);
}

.service-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #E1AFD1, #7469B6);
  color: white;
  font-size: 0.6875rem;
  font-weight: 700;
  border-radius: 20px;
  letter-spacing: 0.02em;
}

.service-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  margin-bottom: 20px;
}

.service-icon svg {
  width: 28px;
  height: 28px;
}

.service-icon.purple {
  background: rgba(116, 105, 182, 0.1);
  color: #7469B6;
}

.service-icon.pink {
  background: rgba(225, 175, 209, 0.2);
  color: #AD88C6;
}

.service-icon.blue {
  background: rgba(0, 122, 255, 0.1);
  color: #007aff;
}

.service-icon.gold {
  background: rgba(255, 159, 10, 0.1);
  color: #ff9f0a;
}

.service-icon.teal {
  background: rgba(48, 209, 88, 0.1);
  color: #30d158;
}

.service-icon.orange {
  background: rgba(255, 149, 0, 0.1);
  color: #ff9500;
}

.service-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.service-content p {
  font-size: 0.9375rem;
  color: #86868b;
  line-height: 1.5;
}

.service-arrow {
  margin-top: auto;
  padding-top: 20px;
  font-size: 1.25rem;
  color: #AD88C6;
  transition: transform 0.3s ease;
}

.service-card:hover .service-arrow {
  transform: translateX(8px);
}

/* ═══════════════════════════════════════════════════════════════════════════
   Partners Section
   ═══════════════════════════════════════════════════════════════════════════ */
.partners-section {
  padding: 100px 0;
  background: white;
  overflow: hidden;
}

.partners-marquee {
  margin-top: 48px;
  overflow: hidden;
}

.marquee-track {
  display: flex;
  gap: 40px;
  animation: marquee 30s linear infinite;
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.partner-logo {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bank-img {
  width: 72px;
  height: 72px;
  object-fit: contain;
  padding: 12px;
  background: white;
  border-radius: 16px;
  border: 1px solid #f0f0f3;
  transition: all 0.3s ease;
}

.bank-img:hover {
  transform: scale(1.1);
  box-shadow: 0 10px 30px -10px rgba(116, 105, 182, 0.2);
}

/* ═══════════════════════════════════════════════════════════════════════════
   CTA Section
   ═══════════════════════════════════════════════════════════════════════════ */
.cta-section {
  padding: 60px 24px 100px;
}

.cta-container {
  position: relative;
  max-width: 1000px;
  margin: 0 auto;
  padding: 80px 60px;
  background: linear-gradient(135deg, #1d1d1f 0%, #2D2660 100%);
  border-radius: 40px;
  overflow: hidden;
}

.cta-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.cta-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.cta-orb-1 {
  top: -100px;
  right: -50px;
  width: 300px;
  height: 300px;
  background: rgba(173, 136, 198, 0.4);
  animation: orbFloat 15s ease-in-out infinite;
}

.cta-orb-2 {
  bottom: -100px;
  left: -50px;
  width: 250px;
  height: 250px;
  background: rgba(225, 175, 209, 0.3);
  animation: orbFloat 20s ease-in-out infinite reverse;
}

.cta-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.cta-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  color: white;
  line-height: 1.15;
  margin-bottom: 20px;
  letter-spacing: -0.03em;
}

.cta-gradient {
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 50%, #AD88C6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cta-description {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 36px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
}

.btn-cta-primary {
  padding: 18px 40px;
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  color: white;
  font-size: 1.0625rem;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.4s ease;
  box-shadow: 0 20px 50px -15px rgba(116, 105, 182, 0.5);
}

.btn-cta-primary:hover {
  transform: scale(1.05) translateY(-3px);
  box-shadow: 0 30px 60px -15px rgba(116, 105, 182, 0.6);
}

/* ═══════════════════════════════════════════════════════════════════════════
   Responsive Design
   ═══════════════════════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 60px;
    padding-top: 100px;
  }

  .hero-visual {
    height: 400px;
  }

  .main-card {
    width: 260px;
  }

  .ai-feature-card.main-feature {
    grid-template-columns: 1fr;
    gap: 40px;
    padding: 40px;
  }

  .ai-feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: auto;
    padding-bottom: 60px;
  }

  .hero-container {
    padding: 80px 20px 40px;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-description {
    font-size: 1.0625rem;
  }

  .hero-cta {
    flex-direction: column;
  }

  .hero-stats {
    flex-wrap: wrap;
    gap: 24px;
  }

  .stat-divider {
    display: none;
  }

  .hero-visual {
    display: none;
  }

  .scroll-indicator {
    display: none;
  }

  .ai-section,
  .services-section,
  .partners-section {
    padding: 80px 0;
  }

  .ai-feature-grid,
  .services-grid {
    grid-template-columns: 1fr;
  }

  .cta-container {
    padding: 48px 28px;
    border-radius: 28px;
  }

  .cta-title {
    font-size: 1.75rem;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

/* ═══════════════════════════════════════════════════════════════════════════
   Dark Mode Styles
   ═══════════════════════════════════════════════════════════════════════════ */
[data-theme="dark"] .home {
  background: #121215;
}

[data-theme="dark"] .hero-gradient-mesh {
  background: 
    radial-gradient(at 40% 20%, rgba(116, 105, 182, 0.35) 0px, transparent 50%),
    radial-gradient(at 80% 0%, rgba(173, 136, 198, 0.3) 0px, transparent 50%),
    radial-gradient(at 0% 50%, rgba(116, 105, 182, 0.25) 0px, transparent 50%);
}

[data-theme="dark"] .ai-chip {
  background: rgba(39, 39, 42, 0.95);
  border-color: rgba(116, 105, 182, 0.4);
}

[data-theme="dark"] .ai-chip-text {
  color: #f0d4eb;
}

[data-theme="dark"] .hero-title .title-word {
  color: #f4f4f5;
}

[data-theme="dark"] .hero-description {
  color: #d4d4d8;
}

[data-theme="dark"] .hero-description strong {
  color: #f0d4eb;
}

[data-theme="dark"] .stat-number {
  color: #f4f4f5;
}

[data-theme="dark"] .stat-label {
  color: #d4d4d8;
}

[data-theme="dark"] .stat-divider {
  background: rgba(116, 105, 182, 0.5);
}

[data-theme="dark"] .floating-card {
  background: rgba(39, 39, 42, 0.98);
  border-color: rgba(116, 105, 182, 0.3);
  box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .card-title {
  color: #d4d4d8;
}

[data-theme="dark"] .card-value {
  color: #f4f4f5;
}

[data-theme="dark"] .mini-label {
  color: #d4d4d8;
}

[data-theme="dark"] .mini-value {
  color: #f4f4f5;
}

[data-theme="dark"] .notif-text {
  color: #f4f4f5;
}

[data-theme="dark"] .ai-section {
  background: linear-gradient(180deg, #121215 0%, #1e1e22 100%);
}

[data-theme="dark"] .section-title {
  color: #f4f4f5;
}

[data-theme="dark"] .section-subtitle {
  color: #d4d4d8;
}

[data-theme="dark"] .ai-feature-card.main-feature {
  background: linear-gradient(145deg, rgba(50, 50, 55, 0.95), rgba(39, 39, 42, 0.98));
  border-color: rgba(116, 105, 182, 0.3);
}

[data-theme="dark"] .feature-title {
  color: #f4f4f5;
}

[data-theme="dark"] .feature-description {
  color: #d4d4d8;
}

[data-theme="dark"] .feature-link {
  color: #f0d4eb;
}

[data-theme="dark"] .ai-mini-feature {
  background: #1e1e22;
  border-color: rgba(116, 105, 182, 0.2);
}

[data-theme="dark"] .ai-mini-feature:hover {
  border-color: rgba(116, 105, 182, 0.5);
  background: #252528;
}

[data-theme="dark"] .ai-mini-feature h4 {
  color: #f4f4f5;
}

[data-theme="dark"] .ai-mini-feature p {
  color: #d4d4d8;
}

[data-theme="dark"] .mini-feature-title {
  color: #f4f4f5;
}

[data-theme="dark"] .mini-feature-desc {
  color: #d4d4d8;
}

[data-theme="dark"] .services-section {
  background: #121215;
}

[data-theme="dark"] .service-card {
  background: #1e1e22;
  border-color: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .service-card:hover {
  border-color: rgba(116, 105, 182, 0.4);
  background: #252528;
}

[data-theme="dark"] .service-card h3 {
  color: #f4f4f5;
}

[data-theme="dark"] .service-card p {
  color: #d4d4d8;
}

[data-theme="dark"] .service-title {
  color: #f4f4f5;
}

[data-theme="dark"] .service-description {
  color: #d4d4d8;
}

[data-theme="dark"] .partners-section {
  background: linear-gradient(180deg, #121215 0%, #1e1e22 100%);
}

[data-theme="dark"] .partners-grid {
  background: #1e1e22;
  border-color: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .cta-section {
  background: #121215;
}

[data-theme="dark"] .cta-container {
  background: linear-gradient(145deg, rgba(50, 50, 55, 0.95), rgba(39, 39, 42, 0.98));
  border-color: rgba(116, 105, 182, 0.3);
}

[data-theme="dark"] .cta-title {
  color: #f4f4f5;
}

[data-theme="dark"] .cta-description {
  color: #d4d4d8;
}

[data-theme="dark"] .scroll-text {
  color: #d4d4d8;
}

[data-theme="dark"] .scroll-mouse {
  border-color: #71717a;
}
</style>