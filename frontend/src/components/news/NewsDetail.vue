<template>
  <section class="news-detail-section">
    <div v-if="!newsStore.newsDetail" class="news-empty">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/>
          <polyline points="10 17 15 12 10 7"/>
          <line x1="15" y1="12" x2="3" y2="12"/>
        </svg>
      </div>
      <p class="empty-title">기사를 선택해주세요</p>
      <span class="empty-desc">왼쪽 목록에서 기사를 클릭하면<br>상세 내용을 확인할 수 있습니다</span>
    </div>

    <article v-else class="detail-content">
      <div class="detail-header">
        <div class="bookmark-badge" :class="{ active: newsStore.newsDetail.is_bookmarked }">
          <svg v-if="newsStore.newsDetail.is_bookmarked" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
          {{ newsStore.newsDetail.is_bookmarked ? '북마크됨' : '미저장' }}
        </div>
        <span class="pub-date">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          {{ newsStore.newsDetail.pubDate || '발행일 정보 없음' }}
        </span>
      </div>

      <h1 class="detail-title">{{ newsStore.newsDetail.title }}</h1>

      <div class="detail-body">
        <p>{{ newsStore.newsDetail.description || '본문 내용이 없습니다.' }}</p>
      </div>

      <div class="detail-actions">
        <a
          :href="newsStore.newsDetail.link"
          target="_blank"
          rel="noopener noreferrer"
          class="btn btn-secondary"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          원문 보기
        </a>

        <button class="btn btn-primary" @click="toggle">
          <svg v-if="newsStore.newsDetail.is_bookmarked" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
          </svg>
          {{ newsStore.newsDetail.is_bookmarked ? '북마크 해제' : '북마크 추가' }}
        </button>
      </div>
    </article>
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
.news-detail-section {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.news-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: #f4f4f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #a1a1aa;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #18181b;
  margin: 0 0 8px;
}

.empty-desc {
  font-size: 0.9375rem;
  color: #71717a;
  line-height: 1.5;
}

.detail-content {
  padding: 32px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.bookmark-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #71717a;
  background: #f4f4f5;
  border-radius: 20px;
}

.bookmark-badge svg {
  width: 14px;
  height: 14px;
}

.bookmark-badge.active {
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
}

.pub-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8125rem;
  color: #71717a;
}

.pub-date svg {
  width: 14px;
  height: 14px;
}

.detail-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  line-height: 1.4;
  margin: 0 0 24px;
}

.detail-body {
  padding: 24px;
  background: #fafafa;
  border-radius: 16px;
  margin-bottom: 24px;
}

.detail-body p {
  font-size: 1rem;
  color: #3f3f46;
  line-height: 1.8;
  white-space: pre-line;
  margin: 0;
}

.detail-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.9375rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn-primary {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  color: white;
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

.btn-secondary {
  background: white;
  color: #52525b;
  border: 2px solid #e4e4e7;
}

.btn-secondary:hover {
  border-color: #7469B6;
  color: #7469B6;
}

@media (max-width: 768px) {
  .detail-content {
    padding: 24px;
  }

  .detail-title {
    font-size: 1.25rem;
  }

  .detail-actions {
    flex-direction: column;
  }

  .btn {
    justify-content: center;
  }
}

/* Dark Mode */
[data-theme="dark"] .news-detail-section {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .empty-icon {
  background: #27272a;
}

[data-theme="dark"] .empty-icon svg {
  color: #71717a;
}

[data-theme="dark"] .empty-title {
  color: #e4e4e7;
}

[data-theme="dark"] .empty-desc {
  color: #71717a;
}

[data-theme="dark"] .bookmark-badge {
  background: #27272a;
  color: #71717a;
}

[data-theme="dark"] .bookmark-badge.active {
  background: rgba(116, 105, 182, 0.2);
  color: #E1AFD1;
}

[data-theme="dark"] .pub-date {
  color: #71717a;
}

[data-theme="dark"] .detail-title {
  color: #e4e4e7;
}

[data-theme="dark"] .detail-body {
  background: #27272a;
}

[data-theme="dark"] .detail-body p {
  color: #a1a1aa;
}

[data-theme="dark"] .btn-secondary {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .btn-secondary:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}
</style>
