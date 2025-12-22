<template>
  <div class="wrap">
    <!-- 상단 영역 -->
    <header class="top">
      <h1 class="title">커뮤니티</h1>

      <!-- 글 작성 버튼 -->
      <RouterLink class="create-btn" :to="{ name: 'CreateView' }">
        작성하기
      </RouterLink>
    </header>

    <!-- 게시판 -->
    <section class="board">
      <!-- 헤더 -->
      <div class="row head">
        <div class="col title">제목</div>
        <div class="col author">작성자</div>
        <div class="col date">작성일</div>
        <div class="col views">조회</div>
      </div>

      <!-- 게시글 목록 -->
      <div
        v-for="article in store.articles"
        :key="article.id"
        class="row body"
        :class="{ notice: article.is_notice }"
      >
        <!-- 제목 -->
        <div class="col title">
          <RouterLink
            class="link"
            :to="{ name: 'DetailView', params: { id: article.id } }"
          >
            {{ article.title }}
          </RouterLink>

          <!-- 댓글 수 -->
          <span v-if="article.comments_count" class="comment-count">
            [{{ article.comments_count }}]
          </span>

          <!-- 이미지 첨부 아이콘 -->
          <span v-if="article.has_image" class="attach">🖼️</span>
        </div>

        <!-- 작성자 -->
        <div class="col author">
          {{ article.author_nickname ?? article.author }}
        </div>

        <!-- 작성일 -->
        <div class="col date">
          {{ formatDate(article.created_at) }}
        </div>

        <!-- 조회수 -->
        <div class="col views">
          {{ article.views }}
        </div>
      </div>

      <!-- 게시글 없을 때 -->
      <div v-if="!store.articles.length" class="empty">
        게시글이 없습니다.
      </div>
    </section>

    <!-- 페이지네이션 -->
    <footer class="pager">
      <button class="pbtn" :disabled="page <= 1" @click="go(page - 1)">‹</button>

      <button
        v-for="p in totalPages"
        :key="p"
        class="pnum"
        :class="{ active: p === page }"
        @click="go(p)"
      >
        {{ p }}
      </button>

      <button class="pbtn" :disabled="page >= totalPages" @click="go(page + 1)">›</button>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'

const store = useCommunityStore()

// 현재 페이지
const page = ref(1)

// 총 페이지 수 (store에 없으면 10으로 가정)
const totalPages = computed(() => store.totalPages ?? 10)

// 게시글 불러오기
const fetchArticles = () => {
  // store.getArticles(page) 형태로 가정
  store.getArticles(page.value)
}

onMounted(() => {
  fetchArticles()
})

// 페이지 이동
const go = (p) => {
  page.value = p
  fetchArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 날짜 포맷: 2025-10-13T00:00 → 2025.10.13
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
.wrap {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
}

/* 상단 */
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.title {
  font-size: 26px;
  margin: 0;
}

.create-btn {
  padding: 10px 14px;
  border-radius: 10px;
  background: #e33;
  color: #fff;
  text-decoration: none;
  font-weight: 700;
}

/* 게시판 */
.board {
  border: 1px solid #eee;
  border-radius: 12px;
  overflow: hidden;
}

.row {
  display: grid;
  grid-template-columns: 1fr 140px 140px 80px;
  align-items: center;
}

.head {
  background: #fafafa;
  border-bottom: 1px solid #eee;
  font-weight: 700;
}

.body {
  border-bottom: 1px solid #f0f0f0;
}

.body:last-child {
  border-bottom: none;
}

.col {
  padding: 14px;
  font-size: 14px;
}

.col.title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.link {
  color: #111;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.comment-count {
  color: red;
  font-weight: 700;
}

.attach {
  font-size: 14px;
  opacity: 0.6;
}

/* 공지글 */
.notice {
  background: #fff5f6;
}

/* 빈 상태 */
.empty {
  padding: 20px;
  text-align: center;
  color: #777;
}

/* 페이지네이션 */
.pager {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.pbtn,
.pnum {
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #eee;
  background: #fff;
  cursor: pointer;
}

.pnum.active {
  border-color: #e33;
  color: #e33;
  font-weight: 800;
}

.pbtn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
