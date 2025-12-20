<template>
  <header>
    <nav>
      <RouterLink :to="{name: 'home'}">home</RouterLink> | 
      <RouterLink :to="{name: 'SignUpView'}">회원가입</RouterLink> |
      <RouterLink :to="{name: 'LogInView'}">로그인</RouterLink> |
      <form @submit.prevent="logOut">
        <input type="submit" value="로그아웃">
      </form>
    </nav>
    <nav>
      <RouterLink :to="{name:'ProductView'}">금융상품</RouterLink> | 
      <RouterLink :to="{name: 'AnalysisView'}">분석하기</RouterLink> | 
      <RouterLink :to="{name:'ProfileView'}">마이페이지</RouterLink> |
      <RouterLink :to="{name:'KakaoMapView'}">은행찾기</RouterLink> |
      <RouterLink :to="{name:'NewsView'}">뉴스</RouterLink> |
      <RouterLink :to="{ name: 'YoutubeLayoutView' }">YouTube</RouterLink> |
      <RouterLink :to="{ name: 'MetalView' }">현물상품</RouterLink> |
    </nav>
  </header>
  <RouterView />

</template>

<script setup>
  import { useAccountStore } from './stores/accounts';
  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
  
</script>

<style scoped>

</style>