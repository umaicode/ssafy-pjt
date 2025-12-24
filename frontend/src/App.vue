<template>
  <div class="app">
    <!-- Navigation -->
    <header class="navbar">
      <div class="navbar-container">
        <!-- Logo -->
        <RouterLink :to="{ name: 'home' }" class="navbar-brand">
          F!NK
        </RouterLink>
        <!-- Main Navigation -->
        <nav class="navbar-menu">
          <RouterLink :to="{ name: 'ProductView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            금융상품
          </RouterLink>
          <RouterLink :to="{ name: 'AnalysisView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
            AI 분석
          </RouterLink>
          <RouterLink :to="{ name: 'NewsView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
            </svg>
            금융뉴스
          </RouterLink>
          <RouterLink :to="{ name: 'YoutubeSearchView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
              <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            유튜브
          </RouterLink>
          <RouterLink :to="{ name: 'MetalView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
            현물
          </RouterLink>
          <RouterLink :to="{ name: 'KakaoMapView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            은행찾기
          </RouterLink>
          <RouterLink :to="{ name: 'CommunityView' }" class="navbar-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
            </svg>
            커뮤니티
          </RouterLink>
        </nav>

                <!-- Exchange Rate Ticker -->
        <div v-if="accountStore.isLogin && exchangeStore.rates.length > 0" class="exchange-ticker">
          <div class="ticker-wrapper">
            <div 
              v-for="(rate, index) in exchangeStore.rates" 
              :key="rate.cur_unit"
              class="ticker-item"
              :class="{ active: index === currentRateIndex }"
            >
              <span class="ticker-name">{{ rate.cur_unit }}</span>
              <span class="ticker-rate">{{ formatRate(rate.deal_bas_r) }}</span>
            </div>
          </div>
        </div>

        <!-- Theme Toggle Button -->
        <div class="navbar-settings">
          <button class="settings-btn" @click="themeStore.toggleTheme" :title="themeStore.isDark ? '라이트 모드' : '다크 모드'">
            <svg v-if="themeStore.isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/>
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
            </svg>
          </button>
        </div>

        <!-- User Actions -->
        <div class="navbar-actions">
          <template v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'LogInView' }" class="btn btn-ghost btn-sm">
              로그인
            </RouterLink>
            <RouterLink :to="{ name: 'SignUpView' }" class="btn btn-primary btn-sm">
              회원가입
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'ProfileView' }" class="user-menu">
              <div class="user-avatar">
                {{ accountStore.nickname?.charAt(0) || 'U' }}
              </div>
              <span class="user-name">{{ accountStore.nickname }}</span>
            </RouterLink>
            <button @click="accountStore.logOut" class="btn btn-ghost btn-sm">
              로그아웃
            </button>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <svg v-if="!mobileMenuOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <Transition name="slide-down">
        <div v-if="mobileMenuOpen" class="mobile-menu">
          <RouterLink :to="{ name: 'ProductView' }" class="mobile-link" @click="mobileMenuOpen = false">금융상품</RouterLink>
          <RouterLink :to="{ name: 'AnalysisView' }" class="mobile-link" @click="mobileMenuOpen = false">AI 분석</RouterLink>
          <RouterLink :to="{ name: 'NewsView' }" class="mobile-link" @click="mobileMenuOpen = false">금융뉴스</RouterLink>
          <RouterLink :to="{ name: 'YoutubeSearchView' }" class="mobile-link" @click="mobileMenuOpen = false">유튜브</RouterLink>
          <RouterLink :to="{ name: 'MetalView' }" class="mobile-link" @click="mobileMenuOpen = false">현물</RouterLink>
          <RouterLink :to="{ name: 'KakaoMapView' }" class="mobile-link" @click="mobileMenuOpen = false">은행찾기</RouterLink>
          <RouterLink :to="{ name: 'CommunityView' }" class="mobile-link" @click="mobileMenuOpen = false">커뮤니티</RouterLink>
          <div class="mobile-divider"></div>
          <!-- Mobile Theme Toggle -->
          <div class="mobile-settings">
            <button class="mobile-settings-btn" @click="themeStore.toggleTheme">
              <svg v-if="themeStore.isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
              </svg>
              {{ themeStore.isDark ? '라이트 모드' : '다크 모드' }}
            </button>
          </div>
          <div class="mobile-divider"></div>
          <template v-if="!accountStore.isLogin">
            <RouterLink :to="{ name: 'LogInView' }" class="mobile-link" @click="mobileMenuOpen = false">로그인</RouterLink>
            <RouterLink :to="{ name: 'SignUpView' }" class="mobile-link" @click="mobileMenuOpen = false">회원가입</RouterLink>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'ProfileView' }" class="mobile-link" @click="mobileMenuOpen = false">마이페이지</RouterLink>
            <button class="mobile-link" @click="accountStore.logOut(); mobileMenuOpen = false">로그아웃</button>
          </template>
        </div>
      </Transition>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <span class="footer-logo">F!NK</span>
            <p class="footer-tagline">AI 기반 스마트 자산관리 플랫폼</p>
          </div>
          <div class="footer-links">
            <a href="#">이용약관</a>
            <a href="#">개인정보처리방침</a>
            <a href="#">고객센터</a>
          </div>
          <p class="footer-copyright">© 2025 F!NK. All rights reserved.</p>
        </div>
      </div>
    </footer>

    <!-- AI 챗봇 -->
    <ChatBot />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAccountStore } from './stores/accounts'
