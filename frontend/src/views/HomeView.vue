<template>
  <div>
    <!-- 메뉴 -->
    <nav>
      <RouterLink :to="{name:'ProductView'}">금융상품</RouterLink> |
      <RouterLink :to="{name:'ProfileView'}">마이페이지</RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

</script>

<style scoped>

</style>