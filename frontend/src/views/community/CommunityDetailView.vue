<template>
  <div class="detail-page">
    <div class="container">
      <RouterLink class="back-link" :to="{ name: 'CommunityView' }">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5"/>
          <path d="M12 19l-7-7 7-7"/>
        </svg>
        목록으로 돌아가기
      </RouterLink>

      <article v-if="store.article" class="article-card">
        <!-- Edit Mode -->
        <template v-if="isEditing">
          <div class="card-header">
            <h2 class="card-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              게시글 수정
            </h2>
          </div>

          <form class="edit-form" @submit.prevent="onUpdateArticle">
            <div class="form-group">
              <label class="form-label">제목</label>
              <input v-model.trim="editTitle" class="form-input" placeholder="제목을 입력하세요" />
            </div>
            <div class="form-group">
              <label class="form-label">내용</label>
              <textarea v-model.trim="editContent" class="form-textarea" placeholder="내용을 입력하세요"></textarea>
            </div>
            <div class="form-actions">
              <button class="btn btn-primary" type="submit" :disabled="!canSave">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                  <polyline points="17 21 17 13 7 13 7 21"/>
                  <polyline points="7 3 7 8 15 8"/>
                </svg>
                저장하기
              </button>
              <button class="btn btn-secondary" type="button" @click="cancelEdit">취소</button>
            </div>
          </form>
        </template>

        <!-- View Mode -->
        <template v-else>
          <div class="card-header">
            <div class="header-top">
              <div class="author-info">
                <div class="avatar">
                  {{ (store.article.author_nickname ?? 'U').charAt(0).toUpperCase() }}
                </div>
                <div class="author-details">
                  <span class="author-name">{{ store.article.author_nickname ?? '익명' }}</span>
                  <span class="article-meta">
                    {{ formatDate(store.article.created_at) }} · 조회 {{ store.article.views ?? 0 }}
                  </span>
                </div>
              </div>

              <div v-if="isAuthor" class="article-actions">
                <button class="action-btn edit-btn" type="button" @click="startEdit">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  수정
                </button>
                <button class="action-btn delete-btn" type="button" @click="onDeleteArticle">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
                  </svg>
                  삭제
                </button>
              </div>
            </div>

            <h1 class="article-title">{{ store.article.title }}</h1>
          </div>

          <div class="article-content">
            <p>{{ store.article.content }}</p>
          </div>

          <div class="like-section">
            <button 
              class="like-btn" 
              :class="{ liked: store.article.is_liked }"
              type="button" 
              @click="onToggleArticleLike"
            >
              <svg v-if="store.article.is_liked" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <span>좋아요</span>
              <span class="like-count">{{ store.article.likes_count ?? 0 }}</span>
            </button>
          </div>
        </template>
      </article>

      <div v-else class="loading-state">
        <div class="loading-spinner"></div>
        <p>게시글을 불러오는 중...</p>
      </div>

      <!-- Comments Section -->
      <Comment
        :comments="store.comments"
        @delete="onDeleteComment"
        @update="onUpdateComment"
        @toggle-like="onToggleCommentLike"
      />
      <CommentCreate @submit="onCreateComment" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'
import Comment from '@/components/community/Comment.vue'
import CommentCreate from '@/components/community/CommentCreate.vue'

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const accountStore = useAccountStore()

const articleId = route.params.id

const isEditing = ref(false)
const editTitle = ref('')
const editContent = ref('')

const canSave = computed(() => editTitle.value && editContent.value)

const isAuthor = computed(() => {
  if (!accountStore.nickname || !store.article) return false
  return accountStore.nickname === store.article.author_nickname
})

onMounted(() => {
  store.getArticleDetail(articleId)
    .then(() => store.getComments(articleId))
    .catch(() => {})
})

const startEdit = () => {
  editTitle.value = store.article.title
  editContent.value = store.article.content
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  editTitle.value = ''
  editContent.value = ''
}

const onUpdateArticle = () => {
  store.updateArticle(articleId, {
    title: editTitle.value,
    content: editContent.value
  })
    .then(() => {
      isEditing.value = false
      alert('수정되었습니다.')
    })
    .catch((err) => {
      console.log(err)
      alert('수정에 실패했습니다.')
    })
}

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

const onCreateComment = (content) => {
  if (!content.trim()) return
  store.createComment(articleId, content)
    .then(() => {})
    .catch(() => {
      alert('댓글 작성에 실패했습니다.')
    })
}

const onUpdateComment = ({ id, content }) => {
  store.updateComment(id, content)
    .then(() => {})
    .catch(() => {
      alert('댓글 수정에 실패했습니다.')
    })
}

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

const onToggleArticleLike = () => {
  store.toggleArticleLike(articleId)
    .then(() => {})
    .catch((err) => {
      console.log(err)
      alert('좋아요 처리에 실패했습니다.')
    })
}

const onToggleCommentLike = (commentId) => {
  store.toggleCommentLike(commentId)
    .then(() => {})
    .catch((err) => {
      console.log(err)
      alert('댓글 좋아요 처리에 실패했습니다.')
    })
}
</script>

