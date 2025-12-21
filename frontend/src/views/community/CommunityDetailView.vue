<template>
  <div class="wrap">
    <RouterLink class="back" :to="{ name: 'CommunityView' }">← 목록으로</RouterLink>

    <section v-if="store.article" class="card">
      <div class="top">
        <h2 class="h2">{{ store.article.title }}</h2>

        <!-- ✅ 게시글 삭제 -->
        <button class="danger" type="button" @click="onDeleteArticle">
          삭제
        </button>
      </div>

      <div class="meta">
        <span>작성자: {{ store.article.author_nickname ?? store.article.author ?? '익명' }}</span>
        <span>작성일: {{ formatDate(store.article.created_at) }}</span>
        <span>조회: {{ store.article.views ?? 0 }}</span>
      </div>

      <p class="body">{{ store.article.content }}</p>
    </section>

    <p v-else class="loading">게시글을 불러오는 중...</p>

    <!-- 댓글 목록 -->
    <Comment :comments="store.comments" @delete="onDeleteComment" />
    <!-- 댓글 작성 -->
    <CommentCreate @submit="onCreateComment" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import Comment from '@/components/community/Comment.vue'
import CommentCreate from '@/components/community/CommentCreate.vue'

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()

const articleId = route.params.id

onMounted(() => {
  // ✅ 상세 + 댓글 같이 불러오기
  store.getArticleDetail(articleId)
    .then(() => store.getComments(articleId))
    .catch(() => {})
})

// 게시글 삭제
const onDeleteArticle = () => {
  const ok = window.confirm('게시글을 삭제할까요?\n삭제 후 복구할 수 없습니다.')
  if (!ok) return

  store.deleteArticle(articleId)
    .then(() => {
      alert('삭제되었습니다.')
      router.push({ name: 'CommunityView' })
    })
    .catch(() => {
      alert('게시글 삭제에 실패했습니다.')
    })
}

// 댓글 작성
const onCreateComment = (content) => {
  if (!content.trim()) return

  store.createComment(articleId, content)
    .then(() => {
      // ✅ 성공 시 store에서 push 해줬으니 별도 처리 없음
    })
    .catch(() => {
      alert('댓글 작성에 실패했습니다.')
    })
}

// 댓글 삭제
const onDeleteComment = (commentId) => {
  store.deleteComment(commentId)
    .then(() => {})
    .catch(() => {
      alert('댓글 삭제에 실패했습니다.')
    })
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
.wrap { max-width: 1000px; margin: 0 auto; padding: 24px 16px; }
.back { display: inline-block; margin-bottom: 12px; text-decoration: none; color: #333; }
.card { border: 1px solid #eee; border-radius: 12px; padding: 16px; }
.top { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.h2 { margin: 0; }
.meta { display: flex; gap: 12px; color: #666; font-size: 13px; margin-top: 8px; flex-wrap: wrap; }
.body { margin-top: 14px; white-space: pre-wrap; }
.loading { color: #777; }
.danger { border: 1px solid #f2b8c6; color: #b00020; background: #fff; border-radius: 10px; padding: 8px 10px; cursor: pointer; }
.danger:hover { background: #fff5f7; border-color: #b00020; }
</style>
