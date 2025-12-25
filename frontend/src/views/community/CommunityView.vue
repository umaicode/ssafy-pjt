<template>
  <div class="community-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">커뮤니티</h1>
          <p class="page-subtitle">다양한 이야기를 나눠보세요</p>
        </div>
        <RouterLink class="create-btn" :to="{ name: 'CreateView' }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          글 작성하기
        </RouterLink>
      </div>
    </header>

    <div class="container">

      <!-- Board -->
      <section class="board-section">
        <div class="board-card">
          <!-- Board Header -->
          <div class="board-header">
            <div class="col-title">제목</div>
            <div class="col-author">작성자</div>
            <div class="col-date">작성일</div>
            <div class="col-views">조회</div>
          </div>

          <!-- Board Body -->
          <div class="board-body">
            <article
              v-for="article in store.articles"
              :key="article.id"
              class="board-row"
              :class="{ notice: article.is_notice }"
            >
              <div class="col-title">
                <RouterLink
                  class="article-link"
                  :to="{ name: 'DetailView', params: { id: article.id } }"
                >
                  <span class="article-title">{{ article.title }}</span>
                </RouterLink>

                <span v-if="article.comments_count" class="comment-count">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                  </svg>
                  {{ article.comments_count }}
                </span>

                <span v-if="article.has_image" class="attach-badge">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                  </svg>
                </span>
              </div>

              <div class="col-author">
                {{ article.author_nickname ?? article.author }}
              </div>

              <div class="col-date">
                {{ formatDate(article.created_at) }}
              </div>

              <div class="col-views">
                {{ article.views }}
              </div>
            </article>

            <!-- Empty State -->
            <div v-if="!store.articles.length" class="empty-state">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <path d="M14 2v6h6"/>
                <path d="M16 13H8"/>
                <path d="M16 17H8"/>
                <path d="M10 9H8"/>
              </svg>
              <p>아직 게시글이 없습니다</p>
              <span>첫 번째 글을 작성해보세요!</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Pagination -->
      <footer class="pagination">
        <button 
          class="page-btn" 
          :disabled="page <= 1" 
          @click="go(page - 1)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </button>

        <button
          v-for="p in totalPages"
          :key="p"
          class="page-num"
          :class="{ active: p === page }"
          @click="go(p)"
        >
          {{ p }}
        </button>

        <button 
          class="page-btn" 
          :disabled="page >= totalPages" 
          @click="go(page + 1)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'

const store = useCommunityStore()

const page = ref(1)
const totalPages = computed(() => store.totalPages ?? 10)

const fetchArticles = () => {
  store.getArticles(page.value)
}

onMounted(() => {
  fetchArticles()
})

const go = (p) => {
  page.value = p
  fetchArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
}
</script>

<style scoped>
.community-page {
  min-height: calc(100vh - 72px);
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #E1AFD1 0%, #AD88C6 50%, #7469B6 100%);
  padding: 30px 24px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.header-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: white;
  margin: 0;
  text-align: left;
}

.page-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  text-align: left;
}

.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.create-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.create-btn svg {
  width: 18px;
  height: 18px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 48px 24px;
}

/* Board */
.board-section {
  margin-bottom: 24px;
}

.board-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.board-header {
  display: grid;
  grid-template-columns: 1fr 140px 140px 80px;
  align-items: center;
  padding: 16px 24px;
  background: #fafafa;
  border-bottom: 2px solid #e4e4e7;
  font-size: 1rem;
  font-weight: 700;
  color: #52525b;
}

.board-body {
  max-height: 600px;
  overflow-y: auto;
}

.board-row {
  display: grid;
  grid-template-columns: 1fr 140px 140px 80px;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f4f4f5;
  transition: background 0.2s;
}

.board-row:last-child {
  border-bottom: none;
}

.board-row:hover {
  background: #fafafa;
}

.board-row.notice {
  background: rgba(116, 105, 182, 0.04);
}

.col-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.article-link {
  text-decoration: none;
}

.article-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #18181b;
  transition: color 0.2s;
}

.article-link:hover .article-title {
  color: #7469B6;
}

.comment-count {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7469B6;
  background: rgba(116, 105, 182, 0.1);
  padding: 3px 8px;
  border-radius: 12px;
}

.comment-count svg {
  width: 12px;
  height: 12px;
}

.attach-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.attach-badge svg {
  width: 16px;
  height: 16px;
  color: #71717a;
}

.col-author {
  color: #52525b;
}

.col-date {
  color: #71717a;
}

.col-views {
  font-weight: 600;
  color: #71717a;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 24px;
  text-align: center;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #d4d4d8;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 600;
  color: #52525b;
  margin: 0 0 4px;
}

.empty-state span {
  font-size: 0.875rem;
  color: #a1a1aa;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.page-btn,
.page-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  background: white;
  border: 2px solid #e4e4e7;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn svg {
  width: 18px;
  height: 18px;
}

.page-btn:hover:not(:disabled),
.page-num:hover {
  border-color: #7469B6;
  color: #7469B6;
}

.page-num.active {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 32px 20px;
  }

  .header-content {
    flex-wrap: wrap;
    gap: 16px;
  }

  .header-icon {
    width: 48px;
    height: 48px;
  }

  .header-icon svg {
    width: 24px;
    height: 24px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.875rem;
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }

  .container {
    padding: 32px 16px;
  }

  .board-header {
    display: none;
  }

  .board-row {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 20px;
  }

  .col-author,
  .col-date,
  .col-views {
    display: inline-block;
    font-size: 0.75rem;
  }

  .col-title {
    flex-wrap: wrap;
  }
}

/* Dark Mode Styles */
[data-theme="dark"] .community-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 50%, #0a0a0a 100%);
}

[data-theme="dark"] .page-header {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 50%, #9b7ab8 100%);
}

[data-theme="dark"] .page-title {
  color: white;
}

[data-theme="dark"] .page-subtitle {
  color: rgba(255, 255, 255, 0.85);
}

[data-theme="dark"] .create-btn {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.25);
}

[data-theme="dark"] .create-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}

[data-theme="dark"] .board-card {
  background: #18181b;
  border-color: rgba(116, 105, 182, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .board-header {
  background: #27272a;
  border-bottom-color: #3f3f46;
}

[data-theme="dark"] .board-header .col-title,
[data-theme="dark"] .board-header .col-author,
[data-theme="dark"] .board-header .col-date,
[data-theme="dark"] .board-header .col-views {
  color: #a1a1aa;
}

[data-theme="dark"] .board-row {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .board-row:hover {
  background: rgba(116, 105, 182, 0.08);
}

[data-theme="dark"] .article-title {
  color: #e4e4e7;
}

[data-theme="dark"] .col-author,
[data-theme="dark"] .col-date,
[data-theme="dark"] .col-views {
  color: #a1a1aa;
}

[data-theme="dark"] .comment-count {
  color: #AD88C6;
}

[data-theme="dark"] .empty-state {
  color: #a1a1aa;
}

[data-theme="dark"] .empty-state p {
  color: #e4e4e7;
}

[data-theme="dark"] .page-btn,
[data-theme="dark"] .page-num {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .page-btn:hover:not(:disabled),
[data-theme="dark"] .page-num:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}

[data-theme="dark"] .page-num.active {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
  color: white;
}
</style>
