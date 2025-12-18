<!-- 프로필 부모vue -->

<template>
  <div>
    <h2>님의 페이지</h2>
    <!-- {{ article.nickname }} 닉네임 추가 예정-->
    <nav class="menu">
      <RouterLink class="menu-link" :to="{ name: 'ProfileMyProduct' }">금융상품 그래프</RouterLink>
      <RouterLink class="menu-link" :to="{ name: 'ProfileWishlist' }">좋아요</RouterLink>
      <RouterLink class="menu-link" :to="{ name: 'ProfileModify' }">회원정보 수정</RouterLink>
    </nav>

    <hr />
    <RouterView />
  </div>
</template>

<script setup>

</script>

<style scoped>
.menu {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.menu-link {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  text-decoration: none;
}

/* RouterLink가 현재 경로일 때 자동으로 class가 붙음 */
.menu-link.router-link-active {
  font-weight: bold;
  border-color: #333;
}
</style>