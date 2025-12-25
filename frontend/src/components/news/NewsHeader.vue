<template>
  <header class="news-header">
    <div class="header-content">
      <div class="header-title">
        <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
          <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
        </svg>
        <span>뉴스</span>
      </div>

      <div class="header-controls">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model.trim="query"
            type="text"
            placeholder="뉴스 검색어를 입력하세요"
            @keyup.enter="onFetch"
          />
          <button class="search-btn" @click="onFetch">
            검색
          </button>
        </div>

        <div class="filter-tabs">
          <button
            class="filter-tab"
            :class="{ active: route.name === 'NewsView' }"
            @click="goAll"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"/>
              <rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/>
            </svg>
            전체
          </button>

          <button
            class="filter-tab"
            :class="{ active: route.name === 'NewsBookmarkView' }"
            @click="goBookmark"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
            </svg>
            북마크
          </button>
        </div>
      </div>
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
  router.push({ name: 'NewsBookmarkView' })
}
</script>

<style scoped>
.news-header {
  background: linear-gradient(135deg, #5b5b6d 0%, #6d698f 100%);
  padding: 20px 24px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.title-icon {
  width: 24px;
  height: 24px;
  color: #E1AFD1;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s;
}

.search-box:focus-within {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(116, 105, 182, 0.5);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.5);
  margin-left: 12px;
}

.search-box input {
  width: 280px;
  padding: 10px 12px;
  font-size: 0.9375rem;
  background: transparent;
  border: none;
  outline: none;
  color: white;
}

.search-box input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-btn {
  padding: 10px 20px;
  font-size: 0.875rem;
  font-weight: 600;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.search-btn:hover {
  opacity: 0.9;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab svg {
  width: 16px;
  height: 16px;
}

.filter-tab:hover {
  color: white;
  background: rgba(255, 255, 255, 0.15);
}

.filter-tab.active {
  color: #7469B6;
  background: white;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box input {
    width: 100%;
  }

  .filter-tabs {
    justify-content: center;
  }
}
</style>
