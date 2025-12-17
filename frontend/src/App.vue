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