import { useExchangeStore } from './stores/exchange'
import { useThemeStore } from './stores/theme'
import ChatBot from './components/ChatBot.vue'

const accountStore = useAccountStore()
const exchangeStore = useExchangeStore()
const themeStore = useThemeStore()

const mobileMenuOpen = ref(false)
const currentRateIndex = ref(0)

let tickerInterval = null

// 환율 포맷팅
const formatRate = (rate) => {
  if (!rate) return '-'
  const numRate = parseFloat(rate.replace(/,/g, ''))
  return numRate.toLocaleString('ko-KR', { maximumFractionDigits: 2 })
}

// 통화별 이모지
const getCurrencyEmoji = (unit) => {
  const emojis = {
    'USD': '🇺🇸',
    'EUR': '🇪🇺',
    'JPY(100)': '🇯🇵',
    'CNH': '🇨🇳',
    'GBP': '🇬🇧',
    'THB': '🇹🇭',
    'SGD': '🇸🇬',
    'HKD': '🇭🇰',
  }
  return emojis[unit] || '💱'
}

// 3초마다 환율 자동 전환
const startTicker = () => {
  if (exchangeStore.rates.length === 0) return
  tickerInterval = setInterval(() => {
    currentRateIndex.value = (currentRateIndex.value + 1) % exchangeStore.rates.length
  }, 3000)
}

onMounted(() => {
  if (accountStore.isLogin) {
    startTicker()
  }
})

onUnmounted(() => {
  if (tickerInterval) clearInterval(tickerInterval)
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #FDFBFD;
}

/* ═══════════════════════════════════════════════════════════════════════════
   Navbar - Glassmorphism Style
   ═══════════════════════════════════════════════════════════════════════════ */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid rgba(116, 105, 182, 0.08);
  transition: all 0.3s ease;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.navbar-brand {
  font-size: 2.6rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.04em;
  text-decoration: none;
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  filter: brightness(1.1);
  transform: scale(1.02);
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 2px;
}

.navbar-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6e6e73;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.25s ease;
  position: relative;
}

.navbar-link::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #E1AFD1, #7469B6);
  border-radius: 1px;
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

.navbar-link:hover {
  color: #7469B6;
  background: rgba(116, 105, 182, 0.06);
}

.navbar-link:hover::after {
  width: 60%;
}

.navbar-link.router-link-active {
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  font-weight: 600;
}

