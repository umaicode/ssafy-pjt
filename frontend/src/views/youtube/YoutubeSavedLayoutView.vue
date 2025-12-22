<template>
  <section class="saved-layout">
    <header class="top">
      <h2>YouTube</h2>
      <div class="search-box">
        <form class="search" @submit.prevent="onSearch">
          <input
            v-model.trim="q"
            class="input"
            placeholder="비디오 검색 (검색 페이지로 이동)"
          />
          <button class="btn" type="submit" :disabled="!q">검색</button>
        </form>
      </div>
      <nav class="nav">
        <RouterLink class="link" :to="{ name: 'YoutubeSavedView' }">비디오</RouterLink>
        <RouterLink class="link" :to="{ name: 'YoutubeChannelsView' }">채널</RouterLink>
      </nav>
    </header>
    <main class="content">
      <RouterView />
    </main>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'

const router = useRouter()
const q = ref('')

const onSearch = () => {
  if (!q.value.trim()) return
  
  // 검색어를 가지고 검색 페이지로 이동
  router.push({
    name: 'YoutubeSearchView',
    query: { q: q.value }
  })
  
  // 검색어 초기화
  q.value = ''
}
</script>

<style scoped>
.saved-layout {
  padding: 8px 0;
}

.top {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
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

.search-box {
  width: 100%;
}

.search {
  display: flex;
  gap: 8px;
}

.input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.btn {
  padding: 8px 14px;
  border: 1px solid #333;
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.content {
  min-height: 200px;
}
</style>
