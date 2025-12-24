<template>
  <div class="profile-page">
    <div class="container">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          {{ (accountStore.nickname || 'U').charAt(0).toUpperCase() }}
        </div>
        <div class="profile-info">
          <h1 class="profile-name">{{ accountStore.nickname }}</h1>
          <p class="profile-greeting">안녕하세요! F!NK와 함께 스마트한 금융생활을 즐겨보세요.</p>
        </div>
      </div>

      <div class="profile-body">
        <!-- Sidebar Menu -->
        <nav class="sidebar-menu">
          <div class="menu-section">
            <span class="menu-label">마이페이지</span>
            <RouterLink class="menu-link" :to="{ name: 'ProfileMyProduct' }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3v18h18"/>
                <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
              </svg>
              금융상품 그래프
            </RouterLink>
            <RouterLink class="menu-link" :to="{ name: 'ProfileWishlist' }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              좋아요 목록
            </RouterLink>
            <RouterLink class="menu-link" :to="{ name: 'ProfileModify' }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
              </svg>
              회원정보 수정
            </RouterLink>
          </div>

          <div class="menu-divider"></div>

          <div class="menu-section">
            <button class="menu-link danger" type="button" @click="onDeleteAccount">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <line x1="18" y1="8" x2="23" y2="13"/>
                <line x1="23" y1="8" x2="18" y2="13"/>
              </svg>
              회원탈퇴
            </button>
          </div>
        </nav>

        <!-- Content Area -->
        <div class="content-area">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const onDeleteAccount = async () => {
  try {
    await accountStore.deleteUser()
  } catch (e) {
    console.log(e)
  }
}
</script>

<style scoped>
.profile-page {
  min-height: calc(100vh - 72px);
  padding: 48px 24px;
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Profile Header */
.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 40px;
  padding: 32px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 50%, #7469B6 100%);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
}

.profile-greeting {
  font-size: 0.9375rem;
  color: #71717a;
  margin: 0;
}

/* Profile Body */
.profile-body {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 32px;
}

/* Sidebar Menu */
.sidebar-menu {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.menu-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 8px 12px;
  margin-bottom: 4px;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #52525b;
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.menu-link svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.menu-link:hover {
  color: #7469B6;
  background: rgba(116, 105, 182, 0.06);
}

.menu-link.router-link-active {
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  font-weight: 600;
}

.menu-link.danger {
  color: #dc2626;
}

.menu-link.danger:hover {
  background: #fef2f2;
}

.menu-divider {
  height: 1px;
  background: #f4f4f5;
  margin: 16px 0;
}

/* Content Area */
.content-area {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  min-height: 600px;
}

/* Responsive */
@media (max-width: 900px) {
  .profile-page {
    padding: 32px 16px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .profile-body {
    grid-template-columns: 1fr;
  }

  .sidebar-menu {
    position: static;
  }

  .content-area {
    padding: 24px;
  }
}

/* Dark Mode */
[data-theme="dark"] .profile-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 50%, #0a0a0a 100%);
}

[data-theme="dark"] .profile-header {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .profile-name {
  color: #e4e4e7;
}

[data-theme="dark"] .profile-greeting {
  color: #71717a;
}

[data-theme="dark"] .sidebar-menu {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .menu-label {
  color: #71717a;
}

[data-theme="dark"] .menu-link {
  color: #a1a1aa;
}

[data-theme="dark"] .menu-link:hover {
  color: #E1AFD1;
  background: rgba(116, 105, 182, 0.1);
}

[data-theme="dark"] .menu-link.router-link-active {
  color: #E1AFD1;
  background: rgba(116, 105, 182, 0.15);
}

[data-theme="dark"] .menu-link.danger {
  color: #f87171;
}

[data-theme="dark"] .menu-link.danger:hover {
  background: rgba(248, 113, 113, 0.1);
}

[data-theme="dark"] .menu-divider {
  background: #27272a;
}

[data-theme="dark"] .content-area {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
</style>