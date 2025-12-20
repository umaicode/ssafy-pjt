<template>
  <section class="youtube-layout">
    <header class="top">
      <h2>YouTube</h2>

      <nav class="nav">
        <RouterLink class="link" :to="{ name: 'YoutubeSearchView' }">검색</RouterLink>
        <RouterLink class="link" :to="{ name: 'YoutubeSavedView' }">저장됨</RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </section>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.youtube-layout {
  padding: 16px;
}

.top {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.nav {
  display: flex;
  gap: 10px;
}

.link {
  text-decoration: none;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  color: inherit;
}

.link.router-link-active {
  border-color: #333;
  font-weight: 700;
}

.content {
  min-height: 200px;
}
</style>