.navbar-link.router-link-active::after {
  width: 60%;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.navbar-link:hover .nav-icon,
.navbar-link.router-link-active .nav-icon {
  opacity: 1;
}

/* Exchange Rate Ticker */
.exchange-ticker {
  position: relative;
  min-width: 140px;
  height: 34px;
  margin: 0 16px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(255, 230, 230, 0.5) 0%, rgba(225, 175, 209, 0.3) 100%);
  border-radius: 17px;
  padding: 0 14px;
  border: 1px solid rgba(116, 105, 182, 0.15);
  box-shadow: 0 2px 10px rgba(116, 105, 182, 0.08);
}

.ticker-wrapper {
  position: relative;
  height: 100%;
}

.ticker-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0;
  transform: translateY(12px);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.ticker-item.active {
  opacity: 1;
  transform: translateY(0);
}

.ticker-flag {
  font-size: 1rem;
}

.ticker-name {
  font-size: 0.6875rem;
  font-weight: 700;
  color: #7469B6;
  min-width: 38px;
  letter-spacing: 0.01em;
}

.ticker-rate {
  font-size: 0.75rem;
  font-weight: 600;
  color: #AD88C6;
  margin-left: auto;
}

/* Settings Buttons */
.navbar-settings {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-right: 12px;
}

.settings-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(116, 105, 182, 0.06);
  border: 1px solid rgba(116, 105, 182, 0.1);
  color: #6e6e73;
  cursor: pointer;
  transition: all 0.25s ease;
}

.settings-btn:hover {
  background: rgba(116, 105, 182, 0.12);
  color: #7469B6;
  transform: translateY(-1px);
}

.settings-btn svg {
  width: 18px;
  height: 18px;
}

.settings-btn.lang-btn {
  font-size: 0.8125rem;
  font-weight: 700;
}

.lang-text {
  line-height: 1;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px 6px 6px;
  background: rgba(116, 105, 182, 0.08);
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.user-menu:hover {
  background: rgba(116, 105, 182, 0.12);
  border-color: rgba(116, 105, 182, 0.1);
  transform: translateY(-1px);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 50%, #7469B6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.2);
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1d1d1f;
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #6e6e73;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.25s ease;
}

.mobile-menu-btn:hover {
  background: rgba(116, 105, 182, 0.08);
  color: #7469B6;
}

.mobile-menu-btn svg {
  width: 24px;
  height: 24px;
}

/* Mobile Menu */
.mobile-menu {
  display: none;
  flex-direction: column;
  padding: 16px;
  background: rgba(255, 255, 255, 0.98);
  border-top: 1px solid rgba(116, 105, 182, 0.08);
}

.mobile-link {
  display: block;
  padding: 14px 16px;
  font-size: 1rem;
  font-weight: 500;
  color: #3f3f46;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.25s ease;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  width: 100%;
}

.mobile-link:hover,
.mobile-link.router-link-active {
  background: rgba(116, 105, 182, 0.08);
  color: #7469B6;
}

.mobile-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(116, 105, 182, 0.15), transparent);
  margin: 12px 0;
}

/* Mobile Settings */
.mobile-settings {
  display: flex;
  gap: 10px;
  padding: 8px 0;
}

.mobile-settings-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  background: rgba(116, 105, 182, 0.06);
  border: 1px solid rgba(116, 105, 182, 0.12);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.mobile-settings-btn svg {
  width: 18px;
  height: 18px;
}

.mobile-settings-btn:hover {
  background: rgba(116, 105, 182, 0.12);
  color: #7469B6;
}

/* ═══════════════════════════════════════════════════════════════════════════
   Main Content
   ═══════════════════════════════════════════════════════════════════════════ */
.main-content {
  flex: 1;
  width: 100%;
}

/* ═══════════════════════════════════════════════════════════════════════════
   Footer - Modern Style (70% 축소)
   ═══════════════════════════════════════════════════════════════════════════ */
.footer {
  background: #2d2d44;
  color: white;
  padding: 20px 24px 28px;
  margin-top: auto;
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(116, 105, 182, 0.4), transparent);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.footer-brand {
  margin-bottom: 16px;
}