<style scoped>
.detail-page {
  min-height: calc(100vh - 72px);
  padding: 48px 24px;
  background: linear-gradient(180deg, #FDFBFD 0%, #FFF5F8 50%, #FAFAFA 100%);
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

/* Back Link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #71717a;
  text-decoration: none;
  margin-bottom: 24px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #7469B6;
}

.back-link svg {
  width: 18px;
  height: 18px;
}

/* Article Card */
.article-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  margin-bottom: 24px;
}

.card-header {
  padding: 28px 32px;
  border-bottom: 1px solid #f4f4f5;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
}

.card-title svg {
  width: 24px;
  height: 24px;
  color: #7469B6;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 16px;
  flex-wrap: wrap;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
}

.author-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #18181b;
}

.article-meta {
  font-size: 0.8125rem;
  color: #71717a;
}

.article-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.edit-btn {
  background: white;
  color: #52525b;
  border: 1px solid #e4e4e7;
}

.edit-btn:hover {
  border-color: #7469B6;
  color: #7469B6;
}

.delete-btn {
  background: white;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.delete-btn:hover {
  background: #fef2f2;
  border-color: #dc2626;
}

.article-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #18181b;
  line-height: 1.4;
  margin: 0;
}

.article-content {
  padding: 28px 32px;
}

.article-content p {
  font-size: 1rem;
  color: #3f3f46;
  line-height: 1.8;
  white-space: pre-wrap;
  margin: 0;
}

.like-section {
  padding: 20px 32px 28px;
  border-top: 1px solid #f4f4f5;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 0.9375rem;
  font-weight: 600;
  background: white;
  color: #71717a;
  border: 2px solid #e4e4e7;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn svg {
  width: 20px;
  height: 20px;
}

.like-btn:hover {
  border-color: #7469B6;
  color: #7469B6;
}

.like-btn.liked {
  background: linear-gradient(135deg, #7469B6 0%, #AD88C6 100%);
  border-color: transparent;
  color: white;
}

.like-count {
  padding: 2px 8px;
  font-size: 0.8125rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.like-btn:not(.liked) .like-count {
  background: #f4f4f5;
}

/* Edit Form */
.edit-form {
  padding: 24px 32px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #52525b;
  margin-bottom: 8px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 14px 18px;
  font-size: 1rem;
  background: #fafafa;
  border: 2px solid #e4e4e7;
  border-radius: 14px;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #7469B6;
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 105, 182, 0.1);
}

.form-textarea {
  min-height: 200px;
  resize: vertical;
}

.form-actions {
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
  transition: all 0.2s;
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

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

/* Loading State */
.loading-state {
  text-align: center;
  padding: 80px 24px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  border: 4px solid rgba(116, 105, 182, 0.1);
  border-top-color: #7469B6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .detail-page {
    padding: 32px 16px;
  }

  .card-header,
  .article-content,
  .like-section,
  .edit-form {
    padding-left: 20px;
    padding-right: 20px;
  }

  .article-title {
    font-size: 1.25rem;
  }

  .header-top {
    flex-direction: column;
    align-items: flex-start;
  }

  .article-actions {
    width: 100%;
  }

  .action-btn {
    flex: 1;
    justify-content: center;
  }
}

/* Dark Mode */
[data-theme="dark"] .detail-page {
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 50%, #0a0a0a 100%);
}

[data-theme="dark"] .back-link {
  color: #a1a1aa;
}

[data-theme="dark"] .back-link:hover {
  color: #E1AFD1;
}

[data-theme="dark"] .article-card {
  background: #18181b;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .card-header {
  border-bottom-color: #27272a;
}

[data-theme="dark"] .card-title {
  color: #e4e4e7;
}

[data-theme="dark"] .author-name {
  color: #e4e4e7;
}

[data-theme="dark"] .article-meta {
  color: #71717a;
}

[data-theme="dark"] .edit-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme="dark"] .edit-btn:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}

[data-theme="dark"] .delete-btn {
  background: #27272a;
  border-color: rgba(220, 38, 38, 0.3);
}

[data-theme="dark"] .delete-btn:hover {
  background: rgba(220, 38, 38, 0.1);
}

[data-theme="dark"] .article-title {
  color: #e4e4e7;
}

[data-theme="dark"] .article-content p {
  color: #a1a1aa;
}

[data-theme="dark"] .like-section {
  border-top-color: #27272a;
}

[data-theme="dark"] .like-btn {
  background: #27272a;
  color: #a1a1aa;
  border-color: #3f3f46;
}

[data-theme="dark"] .like-btn:hover {
  border-color: #7469B6;
  color: #E1AFD1;
}

[data-theme="dark"] .like-btn:not(.liked) .like-count {
  background: #3f3f46;
}

[data-theme="dark"] .form-label {
  color: #a1a1aa;
}

[data-theme="dark"] .form-input,
[data-theme="dark"] .form-textarea {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme="dark"] .form-input:focus,
[data-theme="dark"] .form-textarea:focus {
  background: #18181b;
  border-color: #7469B6;
}

[data-theme="dark"] .form-input::placeholder,
[data-theme="dark"] .form-textarea::placeholder {
  color: #71717a;
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

[data-theme="dark"] .loading-state p {
  color: #a1a1aa;
}
</style>
