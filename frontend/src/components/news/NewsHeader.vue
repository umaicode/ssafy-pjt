<template>
  <header class="nav">
    <div class="title">SSAFY 뉴스 검색기</div>

    <div class="search-box">
      <input
        v-model.trim="query"
        type="text"
        placeholder="검색어를 입력하세요 (예: 인공지능, 금융, SSAFY)"
        @keyup.enter="onFetch"
      />
      <button class="btn primary" @click="onFetch">가져오기</button>

      <button
        class="btn filter-btn"
        :class="{ active: route.name === 'NewsView' }"
        @click="goAll"
      >
        전체 보기
      </button>

      <button
        class="btn filter-btn"
        :class="{ active: route.name === 'NewsBookmarkView' }"
        @click="goBookmark"
      >
        북마크 보기
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNewsStore } from '@/stores/news'

const router = useRouter()
const route = useRoute()
const newsStore = useNewsStore()

const query = ref('')

const onFetch = function () {
  if (!query.value) {
    alert('검색어를 입력하세요.')
    return
  }
  newsStore.fetchNews(query.value)
}

const goAll = function () {
  router.push({ name: 'NewsView' })
}

const goBookmark = function () {
  router.push({ name: 'NewsBookmarkView' }) // 로그인 아니면 router guard에서 막힘
}
</script>

<style scoped>
.nav {
  height: 56px;
  background: #e67e57;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
}
.title { font-weight: 600; }
.search-box { display: flex; align-items: center; gap: 8px; }
.search-box input {
  width: 360px;
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.btn {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}
.btn.primary { background: #2d6cdf; border-color: #2d6cdf; color: #fff; }
.btn.filter-btn.active {
  background: #fff3ee;
  border-color: #e67e57;
  color: #b24b2a;
}
</style>
