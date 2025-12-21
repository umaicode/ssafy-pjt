<template>
  <section class="news-detail">
    <p v-if="!newsStore.newsDetail" class="news-empty">
      왼쪽에서 기사를 선택하세요.
    </p>

    <div v-else class="detail-card">
      <h2 class="detail-title">
        <span class="star">
          {{ newsStore.newsDetail.is_bookmarked ? '★' : '☆' }}</span>
        <span>{{ newsStore.newsDetail.title }}</span>
        
      </h2>

      <p class="meta">발행일: {{ newsStore.newsDetail.pubDate || '정보 없음' }}</p>

      <p class="body">{{ newsStore.newsDetail.description || '' }}</p>

      <p class="link-row">
        <a
          :href="newsStore.newsDetail.link"
          target="_blank"
          rel="noopener noreferrer"
        >
          네이버 뉴스 원문 보기
        </a>
      </p>

      <button class="btn primary" @click="toggle">
        {{ newsStore.newsDetail.is_bookmarked ? '북마크 해제' : '북마크 추가' }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { useNewsStore } from '@/stores/news'
const newsStore = useNewsStore()

const toggle = function () {
  newsStore.toggleBookmark(newsStore.newsDetail.id)
}
</script>

<style scoped>
.news-detail {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px;
  
  height: 100%;
  overflow-y: auto;
}
.news-empty { color: #777; padding: 12px; }
.detail-title { margin: 0 0 10px; }
.meta { color: #666; margin: 0 0 12px; }
.body { white-space: pre-line; line-height: 1.6; }
.link-row { margin: 12px 0; }

.btn {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}
.btn.primary { background: #2d6cdf; border-color: #2d6cdf; color: #fff; }
.star { width: 30px; 
        color: rgb(191, 194, 33);
        padding: 2px;
}
</style>
