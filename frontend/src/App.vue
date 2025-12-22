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
            뉴스
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
          <RouterLink :to="{ name: 'NewsView' }" class="mobile-link" @click="mobileMenuOpen = false">뉴스</RouterLink>
          <RouterLink :to="{ name: 'YoutubeSearchView' }" class="mobile-link" @click="mobileMenuOpen = false">유튜브</RouterLink>
          <RouterLink :to="{ name: 'MetalView' }" class="mobile-link" @click="mobileMenuOpen = false">현물</RouterLink>
          <RouterLink :to="{ name: 'KakaoMapView' }" class="mobile-link" @click="mobileMenuOpen = false">은행찾기</RouterLink>
          <RouterLink :to="{ name: 'CommunityView' }" class="mobile-link" @click="mobileMenuOpen = false">커뮤니티</RouterLink>
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
            <p class="footer-tagline">당신의 금융을 더 스마트하게</p>
          </div>
          <div class="footer-links">
            <a href="#">이용약관</a>
            <a href="#">개인정보처리방침</a>
            <a href="#">고객센터</a>
          </div>
          <p class="footer-copyright">© 2024 F!NK. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from './stores/accounts'

const accountStore = useAccountStore()
const mobileMenuOpen = ref(false)
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(147, 51, 234, 0.1);
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
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, #9333ea 0%, #c084fc 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 4px;
}

.navbar-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #52525b;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.navbar-link:hover {
  color: #9333ea;
  background: rgba(147, 51, 234, 0.08);
}

.navbar-link.router-link-active {
  color: #9333ea;
  background: rgba(147, 51, 234, 0.12);
  font-weight: 600;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
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
  padding: 6px 12px 6px 6px;
  background: rgba(147, 51, 234, 0.08);
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.user-menu:hover {
  background: rgba(147, 51, 234, 0.15);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #9333ea 0%, #c084fc 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #27272a;
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #52525b;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mobile-menu-btn:hover {
  background: rgba(147, 51, 234, 0.08);
  color: #9333ea;
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
  background: white;
  border-top: 1px solid rgba(147, 51, 234, 0.1);
}

.mobile-link {
  display: block;
  padding: 14px 16px;
  font-size: 1rem;
  font-weight: 500;
  color: #3f3f46;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  width: 100%;
}

.mobile-link:hover,
.mobile-link.router-link-active {
  background: rgba(147, 51, 234, 0.08);
  color: #9333ea;
}

.mobile-divider {
  height: 1px;
  background: #e4e4e7;
  margin: 12px 0;
}

/* Main Content */
.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Footer */
.footer {
  background: #18181b;
  color: white;
  padding: 48px 24px;
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
}

.footer-brand {
  margin-bottom: 24px;
}

.footer-logo {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #c084fc 0%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-tagline {
  color: #71717a;
  font-size: 0.875rem;
  margin-top: 8px;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
}

.footer-links a {
  color: #a1a1aa;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #c084fc;
}

.footer-copyright {
  color: #52525b;
  font-size: 0.8125rem;
}

/* Transitions */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 1024px) {
  .navbar-menu {
    display: none;
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

  .main-content {
    padding: 24px 16px;
  }

  .footer {
    padding: 32px 16px;
  }

  .footer-links {
    flex-wrap: wrap;
    gap: 16px;
  }
}
</style>