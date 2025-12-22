<template>
  <section class="news-list-section">
    <div class="list-header">
      <h3 class="list-title">기사 목록</h3>
      <span class="list-count">{{ newsStore.newsList.length }}개</span>
    </div>

    <div class="news-list">
      <div v-if="!newsStore.newsList.length" class="news-empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/>
          <path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>
        </svg>
        <p>아직 저장된 기사가 없습니다.</p>
        <span>검색을 통해 뉴스를 찾아보세요</span>
      </div>

      <article
        v-for="n in newsStore.newsList"
        :key="n.id"
        class="news-item"
        :class="{ selected: newsStore.newsDetail && newsStore.newsDetail.id === n.id }"
        @click="openDetail(n.id)"
      >
        <button 
          class="bookmark-btn"
          :class="{ active: n.is_bookmarked }"
          @click.stop="toggleBookmark(n.id)"
          type="button"
        >
          <svg v-if="n.is_bookmarked" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
        </button>
        <span class="news-title">{{ n.title }}</span>
        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </article>
    </div>
  </section>
</template>

<script setup>
import { useNewsStore } from '@/stores/news'
import { useAccountStore } from '@/stores/accounts'

const newsStore = useNewsStore()
const accountStore = useAccountStore()

const openDetail = (id) => {
  newsStore.getNewsDetail(id)
}

const toggleBookmark = (id) => {
  if (!accountStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }
  newsStore.toggleBookmark(id)
}
</script>

<style scoped>
.news-list-section {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f4f4f5;
}

.list-title {
  font-size: 1rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.list-count {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #9333ea;
  background: #f3e8ff;
  padding: 4px 10px;
  border-radius: 20px;
}

.news-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.news-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
}

.news-empty svg {
  width: 48px;
  height: 48px;
  color: #d4d4d8;
  margin-bottom: 16px;
}

.news-empty p {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #52525b;
  margin: 0 0 4px;
}

.news-empty span {
  font-size: 0.8125rem;
  color: #a1a1aa;
}

.news-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.news-item:hover {
  background: #fafafa;
}

.news-item.selected {
  background: #f3e8ff;
}

.bookmark-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bookmark-btn svg {
  width: 18px;
  height: 18px;
  color: #d4d4d8;
  transition: color 0.2s;
}

.bookmark-btn:hover svg {
  color: #9333ea;
}

.bookmark-btn.active svg {
  color: #9333ea;
}

.news-title {
  flex: 1;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #3f3f46;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-item.selected .news-title {
  color: #18181b;
  font-weight: 600;
}

.chevron {
  width: 16px;
  height: 16px;
  color: #d4d4d8;
  flex-shrink: 0;
}

.news-item.selected .chevron {
  color: #9333ea;
}
</style>