.footer-logo {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #FFE6E6 0%, #E1AFD1 35%, #AD88C6 70%, #7469B6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
}

.footer-tagline {
  color: #86868b;
  font-size: 0.8125rem;
  margin-top: 6px;
  letter-spacing: -0.01em;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
}

.footer-links a {
  color: #a1a1aa;
  font-size: 0.8125rem;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 3px 0;
  position: relative;
}

.footer-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, #E1AFD1, #7469B6);
  transition: width 0.3s ease;
}

.footer-links a:hover {
  color: #E1AFD1;
}

.footer-links a:hover::after {
  width: 100%;
}

.footer-copyright {
  color: #52525b;
  font-size: 0.75rem;
  letter-spacing: -0.01em;
}

/* ═══════════════════════════════════════════════════════════════════════════
   Transitions
   ═══════════════════════════════════════════════════════════════════════════ */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ═══════════════════════════════════════════════════════════════════════════
   Responsive Design
   ═══════════════════════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .navbar-menu {
    display: none;
  }

  .exchange-ticker {
    display: flex;
    max-width: 120px;
    overflow: hidden;
  }

  .navbar-actions {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-menu {
    display: flex;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    height: 64px;
    padding: 0 16px;
  }

  .navbar-brand {
    font-size: 1.5rem;
  }

  .navbar-settings {
    margin-right: 8px;
  }

  .footer {
    padding: 48px 16px 32px;
  }

  .footer-links {
    flex-wrap: wrap;
    gap: 20px;
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   Dark Mode Styles
   ═══════════════════════════════════════════════════════════════════════════ */
[data-theme="dark"] .app {
  background: #0a0a0a;
}

[data-theme="dark"] .navbar {
  background: rgba(10, 10, 10, 0.85);
  border-bottom-color: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .navbar-link {
  color: #a1a1aa;
}

[data-theme="dark"] .navbar-link:hover {
  color: #E1AFD1;
  background: rgba(116, 105, 182, 0.1);
}

[data-theme="dark"] .navbar-link.router-link-active {
  color: #E1AFD1;
  background: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .exchange-ticker {
  background: linear-gradient(135deg, rgba(116, 105, 182, 0.15) 0%, rgba(173, 136, 198, 0.1) 100%);
  border-color: rgba(116, 105, 182, 0.25);
}

[data-theme="dark"] .ticker-name {
  color: #E1AFD1;
}

[data-theme="dark"] .ticker-rate {
  color: #AD88C6;
}

[data-theme="dark"] .settings-btn {
  background: rgba(116, 105, 182, 0.1);
  border-color: rgba(116, 105, 182, 0.2);
  color: #a1a1aa;
}

[data-theme="dark"] .settings-btn:hover {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .user-menu {
  background: rgba(116, 105, 182, 0.12);
}

[data-theme="dark"] .user-menu:hover {
  background: rgba(116, 105, 182, 0.18);
}

[data-theme="dark"] .user-name {
  color: #e4e4e7;
}

[data-theme="dark"] .mobile-menu {
  background: rgba(10, 10, 10, 0.98);
  border-top-color: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .mobile-link {
  color: #a1a1aa;
}

[data-theme="dark"] .mobile-link:hover,
[data-theme="dark"] .mobile-link.router-link-active {
  background: rgba(116, 105, 182, 0.12);
  color: #E1AFD1;
}

[data-theme="dark"] .mobile-settings-btn {
  background: rgba(116, 105, 182, 0.1);
  border-color: rgba(116, 105, 182, 0.2);
  color: #a1a1aa;
}

[data-theme="dark"] .mobile-settings-btn:hover {
  background: rgba(116, 105, 182, 0.18);
  color: #E1AFD1;
}

[data-theme="dark"] .footer {
  background: linear-gradient(180deg, #18181b 0%, #09090b 100%);
}

[data-theme="dark"] .footer-tagline {
  color: #a1a1aa;
}

[data-theme="dark"] .footer-links a {
  color: #d4d4d8;
}

[data-theme="dark"] .footer-copyright {
  color: #71717a;
}
</style>