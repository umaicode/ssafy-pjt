<template>
  <div>
    <h2>{{ accountStore.nickname }}님의 페이지</h2>

    <div class="profile-body">
      <!-- 왼쪽 메뉴 -->
      <nav class="menu">
        <RouterLink class="menu-link" :to="{ name: 'ProfileMyProduct' }">
          금융상품 그래프
        </RouterLink>
        <RouterLink class="menu-link" :to="{ name: 'ProfileWishlist' }">
          좋아요
        </RouterLink>
        <RouterLink class="menu-link" :to="{ name: 'ProfileModify' }">
          회원정보 수정
        </RouterLink>
        
      </nav>

      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>


<script setup>
  import { useAccountStore } from '@/stores/accounts';

  const accountStore = useAccountStore()
</script>

<style scoped>
.profile-body {
  display: flex;
  margin-top: 30px;
  gap: 40px;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 160px;
}

.menu-link {
  padding: 8px 12px;
  border: 1px solid #ddcfcf;
  border-radius: 6px;
  text-decoration: none;
}

/* 활성 메뉴 */
.menu-link.router-link-active {
  font-weight: bold;
  border-color: #333;
  background: #dbe2e9;
}

.content {
  /* flex: 1;   남은 영역 차지 */
  border: 1px solid #ddcfcf;
  border-radius: 20px;
  height: 1000px;
  width: 1200px;
  padding: 30px;
}
</style>